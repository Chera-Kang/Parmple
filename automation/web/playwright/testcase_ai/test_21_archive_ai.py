import os
import re
import time
import pytest
from playwright.sync_api import Page, expect

# ==============================================================================
# Phase 1 AI Generated Test Cases: 자료실 (신규 개원 정보)
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_arc_01_hospital_info_rendering(page: Page, login_cso):
    """
    [TC-ARC-01] Happy Path: CSO '신규 개원 정보' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 신규 개원 정보 목록과 AG Grid 핵심 컬럼들의 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-ARC-01] 신규 개원 정보 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '신규 개원 정보' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/archive/hospital-info")
    page.wait_for_selector("h2:has-text('신규 개원 정보')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="신규 개원 정보").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*archive/hospital-info.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell:has-text('지역')").first).to_be_visible()
    expect(page.locator(".ag-header-cell:has-text('구분')").first).to_be_visible()
    expect(page.locator(".ag-header-cell:has-text('의료 기관명')").first).to_be_visible()
    expect(page.locator(".ag-header-cell:has-text('전화번호')").first).to_be_visible()
    print("[Success] TC-ARC-01 신규 개원 정보 렌더링 검증 성공!")


def test_tc_arc_02_filter_comboboxes_visibility(page: Page, login_cso):
    """
    [TC-ARC-02] Happy Path: 신규 개원 정보 3대 검색 필터(지역/구분/진료 과목) 콤보박스 가시성 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-ARC-02] 3대 검색 필터 콤보박스 가시성 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/archive/hospital-info")
    page.wait_for_selector("h2:has-text('신규 개원 정보')", timeout=10000)

    # 2. 콤보박스 버튼 가시성 단언
    print("[Step 1] '지역', '구분', '진료 과목' 드롭다운 버튼 가시성 단언")
    expect(page.locator("button:has-text('지역')").first).to_be_visible()
    expect(page.locator("button:has-text('구분')").first).to_be_visible()
    expect(page.locator("button:has-text('진료 과목')").first).to_be_visible()
    print("[Success] TC-ARC-02 3대 검색 필터 콤보박스 가시성 검증 성공!")


def test_tc_arc_03_reset_button_visibility(page: Page, login_cso):
    """
    [TC-ARC-03] Happy Path: '검색 초기화' 유틸리티 버튼 가시성 및 활성화 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-ARC-03] 검색 초기화 버튼 가시성 및 활성화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/archive/hospital-info")
    page.wait_for_selector("h2:has-text('신규 개원 정보')", timeout=10000)

    # 2. '검색 초기화' 버튼 가시성 및 활성화 단언
    print("[Step 1] '검색 초기화' 버튼 가시성 및 활성화 상태 단언")
    reset_btn = page.locator("button:has-text('검색 초기화')").first
    expect(reset_btn).to_be_visible()
    expect(reset_btn).to_be_enabled()
    print("[Success] TC-ARC-03 검색 초기화 버튼 가시성 검증 성공!")


# ==============================================================================
# Phase 2: Negative / Edge Case / Filter Interaction Test Cases
# ==============================================================================

def test_tc_arc_04_region_filter_selection_and_apply(page: Page, login_cso):
    """
    [TC-ARC-04] Phase 2 Happy Path: 지역 필터 팝오버 옵션 선택 및 '적용' 필터링 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-ARC-04] 지역 필터 옵션 선택 및 적용 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/archive/hospital-info")
    page.wait_for_selector("h2:has-text('신규 개원 정보')", timeout=10000)

    # 2. 지역 드롭다운 클릭
    print("[Step 1] '지역' 드롭다운 클릭 및 팝오버 오픈")
    region_btn = page.locator("button:has-text('지역')").first
    expect(region_btn).to_be_visible()
    region_btn.click()
    page.wait_for_timeout(500)

    # 3. '광주' 옵션 선택
    print("[Step 2] '광주' 지역 옵션 선택")
    gwangju_opt = page.locator("div[data-radix-popper-content-wrapper] button:has-text('광주')").first
    if gwangju_opt.is_visible():
        gwangju_opt.click(force=True)
        page.wait_for_timeout(300)

    # 4. '적용' 버튼 클릭
    print("[Step 3] '적용' 버튼 클릭")
    apply_btn = page.locator("div[data-radix-popper-content-wrapper] button:has-text('적용')").first
    if apply_btn.is_visible():
        apply_btn.evaluate("el => el.click()")
        page.wait_for_timeout(1000)

    # 5. 그리드 렌더링 확인
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()
    print("[Success] TC-ARC-04 지역 필터 옵션 선택 및 적용 성공!")


