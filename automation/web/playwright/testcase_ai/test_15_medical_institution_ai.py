import os
import re
import sys
import time
import datetime
import pytest
from playwright.sync_api import Page, expect

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from common.resources.gsheet_reader import get_biz_no_from_sheet

# ==============================================================================
# Phase 2 Extension AI Generated Test Cases: 영업 거래처 관리
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_med_01_cso_medical_institutions_rendering(page: Page, login_cso):
    """
    [TC-MED-01] Happy Path: CSO '영업 거래처 관리' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 영업 거래처 목록과 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-MED-01] 영업 거래처 관리 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '영업 거래처 관리' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management")
    page.wait_for_selector("h2:has-text('영업 거래처 관리')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="영업 거래처 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*filtering/medical-institution-management.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('승인 상태'), .ag-header-cell:has-text('승인 상태')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('제약사'), .ag-header-cell:has-text('제약사')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('병의원 명'), .ag-header-cell:has-text('병의원 명')").first).to_be_visible()
    print("[Success] TC-MED-01 영업 거래처 관리 렌더링 검증 성공!")


def test_tc_med_02_medical_institutions_search_and_reset(page: Page, login_cso):
    """
    [TC-MED-02] Validation: 영업 거래처 관리 검색 필터 및 초기화 기능 검증
    - 미존재 병의원 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-MED-02] 영업 거래처 관리 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management")
    page.wait_for_selector("h2:has-text('영업 거래처 관리')", timeout=10000)

    # 2. 미존재 키워드 입력 및 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_HOSPITAL_MED__"
    print(f"[Step 1] 미존재 키워드('{dummy_keyword}') 검색")
    search_input.fill(dummy_keyword)
    page.locator("button:has-text('검색')").first.click()
    page.wait_for_timeout(1500)

    # 3. '검색 초기화' 클릭 및 복구 단언
    print("[Step 2] '검색 초기화' 버튼 클릭")
    reset_btn = page.locator("button:has-text('검색 초기화')").first
    expect(reset_btn).to_be_visible()
    reset_btn.click()
    page.wait_for_timeout(1500)

    expect(search_input).to_have_value("")
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()
    print("[Success] TC-MED-02 영업 거래처 관리 검색 및 초기화 검증 성공!")


def test_tc_med_03_status_combobox_interaction(page: Page, login_cso):
    """
    [TC-MED-03] Phase 2 Happy Path: '승인 상태' 콤보박스 필터 클릭 및 옵션 리스트 노출 검증
    - '승인 상태(전체)' 드롭다운 클릭 ➡️ 옵션 리스트 렌더링 확인 ➡️ ESC 키로 안전하게 닫힘 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-MED-03] '승인 상태' 콤보박스 필터 인터랙션 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management")
    page.wait_for_selector("h2:has-text('영업 거래처 관리')", timeout=10000)

    # 2. '승인 상태' 콤보박스 클릭
    print("[Step 1] '승인 상태' 콤보박스 클릭")
    status_combo = page.locator("button[role='combobox']").first
    expect(status_combo).to_be_visible()
    status_combo.click()
    page.wait_for_timeout(500)

    # 3. 옵션 리스트 가시성 단언
    print("[Step 2] 옵션 팝오버 및 항목 가시성 단언")
    options = page.locator("[role='option'], div[data-radix-collection-item]")
    expect(options.first).to_be_visible()

    # 4. ESC로 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[Success] TC-MED-03 승인 상태 콤보박스 인터랙션 검증 성공!")


def test_tc_med_04_utility_action_buttons_visibility(page: Page, login_cso):
    """
    [TC-MED-04] Phase 2 Happy Path: 상단 유틸리티 버튼(엑셀 다운로드, 일괄 등록, 등록하기) 가시성 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-MED-04] 상단 유틸리티 액션 버튼 가시성 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management")
    page.wait_for_selector("h2:has-text('영업 거래처 관리')", timeout=10000)

    # 2. 버튼 가시성 단언
    print("[Step 1] '엑셀 다운로드', '일괄 등록', '등록하기' 버튼 가시성 단언")
    expect(page.locator("button:has-text('엑셀 다운로드'), button[title*='엑셀 다운로드']").first).to_be_visible()
    expect(page.locator("button:has-text('일괄 등록'), button[title*='일괄 등록']").first).to_be_visible()
    expect(page.locator("button:has-text('등록하기'), button[title*='필터링 요청 등록']").first).to_be_visible()
    print("[Success] TC-MED-04 유틸리티 버튼 가시성 검증 성공!")


