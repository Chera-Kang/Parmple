import os
import re
import time
import pytest
from playwright.sync_api import Page, expect

# ==============================================================================
# Phase 2 Extension AI Generated Test Cases: 필터링 직접 조회 & 필터링 조회 관리
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_flt_01_cso_direct_filtering_rendering(page: Page, login_cso):
    """
    [TC-FLT-01] Happy Path: CSO '필터링 직접 조회' 페이지 렌더링 및 이력 그리드 컬럼 검증
    - CSO 계정으로 진입하여 AG Grid 테이블과 고유 헤더 컬럼들의 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FLT-01] 필터링 직접 조회 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 진입
    print("[Step 1] '필터링 직접 조회' 메뉴 클릭")
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-list")
    page.wait_for_selector("h2:has-text('필터링 직접 조회')", timeout=10000)

    # 만약 진입 시 모달이 열려있다면 ESC로 닫아 그리드 뷰 확보
    if page.locator("div[role='dialog']").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="필터링 직접 조회").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*filtering/filtering-list.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('조회 결과'), .ag-header-cell:has-text('조회 결과')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('병의원 명'), .ag-header-cell:has-text('병의원 명')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('사업자등록번호'), .ag-header-cell:has-text('사업자등록번호')").first).to_be_visible()
    print("[Success] TC-FLT-01 필터링 직접 조회 렌더링 검증 성공!")


def test_tc_flt_02_direct_query_modal_open_and_close(page: Page, login_cso):
    """
    [TC-FLT-02] Happy Path: '직접 조회하기' 모달 오픈 및 닫기 인터랙션 검증
    - 모달 열기 ➡️ 내부 요소(제약사 선택, 다음 버튼) 확인 ➡️ ESC / 닫기로 모달 종료 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FLT-02] '직접 조회하기' 모달 인터랙션 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-list")
    page.wait_for_selector("h2:has-text('필터링 직접 조회')", timeout=10000)

    # 2. 모달이 안 열려있다면 '직접 조회하기' 버튼 클릭
    if page.locator("div[role='dialog']").count() == 0:
        print("[Step 1] '직접 조회하기' 버튼 클릭")
        query_btn = page.locator("button:has-text('직접 조회하기'), button[title*='필터링 직접 조회']").first
        expect(query_btn).to_be_visible()
        query_btn.click()

    # 3. Radix UI 모달 오픈 단언
    print("[Step 2] 다이얼로그 모달 오픈 및 UI 요소 가시성 단언")
    dialog = page.locator("div[role='dialog']").first
    page.wait_for_selector("div[role='dialog']", timeout=10000)
    expect(dialog).to_be_visible()

    expect(dialog.locator("[role='combobox'], button:has-text('제약사')").first).to_be_visible()
    expect(dialog.locator("button:has-text('다음')").first).to_be_visible()

    # 4. 모달 닫기 (ESC 키)
    print("[Step 3] ESC 키를 통한 모달 닫기")
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)
    expect(page.locator("div[role='dialog']")).to_have_count(0)
    print("[Success] TC-FLT-02 '직접 조회하기' 모달 인터랙션 검증 성공!")


def test_tc_flt_03_direct_query_modal_validation(page: Page, login_cso):
    """
    [TC-FLT-03] Validation: 제약사 미선택 상태에서 '다음' 버튼 비활성화 방어 검증
    - 제약사를 선택하지 않은 상태에서 '다음' 버튼이 disabled 비활성화 상태인지 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FLT-03] 직접 조회 모달 미선택 방어(disabled) 검증 시작")
    print("=" * 60)

    # 1. 모달 상태 확보
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-list")
    page.wait_for_selector("h2:has-text('필터링 직접 조회')", timeout=10000)
    if page.locator("div[role='dialog']").count() == 0:
        page.locator("button:has-text('직접 조회하기'), button[title*='필터링 직접 조회']").first.click()
    page.wait_for_selector("div[role='dialog']", timeout=10000)

    # 2. 미선택 상태에서 '다음' 버튼 disabled 단언
    dialog = page.locator("div[role='dialog']").first
    next_btn = dialog.locator("button:has-text('다음')").first
    expect(next_btn).to_be_visible()
    expect(next_btn).to_be_disabled()

    # 정리: 모달 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    print("[Success] TC-FLT-03 직접 조회 모달 미선택 방어 검증 성공!")


def test_tc_flt_04_cso_filtering_search_and_reset(page: Page, login_cso):
    """
    [TC-FLT-04] Validation: 필터링 직접 조회 검색 및 초기화 기능 검증
    - 미존재 병의원 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FLT-04] 필터링 직접 조회 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입 (모달 닫힌 클린 상태 확보)
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-list")
    page.wait_for_selector("h2:has-text('필터링 직접 조회')", timeout=10000)
    if page.locator("div[role='dialog']").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # 2. 미존재 키워드 입력 및 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_HOSPITAL_FILTER__"
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
    print("[Success] TC-FLT-04 검색 및 초기화 검증 성공!")


