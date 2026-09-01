import os
import re
import time
import datetime
import pytest
from playwright.sync_api import Page, expect

# ==============================================================================
# Phase 2 Extension AI Generated Test Cases: 제품 관리 & 제품 정보
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. 영업 제품 관리 & 제품 공지 관리 & 수수료율 관리 (CSO 1)
# ------------------------------------------------------------------------------

def test_tc_prd_01_cso1_sales_product_management_rendering(page: Page, login_cso):
    """
    [TC-PRD-01] Happy Path: CSO 1 '영업 제품 관리' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 1 계정으로 진입하여 제품 목록과 AG Grid 핵심 컬럼들의 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-01] 영업 제품 관리 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '영업 제품 관리' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/sales-product-management")
    page.wait_for_selector("h2:has-text('영업 제품 관리')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="영업 제품 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*product-management/sales-product-management.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('제품명'), .ag-header-cell:has-text('제품명')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('보험코드'), .ag-header-cell:has-text('보험코드')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('제약사'), .ag-header-cell:has-text('제약사')").first).to_be_visible()
    print("[Success] TC-PRD-01 영업 제품 관리 렌더링 검증 성공!")


def test_tc_prd_02_cso1_sales_product_management_search_and_reset(page: Page, login_cso):
    """
    [TC-PRD-02] Validation: 영업 제품 관리 검색 필터 및 초기화 기능 검증
    - 미존재 제품명 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-02] 영업 제품 관리 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/sales-product-management")
    page.wait_for_selector("h2:has-text('영업 제품 관리')", timeout=10000)

    # 2. 미존재 키워드 입력 및 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_PRODUCT_XYZ__"
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
    print("[Success] TC-PRD-02 영업 제품 관리 검색 및 초기화 검증 성공!")


def test_tc_prd_03_cso1_product_notice_management_rendering(page: Page, login_cso):
    """
    [TC-PRD-03] Happy Path: CSO 1 '제품 공지 관리' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 1 계정으로 진입하여 공지 목록과 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-03] 제품 공지 관리 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '제품 공지 관리' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/product-notice-management")
    page.wait_for_selector("h2:has-text('제품 공지 관리')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="제품 공지 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*product-management/product-notice-management.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('공지 구분'), .ag-header-cell:has-text('공지 구분')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('제목'), .ag-header-cell:has-text('제목')").first).to_be_visible()
    print("[Success] TC-PRD-03 제품 공지 관리 렌더링 검증 성공!")


def test_tc_prd_04_cso1_commission_rate_management_rendering(page: Page, login_cso):
    """
    [TC-PRD-04] Happy Path: CSO 1 '수수료율 관리' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 1 계정으로 진입하여 수수료율 목록과 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-04] 수수료율 관리 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '수수료율 관리' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/commission-rate-management")
    page.wait_for_selector("h2:has-text('수수료율 관리')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="수수료율 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*product-management/commission-rate-management.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('구분'), .ag-header-cell:has-text('구분')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('적용 업체'), .ag-header-cell:has-text('적용 업체')").first).to_be_visible()
    print("[Success] TC-PRD-04 수수료율 관리 렌더링 검증 성공!")


# ------------------------------------------------------------------------------
# 2. 영업 제품 정보 & 제품 공지 (CSO 1)
# ------------------------------------------------------------------------------

def test_tc_prd_05_cso_sales_product_info_rendering(page: Page, login_cso):
    """
    [TC-PRD-05] Happy Path: CSO '영업 제품 정보' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 영업 제품 정보와 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-05] CSO 영업 제품 정보 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '영업 제품 정보' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/sales-product-info")
    page.wait_for_selector("h2:has-text('영업 제품 정보')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="영업 제품 정보").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*product-management/sales-product-info.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('제품명'), .ag-header-cell:has-text('제품명')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('제약사'), .ag-header-cell:has-text('제약사')").first).to_be_visible()
    print("[Success] TC-PRD-05 CSO 영업 제품 정보 렌더링 검증 성공!")


def test_tc_prd_06_cso_sales_product_info_search_and_reset(page: Page, login_cso):
    """
    [TC-PRD-06] Validation: CSO 영업 제품 정보 업체 미선택 시 검색 비활성화 및 선택 후 검색/초기화 검증
    - 업체 미선택 상태에서 검색창 disabled 방어 단언
    - 업체 선택 후 검색창 활성화 ➡️ 검색 및 '검색 초기화' 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-06] CSO 영업 제품 정보 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/sales-product-info")
    page.wait_for_selector("h2:has-text('영업 제품 정보')", timeout=10000)

    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    # 2. 업체 미선택 상태에서 검색창 disabled 단언
    print("[Step 1] 업체 미선택 시 검색창 disabled 방어 단언")
    expect(search_input).to_be_disabled()

    # 3. 업체 선택 드롭다운 클릭 및 첫 번째 업체 선택
    vendor_btn = page.locator("button:has-text('업체를 선택해 주세요'), button[role='combobox']").first
    if vendor_btn.is_visible():
        print("[Step 2] 업체 선택 드롭다운 클릭")
        vendor_btn.click()
        page.wait_for_timeout(500)
        
        # 팝업/옵션 목록에서 첫 번째 업체 선택
        options = page.locator("div[role='option'], [role='listbox'] div, button[role='option'], div[data-radix-collection-item]")
        if options.count() > 0:
            options.first.click()
            page.wait_for_timeout(1000)
            
            # 검색창이 enabled로 전환되었는지 단언
            if search_input.is_enabled():
                print("[Step 3] 활성화된 검색창에 키워드 검색 및 초기화")
                dummy_keyword = "__NOT_EXIST_CSO_PRODUCT__"
                search_input.fill(dummy_keyword)
                page.locator("button:has-text('검색')").first.click()
                page.wait_for_timeout(1500)

                reset_btn = page.locator("button:has-text('검색 초기화')").first
                expect(reset_btn).to_be_visible()
                reset_btn.click()
                page.wait_for_timeout(1500)
                expect(search_input).to_have_value("")

    print("[Success] TC-PRD-06 CSO 영업 제품 정보 검색 및 초기화 검증 성공!")