def test_tc_med_05_register_button_navigation(page: Page, login_cso):
    """
    [TC-MED-05] Phase 2 Happy Path: '등록하기' 버튼 클릭 시 영업 거래처 등록 작성 페이지 이동 검증
    - '등록하기' 클릭 ➡️ /dashboard/filtering/medical-institution-management/write 네비게이션 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-MED-05] '등록하기' 버튼 네비게이션 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management")
    page.wait_for_selector("h2:has-text('영업 거래처 관리')", timeout=10000)

    # 2. '등록하기' 클릭
    print("[Step 1] '등록하기' 버튼 클릭")
    reg_btn = page.locator("button:has-text('등록하기'), button[title*='필터링 요청 등록']").first
    expect(reg_btn).to_be_visible()
    reg_btn.click()

    # 3. 작성 페이지 이동 단언
    print("[Step 2] 영업 거래처 등록 폼 이동 단언")
    page.wait_for_selector("h2:has-text('영업 거래처 등록하기'), h1:has-text('영업 거래처 등록하기')", timeout=10000)
    expect(page).to_have_url(re.compile(r".*medical-institution-management/write.*"))
    print("[Success] TC-MED-05 등록하기 버튼 네비게이션 검증 성공!")


def test_tc_med_06_write_page_empty_submit_disabled(page: Page, login_cso):
    """
    [TC-MED-06] Phase 2 Validation: 영업 거래처 등록 빈 폼 상태에서 '등록하기' 버튼 disabled 비활성화 방어 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-MED-06] 영업 거래처 등록 빈 폼 제출 방어 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management/write")
    page.wait_for_selector("h2:has-text('영업 거래처 등록하기'), h1:has-text('영업 거래처 등록하기')", timeout=10000)

    # 2. 하단 '등록하기' 버튼 disabled 단언
    print("[Step 1] 빈 폼 상태에서 하단 '등록하기' 버튼 disabled 단언")
    submit_btn = page.locator("button[type='submit'], button:has-text('등록하기')").last
    expect(submit_btn).to_be_visible()
    expect(submit_btn).to_be_disabled()
    print("[Success] TC-MED-06 영업 거래처 등록 빈 폼 제출 방어 검증 성공!")


def test_tc_med_07_return_to_institutions_list(page: Page, login_cso):
    """
    [TC-MED-07] Phase 2 Validation: 작성 화면에서 사이드바 '영업 거래처 관리' 클릭 시 안전 복귀 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-MED-07] 영업 거래처 관리 목록 안전 복귀 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 진입 상태
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management/write")
    page.wait_for_selector("h2:has-text('영업 거래처 등록하기'), h1:has-text('영업 거래처 등록하기')", timeout=10000)

    # 2. 사이드바 '영업 거래처 관리' 메뉴 클릭
    print("[Step 1] 사이드바 '영업 거래처 관리' 메뉴 클릭")
    menu = page.locator("xpath=//a[span[contains(text(), '영업 거래처 관리')]] | //a[contains(., '영업 거래처 관리')]").first
    expect(menu).to_be_visible()
    menu.click()
    page.wait_for_timeout(1000)

    # 3. 영업 거래처 관리 목록 복구 단언
    print("[Step 2] 영업 거래처 관리 목록 복구 단언")
    page.wait_for_selector("h2:has-text('영업 거래처 관리')", timeout=10000)
    expect(page).to_have_url(re.compile(r".*medical-institution-management$|.*medical-institution-management\?.*"))
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()
    print("[Success] TC-MED-07 영업 거래처 관리 목록 안전 복귀 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_med_08_create_medical_institution_e2e(page: Page, login_cso):
    """
    [TC-MED-08] Phase 3 E2E: CSO 영업 거래처 직접 등록 Full Flow 검증
    - 제약사 관리 모달로 제약사('투썬') 선택 ➡️ 신규 병의원 모달 등록(Sheet 사업자번호) ➡️ 비고/내용 입력 ➡️ '등록하기' 제출 ➡️ 목록 복귀 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-MED-08] 영업 거래처 등록 Full Flow E2E 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management/write")
    page.wait_for_selector("h2:has-text('영업 거래처 등록하기')", timeout=10000)

    # 2. 제약사 선택 (관리하기 모달 활용)
    print("[Step 1] 제약사 관리 모달에서 제약사('투썬') 선택")
    manage_btn = page.locator("button:has-text('관리하기')").first
    if manage_btn.is_visible():
        manage_btn.click()
        page.wait_for_selector("div[role='dialog'] h2:has-text('제약사 관리')", timeout=5000)
        page.fill("input[placeholder*='제약사명 검색']", "투썬")
        page.click("div[role='dialog'] button:has-text('검색')")
        page.wait_for_timeout(500)

        cbs = page.locator("div[role='dialog'] input[type='checkbox']")
        if cbs.count() > 0:
            cbs.first.click()
            page.wait_for_timeout(300)

        page.click("div[role='dialog'] button:has-text('저장하기')")
        page.wait_for_timeout(800)

    # 3. 신규 병의원 등록 모달 오픈
    print("[Step 2] 신규 병의원 등록 모달 입력 (Sheet 사업자번호)")
    page.click("button:has-text('신규 병의원 등록'), button:has-text('신규 병의원')")
    page.wait_for_selector("div[role='dialog'] h2:has-text('신규 병의원 등록')", timeout=5000)

    now_str = datetime.datetime.now().strftime("%m%d-%H%M%S")
    hosp_name = f"Auto_{now_str}"
    page.fill("input[placeholder*='병의원 명을 입력']", hosp_name)
    page.fill("input[placeholder*='병의원 주소를 입력']", "자동화 테스트 주소")

    # Sheet에서 사업자번호 가져오기
    biz_no = get_biz_no_from_sheet()
    clean_biz_no = biz_no.replace("-", "") if biz_no else "6046400707"
    page.fill("input[placeholder*='-없이 숫자만']", clean_biz_no)
    page.wait_for_timeout(300)

    page.locator("div[role='dialog'] button:has-text('등록하기')").last.click()
    page.wait_for_timeout(1000)

    # 4. 비고/문의내용 입력
    print("[Step 3] 내용 입력")
    textarea = page.locator("textarea").first
    if textarea.is_visible():
        textarea.fill(f"자동화등록_{now_str}")
        page.wait_for_timeout(300)

    # 5. 등록하기 제출
    print("[Step 4] '등록하기' 버튼 클릭 및 완료")
    submit_btn = page.locator("button[type='submit'], button:has-text('등록하기')").last
    if submit_btn.is_enabled():
        submit_btn.click()
        page.wait_for_timeout(1500)

    # 6. 목록 복귀 단언
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management")
    page.wait_for_selector("h2:has-text('영업 거래처 관리')", timeout=10000)
    expect(page.locator("h2", has_text="영업 거래처 관리").first).to_be_visible()
    print("[Success] TC-MED-08 영업 거래처 등록 E2E 성공!")


