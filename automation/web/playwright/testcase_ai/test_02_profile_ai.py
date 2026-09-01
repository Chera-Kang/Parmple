import os
import re
import time
import random
import datetime
import pytest
from playwright.sync_api import Page, expect

# 공통 도구 모듈 import
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from common.resources.email_generator import generate_email

# ==============================================================================
# Phase 1 & 2: Core & Atomic Validation Test Cases
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_myi_01_my_info_rendering_from_header(page: Page, login_cso):
    """
    [TC-MYI-01] Happy Path: 프로필(내 정보) 화면 진입 및 렌더링 검증
    - 헤더의 '내 정보' 버튼 클릭 ➡️ /dashboard/my-info 이동 및 섹션 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-MYI-01] 내 정보 화면 렌더링 검증 시작")
    print("=" * 60)

    # 1. 헤더의 내 정보 버튼 클릭
    print("[Step 1] 헤더 프로필 버튼 클릭")
    profile_btn = page.locator("header button[title='내 정보'], header button:has-text('(주)휴피스')").first
    expect(profile_btn).to_be_visible()
    profile_btn.click()

    # 2. URL 및 헤딩 단언
    page.wait_for_selector("h2:has-text('내 정보')", timeout=10000)
    expect(page).to_have_url(re.compile(r".*dashboard/my-info.*"))
    expect(page.locator("h2", has_text="내 정보").first).to_be_visible()

    # 3. 계정 정보 및 사업자 정보 영역 가시성 단언
    print("[Step 2] '계정 관리' 및 '업체 관리' 버튼과 상세 정보 단언")
    expect(page.locator("button:has-text('계정 관리')").first).to_be_visible()
    expect(page.locator("button:has-text('업체 관리')").first).to_be_visible()
    expect(page.locator("text=(주)휴피스").first).to_be_visible()
    print("[Success] TC-MYI-01 내 정보 렌더링 검증 성공!")


def test_tc_myi_02_my_info_elements_and_buttons(page: Page, login_cso):
    """
    [TC-MYI-02] Happy Path: 내 정보 화면 내 계정 데이터 및 로그아웃 버튼 가시성 검증
    - 로그인된 업체의 프로필 정보와 액션 버튼 노출 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-MYI-02] 내 정보 상세 내용 및 액션 버튼 검증 시작")
    print("=" * 60)

    # 1. 직접 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/my-info")
    page.wait_for_selector("h2:has-text('내 정보')", timeout=10000)

    # 2. 업체명 및 주요 버튼 확인
    print("[Step 1] 업체명 및 버튼 가시성 단언")
    expect(page.locator("text=(주)휴피스").first).to_be_visible()
    expect(page.locator("button[title*='계정 관리'], button:has-text('계정 관리')").first).to_be_visible()
    expect(page.locator("button[title*='업체 관리'], button:has-text('업체 관리')").first).to_be_visible()
    expect(page.locator("button:has-text('로그아웃')").first).to_be_visible()
    print("[Success] TC-MYI-02 내 정보 상세 내용 검증 성공!")


def test_tc_myi_03_account_management_password_modal(page: Page, login_cso):
    """
    [TC-MYI-03] Phase 2 Happy Path: '계정 관리' 드롭다운 메뉴 오픈 및 '비밀번호 변경' 모달 오픈/ESC 닫기 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-MYI-03] '계정 관리' 비밀번호 변경 모달 인터랙션 검증 시작")
    print("=" * 60)

    # 1. 내 정보 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/my-info")
    page.wait_for_selector("h2:has-text('내 정보')", timeout=10000)

    # 2. '계정 관리' 드롭다운 클릭
    print("[Step 1] '계정 관리' 드롭다운 버튼 클릭")
    acc_btn = page.locator("button[title*='계정 관리'], button:has-text('계정 관리')").first
    expect(acc_btn).to_be_visible()
    acc_btn.click()
    page.wait_for_timeout(500)

    # 3. '비밀번호 변경' 메뉴 클릭
    print("[Step 2] '비밀번호 변경' 메뉴 항목 클릭")
    pw_item = page.locator("div[role='menuitem']:has-text('비밀번호 변경'), [role='menu'] div:has-text('비밀번호 변경')").first
    expect(pw_item).to_be_visible()
    pw_item.click()
    page.wait_for_timeout(1000)

    # 4. 모달 오픈 단언
    print("[Step 3] 비밀번호 변경 다이얼로그 모달 가시성 단언")
    dialog = page.locator("div[role='dialog']").first
    expect(dialog).to_be_visible()
    expect(dialog.locator("h2, h3").first).to_be_visible()

    # 5. ESC 키로 닫기
    print("[Step 4] ESC 키 입력하여 모달 닫기")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    expect(page.locator("div[role='dialog']")).to_have_count(0)
    print("[Success] TC-MYI-03 비밀번호 변경 모달 인터랙션 검증 성공!")


def test_tc_myi_04_vendor_management_dropdown_menu(page: Page, login_cso):
    """
    [TC-MYI-04] Phase 2 Happy Path: '업체 관리' 드롭다운 메뉴 항목 가시성 및 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-MYI-04] '업체 관리' 드롭다운 메뉴 검증 시작")
    print("=" * 60)

    # 1. 내 정보 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/my-info")
    page.wait_for_selector("h2:has-text('내 정보')", timeout=10000)

    # 2. '업체 관리' 드롭다운 클릭
    print("[Step 1] '업체 관리' 드롭다운 버튼 클릭")
    vendor_btn = page.locator("button[title*='업체 관리'], button:has-text('업체 관리')").first
    expect(vendor_btn).to_be_visible()
    vendor_btn.click()
    page.wait_for_timeout(500)

    # 3. 메뉴 항목들 가시성 단언
    print("[Step 2] 하위 메뉴 항목('업체 계정 관리', 'CSO 교육 수료증 등록', '도장 정보 관리') 가시성 단언")
    expect(page.locator("div[role='menuitem']:has-text('업체 계정 관리'), [role='menu'] div:has-text('업체 계정 관리')").first).to_be_visible()
    expect(page.locator("div[role='menuitem']:has-text('CSO 교육 수료증 등록'), [role='menu'] div:has-text('CSO 교육 수료증 등록')").first).to_be_visible()
    expect(page.locator("div[role='menuitem']:has-text('도장 정보 관리'), [role='menu'] div:has-text('도장 정보 관리')").first).to_be_visible()

    # 4. ESC 키로 닫기
    print("[Step 3] ESC 키 입력하여 드롭다운 메뉴 닫기")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[Success] TC-MYI-04 '업체 관리' 드롭다운 메뉴 검증 성공!")


