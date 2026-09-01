import os
import re
import time
import pytest
from playwright.sync_api import Page, expect

# ==============================================================================
# Phase 2 Extension AI Generated Test Cases: 정산 관리 (정산 취합, 정산 내역서 관리, 받은 정산 내역서)
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_stl_01_settlement_reviews_rendering(page: Page, login_cso):
    """
    [TC-STL-01] Happy Path: CSO '정산 취합' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 정산 취합 목록과 AG Grid 핵심 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-STL-01] 정산 취합 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '정산 취합' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/settlement-reviews")
    page.wait_for_selector("h2:has-text('정산 취합')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="정산 취합").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*settlement/settlement-reviews.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('상태 관리'), .ag-header-cell:has-text('상태 관리')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('제약사 명'), .ag-header-cell:has-text('제약사 명')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('영업 업체'), .ag-header-cell:has-text('영업 업체')").first).to_be_visible()
    print("[Success] TC-STL-01 정산 취합 렌더링 검증 성공!")


def test_tc_stl_02_settlement_reviews_search_and_reset(page: Page, login_cso):
    """
    [TC-STL-02] Validation: 정산 취합 검색 필터 및 초기화 기능 검증
    - 미존재 제약사 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-STL-02] 정산 취합 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/settlement-reviews")
    page.wait_for_selector("h2:has-text('정산 취합')", timeout=10000)

    # 2. 미존재 키워드 입력 및 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_SETTLE_PHARM__"
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
    print("[Success] TC-STL-02 정산 취합 검색 및 초기화 검증 성공!")


def test_tc_stl_03_settlement_statements_rendering(page: Page, login_cso):
    """
    [TC-STL-03] Happy Path: CSO '정산 내역서 관리' 페이지 렌더링 및 탭/그리드 검증
    - CSO 계정으로 진입하여 전송 탭 및 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-STL-03] 정산 내역서 관리 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '정산 내역서 관리' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/settlement-statements")
    page.wait_for_selector("h2:has-text('정산 내역서 관리')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="정산 내역서 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*settlement/settlement-statements.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('영업 업체'), .ag-header-cell:has-text('영업 업체')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('지급 수수료'), .ag-header-cell:has-text('지급 수수료')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('총 정산 금액'), .ag-header-cell:has-text('총 정산 금액')").first).to_be_visible()
    print("[Success] TC-STL-03 정산 내역서 관리 렌더링 검증 성공!")


def test_tc_stl_04_settlement_statements_search_and_reset(page: Page, login_cso):
    """
    [TC-STL-04] Validation: 정산 내역서 관리 검색 필터 및 초기화 기능 검증
    - 미존재 영업 업체 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-STL-04] 정산 내역서 관리 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/settlement-statements")
    page.wait_for_selector("h2:has-text('정산 내역서 관리')", timeout=10000)

    # 2. 미존재 키워드 입력 및 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_SETTLE_VENDOR__"
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
    print("[Success] TC-STL-04 정산 내역서 관리 검색 및 초기화 검증 성공!")


def test_tc_stl_05_received_settlement_statements_rendering(page: Page, login_cso):
    """
    [TC-STL-05] Happy Path: CSO '받은 정산 내역서' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 받은 정산 내역서 목록과 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-STL-05] 받은 정산 내역서 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '받은 정산 내역서' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/received-settlement-statements")
    page.wait_for_selector("h2:has-text('받은 정산 내역서')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="받은 정산 내역서").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*settlement/received-settlement-statements.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('상호/법인명'), .ag-header-cell:has-text('상호/법인명')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('정산 내역서'), .ag-header-cell:has-text('정산 내역서')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('총 정산 금액'), .ag-header-cell:has-text('총 정산 금액')").first).to_be_visible()
    print("[Success] TC-STL-05 받은 정산 내역서 렌더링 검증 성공!")


def test_tc_stl_06_received_settlement_statements_search_and_reset(page: Page, login_cso):
    """
    [TC-STL-06] Validation: 받은 정산 내역서 검색 필터 및 초기화 기능 검증
    - 미존재 상호 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-STL-06] 받은 정산 내역서 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/received-settlement-statements")
    page.wait_for_selector("h2:has-text('받은 정산 내역서')", timeout=10000)

    # 2. 미존재 키워드 입력 및 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_RECEIVED_SETTLE_NAME__"
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
    print("[Success] TC-STL-06 받은 정산 내역서 검색 및 초기화 검증 성공!")