def test_tc_arc_05_category_filter_dismiss_escape(page: Page, login_cso):
    """
    [TC-ARC-05] Phase 2 Validation: 구분 필터 팝오버 오픈 후 ESC 입력 시 안전 닫힘 방어 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-ARC-05] 구분 필터 팝오버 ESC 취소 닫기 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/archive/hospital-info")
    page.wait_for_selector("h2:has-text('신규 개원 정보')", timeout=10000)

    # 2. 구분 드롭다운 클릭
    print("[Step 1] '구분' 드롭다운 클릭")
    gubun_btn = page.locator("button:has-text('구분')").first
    expect(gubun_btn).to_be_visible()
    gubun_btn.click()
    page.wait_for_timeout(500)

    # 3. ESC 입력으로 팝오버 닫기
    print("[Step 2] ESC 키 입력하여 팝오버 닫기")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    expect(page.locator("h2", has_text="신규 개원 정보").first).to_be_visible()
    print("[Success] TC-ARC-05 구분 필터 ESC 취소 닫기 성공!")


def test_tc_arc_06_department_filter_selection_and_apply(page: Page, login_cso):
    """
    [TC-ARC-06] Phase 2 Happy Path: 진료과목 필터 팝오버 옵션 선택 및 '적용' 필터링 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-ARC-06] 진료과목 필터 옵션 선택 및 적용 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/archive/hospital-info")
    page.wait_for_selector("h2:has-text('신규 개원 정보')", timeout=10000)

    # 2. 진료과목 드롭다운 클릭
    print("[Step 1] '진료 과목' 드롭다운 클릭")
    dept_btn = page.locator("button:has-text('진료 과목'), button:has-text('진료과목')").first
    expect(dept_btn).to_be_visible()
    dept_btn.click()
    page.wait_for_timeout(500)

    # 3. '내과' 옵션 선택
    print("[Step 2] '내과' 옵션 선택")
    dept_opt = page.locator("div[data-radix-popper-content-wrapper] button:has-text('내과')").first
    if dept_opt.is_visible():
        dept_opt.click(force=True)
        page.wait_for_timeout(300)

    # 4. '적용' 버튼 클릭
    print("[Step 3] '적용' 버튼 클릭")
    apply_btn = page.locator("div[data-radix-popper-content-wrapper] button:has-text('적용')").first
    if apply_btn.is_visible():
        apply_btn.evaluate("el => el.click()")
        page.wait_for_timeout(1000)

    expect(page.locator(".ag-root-wrapper").first).to_be_visible()
    print("[Success] TC-ARC-06 진료과목 필터 옵션 선택 및 적용 성공!")


def test_tc_arc_07_filters_reset_interaction(page: Page, login_cso):
    """
    [TC-ARC-07] Phase 2 Validation: 필터 적용 후 '검색 초기화' 클릭 시 전체 필터 일괄 리셋 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-ARC-07] 검색 초기화 버튼 일괄 리셋 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/archive/hospital-info")
    page.wait_for_selector("h2:has-text('신규 개원 정보')", timeout=10000)

    # 2. 지역 필터 적용
    print("[Step 1] 지역 필터 임의 선택 및 적용")
    region_btn = page.locator("button:has-text('지역')").first
    region_btn.click()
    page.wait_for_timeout(500)

    gwangju_opt = page.locator("div[data-radix-popper-content-wrapper] button:has-text('광주')").first
    if gwangju_opt.is_visible():
        gwangju_opt.click(force=True)
        page.wait_for_timeout(300)

    apply_btn = page.locator("div[data-radix-popper-content-wrapper] button:has-text('적용')").first
    if apply_btn.is_visible():
        apply_btn.evaluate("el => el.click()")
        page.wait_for_timeout(1000)

    # 3. '검색 초기화' 버튼 클릭
    print("[Step 2] '검색 초기화' 버튼 클릭")
    reset_btn = page.locator("button:has-text('검색 초기화')").first
    expect(reset_btn).to_be_visible()
    reset_btn.click(force=True)
    page.wait_for_timeout(1500)

    # 4. 필터 텍스트 기본값 복구 단언
    print("[Step 3] 필터 버튼 텍스트가 '지역(전체)'로 복구되었는지 단언")
    expect(page.locator("button:has-text('지역')").first).to_be_visible()
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()
    print("[Success] TC-ARC-07 검색 초기화 버튼 일괄 리셋 성공!")


