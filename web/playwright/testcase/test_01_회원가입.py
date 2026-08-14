import os
import time
import random
import pytest
from playwright.sync_api import Page, expect

# 공통 도구 모듈 import
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(ROOT_DIR)

from common.resources.gsheet_reader import get_biz_no_from_sheet
from common.resources.email_generator import generate_email
from common.resources.email_reader import fetch_auth_code
from common.resources.admin_api import AdminAPI

# 파일 경로 상수
BIZNO_FILE = os.path.join(ROOT_DIR, "common", "resources", "used_bizNo.txt")
TESTFILE_PATH1 = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF.pdf")
TESTFILE_PATH2 = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF_2.pdf")

# =============================================================================
# Helper Functions
# =============================================================================

def record_biz_number(raw_biz_no: str) -> str:
    """사업자번호에서 하이픈을 제거하고 used_bizNo.txt 파일에 기록합니다."""
    clean_biz_no = raw_biz_no.replace("-", "").strip()
    with open(BIZNO_FILE, "a", encoding="utf-8") as f:
        f.write(f"{clean_biz_no}\n")
    print(f"[BizNo] Recorded bizNo: {clean_biz_no}")
    return clean_biz_no

def get_last_biz_number() -> str:
    """used_bizNo.txt 파일에서 마지막으로 사용된 사업자번호를 조회합니다."""
    if not os.path.exists(BIZNO_FILE):
        raise FileNotFoundError(f"사업자번호 파일이 없습니다: {BIZNO_FILE}")
    with open(BIZNO_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        raise ValueError("used_bizNo.txt에 기록된 사업자번호가 없습니다.")
    return lines[-1]

def approve_pending_company_via_admin():
    """Admin API를 통해 승인 대기 중인 업체를 승인 처리합니다."""
    api = AdminAPI()
    company_id = api.get_pending_review_id()
    if not company_id:
        raise Exception("어드민 승인 대기 중인 업체를 찾을 수 없습니다.")
    
    success = api.approve_company_review(company_id)
    if not success:
        raise Exception(f"어드민 승인 처리에 실패했습니다. (Company ID: {company_id})")
    print(f"[Admin API] 업체 승인 완료 (Company ID: {company_id})")
    return company_id

# 모듈 단위에서 생성된 이메일을 공유하기 위한 컨테이너
class TestContext:
    registered_email = ""


# =============================================================================
# Test Cases (01. 회원가입)
# =============================================================================

def test_01_new_member_registration_flow(page: Page, base_url, credentials):
    """
    [1. 신규 회원가입 Flow]
    - Google Sheet에서 새 사업자번호 추출 및 기록
    - 첨부파일 등록 (사업자등록증, CSO신고증)
    - 이메일 생성 및 Gmail 인증번호 자동 추출/입력
    - 회원가입 완료 후 Admin API 승인
    - 가입한 신규 계정으로 로그인/로그아웃 검증
    """
    print("\n" + "=" * 60)
    print(" 1. 신규 회원가입 Flow 시작")
    print("=" * 60)

    # 1. 로그인 페이지 이동 및 회원가입 버튼 클릭
    page.goto(base_url)
    page.wait_for_selector("a:has-text('회원가입')", timeout=10000)
    page.click("a:has-text('회원가입')")

    # 1.1. 사업자등록번호 입력
    print("[1.1] Google Sheet에서 사업자번호 가져오기")
    biz_no = get_biz_no_from_sheet()
    if biz_no.startswith("ERROR") or biz_no == "NO_BIZ_NO":
        pytest.fail(f"사용 가능한 사업자번호를 가져오지 못했습니다: {biz_no}")
    
    clean_biz_no = record_biz_number(biz_no)
    print(f"-> 사용할 사업자번호: {clean_biz_no}")

    page.wait_for_selector("input#bizNumber", timeout=5000)
    page.fill("input#bizNumber", clean_biz_no)
    page.click("button:has-text('확인')")

    # 신규 가입 가능 팝업 확인
    page.wait_for_selector("h2:has-text('신규 가입 가능한 사업자번호 입니다')", timeout=5000)
    page.locator("button", has_text="확인").last.click()

    # 1.2. 회원가입 상세 페이지 확인
    print("[1.2] 회원가입 상세 페이지 진입 확인")
    page.wait_for_selector("h1:has-text('회원가입')", timeout=5000)

    # 1.3. 파일 첨부 (사업자등록증 / CSO신고증)
    print("[1.3] 필수 증빙 파일 첨부")
    page.locator("#bizRegCertFileUuid input[type='file']").set_input_files(TESTFILE_PATH1)
    page.wait_for_timeout(500)
    page.locator("#salesCertFileUuid input[type='file']").set_input_files(TESTFILE_PATH2)
    page.wait_for_timeout(500)

    # 1.4. 이메일 생성 및 인증번호 발송
    print("[1.4] 고유 이메일 생성 및 인증번호 발송 요청")
    email_addr = generate_email()
    TestContext.registered_email = email_addr
    print(f"-> 생성된 이메일: {email_addr}")

    page.fill("input#email", email_addr)
    page.click("button:has-text('인증번호 발송')")
    
    page.wait_for_selector("h2:has-text('이메일로 인증번호를 발송했습니다.')", timeout=8000)
    page.click("button:has-text('확인')")

    # 1.5. 이메일 인증번호 수신 및 입력
    print("[1.5] Gmail IMAP에서 인증번호 수신 대기...")
    page.wait_for_timeout(5000) # 메일 도달 대기
    auth_code = fetch_auth_code(max_retries=10, retry_delay=3)
    print(f"-> 수신된 인증번호: {auth_code}")
    
    if auth_code == "NO_CODE" or not auth_code.isdigit():
        pytest.fail(f"이메일 인증번호 수신에 실패했습니다: {auth_code}")

    page.fill("input#emailVerificationKey", auth_code)
    page.click("button:has-text('인증하기')")
    page.wait_for_timeout(500)

    # 1.6. 비밀번호 입력
    print("[1.6] 비밀번호 입력")
    page.fill("input#password", credentials["password"])
    page.fill("input#passwordCheck", credentials["password"])

    # 1.7. 회원정보 입력 (이름, 전화번호)
    print("[1.7] 회원정보(이름/연락처) 입력")
    page.fill("input#name", "자동화테스트")
    random_phone = f"010{random.randint(10000000, 99999999)}"
    page.fill("input#phone", random_phone)

    # 1.8. 약관 동의 및 가입하기 완료
    print("[1.8] 약관 전체 동의 및 가입 신청")
    page.click("button#termsAll")
    page.click("button:has-text('가입하기')")

    # 가입 완료 팝업 확인
    page.wait_for_selector("button:has-text('확인')", timeout=10000)
    page.click("button:has-text('확인')")
    page.wait_for_timeout(1000)

    # 1.9. Admin API 승인 절차 수행
    print("[1.9] Admin API를 통한 업체 승인 처리")
    approve_pending_company_via_admin()
    page.wait_for_timeout(1000)

    # 1.10. 방금 가입한 신규 계정으로 로그인 검증
    print("[1.10] 신규 가입 계정으로 로그인 검증")
    page.goto(base_url)
    page.wait_for_selector("input[name='email']", timeout=5000)
    page.fill("input[name='email']", email_addr)
    page.fill("input[name='password']", credentials["password"])
    page.click("button:has-text('로그인')")

    page.wait_for_selector("h2:has-text('내 정보')", timeout=10000)
    expect(page.locator("h2", has_text="내 정보")).to_be_visible()

    # 로그아웃
    print("[1.11] 로그아웃 수행")
    page.click("button:has-text('로그아웃')")
    page.wait_for_selector("a:has-text('회원가입')", timeout=5000)
    print("[Success] 1. 신규 회원가입 Flow 성공 완료!")


def test_03_find_id_flow(page: Page, base_url):
    """
    [3. 아이디 찾기 Flow]
    - 이전에 사용했던 마지막 사업자번호로 아이디 찾기 수행
    """
    print("\n" + "=" * 60)
    print(" 3. 아이디 찾기 Flow 시작")
    print("=" * 60)

    page.goto(base_url)
    page.wait_for_selector("a:has-text('아이디 찾기')", timeout=10000)
    page.click("a:has-text('아이디 찾기')")

    # 아이디 찾기 페이지 확인
    heading = page.locator("h1", has_text="가입정보 확인 후 아이디를 찾을 수 있습니다")
    heading.wait_for(timeout=5000)

    # 마지막으로 사용했던 사업자번호 조회
    last_biz_no = get_last_biz_number()
    print(f"-> 사용할 사업자번호: {last_biz_no}")

    page.fill("input#businessNumber", last_biz_no)
    page.fill("input#name", "자동화테스트")
    page.click("button:has-text('아이디 찾기')")

    # 결과 팝업 확인
    result_popup = page.locator("h2", has_text="가입하신 아이디 입니다")
    result_popup.wait_for(timeout=10000)
    expect(result_popup).to_be_visible()

    page.click("button:has-text('확인')")
    page.wait_for_selector("a:has-text('회원가입')", timeout=5000)
    print("[Success] 3. 아이디 찾기 Flow 성공 완료!")


def test_04_reset_password_flow(page: Page, base_url, credentials):
    """
    [4. 비밀번호 재설정 Flow]
    - 1번에서 가입했던 이메일로 비밀번호 재설정 메일 발송
    - 인증번호 수신 후 비밀번호 변경 완료 검증
    """
    print("\n" + "=" * 60)
    print(" 4. 비밀번호 재설정 Flow 시작")
    print("=" * 60)

    target_email = TestContext.registered_email
    if not target_email:
        # 1번 Flow를 건너뛰고 단독 실행된 경우 기본 CSO 이메일 사용
        target_email = credentials["id_cso"]
    print(f"-> 대상 이메일: {target_email}")

    page.goto(base_url)
    page.wait_for_selector("a:has-text('비밀번호 재설정')", timeout=10000)
    page.click("a:has-text('비밀번호 재설정')")

    page.wait_for_selector("h1:has-text('비밀번호를 잊으셨나요?')", timeout=5000)

    # 이메일 입력 및 인증번호 발송
    page.fill("input#email", target_email)
    page.click("button:has-text('인증번호 발송')")
    
    page.wait_for_selector("h2:has-text('이메일로 인증번호를 발송했습니다.')", timeout=8000)
    page.click("button:has-text('확인')")

    # 인증번호 수신 및 입력
    print("[4.3] Gmail IMAP에서 비밀번호 재설정 인증번호 수신 대기...")
    page.wait_for_timeout(5000)
    code = fetch_auth_code(max_retries=10, retry_delay=3)
    print(f"-> 수신된 인증번호: {code}")

    if code == "NO_CODE" or not code.isdigit():
        pytest.fail(f"비밀번호 재설정 인증번호 수신에 실패했습니다: {code}")

    page.fill("input#emailcode", code)
    page.click("button:has-text('인증하기')")
    page.wait_for_timeout(500)

    # 다음 단계 버튼 클릭
    page.click("button:has-text('다음')")
    page.wait_for_selector("h1:has-text('비밀번호를 재설정 해주세요')", timeout=5000)

    # 비밀번호 재설정
    page.fill("input#password", credentials["password"])
    page.fill("input#confirmPassword", credentials["password"])
    page.click("button:has-text('비밀번호 변경하기')")

    # 변경 완료 팝업 확인
    page.wait_for_selector("h2:has-text('비밀번호가 변경되었습니다')", timeout=8000)
    page.click("button:has-text('확인')")

    # 로그인 페이지 복귀 확인
    page.wait_for_selector("a:has-text('회원가입')", timeout=5000)
    print("[Success] 4. 비밀번호 재설정 Flow 성공 완료!")
