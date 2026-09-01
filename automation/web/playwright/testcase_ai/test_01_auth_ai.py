import os
import re
import time
import random
import pytest
from playwright.sync_api import Page, expect

# 공통 도구 모듈 import
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from common.resources.gsheet_reader import get_biz_no_from_sheet
from common.resources.email_generator import generate_email
from common.resources.email_reader import fetch_auth_code
from common.resources.admin_api import AdminAPI

# 파일 경로 상수
BIZNO_FILE = os.path.join(ROOT_DIR, "common", "resources", "used_bizNo.txt")
TESTFILE_PATH1 = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF.pdf")
TESTFILE_PATH2 = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF_2.pdf")

BASE_URL = "https://qa.erp.parmple.com/"

# ==============================================================================
# Helper Functions
# ==============================================================================

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

class TestContext:
    registered_email = ""

# ==============================================================================
# Phase 1 & 2: Core & Atomic Validation Test Cases
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_aut_01_login_page_rendering(page: Page):
    """
    [TC-AUT-01] Happy Path: 로그인 페이지 렌더링 검증
    - /auth/login 진입 ➡️ 이메일/비밀번호 필드, 로그인 버튼, 링크 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-01] 로그인 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 페이지 진입
    page.goto(BASE_URL)
    page.wait_for_selector("a:has-text('회원가입')", timeout=15000)

    # 2. 폼 요소 가시성 단언
    expect(page.locator("input[name='email']")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()
    expect(page.locator("button:has-text('로그인')")).to_be_visible()
    expect(page.locator("a:has-text('회원가입')")).to_be_visible()
    expect(page.locator("a:has-text('아이디 찾기')")).to_be_visible()
    expect(page.locator("a:has-text('비밀번호 재설정')")).to_be_visible()
    print("[Success] TC-AUT-01 로그인 페이지 렌더링 검증 성공!")


def test_tc_aut_02_cso_successful_login(page: Page, credentials):
    """
    [TC-AUT-02] Happy Path: CSO 정상 로그인 검증
    - CSO 계정 로그인 ➡️ 대시보드 진입 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-02] CSO 정상 로그인 검증 시작")
    print("=" * 60)

    # 1. 로그인 수행
    page.goto(BASE_URL)
    page.wait_for_selector("input[name='email']", timeout=15000)
    page.fill("input[name='email']", credentials["id_cso"])
    page.fill("input[name='password']", credentials["password"])
    page.click("button:has-text('로그인')")

    # 2. 대시보드 진입 단언
    page.wait_for_selector("h2:has-text('회원 업체 관리')", timeout=15000)
    expect(page).to_have_url(re.compile(r".*dashboard.*"))
    expect(page.locator("h2", has_text="회원 업체 관리").first).to_be_visible()
    print("[Success] TC-AUT-02 CSO 정상 로그인 검증 성공!")


def test_tc_aut_03_pharm_successful_login(page: Page, credentials):
    """
    [TC-AUT-03] Happy Path: 제약사 정상 로그인 검증
    - 제약사 계정 로그인 ➡️ 대시보드 진입 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-03] 제약사 정상 로그인 검증 시작")
    print("=" * 60)

    # 1. 로그인 수행
    page.goto(BASE_URL)
    page.wait_for_selector("input[name='email']", timeout=15000)
    page.fill("input[name='email']", credentials["id_pharm1"])
    page.fill("input[name='password']", credentials["password"])
    page.click("button:has-text('로그인')")

    # 2. 제약사 대시보드 진입 단언
    page.wait_for_selector("xpath=//h2[contains(., '회원 업체 관리')] | //h2[contains(., '계약서 관리')] | //h2[contains(., '받은 재위탁 통보서')]", timeout=15000)
    expect(page).to_have_url(re.compile(r".*dashboard.*"))
    print("[Success] TC-AUT-03 제약사 정상 로그인 검증 성공!")


def test_tc_aut_04_invalid_credentials_login_blocked(page: Page):
    """
    [TC-AUT-04] Negative: 잘못된 계정 정보 로그인 차단 검증
    - 미등록/오류 계정 시도 시 대시보드 진입 차단 및 로그인 페이지 유지 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-04] 잘못된 계정 로그인 차단 검증 시작")
    print("=" * 60)

    # 1. 잘못된 계정 로그인 시도
    page.goto(BASE_URL)
    page.wait_for_selector("input[name='email']", timeout=15000)
    page.fill("input[name='email']", "invalid_cso_9999@parmple.com")
    page.fill("input[name='password']", "wrong_pw_123456!")
    page.click("button:has-text('로그인')")
    page.wait_for_timeout(2000)

    # 2. 대시보드로 이동하지 않고 로그인 페이지 유지 단언
    expect(page).to_have_url(re.compile(r".*auth/login.*"))
    expect(page.locator("button:has-text('로그인')")).to_be_visible()
    print("[Success] TC-AUT-04 잘못된 계정 로그인 차단 검증 성공!")


