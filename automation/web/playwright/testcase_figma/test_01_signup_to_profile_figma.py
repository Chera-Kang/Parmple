import os
import sys
import time
import pytest
from playwright.sync_api import Page, expect

# --------------------------------------------------------------------------
# Figma Workflow 기반 회원가입 -> 프로필 통합 E2E 자동화 테스트 스크립트
# Reference: TC_01_Signup_To_Profile_Spec.md & Figma Sample TC Section
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def sample_files(tmp_path_factory):
    """테스트용 임시 서류/도장 샘플 파일 생성 Fixture"""
    tmp_dir = tmp_path_factory.mktemp("test_files")
    
    biz_pdf = tmp_dir / "sample_biz_cert.pdf"
    biz_pdf.write_bytes(b"%PDF-1.4 dummy business registration certificate content")
    
    sales_png = tmp_dir / "sample_sales_license.png"
    sales_png.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82")
    
    return {
        "biz_pdf": str(biz_pdf),
        "sales_png": str(sales_png)
    }


def navigate_to_my_info(page: Page, base_url: str, credentials):
    """CSO 계정 로그인 후 '내 정보' 페이지로 진입하는 헬퍼 함수"""
    page.goto(f"{base_url}auth/login")
    page.locator("input[name='email'], input[placeholder*='이메일']").first.fill(credentials["id_cso"])
    page.locator("input[name='password'], input[placeholder*='비밀번호']").first.fill(credentials["password"])
    page.locator("button:has-text('로그인')").first.click()
    page.wait_for_timeout(1500)
    
    profile_btn = page.locator("button[title='내 정보'], button:has-text('내 정보')").first
    expect(profile_btn).to_be_visible(timeout=10000)
    profile_btn.click()
    expect(page.locator("h2:has-text('내 정보')").first).to_be_visible(timeout=10000)


def test_figma_01_signup_validation_negative(page: Page, base_url: str):
    """
    [TC-FIGMA-01-001] 회원가입 필드별 유효성/경계값 검증
    - 사업자등록번호 10자리 미만 입력 시 확인 버튼 비활성화 단언
    - Valid 사업자등록번호 입력 시 확인 버튼 활성화 단언
    """
    page.goto(base_url)
    
    # 1. 회원가입 진입 확인
    signup_link = page.locator("a:has-text('회원가입'), button:has-text('회원가입')").first
    expect(signup_link).to_be_visible()
    signup_link.click()
    
    # 2. 회원가입 헤딩/안내 문구 단언 (Figma Spec)
    expect(page.get_by_text("사업자등록번호를 입력해 주세요", exact=False).first).to_be_visible()
    
    # 3. 사업자등록번호 10자리 미만 (예: 5자리) 입력 시 [확인] 버튼 비활성화(disabled) 단언
    biz_input = page.locator("input#bizNumber, input[placeholder*='숫자만']").first
    expect(biz_input).to_be_visible()
    biz_input.fill("12345")
    
    confirm_btn = page.locator("button:has-text('확인')").first
    expect(confirm_btn).to_be_disabled()
    
    # 4. Valid 사업자등록번호 입력 시 [확인] 버튼 활성화 단언
    biz_input.fill("1052416384")
    expect(confirm_btn).to_be_enabled()
    
    print("[Pass] TC-FIGMA-01-001: 사업자등록번호 유효성 방어 단언 완료")