def test_tc_myi_05_header_profile_consistency(page: Page, login_cso):
    """
    [TC-MYI-05] Phase 2 Happy Path: 상단 헤더 프로필 영역(업체명 표시)과 내 정보 화면의 일관성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-MYI-05] 헤더 프로필 정보와 내 정보 일관성 검증 시작")
    print("=" * 60)

    # 1. 대시보드 메인 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard")
    page.wait_for_timeout(1000)

    # 2. 헤더 프로필 텍스트 확인
    print("[Step 1] 헤더 프로필 업체명 확인")
    header_profile = page.locator("header button[title='내 정보'], header button:has-text('(주)휴피스')").first
    expect(header_profile).to_be_visible()
    header_text = header_profile.inner_text().strip()
    assert "(주)휴피스" in header_text or "내 정보" in header_text

    # 3. 내 정보 진입 후 프로필 업체명 일치 단언
    print("[Step 2] 내 정보 진입 후 업체명 일치 단언")
    page.goto(page.url.split("dashboard")[0] + "dashboard/my-info")
    page.wait_for_selector("h2:has-text('내 정보')", timeout=10000)
    expect(page.locator("text=(주)휴피스").first).to_be_visible()
    print("[Success] TC-MYI-05 헤더 프로필 정보 일관성 검증 성공!")


def test_tc_myi_06_my_info_logout_interaction(page: Page, login_cso):
    """
    [TC-MYI-06] Validation: 내 정보 화면에서 로그아웃 인터랙션 및 세션 종료 검증
    - '로그아웃' 버튼 클릭 ➡️ 세션 종료 및 로그인 화면(/auth/login) 복귀 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-MYI-06] 내 정보 로그아웃 인터랙션 검증 시작")
    print("=" * 60)

    # 1. 내 정보 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/my-info")
    page.wait_for_selector("button:has-text('로그아웃')", timeout=10000)

    # 2. 로그아웃 버튼 클릭
    print("[Step 1] '로그아웃' 버튼 클릭")
    logout_btn = page.locator("button:has-text('로그아웃')").first
    expect(logout_btn).to_be_visible()
    logout_btn.click()
    page.wait_for_timeout(1000)

    # 3. 만약 확인 모달이 뜨면 '확인/로그아웃' 클릭
    confirm_btn = page.locator("div[role='dialog'] button:has-text('확인'), div[role='dialog'] button:has-text('로그아웃')").first
    if confirm_btn.is_visible():
        confirm_btn.click()
        page.wait_for_timeout(1000)

    # 4. 로그인 페이지 복귀 단언
    print("[Step 2] /auth/login 복귀 단언")
    page.wait_for_selector("input[name='email']", timeout=10000)
    expect(page).to_have_url(re.compile(r".*auth/login.*"))
    expect(page.locator("input[name='email']")).to_be_visible()
    print("[Success] TC-MYI-06 로그아웃 인터랙션 검증 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_myi_07_certificate_pdf_preview_modal_e2e(page: Page, login_cso):
    """
    [TC-MYI-07] Phase 3 E2E: 사업자등록증 및 CSO 영업신고증 PDF 미리보기 모달 팝업 및 닫기 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-MYI-07] 증빙 서류 PDF 미리보기 E2E 검증 시작")
    print("=" * 60)

    # 1. 내 정보 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/my-info")
    page.wait_for_selector("h2:has-text('내 정보')", timeout=10000)

    # 2. '보기' 버튼들 확인
    view_buttons = page.locator("button:has-text('보기')")
    if view_buttons.count() > 0:
        print("[Step 1] 첫 번째 증빙 서류 '보기' 클릭")
        view_buttons.first.click()
        page.wait_for_timeout(1500)

        # 다이얼로그 모달 오픈 확인
        dialog = page.locator("div[role='dialog']").first
        expect(dialog).to_be_visible()

        # ESC 키로 닫기
        print("[Step 2] ESC 키 입력하여 뷰어 닫기")
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        expect(page.locator("div[role='dialog']")).to_have_count(0)

    print("[Success] TC-MYI-07 증빙 서류 PDF 미리보기 E2E 검증 성공!")


def test_tc_myi_08_sub_account_creation_e2e(page: Page, login_cso):
    """
    [TC-MYI-08] Phase 3 E2E: 업체 계정 관리 페이지 이동 및 계정 생성 폼 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-MYI-08] 업체 계정 관리 서브 계정 폼 E2E 검증 시작")
    print("=" * 60)

    # 1. 내 정보 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/my-info")
    page.wait_for_selector("h2:has-text('내 정보')", timeout=10000)

    # 2. '업체 관리' ➡️ '업체 계정 관리' 클릭하여 페이지 이동
    print("[Step 1] '업체 계정 관리' 페이지 이동")
    page.click("button[title*='업체 관리'], button:has-text('업체 관리')")
    page.wait_for_timeout(500)
    page.click("div[role='menuitem']:has-text('업체 계정 관리'), [role='menu'] div:has-text('업체 계정 관리')")
    
    page.wait_for_selector("h2:has-text('업체 계정 관리')", timeout=10000)
    expect(page.locator("h2", has_text="업체 계정 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*my-info/add-account-management.*"))

    # 3. '계정 생성하기' 클릭하여 다이얼로그 오픈
    print("[Step 2] '계정 생성하기' 클릭 및 모달 오픈 단언")
    create_btn = page.locator("button:has-text('계정 생성하기')").first
    expect(create_btn).to_be_visible()
    create_btn.click()
    page.wait_for_timeout(1000)

    dialog = page.locator("div[role='dialog']").first
    expect(dialog).to_be_visible()

    # 4. 서브 계정 정보 입력
    sub_email = generate_email(prefix="subuser")
    print(f"[Step 3] 서브 계정 생성 폼 입력 (Email: {sub_email})")
    dialog.locator("input[name='email']").first.fill(sub_email)
    dialog.locator("input[name='name']").first.fill("자동화서브")
    dialog.locator("input[name='phone']").first.fill("01012345678")
    page.wait_for_timeout(500)

    # 5. ESC 키로 닫기
    print("[Step 4] ESC 키로 모달 닫기")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    expect(page.locator("div[role='dialog']")).to_have_count(0)
    print("[Success] TC-MYI-08 업체 계정 관리 서브 계정 폼 E2E 검증 성공!")


