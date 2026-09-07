import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from tqdm import tqdm

class SmartCrawler:
    """사이트 상태 점검 및 적응형 지연 기능을 갖춘 지능형 크롤러"""
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://bizno.net/"
        }
        self.last_response_time = 0
        self.consecutive_blocks = 0

    def check_site_health(self):
        """[사전 확인] 본격 수집 전 사이트 접근 가능 여부 및 반응 속도 체크"""
        print("🔍 작업을 시작하기 전 사이트 건강 상태를 점검합니다...")
        try:
            start_t = time.time()
            res = self.session.get("https://bizno.net/", headers=self.headers, timeout=10)
            elapsed = time.time() - start_t
            
            if res.status_code == 200:
                if elapsed < 2.0:
                    print(f"✅ 사이트 상태 양호 (반응 속도: {elapsed:.2f}s)")
                    return True
                else:
                    print(f"⚠️ 사이트 불안정 (반응 속도 느림: {elapsed:.2f}s). 주의가 필요합니다.")
                    return True
            else:
                print(f"❌ 사이트 접근 불가 (HTTP {res.status_code}). 아직 차단 중일 수 있습니다.")
                return False
        except Exception as e:
            print(f"❌ 접속 오류 발생: {e}")
            return False

    def get_details(self, b_no):
        clean = "".join(filter(str.isdigit, str(b_no)))
        if not clean or len(clean) != 10:
            return {"사업자번호": b_no, "상호명": "번호유효성오류", "대표자명": "-", "주소": "-"}
        
        url = f"https://bizno.net/article/{clean}"
        try:
            # 💡 [적응형 지연] 이전 응답이 느렸다면(부하 징취) 더 길게 쉽니다.
            base_delay = 2.0 if self.last_response_time < 3.0 else 7.0
            time.sleep(random.uniform(base_delay, base_delay + 3.0))
            
            start_t = time.time()
            response = self.session.get(url, headers=self.headers, timeout=15)
            self.last_response_time = time.time() - start_t
            
            # 차단 또는 봇 감지 징후 포착
            if response.status_code in [403, 429] or "봇" in response.text or "비정상" in response.text:
                return "BLOCK"
                
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                h1 = soup.find('h1')
                biz_name = h1.get_text(separator=' ', strip=True) if h1 else ""
                
                if not biz_name or biz_name == clean or "검색 결과가 없습니다" in response.text:
                    # '정보없음'은 차단은 아니므로 정상 리턴
                    return {"사업자번호": b_no, "상호명": "DB미등록(정보없음)", "대표자명": "-", "주소": "-"}

                rep_name, address = "-", "-"
                for th in soup.find_all('th'):
                    label = th.get_text(strip=True)
                    td = th.find_next_sibling('td')
                    if td:
                        val = td.get_text(strip=True)
                        if "대표자명" in label: rep_name = val
                        elif "회사주소" in label: address = val
                
                if "(" in biz_name and clean in biz_name:
                    biz_name = biz_name.split("(")[0].strip()

                return {"사업자번호": b_no, "상호명": biz_name, "대표자명": rep_name, "주소": address}
            
            return {"사업자번호": b_no, "상호명": f"HTTP {response.status_code}", "대표자명": "-", "주소": "-"}
        except Exception:
            return {"사업자번호": b_no, "상호명": "접속실패", "대표자명": "-", "주소": "-"}

def get_unique_filename(base_path):
    """파일명이 겹치면 (2), (3) 형태로 넘버링을 붙여 반환"""
    if not os.path.exists(base_path):
        return base_path
    
    filename, extension = os.path.splitext(base_path)
    counter = 2
    while os.path.exists(f"{filename} ({counter}){extension}"):
        counter += 1
    return f"{filename} ({counter}){extension}"

def main():
    # 스크립트 파일의 실제 위치를 기준으로 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 💡 세션당 수집량: 회사 와이파이라면 50~100 사이를 추천합니다.
    TARGET_PER_SESSION = 100 
    input_file = os.path.join(base_dir, "biz.txt")
    base_output = os.path.join(base_dir, "result.xlsx")
    
    # [수정] 실행할 때마다 새로운 결과 파일 생성 (넘버링 적용)
    output_file = get_unique_filename(base_output)
    
    if not os.path.exists(input_file):
        print(f"❌ {input_file} 파일이 없습니다.")
        return

    # 기존 데이터 로드 (모든 result*.xlsx 파일을 뒤져서 이미 한 건 제외하기)
    processed_nos = set()
    import glob
    for f_path in glob.glob(os.path.join(base_dir, "result*.xlsx")):
        try:
            temp_df = pd.read_excel(f_path)
            if '사업자번호' in temp_df.columns:
                processed_nos.update(temp_df['사업자번호'].astype(str).tolist())
        except:
            continue
            
    if processed_nos:
        print(f"🔄 기존 결과 파일들에서 총 {len(processed_nos)}건의 중복 항목을 제외합니다.")

    # 목록 준비
    with open(input_file, "r", encoding="utf-8") as f:
        raw_nos = list(dict.fromkeys([line.strip() for line in f.readlines() if line.strip()]))
        todo_nos = [n for n in raw_nos if n not in processed_nos]

    if not todo_nos:
        print("✅ 모든 조회가 완료되었습니다 (더 이상 조회할 번호가 없습니다).")
        return

    print(f"🔍 남은 수집 대상: {len(todo_nos)}건")
    
    crawler = SmartCrawler()
    if not crawler.check_site_health():
        print("🛑 사이트 상태가 좋지 않아 작업을 중단합니다. IP를 확인해 주세요.")
        return

    current_session_nos = todo_nos[:TARGET_PER_SESSION]
    print(f"🚀 [새 세션 시작] {output_file} 파일에 {len(current_session_nos)}건 수집을 시작합니다.")
    
    all_results = []
    session_count = 0
    try:
        for b_no in tqdm(current_session_nos, desc="데이터 수집 중"):
            res = crawler.get_details(b_no)
            
            if res == "BLOCK":
                print(f"\n🛑 [차단 감지] 사이트 방어벽이 작동했습니다. 현재 IP로는 더 이상 진행이 어렵습니다.")
                break
                
            if isinstance(res, dict):
                all_results.append(res)
                session_count += 1
            
            # 중간 저장 (10건마다)
            if session_count % 10 == 0 and all_results:
                pd.DataFrame(all_results).to_excel(output_file, index=False)
                    
    except KeyboardInterrupt:
        print("\n⚠️ 수동 중단되었습니다.")

    if all_results:
        pd.DataFrame(all_results).to_excel(output_file, index=False)
        print(f"\n✅ 완료: {session_count}건이 {output_file}에 저장되었습니다.")
        
        wait_exit = random.uniform(5, 10)
        print(f"⏳ {int(wait_exit)}초 후 종료합니다...")
        time.sleep(wait_exit)
    else:
        print("\n❌ 수집된 데이터가 없습니다.")
        
    print("🚀 작업을 마칩니다. 다음 수집을 위해 IP를 변경해 주세요.")

if __name__ == "__main__":
    main()