def test_tc_aut_05_signup_page_navigation(page: Page):
    """
    [TC-AUT-05] Happy Path: 회원가입 화면 이동 및 렌더링 검증
    - '회원가입' 링크 클릭 ➡️ /auth/register 이동 및 사업자번호 입력창/확인 버튼 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-05] 회원가입 화면 이동 검증 시작")
    print("=" * 60)

    # 1. 로그인 페이지 진입 후 회원가입 클릭
    page.goto(BASE_URL)
    page.wait_for_selector("a:has-text('회원가입')", timeout=15000)
    page.locator("a:has-text('회원가입')").first.click()

    # 2. 회원가입 페이지 렌더링 단언
    page.wait_for_selector("input[placeholder*='-없이 숫자만 입력']", timeout=10000)
    expect(page).to_have_url(re.compile(r".*auth/register.*"))
    expect(page.locator("input[placeholder*='-없이 숫자만 입력']")).to_be_visible()
    expect(page.locator("button:has-text('확인')")).to_be_visible()
    print("[Success] TC-AUT-05 회원가입 화면 이동 검증 성공!")


def test_tc_aut_06_signup_return_to_login(page: Page):
    """
    [TC-AUT-06] Validation: 회원가입에서 '로그인으로 돌아가기' 검증
    - '로그인으로 돌아가기' 버튼 클릭 ➡️ 다시 /auth/login 복귀 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-06] 회원가입에서 로그인 복귀 검증 시작")
    print("=" * 60)

    # 1. 회원가입 페이지 직접 이동
    page.goto(BASE_URL + "auth/register")
    page.wait_for_selector("button:has-text('로그인으로 돌아가기')", timeout=10000)

    # 2. 돌아가기 클릭
    page.locator("button:has-text('로그인으로 돌아가기')").first.click()

    # 3. 로그인 페이지 복귀 단언
    page.wait_for_selector("input[name='email']", timeout=10000)
    expect(page).to_have_url(re.compile(r".*auth/login.*"))
    expect(page.locator("input[name='email']")).to_be_visible()
    print("[Success] TC-AUT-06 로그인 복귀 검증 성공!")