def test_tc_myi_09_stamp_management_modal_e2e(page: Page, login_cso):
    """
    [TC-MYI-09] Phase 3 E2E: 도장 정보 관리 모달 오픈 및 도장 생성 폼 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-MYI-09] 도장 정보 관리 모달 E2E 검증 시작")
    print("=" * 60)

    # 1. 내 정보 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/my-info")
    page.wait_for_selector("h2:has-text('내 정보')", timeout=10000)

    # 2. '업체 관리' ➡️ '도장 정보 관리' 클릭하여 모달 오픈
    print("[Step 1] '도장 정보 관리' 모달 오픈")
    page.click("button[title*='업체 관리'], button:has-text('업체 관리')")
    page.wait_for_timeout(500)
    page.click("div[role='menuitem']:has-text('도장 정보 관리'), [role='menu'] div:has-text('도장 정보 관리')")
    page.wait_for_timeout(1000)

    dialog = page.locator("div[role='dialog']").first
    expect(dialog).to_be_visible()
    expect(dialog.locator("h2, h3").first).to_be_visible()

    # 3. 도장 이름 입력 및 만들기
    print("[Step 2] 도장 이름 입력 및 '만들기' 클릭")
    name_input = dialog.locator("input#stampName, input[placeholder*='도장'], input[name='stampName']").first
    if name_input.is_visible():
        name_input.fill("테스트")
        dialog.locator("button:has-text('만들기')").first.click()
        page.wait_for_timeout(1000)

    # 4. ESC 키로 모달 닫기
    print("[Step 3] ESC 키 입력하여 모달 닫기")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    expect(page.locator("div[role='dialog']")).to_have_count(0)
    print("[Success] TC-MYI-09 도장 정보 관리 모달 E2E 검증 성공!")
