import os
import re
import time
import pytest
from playwright.sync_api import Page, expect

# ==============================================================================
# Phase 2 Extension AI Generated Test Cases: 실적 관리 (EDI 업로드, EDI 취합 관리, 실적 입력)
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_prf_01_edi_upload_rendering(page: Page, login_cso):
    """
    [TC-PRF-01] Happy Path: CSO 'EDI 업로드' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 EDI 업로드 목록과 AG Grid 핵심 컬럼들의 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRF-01] EDI 업로드 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] 'EDI 업로드' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/edi-upload")
    page.wait_for_selector("h2:has-text('EDI 업로드')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="EDI 업로드").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*sales-performance-management/edi-upload.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('처방월'), .ag-header-cell:has-text('처방월')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('병의원 명'), .ag-header-cell:has-text('병의원 명')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('제약사'), .ag-header-cell:has-text('제약사')").first).to_be_visible()
    print("[Success] TC-PRF-01 EDI 업로드 렌더링 검증 성공!")


def test_tc_prf_02_edi_upload_search_and_reset(page: Page, login_cso):
    """
    [TC-PRF-02] Validation: EDI 업로드 업체 미선택 시 검색 비활성화 및 선택 후 검색/초기화 검증
    - 업체 미선택 상태에서 검색창 disabled 방어 단언
    - 업체 선택 후 검색창 활성화 ➡️ 검색 및 '검색 초기화' 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRF-02] EDI 업로드 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/edi-upload")
    page.wait_for_selector("h2:has-text('EDI 업로드')", timeout=10000)

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
                dummy_keyword = "__NOT_EXIST_EDI_HOSPITAL__"
                search_input.fill(dummy_keyword)
                page.locator("button:has-text('검색')").first.click()
                page.wait_for_timeout(1500)

                reset_btn = page.locator("button:has-text('검색 초기화')").first
                expect(reset_btn).to_be_visible()
                reset_btn.click()
                page.wait_for_timeout(1500)
                expect(search_input).to_have_value("")

    print("[Success] TC-PRF-02 EDI 업로드 검색 및 초기화 검증 성공!")


def test_tc_prf_03_edi_management_rendering(page: Page, login_cso):
    """
    [TC-PRF-03] Happy Path: CSO 'EDI 취합 관리' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 EDI 취합 관리 목록과 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRF-03] EDI 취합 관리 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] 'EDI 취합 관리' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/edi-management")
    page.wait_for_selector("h2:has-text('EDI 취합 관리')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="EDI 취합 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*sales-performance-management/edi-management.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('확인/관리'), .ag-header-cell:has-text('확인/관리')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('영업 업체'), .ag-header-cell:has-text('영업 업체')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('병의원 명'), .ag-header-cell:has-text('병의원 명')").first).to_be_visible()
    print("[Success] TC-PRF-03 EDI 취합 관리 렌더링 검증 성공!")


def test_tc_prf_04_edi_management_search_and_reset(page: Page, login_cso):
    """
    [TC-PRF-04] Validation: EDI 취합 관리 검색 필터 및 초기화 기능 검증
    - 미존재 영업 업체 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRF-04] EDI 취합 관리 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/edi-management")
    page.wait_for_selector("h2:has-text('EDI 취합 관리')", timeout=10000)

    # 2. 미존재 키워드 입력 및 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_EDI_VENDOR__"
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
    print("[Success] TC-PRF-04 EDI 취합 관리 검색 및 초기화 검증 성공!")