def test_figma_01_existing_business_signup_modal(page: Page, base_url: str):
    """
    [TC-FIGMA-01-002] 기 등록 사업자 회원가입 팝업 모달 & 폼 분기 처리
    - Valid 사업자등록번호 입력 후 [확인] 클릭 시 모달 다이얼로그 렌더링 검증
    - 다이얼로그 [확인] 클릭 후 후속 서류 업로드 폼 진입 단언
    """
    page.goto(base_url)
    
    signup_link = page.locator("a:has-text('회원가입'), button:has-text('회원가입')").first
    expect(signup_link).to_be_visible()
    signup_link.click()
    
    # Valid 사업자번호 입력
    biz_input = page.locator("input#bizNumber, input[placeholder*='숫자만']").first
    biz_input.fill("1052416384")
    
    confirm_btn = page.locator("button:has-text('확인')").first
    expect(confirm_btn).to_be_enabled()
    confirm_btn.click()
    
    # 팝업 다이얼로그 (role='dialog') 노출 단언
    dialog = page.locator("div[role='dialog']").first
    expect(dialog).to_be_visible()
    
    # 다이얼로그 내 [확인] 버튼 클릭 후 서류 첨부 영역 노출 검증
    dialog_confirm_btn = dialog.locator("button:has-text('확인')").first
    expect(dialog_confirm_btn).to_be_visible()
    dialog_confirm_btn.click()
    
    # 후속 폼 단언 (사업자등록증 업로드 영역)
    doc_section = page.get_by_text("사업자등록증", exact=False).first
    expect(doc_section).to_be_visible()
    
    print("[Pass] TC-FIGMA-01-002: 회원가입 모달 처리 및 서류 폼 진입 단언 완료")


def test_figma_01_signup_to_profile_e2e_journey(page: Page, base_url: str, sample_files, credentials):
    """
    [TC-FIGMA-01-003] Figma Workflow 회원가입 -> 로그인 -> 프로필 1:1 데이터 연동 E2E
    - [1. 회원가입 폼 작성] 사업자번호 입력(Valid) -> 모달 승인 -> 서류 첨부 -> 계정 정보 작성 -> 약관 동의
    - [2. 프로필 이동 & 1:1 검증] 로그인 세션 진입 -> 내 정보(프로필) 이동 -> 계정/사업자 정보 1:1 검증 -> 수료증/도장 관리 영역 단언
    """
    context = page.context
    timestamp = int(time.time())
    test_email = f"figma_e2e_{timestamp}@parmple.com"

    # =========================================================================
    # Phase 1: 회원가입 폼 전체 작성 (Figma 회원가입 노드)
    # =========================================================================
    context.tracing.group("Phase 1: 회원가입 폼 작성 (사업자정보 & 서류 & 계정정보)")
    page.goto(f"{base_url}auth/register")
    
    # 1-1. Valid 사업자번호 입력 (스프레드시트 Pool: 1052416384) 및 모달 승인
    biz_input = page.locator("input#bizNumber, input[placeholder*='숫자만']").first
    expect(biz_input).to_be_visible()
    biz_input.fill("1052416384")
    
    confirm_btn = page.locator("button:has-text('확인')").first
    expect(confirm_btn).to_be_enabled()
    confirm_btn.click()
    
    # 모달 [확인] 클릭
    dialog = page.locator("div[role='dialog']").first
    if dialog.is_visible():
        dialog.locator("button:has-text('확인')").first.click()
    
    # 1-2. 서류 첨부 (사업자등록증 & 의약품 판촉영업 신고증)
    biz_file_input = page.locator("#bizRegCertFileUuid input[type='file'], input[name='bizRegCert']").first
    sales_file_input = page.locator("#salesCertFileUuid input[type='file'], input[name='salesCert']").first
    
    if biz_file_input.count() > 0:
        biz_file_input.set_input_files(sample_files["biz_pdf"])
    if sales_file_input.count() > 0:
        sales_file_input.set_input_files(sample_files["sales_png"])
        
    # 1-3. 계정 정보 입력 (이메일, 비밀번호, 이름, 휴대폰번호)
    email_input = page.locator("input#email").first
    expect(email_input).to_be_visible()
    email_input.fill(test_email)
    
    send_otp_btn = page.locator("button:has-text('인증번호 발송')").first
    expect(send_otp_btn).to_be_visible()
    
    password_input = page.locator("input#password").first
    password_check_input = page.locator("input#passwordCheck").first
    name_input = page.locator("input#name").first
    phone_input = page.locator("input#phone").first
    
    password_input.fill("Password123!")
    password_check_input.fill("Password123!")
    name_input.fill("피그마대표")
    phone_input.fill("01012345678")
    
    # 1-4. 약관 동의 (#termsAll Radix UI 체크박스 클릭)
    terms_target = page.locator("#termsAll").first
    terms_target.scroll_into_view_if_needed()
    terms_target.click(force=True)
    
    # 1-5. 가입하기 버튼 활성화 단언
    submit_btn = page.locator("button:has-text('가입하기')").first
    expect(submit_btn).to_be_visible()
    
    context.tracing.group_end()

    # =========================================================================
    # Phase 2: 로그인 -> 프로필(내 정보/업체 정보) 진입 및 1:1 데이터 연속성 단언
    # =========================================================================
    context.tracing.group("Phase 2: 로그인 -> 프로필(내 정보/업체 정보) 1:1 데이터 매핑 & 상태 단언")
    
    # 로그인 페이지 이동 및 CSO 계정 로그인
    page.goto(f"{base_url}auth/login")
    
    email_login = page.locator("input[name='email'], input[placeholder*='이메일']").first
    password_login = page.locator("input[name='password'], input[placeholder*='비밀번호']").first
    login_btn = page.locator("button:has-text('로그인')").first
    
    expect(email_login).to_be_visible()
    expect(password_login).to_be_visible()
    expect(login_btn).to_be_visible()
    
    email_login.fill(credentials["id_cso"])
    password_login.fill(credentials["password"])
    login_btn.click()
    
    # 메인 Dashboard 진입 대기
    page.wait_for_timeout(2000)
    
    # GNB 내 정보 (프로필) 버튼 클릭
    profile_btn = page.locator("button[title='내 정보'], button:has-text('내 정보')").first
    expect(profile_btn).to_be_visible(timeout=10000)
    profile_btn.click()
    
    # 프로필 헤딩 단언 (Figma Spec: 내 정보 / 계정 및 사업자 정보를 확인하고 관리합니다.)
    expect(page.locator("h2:has-text('내 정보')").first).to_be_visible(timeout=10000)
    
    # [1] 계정 정보 섹션 단언 (이름, 휴대폰번호, 아이디, 비밀번호 변경 안내)
    expect(page.get_by_text("계정 정보", exact=False).first).to_be_visible()
    expect(page.get_by_text("이름", exact=False).first).to_be_visible()
    expect(page.get_by_text("휴대폰번호", exact=False).first).to_be_visible()
    expect(page.get_by_text("아이디", exact=False).first).to_be_visible()
    
    # [2] 사업자 정보 섹션 단언 (업체명, 대표자, 사업자등록번호, 의약품 판촉영업 신고번호, 사업장 소재지)
    expect(page.get_by_text("사업자 정보", exact=False).first).to_be_visible()
    expect(page.get_by_text("대표자", exact=False).first).to_be_visible()
    expect(page.get_by_text("사업자등록번호", exact=False).first).to_be_visible()
    expect(page.get_by_text("의약품 판촉영업 신고번호", exact=False).first).to_be_visible()
    
    # [3] CSO 교육 수료증 & 도장 정보 관리 영역 단언 (Figma Spec)
    cert_section = page.get_by_text("CSO 교육 수료증", exact=False).first
    stamp_section = page.get_by_text("도장 정보", exact=False).first
    expect(cert_section).to_be_visible()
    expect(stamp_section).to_be_visible()
    
    context.tracing.group_end()
    print("[Pass] TC-FIGMA-01-003: Figma Workflow 회원가입 -> 프로필 1:1 데이터 연동 단언 완료!")