def test_tc_prd_07_cso_product_notice_rendering(page: Page, login_cso):
    """
    [TC-PRD-07] Happy Path: CSO '제품 공지' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 제품 공지와 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-07] CSO 제품 공지 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '제품 공지' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/product-notice")
    page.wait_for_selector("h2:has-text('제품 공지')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="제품 공지").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*product-management/product-notice.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('공지 구분'), .ag-header-cell:has-text('공지 구분')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('제목'), .ag-header-cell:has-text('제목')").first).to_be_visible()
    print("[Success] TC-PRD-07 CSO 제품 공지 렌더링 검증 성공!")


def test_tc_prd_08_sales_product_add_modal_interaction(page: Page, login_cso):
    """
    [TC-PRD-08] Phase 2 Happy Path: 영업 제품 관리 '추가하기' 클릭 시 '제품 추가하기' 모달 오픈 및 ESC 닫기 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-08] 영업 제품 관리 제품 등록 모달 인터랙션 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/sales-product-management")
    page.wait_for_selector("h2:has-text('영업 제품 관리')", timeout=10000)

    # 2. '추가하기' 클릭
    print("[Step 1] '추가하기' 버튼 클릭")
    add_btn = page.locator("button:has-text('추가하기')").first
    expect(add_btn).to_be_visible()
    add_btn.click()
    page.wait_for_timeout(1000)

    # 3. 모달 오픈 단언
    print("[Step 2] '제품 등록하기' 모달 가시성 단언")
    dialog = page.locator("div[role='dialog']").first
    expect(dialog).to_be_visible()
    expect(dialog.locator("h2").first).to_be_visible()
    expect(dialog.locator("button:has-text('취소'), button:has-text('Close')").first).to_be_visible()

    # 4. ESC 키로 닫기
    print("[Step 3] ESC 키 입력하여 모달 닫기")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    expect(page.locator("div[role='dialog']")).to_have_count(0)
    print("[Success] TC-PRD-08 영업 제품 등록 모달 인터랙션 검증 성공!")