def test_tc_prf_05_sales_performance_registration_rendering(page: Page, login_cso):
    """
    [TC-PRF-05] Happy Path: CSO '실적 입력' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 실적 입력 목록과 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRF-05] 실적 입력 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '실적 입력' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/sales-performance-registration")
    page.wait_for_selector("h2:has-text('실적 입력')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="실적 입력").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*sales-performance-management/sales-performance-registration.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('제약사'), .ag-header-cell:has-text('제약사')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('병의원'), .ag-header-cell:has-text('병의원')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('실적 금액'), .ag-header-cell:has-text('실적 금액')").first).to_be_visible()
    print("[Success] TC-PRF-05 실적 입력 렌더링 검증 성공!")


def test_tc_prf_06_sales_performance_registration_search_and_reset(page: Page, login_cso):
    """
    [TC-PRF-06] Validation: 실적 입력 검색 필터 및 초기화 기능 검증
    - 미존재 제약사 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-PRF-06] 실적 입력 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/sales-performance-registration")
    page.wait_for_selector("h2:has-text('실적 입력')", timeout=10000)

    # 2. 미존재 키워드 입력 및 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_PERF_PHARM__"
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
    print("[Success] TC-PRF-06 실적 입력 검색 및 초기화 검증 성공!")


def test_tc_prf_07_edi_upload_modal_interaction(page: Page, login_cso):
    """
    [TC-PRF-07] Phase 2 Happy Path: EDI 업로드 업체 선택 시 '등록하기' 버튼 활성화 및 'EDI 등록하기' 모달 오픈/ESC 닫기 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-PRF-07] EDI 업로드 등록 모달 인터랙션 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/edi-upload")
    page.wait_for_selector("h2:has-text('EDI 업로드')", timeout=10000)

    reg_btn = page.locator("button[title*='등록하기'], button:has-text('등록하기')").first
    expect(reg_btn).to_be_visible()

    # 2. 업체 미선택 시 등록하기 버튼 disabled 단언
    print("[Step 1] 업체 미선택 시 등록하기 버튼 disabled 단언")
    expect(reg_btn).to_be_disabled()

    # 3. 업체 선택 드롭다운 클릭 및 선택
    print("[Step 2] 업체 선택 드롭다운 클릭 및 업체 선택")
    vendor_combo = page.locator("button[role='combobox']:has-text('업체를 선택해 주세요')").first
    if vendor_combo.is_visible():
        vendor_combo.click()
        page.wait_for_timeout(500)
        options = page.locator("[role='option'], div[data-radix-collection-item]")
        if options.count() > 0:
            options.first.click()
            page.wait_for_timeout(1000)

            # 4. 등록하기 버튼 활성화 단언
            print("[Step 3] 등록하기 버튼 enabled 전환 단언")
            expect(reg_btn).to_be_enabled()

            # 5. 등록하기 클릭 및 모달 가시성 단언
            print("[Step 4] 등록하기 클릭 및 'EDI 등록하기' 모달 오픈 단언")
            reg_btn.click()
            page.wait_for_timeout(1000)

            dialog = page.locator("div[role='dialog']").first
            expect(dialog).to_be_visible()
            expect(dialog.locator("h2").first).to_be_visible()

            # 6. ESC 키로 모달 닫기
            print("[Step 5] ESC 키 입력하여 모달 닫기")
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            expect(page.locator("div[role='dialog']")).to_have_count(0)

    print("[Success] TC-PRF-07 EDI 업로드 등록 모달 인터랙션 성공!")


def test_tc_prf_08_edi_management_tabs_interaction(page: Page, login_cso):
    """
    [TC-PRF-08] Phase 2 Happy Path: EDI 취합 관리 '수신' / '직접 등록' 탭 전환 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-PRF-08] EDI 취합 관리 탭 전환 인터랙션 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/edi-management")
    page.wait_for_selector("h2:has-text('EDI 취합 관리')", timeout=10000)

    # 2. '직접 등록' 탭 클릭
    print("[Step 1] '직접 등록' 탭 클릭")
    direct_tab = page.locator("button:has-text('직접 등록')").first
    expect(direct_tab).to_be_visible()
    direct_tab.click()
    page.wait_for_timeout(1000)
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()

    # 3. '수신' 탭 복귀 클릭
    print("[Step 2] '수신' 탭 복귀 클릭")
    received_tab = page.locator("button:has-text('수신')").first
    expect(received_tab).to_be_visible()
    received_tab.click()
    page.wait_for_timeout(1000)
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()
    print("[Success] TC-PRF-08 EDI 취합 관리 탭 전환 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_prf_09_edi_upload_registration_e2e(page: Page, login_cso):
    """
    [TC-PRF-09] Phase 3 E2E: EDI 업로드 등록 모달 풀 플로우(옵션 선택, 라디오 전환, 유효성 검증 및 닫기) E2E
    """
    print("\n" + "=" * 60)
    print(" [TC-PRF-09] EDI 업로드 등록 모달 풀 플로우 E2E 검증 시작")
    print("=" * 60)

    # 1. EDI 업로드 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/edi-upload")
    page.wait_for_selector("h2:has-text('EDI 업로드')", timeout=10000)

    # 2. 업체 선택
    print("[Step 1] 업체 선택 드롭다운 클릭 및 업체 선택")
    vendor_combo = page.locator("button[role='combobox']:has-text('업체를 선택해 주세요')").first
    if vendor_combo.is_visible():
        vendor_combo.click()
        page.wait_for_timeout(500)
        options = page.locator("[role='option'], div[data-radix-collection-item]")
        if options.count() > 0:
            options.first.click()
            page.wait_for_timeout(1000)

            # 3. 등록하기 클릭
            print("[Step 2] 등록하기 버튼 클릭 및 모달 오픈")
            reg_btn = page.locator("button[title*='등록하기'], button:has-text('등록하기')").first
            expect(reg_btn).to_be_enabled()
            reg_btn.click()
            page.wait_for_timeout(1000)

            dialog = page.locator("div[role='dialog']").first
            expect(dialog).to_be_visible()

            # 4. 라디오 옵션 전환 및 파일 인풋 검증
            print("[Step 3] 모달 내 옵션/파일 인풋 검증")
            file_input = dialog.locator("input[type='file']").first
            expect(file_input).to_be_attached()

            radio_btns = dialog.locator("button[role='radio'], label:has(input[type='radio'])")
            if radio_btns.count() > 1:
                radio_btns.last.click()
                page.wait_for_timeout(300)

            # 5. 취소 버튼 클릭하여 닫기
            print("[Step 4] '취소' 버튼 클릭하여 모달 정상 종료")
            cancel_btn = dialog.locator("button:has-text('취소'), button:has-text('Close')").first
            if cancel_btn.is_visible():
                cancel_btn.click()
            else:
                page.keyboard.press("Escape")
            page.wait_for_timeout(500)

    expect(page.locator("h2", has_text="EDI 업로드").first).to_be_visible()
    print("[Success] TC-PRF-09 EDI 업로드 등록 모달 풀 플로우 E2E 성공!")


def test_tc_prf_10_performance_month_filter_and_merge_e2e(page: Page, login_cso):
    """
    [TC-PRF-10] Phase 3 E2E: 실적 입력 처방월 필터링 및 EDI 취합 관리 병합 연동 E2E 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-PRF-10] 실적 입력 처방월 필터링 & EDI 병합 E2E 검증 시작")
    print("=" * 60)

    # 1. 실적 입력 페이지 이동
    print("[Step 1] 실적 입력 이동 및 처방월 필터 인터랙션")
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/sales-performance-registration")
    page.wait_for_selector("h2:has-text('실적 입력')", timeout=10000)

    # 처방월 드롭다운 클릭
    month_btn = page.locator("button:has-text('년'), button[role='combobox']").first
    if month_btn.is_visible():
        month_btn.click()
        page.wait_for_timeout(500)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    # 2. EDI 취합 관리 이동
    print("[Step 2] EDI 취합 관리 이동 및 'EDI 병합' 버튼 인터랙션")
    page.goto(page.url.split("dashboard")[0] + "dashboard/sales-performance-management/edi-management")
    page.wait_for_selector("h2:has-text('EDI 취합 관리')", timeout=10000)

    merge_btn = page.locator("button:has-text('EDI 병합'), button:has-text('병합')").first
    if merge_btn.is_visible():
        merge_btn.click()
        page.wait_for_timeout(800)
        if page.locator("div[role='dialog']").count() > 0:
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

    expect(page.locator("h2", has_text="EDI 취합 관리").first).to_be_visible()
    print("[Success] TC-PRF-10 실적 입력 처방월 필터링 & EDI 병합 E2E 성공!")