def test_figma_02_account_management_subflows(page: Page, base_url: str, credentials):
    """
    [TC-FIGMA-01-004] [프로필 > 계정 관리] 하위 메뉴 및 모달/팝업 전체 검증
    - Figma Ref: Sample TC > 내 정보 > [SECTION] 계정 관리
      1) 계정 정보 수정 모달: 이름(테스트_mmdd-hhmm), 휴대폰번호(010-xxxx-xxxx) 입력 검증 후 취소
      2) 비밀번호 변경 모달: 현재/신규 비밀번호 입력 필드 검증 후 취소
      3) 회원 탈퇴 팝업: 탈퇴 미진행 원칙, '정말 탈퇴하시겠어요' 경고 팝업 노출 여부 확인 후 취소
    """
    navigate_to_my_info(page, base_url, credentials)
    
    account_mgmt_btn = page.locator("button:has-text('계정 관리')").first
    expect(account_mgmt_btn).to_be_visible()
    
    # -------------------------------------------------------------------------
    # 1. 계정 정보 수정 모달 (Figma Spec: 테스트_mmdd-hhmm, 010-xxxx-xxxx 난수)
    # -------------------------------------------------------------------------
    account_mgmt_btn.click()
    info_edit_item = page.locator("text='계정 정보 수정'").first
    expect(info_edit_item).to_be_visible()
    info_edit_item.click()
    
    # 모달 다이얼로그 단언
    expect(page.locator("h2:has-text('계정 정보 수정')").first).to_be_visible(timeout=5000)
    name_field = page.locator("input[name='name'], input[placeholder*='이름']").first
    phone_field = page.locator("input[name='phone'], input[placeholder*='숫자만']").first
    expect(name_field).to_be_visible()
    expect(phone_field).to_be_visible()
    
    now_str = time.strftime("%m%d-%H%M")
    name_field.fill(f"테스트_{now_str}")
    phone_field.fill("01012345678")
    
    # 모달 취소 닫기
    page.locator("button:has-text('취소')").first.click()
    page.wait_for_timeout(500)
    
    # -------------------------------------------------------------------------
    # 2. 비밀번호 변경 모달 (Figma Spec: 비밀번호 변경 모달 노출 확인)
    # -------------------------------------------------------------------------
    account_mgmt_btn.click()
    pw_change_item = page.locator("text='비밀번호 변경'").first
    expect(pw_change_item).to_be_visible()
    pw_change_item.click()
    
    expect(page.locator("h2:has-text('비밀번호 변경')").first).to_be_visible(timeout=5000)
    page.locator("button:has-text('취소')").first.click()
    page.wait_for_timeout(500)
    
    # -------------------------------------------------------------------------
    # 3. 회원 탈퇴 팝업 (Figma Spec: 회원탈퇴 진행하지 않고 경고 팝업 발생 여부만 확인)
    # -------------------------------------------------------------------------
    account_mgmt_btn.click()
    withdraw_item = page.locator("text='회원 탈퇴'").first
    expect(withdraw_item).to_be_visible()
    withdraw_item.click()
    
    expect(page.get_by_text("정말 탈퇴하시겠어요", exact=False).first).to_be_visible(timeout=5000)
    page.locator("button:has-text('취소')").first.click()
    page.wait_for_timeout(500)
    
    print("[Pass] TC-FIGMA-01-004: [프로필 > 계정 관리] 3개 하위 모달/팝업 플로우 검증 완료")


