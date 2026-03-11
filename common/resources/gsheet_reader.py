import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import os
from dotenv import load_dotenv

# .env 파일 로드 (보안 설정)
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", "auth", ".env")
load_dotenv(env_path)

# 설정 (환경 변수 또는 상대 경로 활용)
CREDS_PATH = os.path.join(current_dir, "..", "auth", "credentials.json")
SPREADSHEET_KEY = os.getenv("GSHEET_KEY")

def get_biz_no_from_sheet():
    # API 인증 설정
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    try:
        # 인증 파일 확인
        if not os.path.exists(CREDS_PATH):
            return f"ERROR: Credentials file not found at {CREDS_PATH}"

        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, scope)
        client = gspread.authorize(creds)
        
        # 스프레드시트 열기 (ID 기준)
        spreadsheet = client.open_by_key(SPREADSHEET_KEY)
        sheet = spreadsheet.get_worksheet(0) # 첫 번째 시트
        
        # 모든 데이터 가져오기
        # get_all_values()는 리스트의 리스트를 반환함 (1-indexed가 아님)
        records = sheet.get_all_values()
        
        if not records:
            return "ERROR: Sheet is empty"

        # 데이터 처리 (헤더 제외 2행부터 시작)
        for i, row in enumerate(records):
            if i == 0:  # 헤더(제목 행) 건너뛰기
                continue
            
            # A열: 체크박스 (index 0)
            # F열: 사업자번호 (index 5)
            # gspread에서 체크박스 미체크 상태는 'FALSE' (문자열)로 반환됨
            is_checked = row[0].strip().upper()
            biz_no = row[5].strip() if len(row) > 5 else None

            if is_checked == 'FALSE' or is_checked == '':
                if biz_no:
                    # A열(체크박스)을 TRUE로 업데이트
                    # i+1은 현재 행의 1-indexed 값
                    sheet.update_cell(i + 1, 1, 'TRUE')
                    return biz_no
                    
        return "NO_BIZ_NO"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    # Robot Framework에서 호출 시 결과 출력
    result = get_biz_no_from_sheet()
    print(result)