def test_tc_aut_07_signup_business_number_disabled_validation(page: Page):
    """
    [TC-AUT-07] Phase 2 Validation: 회원가입 사업자번호 미입력/불완전 입력 시 '확인' 버튼 disabled 방어 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-07] 회원가입 사업자번호 비활성화(disabled) 방어 검증 시작")
    print("=" * 60)

    # 1. 회원가입 화면 진입
    page.goto(BASE_URL + "auth/register")
    page.wait_for_selector("input[placeholder*='-없이 숫자만 입력']", timeout=10000)

    confirm_btn = page.locator("button:has-text('확인')").first
    expect(confirm_btn).to_be_visible()

    # 2. 빈 상태에서 확인 버튼 disabled 단언
    print("[Step 1] 빈 입력 상태에서 '확인' 버튼 disabled 단언")
    expect(confirm_btn).to_be_disabled()

    # 3. 불완전한 번호(123) 입력 후 disabled 유지 단언
    print("[Step 2] 3자리 짧은 번호 입력 시 '확인' 버튼 disabled 유지 단언")
    page.fill("input[placeholder*='-없이 숫자만 입력']", "123")
    page.wait_for_timeout(300)
    expect(confirm_btn).to_be_disabled()
    print("[Success] TC-AUT-07 회원가입 사업자번호 방어 검증 성공!")


def test_tc_aut_08_find_password_page_navigation(page: Page):
    """
    [TC-AUT-08] Phase 2 Happy Path: 로그인 화면에서 '비밀번호 재설정' 링크 클릭 및 렌더링 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-08] 비밀번호 재설정 화면 이동 검증 시작")
    print("=" * 60)

    # 1. 로그인 페이지 진입
    page.goto(BASE_URL)
    page.wait_for_selector("a:has-text('비밀번호 재설정')", timeout=15000)

    # 2. '비밀번호 재설정' 클릭
    print("[Step 1] '비밀번호 재설정' 링크 클릭")
    page.click("a:has-text('비밀번호 재설정')")

    # 3. /auth/find-password 이동 및 폼 가시성 단언
    print("[Step 2] /auth/find-password 렌더링 및 이메일 입력창 단언")
    page.wait_for_selector("input[placeholder*='이메일']", timeout=10000)
    expect(page).to_have_url(re.compile(r".*auth/find-password.*"))
    expect(page.locator("input[placeholder*='이메일']").first).to_be_visible()
    expect(page.locator("a[href*='/auth/login'], button:has-text('취소')").first).to_be_visible()
    print("[Success] TC-AUT-08 비밀번호 재설정 화면 이동 검증 성공!")


