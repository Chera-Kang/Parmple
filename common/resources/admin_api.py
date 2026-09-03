import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import json
import random
import os
import sys
from dotenv import load_dotenv

# =============================================================================
# 1. 초기 설정 및 환경 변수 로드
# =============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, "common", "auth", ".env")
load_dotenv(ENV_PATH)

API_URL = os.getenv("ADMIN_API_URL", "https://qa.api.parmple.com")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("PASSWORD")

# =============================================================================
# 2. 어드민 API 관리 클래스
# =============================================================================

class AdminAPI:
    def __init__(self, api_url=API_URL):
        self.api_url = api_url
        self.access_token = None

    def login(self, email=ADMIN_EMAIL, password=ADMIN_PASSWORD):
        """ 어드민 로그인 및 토큰 획득 """
        url = f"{self.api_url}/api/v1/admins/auth/login"
        payload = {"email": email, "password": password}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['data']['detail']['accessToken']
            return self.access_token
        else:
            raise Exception(f"Login Failed: {response.status_code} - {response.text}")

    def get_registered_company_info(self):
        """ 등록 상태(어드민 승인 완료, 미가입)인 업체 정보 조회 """
        if not self.access_token:
            self.login()

        url = f"{self.api_url}/api/v1/admins/companies/cso/search"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "filterModel": {"isSignedUp": False},
            "sortModel": {"createdAt": "desc"},
            "page": 1,
            "size": 50
        }
        
        response = requests.post(url, json=payload, headers=headers, verify=False)
        if response.status_code == 200:
            items = response.json()['data']['items']
            if not items: return None
            
            item = random.choice(items)
            def clean_val(v):
                return str(v).replace("\n", "").replace("\r", "").replace("\t", "").strip() if v else ""

            return {
                "bizName": clean_val(item.get("bizName")),
                "bizRegNo": clean_val(item.get("bizRegNo")),
                "csoReportNo": clean_val(item.get("csoReportNo"))
            }
        else:
            raise Exception(f"Fetch Company Failed: {response.status_code}")

    def get_pending_review_id(self):
        """ 승인 대기 중인 첫 번째 업체 리뷰 ID 조회 """
        if not self.access_token:
            self.login()

        url = f"{self.api_url}/api/v1/admins/company-reviews/search"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "filterModel": {},
            "sortModel": {"createdAt": "desc"},
            "page": 1,
            "size": 50
        }
        
        response = requests.post(url, json=payload, headers=headers, verify=False)
        if response.status_code == 200:
            items = response.json()['data']['items']
            if items: return items[0]['id']
        return None

    def approve_company_review(self, company_id, cso_report_no="자동화테스트"):
        """ 업체 승인 처리 """
        if not self.access_token:
            self.login()

        url = f"{self.api_url}/api/v1/admins/company-reviews/{company_id}/approve"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {"csoReportNo": cso_report_no}
        
        response = requests.post(url, json=payload, headers=headers, verify=False)
        return response.status_code == 200

# =============================================================================
# 3. 메인 실행부 (CLI 지원)
# =============================================================================

if __name__ == "__main__":
    try:
        api = AdminAPI()
        if len(sys.argv) > 1:
            cmd = sys.argv[1]
            if cmd == "get_company":
                info = api.get_registered_company_info()
                print(json.dumps(info, ensure_ascii=False) if info else json.dumps({"error": "No data"}))
            elif cmd == "get_token":
                print(api.login())
            elif cmd == "get_review_id":
                print(api.get_pending_review_id())
            elif cmd == "approve" and len(sys.argv) > 2:
                success = api.approve_company_review(sys.argv[2])
                print("SUCCESS" if success else "FAILED")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