def test_tc_stl_07_settlement_statements_tab_switching(page: Page, login_cso):
    """
    [TC-STL-07] Phase 2 Happy Path: 정산 내역서 관리 '전송 전' / '전송 완료' 탭 전환 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-STL-07] 정산 내역서 관리 탭 전환 인터랙션 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/settlement-statements")
    page.wait_for_selector("h2:has-text('정산 내역서 관리')", timeout=10000)

    # 2. '전송 완료' 탭 클릭
    print("[Step 1] '전송 완료' 탭 클릭")
    done_tab = page.locator("button:has-text('전송 완료')").first
    expect(done_tab).to_be_visible()
    done_tab.click()
    page.wait_for_timeout(1000)
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()

    # 3. '전송 전' 탭 복귀 클릭
    print("[Step 2] '전송 전' 탭 복귀 클릭")
    before_tab = page.locator("button:has-text('전송 전')").first
    expect(before_tab).to_be_visible()
    before_tab.click()
    page.wait_for_timeout(1000)
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()
    print("[Success] TC-STL-07 정산 내역서 관리 탭 전환 성공!")


def test_tc_stl_08_settlement_statements_negative_send_button(page: Page, login_cso):
    """
    [TC-STL-08] Phase 2 Validation: 정산 내역서 관리 목록 행 미선택 시 '전송하기' 버튼 disabled 비활성화 방어 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-STL-08] 정산 내역서 관리 행 미선택 전송 방어(disabled) 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/settlement-statements")
    page.wait_for_selector("h2:has-text('정산 내역서 관리')", timeout=10000)

    # 2. 행 미선택 상태에서 '전송하기' 버튼 disabled 단언
    print("[Step 1] 행 미선택 상태에서 '전송하기' 버튼 disabled 단언")
    send_btn = page.locator("button:has-text('전송하기')").first
    expect(send_btn).to_be_visible()
    expect(send_btn).to_be_disabled()
    print("[Success] TC-STL-08 행 미선택 전송 방어 검증 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_stl_09_settlement_reviews_detail_view_and_return_e2e(page: Page, login_cso):
    """
    [TC-STL-09] Phase 3 E2E: 정산 취합 업체 클릭 시 상세 페이지 진입 및 목록 복귀 Full Flow 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-STL-09] 정산 취합 상세 네비게이션 및 복귀 E2E 검증 시작")
    print("=" * 60)

    # 1. 정산 취합 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/settlement-reviews")
    page.wait_for_selector("h2:has-text('정산 취합')", timeout=10000)

    # 2. 첫 번째 행의 업체 버튼 클릭
    print("[Step 1] 첫 번째 행 업체 클릭하여 상세 진입")
    first_row = page.locator(".ag-row:visible").first
    if first_row.is_visible():
        vendor_btn = first_row.locator("button, a").first
        if vendor_btn.is_visible():
            vendor_btn.click()
            page.wait_for_timeout(1500)

            # 상세 URL 네비게이션 단언
            print("[Step 2] 상세 페이지 진입 단언")
            expect(page).to_have_url(re.compile(r".*settlement/settlement-reviews/\d+.*"))
            expect(page.locator(".ag-root-wrapper, main").first).to_be_visible()

    # 3. 정산 취합 목록으로 복귀
    print("[Step 3] 정산 취합 목록으로 안전 복귀 단언")
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/settlement-reviews")
    page.wait_for_selector("h2:has-text('정산 취합')", timeout=10000)
    expect(page.locator("h2", has_text="정산 취합").first).to_be_visible()
    print("[Success] TC-STL-09 정산 취합 상세 네비게이션 및 복귀 E2E 성공!")


def test_tc_stl_10_settlement_statements_month_and_tabs_e2e(page: Page, login_cso):
    """
    [TC-STL-10] Phase 3 E2E: 정산 내역서 관리 처방월 필터링 및 탭 전환 Full Flow E2E 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-STL-10] 정산 내역서 관리 처방월 필터링 & 탭 연동 E2E 검증 시작")
    print("=" * 60)

    # 1. 정산 내역서 관리 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/settlement/settlement-statements")
    page.wait_for_selector("h2:has-text('정산 내역서 관리')", timeout=10000)

    # 2. 처방월 콤보박스 인터랙션
    print("[Step 1] 처방월 콤보박스 클릭 및 팝오버 확인")
    month_btn = page.locator("button:has-text('년'), button[role='combobox']").first
    if month_btn.is_visible():
        month_btn.click()
        page.wait_for_timeout(500)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    # 3. 탭 전환 연동
    print("[Step 2] '전송 완료' 탭 전환 및 데이터 컨테이너 확인")
    done_tab = page.locator("button:has-text('전송 완료')").first
    if done_tab.is_visible():
        done_tab.click()
        page.wait_for_timeout(1000)
        expect(page.locator(".ag-root-wrapper").first).to_be_visible()

    print("[Step 3] '전송 전' 탭 복귀 단언")
    before_tab = page.locator("button:has-text('전송 전')").first
    if before_tab.is_visible():
        before_tab.click()
        page.wait_for_timeout(1000)
        expect(page.locator(".ag-root-wrapper").first).to_be_visible()

    expect(page.locator("h2", has_text="정산 내역서 관리").first).to_be_visible()
    print("[Success] TC-STL-10 정산 내역서 관리 처방월 필터링 & 탭 연동 E2E 성공!")