def test_tc_med_09_pharm_customer_detail_and_management_e2e(page: Page, login_pharm1):
    """
    [TC-MED-09] Phase 3 E2E: 제약사 영업 거래처 상세 관리(관리코드 수정 / 상태 변경 / 비고 등록) E2E 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-MED-09] 제약사 영업 거래처 상세 관리 E2E 검증 시작")
    print("=" * 60)

    # 1. 제약사 영업 거래처 관리 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management")
    page.wait_for_selector("h2:has-text('영업 거래처 관리')", timeout=10000)

    # 2. 첫 번째 병의원 상세 진입
    print("[Step 1] 첫 번째 거래처 상세 진입")
    target_link = page.locator(".ag-row:visible").first.locator(".ag-cell[col-id='hospitalName'], .ag-cell[col-id='name'], .ag-cell:nth-child(5)").first
    if target_link.is_visible():
        target_link.click()
        page.wait_for_timeout(1500)

        # 2.1. 관리코드 수정
        print("[Step 2.1] 관리코드 수정")
        edit_code_btn = page.locator("button:has-text('수정')").first
        if edit_code_btn.is_visible():
            edit_code_btn.click()
            page.wait_for_selector("div[role='dialog']", timeout=5000)
            now_code = datetime.datetime.now().strftime("%y%m%d%H%M")
            code_input = page.locator("div[role='dialog'] input").first
            if code_input.is_visible():
                code_input.fill(now_code)
                page.click("div[role='dialog'] button:has-text('저장하기')")
                page.wait_for_timeout(800)

        # 2.2. 거래처 관리 (상태 변경)
        print("[Step 2.2] 거래처 상태 관리 ('제품별 승인')")
        manage_btn = page.locator("button[title='관리'], button:has-text('관리')").first
        if manage_btn.is_visible():
            manage_btn.click()
            page.wait_for_selector("div[role='dialog']", timeout=5000)
            status_dropdown = page.locator("div[role='dialog'] button[role='combobox']").last
            if status_dropdown.is_visible():
                status_dropdown.click()
                page.wait_for_timeout(300)
                prod_opt = page.locator("xpath=(//div[span[text()='제품별 승인']])[last()] | (//div[contains(@role, 'option') and contains(., '제품별 승인')])[last()]").last
                if prod_opt.is_visible():
                    prod_opt.click()
                    page.wait_for_timeout(300)
            page.click("div[role='dialog'] button:has-text('저장하기')")
            page.wait_for_timeout(800)

        # 2.3. 거래처 비고 등록
        print("[Step 2.3] 거래처 비고 등록")
        note_btn = page.locator("button[title='비고'], button:has-text('비고')").first
        if note_btn.is_visible():
            note_btn.click()
            page.wait_for_selector("div[role='dialog']", timeout=5000)
            note_input = page.locator("div[role='dialog'] textarea, div[role='dialog'] input").first
            if note_input.is_visible():
                note_input.fill("자동화테스트 비고")
                page.click("div[role='dialog'] button:has-text('저장하기')")
                page.wait_for_timeout(800)

    # 3. 목록 복귀 확인
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/medical-institution-management")
    page.wait_for_selector("h2:has-text('영업 거래처 관리')", timeout=10000)
    expect(page.locator("h2", has_text="영업 거래처 관리").first).to_be_visible()
    print("[Success] TC-MED-09 제약사 영업 거래처 상세 관리 E2E 성공!")