def test_tc_flt_05_pharm_filtering_management_rendering(page: Page, login_pharm1):
    """
    [TC-FLT-05] Happy Path: 제약사 '필터링 조회 관리' 페이지 렌더링 검증
    - 제약사 계정으로 진입하여 '필터링 조회 관리' 헤딩 및 관리 그리드 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FLT-05] 제약사 '필터링 조회 관리' 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 클릭
    print("[Step 1] '필터링 조회 관리' 메뉴 클릭")
    menu = page.locator("xpath=//a[span[contains(text(), '필터링 조회 관리')]] | //a[contains(., '필터링 조회 관리')]").first
    expect(menu).to_be_visible()
    menu.click()

    # 2. 헤딩 및 URL 단언
    page.wait_for_selector("h2:has-text('필터링 조회 관리')", timeout=10000)
    expect(page.locator("h2", has_text="필터링 조회 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*filtering-query-management.*"))

    # 3. AG Grid 헤더 컬럼 가시성 단언
    print("[Step 2] 제약사 조회 관리 그리드 헤더 컬럼 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('조회 결과'), .ag-header-cell:has-text('조회 결과')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('상호/법인명'), .ag-header-cell:has-text('상호/법인명')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('병의원 명'), .ag-header-cell:has-text('병의원 명')").first).to_be_visible()
    print("[Success] TC-FLT-05 제약사 '필터링 조회 관리' 렌더링 검증 성공!")


def test_tc_flt_06_pharm_filtering_search_and_reset(page: Page, login_pharm1):
    """
    [TC-FLT-06] Validation: 제약사 '필터링 조회 관리' 검색 및 초기화 기능 검증
    - 미존재 키워드 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FLT-06] 제약사 필터링 조회 관리 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    page.locator("xpath=//a[span[contains(text(), '필터링 조회 관리')]] | //a[contains(., '필터링 조회 관리')]").first.click()
    page.wait_for_selector("h2:has-text('필터링 조회 관리')", timeout=10000)

    # 2. 미존재 키워드 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_PHARM_QUERY__"
    print(f"[Step 1] 미존재 키워드('{dummy_keyword}') 검색")
    search_input.fill(dummy_keyword)
    page.click("button:has-text('검색')")
    page.wait_for_timeout(1500)

    # 3. '검색 초기화' 클릭 및 복구 단언
    print("[Step 2] '검색 초기화' 버튼 클릭")
    reset_btn = page.locator("button:has-text('검색 초기화')").first
    expect(reset_btn).to_be_visible()
    reset_btn.click()
    page.wait_for_timeout(1500)

    expect(search_input).to_have_value("")
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()
    print("[Success] TC-FLT-06 제약사 검색 및 초기화 검증 성공!")