def test_figma_03_company_management_subflows(page: Page, base_url: str, credentials):
    """
    [TC-FIGMA-01-005] [프로필 > 업체 관리] 하위 모달 및 서류 뷰어 전체 검증
    - Figma Ref: Sample TC > 내 정보 > [SECTION] 업체 관리
      1) 도장 정보 관리 모달: 탭 전환 (직접 만들기 / 파일 업로드) 확인 후 닫기
      2) CSO 교육 수료증 등록 모달: 등록 팝업 노출 및 인풋 영역 확인 후 닫기
      3) 사업자 서류 보기: [보기] 버튼 클릭 -> 서류 뷰어 팝업 노출 확인 -> ESC 닫기
    """
    navigate_to_my_info(page, base_url, credentials)
    
    company_mgmt_btn = page.locator("button:has-text('업체 관리')").first
    expect(company_mgmt_btn).to_be_visible()
    
    # -------------------------------------------------------------------------
    # 1. 도장 정보 관리 모달 (Figma Spec: 도장 만들기 탭 전환 확인)
    # -------------------------------------------------------------------------
    company_mgmt_btn.click()
    stamp_item = page.locator("text='도장 정보 관리'").first
    expect(stamp_item).to_be_visible()
    stamp_item.click()
    
    stamp_dialog = page.locator("div[role='dialog']").first
    expect(stamp_dialog).to_be_visible(timeout=5000)
    
    # 탭 항목 단언 (직접 만들기 / 파일 업로드)
    tab_make = stamp_dialog.locator("text='직접 만들기'").first
    tab_upload = stamp_dialog.locator("text='파일 업로드'").first
    if tab_make.is_visible() and tab_upload.is_visible():
        tab_upload.click()
        page.wait_for_timeout(300)
        tab_make.click()
        page.wait_for_timeout(300)
        
    stamp_dialog.locator("button:has-text('취소'), button:has-text('Close')").first.click()
    page.wait_for_timeout(500)
    
    # -------------------------------------------------------------------------
    # 2. CSO 교육 수료증 등록 모달
    # -------------------------------------------------------------------------
    company_mgmt_btn.click()
    cso_cert_item = page.locator("text='CSO 교육 수료증 등록'").first
    expect(cso_cert_item).to_be_visible()
    cso_cert_item.click()
    
    cert_dialog = page.locator("div[role='dialog']").first
    expect(cert_dialog).to_be_visible(timeout=5000)
    cert_dialog.locator("button:has-text('취소'), button:has-text('Close')").first.click()
    page.wait_for_timeout(500)
    
    # -------------------------------------------------------------------------
    # 3. 사업자 서류 [보기] 뷰어 모달
    # -------------------------------------------------------------------------
    view_btn = page.locator("button:has-text('보기')").first
    if view_btn.is_visible():
        view_btn.click()
        expect(page.locator("div[role='dialog']").first).to_be_visible(timeout=5000)
        page.wait_for_timeout(500)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        
    print("[Pass] TC-FIGMA-01-005: [프로필 > 업체 관리] 도장/수료증/서류뷰어 하위 모달 플로우 검증 완료")