def test_tc_aut_09_find_id_page_navigation(page: Page):
    """
    [TC-AUT-09] Phase 2 Happy Path: 로그인 화면에서 '아이디 찾기' 링크 클릭 및 렌더링 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-09] 아이디 찾기 화면 이동 검증 시작")
    print("=" * 60)

    # 1. 로그인 페이지 진입
    page.goto(BASE_URL)
    page.wait_for_selector("a:has-text('아이디 찾기')", timeout=15000)

    # 2. '아이디 찾기' 클릭
    print("[Step 1] '아이디 찾기' 링크 클릭")
    page.click("a:has-text('아이디 찾기')")

    # 3. /auth/find-id 이동 및 폼 가시성 단언
    print("[Step 2] /auth/find-id 렌더링 및 본인인증 폼 단언")
    page.wait_for_selector("button:has-text('아이디 찾기')", timeout=10000)
    expect(page).to_have_url(re.compile(r".*auth/find-id.*"))
    expect(page.locator("input[placeholder*='-없이 숫자만 입력']").first).to_be_visible()
    expect(page.locator("button:has-text('아이디 찾기')").first).to_be_visible()
    print("[Success] TC-AUT-09 아이디 찾기 화면 이동 검증 성공!")


def test_tc_aut_10_find_password_return_to_login(page: Page):
    """
    [TC-AUT-10] Phase 2 Validation: 비밀번호 재설정 화면에서 '취소/로그인 복귀' 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-10] 비밀번호 재설정에서 로그인 복귀 검증 시작")
    print("=" * 60)

    # 1. 재설정 페이지 진입
    page.goto(BASE_URL + "auth/find-password")
    page.wait_for_selector("a[href*='/auth/login'], button:has-text('취소')", timeout=10000)

    # 2. '취소' 클릭
    print("[Step 1] '취소' 링크/버튼 클릭")
    page.locator("a[href*='/auth/login'], button:has-text('취소')").first.click()

    # 3. 로그인 페이지 복귀 단언
    print("[Step 2] /auth/login 복귀 단언")
    page.wait_for_selector("input[name='email']", timeout=10000)
    expect(page).to_have_url(re.compile(r".*auth/login.*"))
    expect(page.locator("input[name='email']")).to_be_visible()
    print("[Success] TC-AUT-10 비밀번호 재설정에서 로그인 복귀 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_aut_11_full_cycle_signup_and_admin_approval_e2e(page: Page, credentials):
    """
    [TC-AUT-11] Phase 3 E2E: 신규 회원가입 ➡️ Gmail 실시간 인증 ➡️ Admin API 승인 ➡️ 신규 계정 로그인 Full Flow
    - Google Sheet에서 새 사업자번호 추출 및 기록
    - 필수 증빙 파일 첨부 (사업자등록증, CSO신고증)
    - 고유 이메일 생성 및 Gmail IMAP 실시간 인증번호 자동 추출/입력
    - 회원가입 완료 후 Admin API 승인 호출
    - 가입된 신규 계정으로 실제 로그인 및 로그아웃 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-11] 신규 회원가입 및 Admin 승인/로그인 E2E 워크플로우 시작")
    print("=" * 60)

    # 1. 로그인 페이지 이동 및 회원가입 버튼 클릭
    print("[Step 1] 회원가입 페이지 이동")
    page.goto(BASE_URL)
    page.wait_for_selector("a:has-text('회원가입')", timeout=15000)
    page.click("a:has-text('회원가입')")

    # 2. 사업자등록번호 입력
    print("[Step 2] Google Sheet에서 미사용 사업자번호 가져오기")
    biz_no = get_biz_no_from_sheet()
    if biz_no.startswith("ERROR") or biz_no == "NO_BIZ_NO":
        pytest.fail(f"사용 가능한 사업자번호를 가져오지 못했습니다: {biz_no}")
    
    clean_biz_no = record_biz_number(biz_no)
    print(f"-> 사용할 사업자번호: {clean_biz_no}")

    page.wait_for_selector("input#bizNumber, input[placeholder*='-없이 숫자만 입력']", timeout=10000)
    page.fill("input#bizNumber, input[placeholder*='-없이 숫자만 입력']", clean_biz_no)
    page.click("button:has-text('확인')")

    # 신규 가입 가능 팝업 확인
    page.wait_for_selector("h2:has-text('신규 가입 가능한 사업자번호 입니다')", timeout=10000)
    page.locator("button", has_text="확인").last.click()

    # 3. 회원가입 상세 페이지 진입 및 파일 첨부
    print("[Step 3] 회원가입 상세 페이지 확인 및 필수 증빙 파일 첨부")
    page.wait_for_selector("h1:has-text('회원가입')", timeout=10000)

    page.locator("#bizRegCertFileUuid input[type='file']").set_input_files(TESTFILE_PATH1)
    page.wait_for_timeout(500)
    page.locator("#salesCertFileUuid input[type='file']").set_input_files(TESTFILE_PATH2)
    page.wait_for_timeout(500)

    # 4. 이메일 생성 및 인증번호 발송 요청
    print("[Step 4] 고유 이메일 생성 및 Gmail 인증번호 발송 요청")
    email_addr = generate_email()
    TestContext.registered_email = email_addr
    print(f"-> 생성된 이메일: {email_addr}")

    page.fill("input#email", email_addr)
    page.click("button:has-text('인증번호 발송')")
    
    page.wait_for_selector("h2:has-text('이메일로 인증번호를 발송했습니다.')", timeout=10000)
    page.click("button:has-text('확인')")

    # 5. 이메일 인증번호 수신 및 입력
    print("[Step 5] Gmail IMAP에서 인증번호 수신 대기...")
    page.wait_for_timeout(5000)
    auth_code = fetch_auth_code(max_retries=10, retry_delay=3)
    print(f"-> 수신된 인증번호: {auth_code}")
    
    if auth_code == "NO_CODE" or not auth_code.isdigit():
        pytest.fail(f"이메일 인증번호 수신에 실패했습니다: {auth_code}")

    page.fill("input#emailVerificationKey", auth_code)
    page.click("button:has-text('인증하기')")
    page.wait_for_timeout(500)

    # 6. 비밀번호 및 담당자 정보 입력
    print("[Step 6] 비밀번호 및 회원정보(이름/연락처) 입력")
    page.fill("input#password", credentials["password"])
    page.fill("input#passwordCheck", credentials["password"])

    page.fill("input#name", "자동화테스트")
    random_phone = f"010{random.randint(10000000, 99999999)}"
    page.fill("input#phone", random_phone)

    # 7. 약관 동의 및 가입하기 제출
    print("[Step 7] 약관 전체 동의 및 가입 신청 제출")
    page.click("button#termsAll")
    page.click("button:has-text('가입하기')")

    # 가입 완료 팝업 확인
    page.wait_for_selector("button:has-text('확인')", timeout=10000)
    page.click("button:has-text('확인')")
    page.wait_for_timeout(1000)

    # 8. Admin API 승인 절차 수행
    print("[Step 8] Admin API를 통한 업체 즉시 승인 처리")
    approve_pending_company_via_admin()
    page.wait_for_timeout(1000)

    # 9. 방금 가입한 신규 계정으로 로그인 검증
    print("[Step 9] 신규 가입 계정으로 대시보드 로그인 검증")
    page.goto(BASE_URL)
    page.wait_for_selector("input[name='email']", timeout=10000)
    page.fill("input[name='email']", email_addr)
    page.fill("input[name='password']", credentials["password"])
    page.click("button:has-text('로그인')")

    page.wait_for_selector("h2:has-text('내 정보')", timeout=15000)
    expect(page.locator("h2", has_text="내 정보")).to_be_visible()

    # 10. 로그아웃 수행
    print("[Step 10] 로그아웃 수행 및 복귀 검증")
    page.click("button:has-text('로그아웃')")
    page.wait_for_selector("a:has-text('회원가입')", timeout=10000)
    print("[Success] TC-AUT-11 신규 회원가입 및 Admin 승인/로그인 E2E 워크플로우 완결 성공!")


def test_tc_aut_12_find_id_e2e_flow(page: Page):
    """
    [TC-AUT-12] Phase 3 E2E: 마지막으로 가입한 사업자번호 기반 아이디 찾기 Full Flow 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-AUT-12] 가입 사업자번호 기반 아이디 찾기 E2E 워크플로우 시작")
    print("=" * 60)

    # 1. 페이지 이동
    page.goto(BASE_URL)
    page.wait_for_selector("a:has-text('아이디 찾기')", timeout=10000)
    page.click("a:has-text('아이디 찾기')")

    # 2. 아이디 찾기 페이지 확인
    heading = page.locator("h1", has_text="가입정보 확인 후 아이디를 찾을 수 있습니다")
    heading.wait_for(timeout=10000)

    # 3. 마지막으로 사용했던 사업자번호 조회
    last_biz_no = get_last_biz_number()
    print(f"-> 조회할 사업자번호: {last_biz_no}")

    page.fill("input#businessNumber, input[placeholder*='-없이 숫자만 입력']", last_biz_no)
    page.fill("input#name, input[placeholder*='홍길동']", "자동화테스트")
    page.click("button:has-text('아이디 찾기')")

    # 4. 결과 팝업 확인
    print("[Step 2] 가입 아이디 조회 결과 팝업 단언")
    result_popup = page.locator("h2", has_text="가입하신 아이디 입니다")
    result_popup.wait_for(timeout=10000)
    expect(result_popup).to_be_visible()

    page.click("button:has-text('확인')")
    page.wait_for_selector("a:has-text('회원가입')", timeout=10000)
    print("[Success] TC-AUT-12 아이디 찾기 E2E 워크플로우 완결 성공!")