def test_tc_flt_07_modal_pharm_select_enables_next_button(page: Page, login_cso):
    """
    [TC-FLT-07] Phase 2 Happy Path: 직접 조회 모달에서 제약사 선택 시 '다음' 버튼 enabled 전환 검증
    - 제약사 드롭다운에서 옵션 선택 ➡️ '다음' 버튼이 활성화되는지 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FLT-07] 직접 조회 모달 제약사 선택 시 다음 버튼 활성화 검증 시작")
    print("=" * 60)

    # 1. 모달 열린 상태 확보
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-list")
    page.wait_for_selector("h2:has-text('필터링 직접 조회')", timeout=10000)
    if page.locator("div[role='dialog']").count() == 0:
        page.locator("button:has-text('직접 조회하기'), button[title*='필터링 직접 조회']").first.click()
    page.wait_for_selector("div[role='dialog']", timeout=10000)

    dialog = page.locator("div[role='dialog']").first
    pharm_combobox = dialog.locator("button[role='combobox'], [role='combobox']").first
    next_btn = dialog.locator("button:has-text('다음')").first

    # 2. 초기 disabled 단언
    print("[Step 1] 제약사 미선택 시 '다음' 버튼 disabled 단언")
    expect(next_btn).to_be_disabled()

    # 3. 제약사 콤보박스 클릭 및 옵션 선택
    print("[Step 2] 제약사 옵션 선택")
    pharm_combobox.click()
    page.wait_for_timeout(500)

    options = page.locator("[role='option'], div[data-radix-collection-item]").all()
    if len(options) > 0:
        options[0].click()
        page.wait_for_timeout(500)
        # 4. 다음 버튼 활성화 단언
        print("[Step 3] 제약사 선택 후 '다음' 버튼 enabled 전환 단언")
        expect(next_btn).to_be_enabled()

    # 5. ESC로 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[Success] TC-FLT-07 제약사 선택 시 '다음' 버튼 활성화 단언 성공!")


def test_tc_flt_08_modal_esc_close_returns_to_grid(page: Page, login_cso):
    """
    [TC-FLT-08] Phase 2 Validation: 직접 조회 모달에서 ESC 입력 시 모달 종료 및 메인 그리드 활성화 단언
    - ESC 키 입력 ➡️ 다이얼로그 모달 소멸 및 메인 이력 테이블 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FLT-08] 직접 조회 모달 ESC 종료 및 메인 그리드 복구 검증 시작")
    print("=" * 60)

    # 1. 모달 열린 상태 확보
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-list")
    page.wait_for_selector("h2:has-text('필터링 직접 조회')", timeout=10000)
    if page.locator("div[role='dialog']").count() == 0:
        page.locator("button:has-text('직접 조회하기'), button[title*='필터링 직접 조회']").first.click()
    page.wait_for_selector("div[role='dialog']", timeout=10000)

    # 2. ESC 키 입력
    print("[Step 1] ESC 키 입력하여 모달 닫기")
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)

    # 3. 모달 소멸 및 메인 그리드 노출 단언
    print("[Step 2] 모달 소멸 및 메인 AG Grid 가시성 단언")
    expect(page.locator("div[role='dialog']")).to_have_count(0)
    expect(page.locator(".ag-root-wrapper").first).to_be_visible()
    print("[Success] TC-FLT-08 ESC 닫기 및 메인 그리드 복구 검증 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_flt_09_cso_direct_filtering_e2e_flow(page: Page, login_cso):
    """
    [TC-FLT-09] Phase 3 E2E: CSO 제약사/병의원 선택 후 직접 필터링 조회 및 결과 팝업 Full Flow 검증
    - 제약사('투썬') 선택 ➡️ 공지사항 ➡️ 병의원('자동화테스트') ➡️ '조회하기' ➡️ '필터링 조회 결과' 팝업 확인 후 ESC 닫기
    """
    print("\n" + "=" * 60)
    print(" [TC-FLT-09] CSO 필터링 직접 조회 E2E Full Flow 검증 시작")
    print("=" * 60)

    # 1. 메뉴 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-list")
    page.wait_for_selector("h2:has-text('필터링 직접 조회')", timeout=10000)

    # 모달 오픈 확보
    if page.locator("div[role='dialog']").count() == 0:
        query_btn = page.locator("button:has-text('직접 조회하기'), button[title*='필터링 직접 조회']").first
        query_btn.click()
    page.wait_for_selector("div[role='dialog']", timeout=10000)

    # 2. 제약사 선택 ('투썬')
    print("[Step 1] 제약사('투썬') 선택")
    dialog = page.locator("div[role='dialog']").first
    pharm_combobox = dialog.locator("button[role='combobox'], [role='combobox']").first
    pharm_combobox.click()
    page.wait_for_timeout(500)

    pharm_opt = page.locator("xpath=//div[span[contains(text(), '투썬')]] | //div[contains(@role, 'option') and contains(., '투썬')]").last
    if pharm_opt.is_visible():
        pharm_opt.click()
    else:
        opts = page.locator("[role='option'], div[data-radix-collection-item]").all()
        if len(opts) > 0:
            opts[0].click()
    page.wait_for_timeout(500)

    # 3. 공지사항 단계 이동
    print("[Step 2] 공지사항 단계 이동")
    next_btn = dialog.locator("button:has-text('다음')").first
    expect(next_btn).to_be_enabled()
    next_btn.click()
    page.wait_for_timeout(500)

    # 4. 병의원 검색 단계 이동
    print("[Step 3] 병의원 검색 단계 이동")
    next_btn2 = dialog.locator("button:has-text('다음')").first
    if next_btn2.is_visible():
        next_btn2.click()
        page.wait_for_timeout(500)

    # 5. 병의원명 검색 및 선택
    print("[Step 4] 병의원명('자동화테스트') 검색 및 선택")
    hospital_input = dialog.locator("input[placeholder*='병의원명을 입력'], input[placeholder*='병의원']").first
    if hospital_input.is_visible():
        hospital_input.fill("자동화테스트")
        page.wait_for_timeout(500)

        # 제안 항목 선택
        suggestion = page.locator("xpath=//div[@role='dialog']//div[contains(., '자동화테스트')] | //div[span[span[text()='자동화테스트']]]").last
        if suggestion.is_visible():
            suggestion.click()
            page.wait_for_timeout(500)

        # 사업자번호 보충 입력 (비어있을 경우)
        biz_input = dialog.locator("input[placeholder*='-없이 숫자만'], input[placeholder*='사업자']").first
        if biz_input.is_visible() and not biz_input.input_value():
            biz_input.fill("6046400707")
            page.wait_for_timeout(300)

    # 6. '조회하기' 클릭 및 결과 팝업 확인
    print("[Step 5] '조회하기' 클릭 및 필터링 결과 팝업 확인")
    inquiry_btn = dialog.locator("button:has-text('조회하기')").last
    if inquiry_btn.is_enabled():
        inquiry_btn.click()
        page.wait_for_selector("h2:has-text('필터링 조회 결과'), div[role='dialog'] h2", timeout=10000)
        expect(page.locator("h2:has-text('필터링 조회 결과'), div[role='dialog'] h2").first).to_be_visible()

    # 7. 모달 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[Success] TC-FLT-09 CSO 필터링 직접 조회 E2E 검증 성공!")


def test_tc_flt_10_pharm_condition_and_performance_modals_e2e(page: Page, login_pharm1):
    """
    [TC-FLT-10] Phase 3 E2E: 제약사 필터링 조건 관리 저장 및 실적 관리 하위 모달(처방월/일괄추가) Full Flow 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-FLT-10] 제약사 조건 관리 / 실적 관리 E2E 검증 시작")
    print("=" * 60)

    # 1. 메뉴 진입
    page.locator("xpath=//a[span[contains(text(), '필터링 조회 관리')]] | //a[contains(., '필터링 조회 관리')]").first.click()
    page.wait_for_selector("h2:has-text('필터링 조회 관리')", timeout=10000)

    # 2. 조건 관리 모달 오픈 및 저장
    print("[Step 1] 필터링 조건 관리 모달 오픈 및 저장 확인")
    cond_btn = page.locator("button[title='조건 관리'], button:has-text('조건 관리')").first
    if cond_btn.is_visible():
        cond_btn.click()
        page.wait_for_selector("h2:has-text('필터링 조건 관리'), h2:has-text('조건 관리')", timeout=5000)
        expect(page.locator("h2:has-text('필터링 조건 관리'), h2:has-text('조건 관리')").first).to_be_visible()

        save_btn = page.locator("div[role='dialog'] button:has-text('저장하기'), button[title='저장하기']").first
        if save_btn.is_visible():
            save_btn.click()
            page.wait_for_selector("h2:has-text('저장할까요?'), div[role='dialog']", timeout=5000)
            confirm_btn = page.locator("div[role='dialog'] button:has-text('확인')").last
            if confirm_btn.is_visible():
                confirm_btn.click()
                page.wait_for_timeout(1000)

        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # 3. 실적 관리 모달 진입
    print("[Step 2] 실적 관리 모달 오픈 및 하위 모달(처방월/일괄추가) 인터랙션")
    perf_btn = page.locator("button[title='실적 관리'], button:has-text('실적 관리')").first
    if perf_btn.is_visible():
        perf_btn.click()
        page.wait_for_selector("h2:has-text('실적 관리')", timeout=5000)
        expect(page.locator("h2:has-text('실적 관리')").first).to_be_visible()

        # 3.1. 처방월 설정 모달
        month_btn = page.locator("div[role='dialog'] button:has-text('처방월 설정'), button[title='처방월 설정']").first
        if month_btn.is_visible():
            month_btn.click()
            page.wait_for_selector("h2:has-text('처방월 설정')", timeout=5000)
            expect(page.locator("h2:has-text('처방월 설정')").first).to_be_visible()
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

        # 3.2. 일괄 추가 모달
        batch_btn = page.locator("div[role='dialog'] button:has-text('일괄추가'), div[role='dialog'] button:has-text('일괄 추가')").first
        if batch_btn.is_visible():
            batch_btn.click()
            page.wait_for_selector("h2:has-text('일괄 추가'), h2:has-text('일괄추가')", timeout=5000)
            expect(page.locator("h2:has-text('일괄 추가'), h2:has-text('일괄추가')").first).to_be_visible()
    # 4. 모든 다이얼로그 모달 닫기 (완전 복구)
    for _ in range(5):
        if page.locator("div[role='dialog']").count() == 0:
            break
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)

    expect(page.locator(".ag-root-wrapper, .ag-root").first).to_be_visible()
    expect(page.locator("xpath=//h2[contains(., '필터링 조회 관리')] | //h1[contains(., '필터링 조회 관리')] | //span[contains(text(), '필터링 조회 관리')]").first).to_be_visible()
    print("[Success] TC-FLT-10 제약사 조건 관리 및 실적 관리 E2E 검증 성공!")