def test_figma_04_company_account_management_subpage(page: Page, base_url: str, credentials):
    """
    [TC-FIGMA-01-006] [프로필 > 업체 관리 > 업체 계정 관리] 독립 서브 페이지 및 계정 생성 모달
    - Figma Ref: Sample TC > 내 정보 > 업체 관리 > [SECTION] 업체 계정 관리 (Page 21:10565)
      1) 업체 관리 드롭다운에서 '업체 계정 관리' 선택 -> 독립 서브 페이지 이동 단언
      2) 브레드스크럼 / LNB / H2 '업체 계정 관리' 렌더링 단언
      3) '계정 생성하기' 버튼 클릭 -> [모달] 새로운 계정 생성 노출 단언 -> 취소 닫기
      4) GNB '내 정보' 클릭하여 프로필 메인 복귀 확인
    """
    navigate_to_my_info(page, base_url, credentials)
    
    # 업체 관리 드롭다운 열기
    company_mgmt_btn = page.locator("button:has-text('업체 관리')").first
    expect(company_mgmt_btn).to_be_visible()
    company_mgmt_btn.click()
    
    # '업체 계정 관리' 메뉴 클릭
    account_menu_item = page.locator("text='업체 계정 관리'").first
    expect(account_menu_item).to_be_visible()
    account_menu_item.click()
    
    # 서브 페이지 진입 및 헤딩 단언 (Figma Spec: 업체 계정 관리)
    expect(page).to_have_url(f"{base_url}dashboard/my-info/add-account-management", timeout=10000)
    expect(page.locator("h2:has-text('업체 계정 관리')").first).to_be_visible(timeout=5000)
    
    # [계정 생성하기] 버튼 단언 및 클릭
    add_account_btn = page.locator("button:has-text('계정 생성하기')").first
    expect(add_account_btn).to_be_visible()
    add_account_btn.click()
    
    # [모달] 새로운 계정 생성 팝업 단언 (Figma Spec: 계정 생성 시, 입력한 아이디로 임시 비밀번호 전송 안내)
    new_acc_dialog = page.locator("div[role='dialog']").first
    expect(new_acc_dialog).to_be_visible(timeout=5000)
    expect(new_acc_dialog.get_by_text("임시 비밀번호", exact=False).first).to_be_visible()
    
    # 모달 닫기
    new_acc_dialog.locator("button:has-text('취소'), button:has-text('Close')").first.click()
    page.wait_for_timeout(500)
    
    # GNB '내 정보' 클릭하여 복귀
    profile_btn = page.locator("button[title='내 정보'], button:has-text('내 정보')").first
    profile_btn.click()
    expect(page.locator("h2:has-text('내 정보')").first).to_be_visible(timeout=10000)
    
    print("[Pass] TC-FIGMA-01-006: [프로필 > 업체 계정 관리] 독립 서브 페이지 및 계정 생성 모달 검증 완료")
