import requests
import json
import time
import pandas as pd
import urllib.parse
import os
import gspread
from datetime import datetime
import sys

class BusinessNumberChecker:
    def __init__(self, service_key, cred_path):
        self.service_key = service_key
        self.encoded_key = urllib.parse.quote(service_key, safe='')
        self.base_url = "https://api.odcloud.kr/api/nts-businessman/v1/status"
        self.batch_size = 100
        self.delay = 0.3
        self.gc = gspread.service_account(filename=cred_path)

    def clean_no(self, b_no):
        if not b_no: return ""
        return str(b_no).replace("-", "").replace(" ", "").strip()

    def format_no(self, b_no):
        clean = self.clean_no(b_no)
        return f"{clean[:3]}-{clean[3:5]}-{clean[5:]}" if len(clean) == 10 else b_no

    def check_batch(self, batch, retries=3):
        url = f"{self.base_url}?serviceKey={self.encoded_key}"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        payload = {"b_no": [self.clean_no(n) for n in batch]}
        
        for attempt in range(retries):
            try:
                res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
                if res.status_code == 200:
                    return res.json()
                elif res.status_code == 429:
                    print(f"\n⚠️ API 요청 제한(429). {attempt+1}번 재시도 전 대기...")
                    time.sleep(3)
                else:
                    print(f"\n⚠️ API 응답 오류 ({res.status_code}). {attempt+1}번 재시도 중...")
            except Exception as e:
                print(f"\n🚨 네트워크 오류: {e}. {attempt+1}번 재시도 중...")
            
            if attempt < retries - 1:
                time.sleep(2)
        
        return None

    def process_results(self, res_data, batch):
        if res_data is None:
            return [{"b_no": self.format_no(n), "status": "API오류", "detail": "조회 실패 (기존 시트 유지)"} for n in batch]

        api_map = {item["b_no"]: item for item in res_data.get("data", [])}
        results = []
        for n in batch:
            clean = self.clean_no(n)
            fmt = self.format_no(n)
            if clean in api_map:
                item = api_map[clean]
                stt, tax = item.get("b_stt", ""), item.get("tax_type", "")
                if stt == "계속사업자": status = "정상"
                elif stt == "휴업자": status = "휴업"
                elif stt == "폐업자": status = "폐업"
                else: status = "정보없음"
                detail = tax if status != "폐업" else f"폐업일: {item.get('end_dt', '')}"
                results.append({"b_no": fmt, "status": status, "detail": detail})
            else:
                results.append({"b_no": fmt, "status": "정보없음", "detail": "국세청 미등록"})
        return results

    def print_progress(self, current, total):
        bar_length = 30
        filled_length = int(round(bar_length * current / float(total)))
        percent = round(100.0 * current / float(total), 1)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(f'\r   🔍 [{bar}] {percent}% ({current}/{total})')
        sys.stdout.flush()

    def run_all_sheets(self, spreadsheet_url):
        print(f"\n🕒 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        doc = self.gc.open_by_url(spreadsheet_url)
        all_worksheets = doc.worksheets()
        
        try:
            target_sheet = doc.worksheet("휴업/폐업")
        except gspread.exceptions.WorksheetNotFound:
            target_sheet = doc.add_worksheet(title="휴업/폐업", rows="100", cols="5")
            target_sheet.append_row(["이전 시트", "사업자번호", "상태", "상세정보", "조회일시"])

        for sheet in all_worksheets:
            source_name = sheet.title
            if source_name == "휴업/폐업": continue

            print(f"\n📂 [{source_name}] 시트 시작")
            all_rows = sheet.get_all_values()
            if len(all_rows) <= 1:
                print(f"   ⏩ 데이터가 없어 건너뜁니다.")
                continue

            b_nos_to_check = []
            for row in all_rows[1:]:
                b_no = row[5] if len(row) > 5 else ""
                clean = self.clean_no(b_no)
                if clean: b_nos_to_check.append(clean)
            
            unique_nos = list(set(b_nos_to_check))
            if not unique_nos:
                print(f"   ⏩ F열에 유효한 번호가 없어 건너뜀.")
                continue

            api_results_map = {}
            for i in range(0, len(unique_nos), self.batch_size):
                batch = unique_nos[i:i + self.batch_size]
                res = self.check_batch(batch)
                processed = self.process_results(res, batch)
                for p in processed:
                    api_results_map[self.clean_no(p["b_no"])] = p
                
                self.print_progress(min(i + self.batch_size, len(unique_nos)), len(unique_nos))
                if i + self.batch_size < len(unique_nos): time.sleep(self.delay)
            print()

            remaining_rows = [all_rows[0]]
            rows_to_move = []
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for row in all_rows[1:]:
                b_no = row[5] if len(row) > 5 else ""
                clean = self.clean_no(b_no)
                
                if clean in api_results_map:
                    api_res = api_results_map[clean]
                    if api_res["status"] in ["정상", "API오류"]:
                        remaining_rows.append(row)
                    else:
                        rows_to_move.append([source_name, api_res["b_no"], api_res["status"], api_res["detail"], now_str])
                else:
                    remaining_rows.append(row)

            if rows_to_move:
                print(f"   🚚 {len(rows_to_move)}건 이동 및 시트 정리 중...")
                target_sheet.append_rows(rows_to_move)
                sheet.update(remaining_rows, value_input_option='USER_ENTERED')
                
                if len(all_rows) > len(remaining_rows):
                    last_col_idx = len(all_rows[0])
                    last_col_letter = gspread.utils.rowcol_to_a1(1, last_col_idx).replace('1', '')
                    clear_range = f"A{len(remaining_rows) + 1}:{last_col_letter}{len(all_rows)}"
                    sheet.batch_clear([clear_range])
            else:
                print(f"   ✅ 모든 데이터 정상 또는 확인 불가 (이동 없음)")

        print(f"\n🕒 완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("✨ 모든 작업이 완료되었습니다!\n")

if __name__ == "__main__":
    # 공통 auth 경로 설정 및 .env 로드
    base_dir = os.path.dirname(os.path.abspath(__file__))
    auth_dir = os.path.join(base_dir, "..", "auth")
    env_file = os.path.join(auth_dir, ".env")
    
    try:
        from dotenv import load_dotenv
        if os.path.exists(env_file):
            load_dotenv(env_file)
    except ImportError:
        pass

    SERVICE_KEY = os.environ.get("ODCLOUD_SERVICE_KEY")
    CRED_PATH = os.environ.get(
        "CRED_PATH",
        os.path.join(auth_dir, "credentials.json")
    )
    
    gsheet_key = os.environ.get("GSHEET_KEY")
    SHEET_URL = os.environ.get("SHEET_URL", f"https://docs.google.com/spreadsheets/d/{gsheet_key}" if gsheet_key else None)
    
    if not SERVICE_KEY:
        print("❌ 공공데이터포털 API 인증키(ODCLOUD_SERVICE_KEY)가 설정되지 않았습니다.")
        print("   tools/auth/.env 파일에 'ODCLOUD_SERVICE_KEY'를 설정해 주세요.")
        sys.exit(1)

    if not os.path.exists(CRED_PATH):
        print(f"❌ 인증 키 파일을 찾을 수 없습니다: {CRED_PATH}")
        print("   tools/auth/credentials.json 파일이 존재하는지 확인해 주세요.")
        sys.exit(1)

    if not SHEET_URL or not gsheet_key:
        print("❌ 구글 스프레드시트 키(GSHEET_KEY)가 설정되지 않았습니다.")
        print("   tools/auth/.env 파일에 'GSHEET_KEY'를 설정해 주세요.")
        sys.exit(1)

    checker = BusinessNumberChecker(SERVICE_KEY, CRED_PATH)
    checker.run_all_sheets(SHEET_URL)