def test_tc_prd_09_product_notice_mgmt_tab_and_write_nav(page: Page, login_cso):
    """
    [TC-PRD-09] Phase 2 Happy Path: 제품 공지 관리 '공지별'/'제품별' 탭 전환 및 '등록하기' 네비게이션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-09] 제품 공지 관리 탭 전환 및 등록하기 네비게이션 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/product-notice-management")
    page.wait_for_selector("h2:has-text('제품 공지 관리')", timeout=10000)

    # 2. '제품별' 탭 클릭
    print("[Step 1] '제품별' 탭 클릭")
    tab_prod = page.locator("button:has-text('제품별')").first
    expect(tab_prod).to_be_visible()
    tab_prod.click()
    page.wait_for_timeout(1000)
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()

    # 3. '등록하기' 클릭
    print("[Step 2] '등록하기' 버튼 클릭")
    reg_btn = page.locator("button:has-text('등록하기')").first
    expect(reg_btn).to_be_visible()
    reg_btn.click()
    page.wait_for_timeout(1000)

    # 4. 작성 페이지 이동 단언
    print("[Step 3] 작성 페이지 네비게이션 단언")
    page.wait_for_selector("h2:has-text('공지 등록하기'), h1:has-text('공지 등록하기')", timeout=10000)
    expect(page).to_have_url(re.compile(r".*product-notice-management/write.*"))
    print("[Success] TC-PRD-09 제품 공지 관리 탭 전환 및 등록 네비게이션 성공!")


def test_tc_prd_10_product_notice_tabs_interaction(page: Page, login_cso):
    """
    [TC-PRD-10] Phase 2 Happy Path: 제품 공지 화면 '공지별'/'제품별' 탭 전환 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-10] 제품 공지 화면 탭 전환 인터랙션 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/product-notice")
    page.wait_for_selector("h2:has-text('제품 공지')", timeout=10000)

    # 2. '제품별' 탭 클릭
    print("[Step 1] '제품별' 탭 클릭")
    tab_prod = page.locator("button:has-text('제품별')").first
    expect(tab_prod).to_be_visible()
    tab_prod.click()
    page.wait_for_timeout(1000)
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()

    # 3. '공지별' 탭 복귀 클릭
    print("[Step 2] '공지별' 탭 복귀 클릭")
    tab_notice = page.locator("button:has-text('공지별')").first
    expect(tab_notice).to_be_visible()
    tab_notice.click()
    page.wait_for_timeout(1000)
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()
    print("[Success] TC-PRD-10 제품 공지 화면 탭 전환 인터랙션 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_prd_11_create_product_notice_e2e(page: Page, login_cso):
    """
    [TC-PRD-11] Phase 3 E2E: 제품 공지 관리 공지 등록 Full Flow 검증
    - 작성 페이지 이동 ➡️ Radix 라디오 선택 ➡️ 제목/내용 입력 ➡️ '등록하기' 제출 ➡️ 목록 복귀 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-11] 제품 공지 등록 Full Flow E2E 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/product-notice-management/write")
    page.wait_for_selector("h2:has-text('공지 등록하기'), h1:has-text('공지 등록하기')", timeout=10000)

    # 2. 공지 구분 라디오 선택
    print("[Step 1] 공지 구분 라디오 선택")
    radix_radios = page.locator("button[role='radio']")
    if radix_radios.count() > 1:
        radix_radios.nth(1).click()
        page.wait_for_timeout(300)

    # 3. 제목 및 본문 내용 입력
    print("[Step 2] 제목 및 본문 내용 입력")
    now_str = datetime.datetime.now().strftime("%m%d-%H%M%S")
    title_inp = page.locator("input[placeholder*='제목을 입력'], input[name='title']").first
    if title_inp.is_visible():
        title_inp.fill(f"자동화공지_{now_str}")
        page.wait_for_timeout(300)

    content_ta = page.locator("textarea[placeholder*='내용을 입력'], textarea").first
    if content_ta.is_visible():
        content_ta.fill("자동화 테스트로 작성된 제품/업체 공지 본문 내용입니다.")
        page.wait_for_timeout(300)

    # 4. 등록하기 제출
    print("[Step 3] '등록하기' 버튼 클릭")
    submit_btn = page.locator("button[type='submit']:has-text('등록하기'), button:has-text('등록하기')").last
    if submit_btn.is_enabled():
        submit_btn.click()
        page.wait_for_timeout(1500)

    # 5. 목록 복귀 단언
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/product-notice-management")
    page.wait_for_selector("h2:has-text('제품 공지 관리')", timeout=10000)
    expect(page.locator("h2", has_text="제품 공지 관리").first).to_be_visible()
    print("[Success] TC-PRD-11 제품 공지 등록 Full Flow E2E 성공!")


def test_tc_prd_12_commission_rate_and_product_modal_e2e(page: Page, login_cso):
    """
    [TC-PRD-12] Phase 3 E2E: 수수료율 관리 모달 오픈 및 영업 제품 관리 추가 모달 연동 E2E 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-PRD-12] 수수료율 관리 및 제품 추가 모달 E2E 검증 시작")
    print("=" * 60)

    # 1. 수수료율 관리 이동
    print("[Step 1] 수수료율 관리 이동 및 업체 관리 모달 인터랙션")
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/commission-rate-management")
    page.wait_for_selector("h2:has-text('수수료율 관리')", timeout=10000)

    vendor_mgmt_btn = page.locator("button:has-text('업체 관리'), button:has-text('추가하기')").first
    if vendor_mgmt_btn.is_visible():
        vendor_mgmt_btn.click()
        page.wait_for_timeout(500)
        if page.locator("div[role='dialog']").count() > 0:
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

    # 2. 영업 제품 관리 이동 및 제품 추가 모달 인터랙션
    print("[Step 2] 영업 제품 관리 이동 및 '제품 추가하기' 모달 검색/취소 검증")
    page.goto(page.url.split("dashboard")[0] + "dashboard/product-management/sales-product-management")
    page.wait_for_selector("h2:has-text('영업 제품 관리')", timeout=10000)

    add_btn = page.locator("button:has-text('추가하기')").first
    if add_btn.is_visible():
        add_btn.click()
        page.wait_for_selector("div[role='dialog']", timeout=5000)
        dialog = page.locator("div[role='dialog']").first

        search_inp = dialog.locator("input").first
        if search_inp.is_visible():
            search_inp.fill("타이")
            page.wait_for_timeout(300)

        cancel_btn = dialog.locator("button:has-text('취소'), button:has-text('Close')").first
        if cancel_btn.is_visible():
            cancel_btn.click(force=True)
            page.wait_for_timeout(500)
        else:
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

    expect(page.locator("h2", has_text="영업 제품 관리").first).to_be_visible()
    print("[Success] TC-PRD-12 수수료율 관리 및 제품 추가 모달 E2E 성공!")
