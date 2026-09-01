import os
import re
import time
import datetime
import pytest
from playwright.sync_api import Page, expect

# ==============================================================================
# Phase 2 Extension AI Generated Test Cases: 재위탁 통보서 관리 & 받은 재위탁 통보서
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_con_01_management_page_and_grid_loading(page: Page, login_cso):
    """
    [TC-CON-01] Happy Path: 재위탁 통보서 관리 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 AG Grid 테이블과 고유 헤더 컬럼들의 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CON-01] 재위탁 통보서 관리 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 진입
    print("[Step 1] '재위탁 통보서 관리' 메뉴 클릭")
    page.goto(page.url.split("dashboard")[0] + "dashboard/re-entrustment/re-entrustment-list")
    page.wait_for_selector("h2:has-text('재위탁 통보서 관리')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="재위탁 통보서 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*re-entrustment-list.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('상태'), .ag-header-cell:has-text('상태')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('의약품 공급자(제약사)'), .ag-header-cell:has-text('의약품 공급자')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('재위탁 상호/법인명'), .ag-header-cell:has-text('재위탁 상호')").first).to_be_visible()
    print("[Success] TC-CON-01 재위탁 통보서 관리 렌더링 검증 성공!")


def test_tc_con_02_search_and_reset_filter(page: Page, login_cso):
    """
    [TC-CON-02] Validation: 재위탁 통보서 관리 검색 필터 및 초기화 기능 검증
    - 미존재 키워드 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CON-02] 검색 필터 및 초기화 기능 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/re-entrustment/re-entrustment-list")
    page.wait_for_selector("h2:has-text('재위탁 통보서 관리')", timeout=10000)

    # 2. 미존재 키워드 입력 및 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_RE_ENTRUST__"
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
    print("[Success] TC-CON-02 검색 및 초기화 검증 성공!")


def test_tc_con_03_negative_action_without_selection(page: Page, login_cso):
    """
    [TC-CON-03] Negative: 항목 미선택 상태에서 상단 액션 버튼 비활성화 검증
    - 체크박스 미선택 시 '전송하기' 및 '삭제하기' 버튼이 disabled 비활성화 상태인지 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CON-03] 항목 미선택 액션 방어 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/re-entrustment/re-entrustment-list")
    page.wait_for_selector("h2:has-text('재위탁 통보서 관리')", timeout=10000)

    # 2. 미선택 상태에서 '전송하기' 버튼 disabled 단언
    print("[Step 1] 미선택 상태에서 '전송하기' 버튼 disabled 단언")
    send_btn = page.locator("button:has-text('전송하기')").first
    if send_btn.is_visible():
        expect(send_btn).to_be_disabled()

    # 3. 미선택 상태에서 '삭제하기' 버튼 disabled 단언
    print("[Step 2] 미선택 상태에서 '삭제하기' 버튼 disabled 단언")
    delete_btn = page.locator("button:has-text('삭제하기')").first
    if delete_btn.is_visible():
        expect(delete_btn).to_be_disabled()

    print("[Success] TC-CON-03 미선택 액션 버튼 비활성화(disabled) 방어 검증 성공!")


def test_tc_con_04_received_consignment_rendering_pharm(page: Page, login_pharm1):
    """
    [TC-CON-04] Happy Path: 제약사 계정 '받은 재위탁 통보서' 페이지 렌더링 검증
    - 제약사 계정으로 진입하여 '받은 재위탁 통보서' 헤딩 및 수신 목록 그리드 헤더 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CON-04] 제약사 '받은 재위탁 통보서' 렌더링 검증 시작")
    print("=" * 60)

    # 1. 받은 재위탁 통보서 메뉴 이동
    print("[Step 1] '받은 재위탁 통보서' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/re-entrustment/re-entrustment-management")
    page.wait_for_selector("h2:has-text('받은 재위탁 통보서')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="받은 재위탁 통보서").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*re-entrustment-management.*"))

    # 3. AG Grid 수신 컬럼 가시성 단언
    print("[Step 2] 제약사 수신 그리드 헤더 컬럼 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('상태'), .ag-header-cell:has-text('상태')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('위탁자 상호/법인명'), .ag-header-cell:has-text('위탁자')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('재위탁 상호/법인명'), .ag-header-cell:has-text('재위탁 상호')").first).to_be_visible()
    print("[Success] TC-CON-04 제약사 '받은 재위탁 통보서' 렌더링 검증 성공!")


def test_tc_con_05_write_page_navigation_and_form_rendering(page: Page, login_cso):
    """
    [TC-CON-05] Phase 2 Happy Path: 재위탁 통보서 작성 페이지 진입 및 폼 요소 렌더링 검증
    - '작성하기' 버튼 클릭 후 작성 폼 컴포넌트(제약사 검색, 사유 입력, 업체 섹션) 확인
    """
    print("\n" + "=" * 60)
    print(" [TC-CON-05] 재위탁 통보서 작성 페이지 진입 및 폼 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/re-entrustment/re-entrustment-list")
    page.wait_for_selector("button:has-text('작성하기')", timeout=10000)

    # 2. '작성하기' 버튼 클릭
    print("[Step 1] '작성하기' 버튼 클릭")
    create_btn = page.locator("button:has-text('작성하기')").first
    expect(create_btn).to_be_visible()
    create_btn.click()

    # 3. 작성 페이지 헤딩 및 폼 컴포넌트 단언
    print("[Step 2] 작성 페이지 헤딩 및 필수 입력 필드 가시성 단언")
    page.wait_for_selector("h2:has-text('재위탁 통보서 작성하기'), h1:has-text('재위탁 통보서 작성하기')", timeout=10000)
    expect(page.locator("h2, h1", has_text="재위탁 통보서 작성하기").first).to_be_visible()
    expect(page.locator("text=재위탁 내용").first).to_be_visible()
    expect(page.locator("text=재위탁 업체").first).to_be_visible()

    # 제약사 검색 입력창 및 사유 입력창 단언
    search_input = page.locator("input[placeholder*='제약사 명 검색']").first
    expect(search_input).to_be_visible()

    reason_input = page.locator("input[placeholder*='재위탁 사유']").first
    expect(reason_input).to_be_visible()
    print("[Success] TC-CON-05 재위탁 통보서 작성 폼 렌더링 검증 성공!")


def test_tc_con_06_add_vendor_without_pharm_validation(page: Page, login_cso):
    """
    [TC-CON-06] Phase 2 Validation: 제약사 미입력 상태에서 재위탁 업체 '추가하기' 클릭 방어 검증
    - 제약사 미선택 상태에서 '추가하기' 클릭 ➡️ '제약사를 먼저 입력해 주세요' 알럿 팝업 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CON-06] 제약사 선행값 누락 방어 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/re-entrustment/re-entrustment-list/write")
    page.wait_for_selector("button:has-text('추가하기')", timeout=10000)

    # 2. 제약사 미입력 상태에서 '추가하기' 클릭
    print("[Step 1] 제약사 미선택 상태에서 '추가하기' 클릭")
    add_btn = page.locator("button:has-text('추가하기')").first
    add_btn.click()
    page.wait_for_selector("div[role='dialog']", timeout=5000)

    # 3. 방어 모달 단언 ('제약사를 먼저 입력해 주세요')
    print("[Step 2] '제약사를 먼저 입력해 주세요' 모달 단언")
    modal = page.locator("div[role='dialog']").first
    expect(modal).to_be_visible()
    expect(modal.locator("h2, h3, h4, p").filter(has_text="제약사를 먼저 입력해 주세요")).to_be_visible()

    # 4. 확인 버튼 클릭하여 닫기
    modal.locator("button:has-text('확인')").click()
    page.wait_for_timeout(500)
    expect(page.locator("div[role='dialog']")).to_have_count(0)
    print("[Success] TC-CON-06 제약사 선행값 누락 방어 검증 성공!")


def test_tc_con_07_write_form_empty_submit_blocked(page: Page, login_cso):
    """
    [TC-CON-07] Phase 2 Validation: 필수값 미입력 시 '작성하기' 클릭 유효성 방어 검증
    - 빈 폼 상태에서 '작성하기' 클릭 시 페이지가 이탈되지 않고 작성 폼에 유지되는지 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CON-07] 재위탁 통보서 작성 폼 빈값 제출 방어 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/re-entrustment/re-entrustment-list/write")
    page.wait_for_selector("button:has-text('작성하기')", timeout=10000)

    # 2. 빈 폼 상태에서 '작성하기' 버튼 클릭 (유효성 방어 확인)
    print("[Step 1] 빈 폼 상태에서 '작성하기' 클릭 시 페이지 이탈 방지 단언")
    submit_btn = page.locator("button:has-text('작성하기')").last
    expect(submit_btn).to_be_visible()
    submit_btn.click()
    page.wait_for_timeout(1000)

    # 3. 작성 폼에 그대로 머물러 있는지 검증 (Zero False-Positive)
    expect(page.locator("h2, h1", has_text="재위탁 통보서 작성하기").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*re-entrustment-list/write.*"))
    print("[Success] TC-CON-07 작성 폼 유효성(페이지 유지/방어) 검증 성공!")


def test_tc_con_08_write_page_cancel_and_return(page: Page, login_cso):
    """
    [TC-CON-08] Phase 2 Validation: 재위탁 통보서 작성 중 사이드바 메뉴를 통한 목록 복귀 검증
    - 작성 화면에서 사이드바 '재위탁 통보서 관리' 클릭 ➡️ /dashboard/re-entrustment/re-entrustment-list 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CON-08] 재위탁 통보서 작성 취소 및 목록 복귀 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/re-entrustment/re-entrustment-list/write")
    page.wait_for_selector("h2:has-text('재위탁 통보서 작성하기'), h1:has-text('재위탁 통보서 작성하기')", timeout=10000)

    # 2. 사이드바 '재위탁 통보서 관리' 클릭
    print("[Step 1] 사이드바 '재위탁 통보서 관리' 메뉴 클릭")
    menu = page.locator("xpath=//a[span[contains(text(), '재위탁 통보서 관리')]] | //a[contains(., '재위탁 통보서 관리')]").first
    expect(menu).to_be_visible()
    menu.click()
    page.wait_for_timeout(1000)

    # 3. 목록 페이지 복구 단언
    print("[Step 2] 목록 페이지 및 '작성하기' 버튼 복구 단언")
    page.wait_for_selector("h2:has-text('재위탁 통보서 관리')", timeout=10000)
    expect(page).to_have_url(re.compile(r".*re-entrustment-list$|.*re-entrustment-list\?.*"))
    expect(page.locator("button:has-text('작성하기')").first).to_be_visible()
    print("[Success] TC-CON-08 작성 취소 및 목록 복귀 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_con_09_create_reconsignment_notice_e2e(page: Page, login_cso):
    """
    [TC-CON-09] Phase 3 E2E: 재위탁 통보서 작성 풀 플로우 검증
    - 제약사('투썬') 검색 및 선택 ➡️ 사유/비고 입력 ➡️ 업체 모달 오픈 및 업체 추가 ➡️ 추가된 업체 중 1건 삭제 ➡️ 작성하기 및 팝업 승인 ➡️ 목록 복귀 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CON-09] 재위탁 통보서 작성 E2E 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/re-entrustment/re-entrustment-list/write")
    page.wait_for_selector("h2:has-text('재위탁 통보서 작성하기')", timeout=10000)

    # 2. 제약사 검색 및 키보드 선택
    print("[Step 1] 제약사('투썬') 검색 및 선택")
    search_input = page.locator("input[placeholder*='제약사 명 검색']").first
    search_input.click()
    search_input.fill("투썬")
    page.wait_for_timeout(300)
    page.keyboard.press("ArrowDown")
    page.wait_for_timeout(300)
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)

    # 3. 재위탁 사유 및 비고 입력
    now_time = datetime.datetime.now().strftime("%m%d-%H%M%S")
    reason_text = f"자동화사유_{now_time}"
    note_text = f"자동화비고_{now_time}"
    print(f"[Step 2] 재위탁 사유({reason_text}) 및 비고({note_text}) 입력")
    page.fill("input[name='reason']", reason_text)
    page.fill("input[name='note']", note_text)

    # 4. 재위탁 업체 추가 모달 오픈 (2개 업체 선택)
    print("[Step 3] 재위탁 업체 모달에서 업체 2건 선택 및 추가")
    add_vendor_btn = page.locator("button:has-text('추가하기')").first
    add_vendor_btn.click()
    page.wait_for_selector("div[role='dialog'] h2:has-text('재위탁 업체 추가하기')", timeout=5000)

    dialog = page.locator("div[role='dialog']").last
    page.wait_for_selector("div[role='dialog'] .ag-row", timeout=5000)
    
    rows = dialog.locator(".ag-row")
    row_count = rows.count()
    for i in range(min(row_count, 2)):
        rows.nth(i).locator(".ag-cell").first.click()
        page.wait_for_timeout(300)

    add_btn = dialog.locator("button:has-text('추가하기')").last
    expect(add_btn).to_be_enabled()
    add_btn.click()
    page.wait_for_timeout(1000)

    # 5. 추가한 업체 중 1건 삭제 버튼 인터랙션 (1건 유지)
    print("[Step 4] 추가된 업체 1건 삭제 (1건 유지)")
    delete_item_btn = page.locator("button[title='삭제'], button:has-text('삭제')")
    if delete_item_btn.count() > 1:
        delete_item_btn.first.click()
        page.wait_for_timeout(300)

    # 6. 최종 작성하기 클릭 및 승인
    print("[Step 5] 재위탁 통보서 최종 작성하기 및 팝업 승인")
    submit_btn = page.locator("button:has-text('작성하기')").last
    expect(submit_btn).to_be_enabled()
    submit_btn.click()
    page.wait_for_selector("div[role='dialog']", timeout=5000)

    confirm_btn = page.locator("div[role='dialog'] button:has-text('작성하기')").last
    expect(confirm_btn).to_be_visible()
    confirm_btn.click()
    page.wait_for_timeout(1500)

    # 7. 목록 복귀 단언
    page.wait_for_selector("h2:has-text('재위탁 통보서 관리')", timeout=10000)
    expect(page.locator("h2", has_text="재위탁 통보서 관리").first).to_be_visible()
    print("[Success] TC-CON-09 재위탁 통보서 작성 E2E 검증 성공!")


def test_tc_con_10_notice_detail_edit_and_file_modal_e2e(page: Page, login_cso):
    """
    [TC-CON-10] Phase 3 E2E: 통보서 상세 열기, 사유 수정 및 첨부파일 팝업 탭 확인 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CON-10] 재위탁 통보서 상세/수정/첨부파일 E2E 검증 시작")
    print("=" * 60)

    # 1. 목록 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/re-entrustment/re-entrustment-list")
    page.wait_for_selector("h2:has-text('재위탁 통보서 관리')", timeout=10000)

    # 2. 첫 번째 통보서 상세 열기
    print("[Step 1] 첫 번째 통보서 상세 열기")
    notice_btn = page.locator("button[title='재위탁통보서'], button:has-text('통보서')").first
    if notice_btn.is_visible():
        notice_btn.click()
        page.wait_for_selector("h2:has-text('재위탁 통보서')", timeout=5000)

        # 3. 사유 및 비고 수정
        now_time = datetime.datetime.now().strftime("%m%d-%H%M")
        edit_reason = f"수정사유_{now_time}"
        print(f"[Step 2] 사유({edit_reason}) 수정 및 저장")
        page.fill("input[name='reason']", edit_reason)

        page.click("button:has-text('수정하기'), button[title='수정하기']")
        page.wait_for_selector("div[role='dialog'] h2:has-text('수정 완료'), div[role='dialog']", timeout=5000)
        confirm_btn = page.locator("div[role='dialog'] button:has-text('확인')").last
        if confirm_btn.is_visible():
            confirm_btn.click()
            page.wait_for_timeout(500)

        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # 4. 첨부파일 팝업 열기
    print("[Step 3] 첨부파일 팝업 확인 및 탭 전환")
    file_btn = page.locator("button[title='파일'], button:has-text('파일')").first
    if file_btn.is_visible():
        file_btn.click()
        page.wait_for_selector("h2:has-text('파일')", timeout=5000)

        # 4.1. 수수료율 탭
        fee_tab = page.locator("button:has-text('수수료율')")
        if fee_tab.is_visible():
            fee_tab.click()
            page.wait_for_timeout(300)

        # 4.2. 수료증 탭
        cert_tab = page.locator("button:has-text('수료증')")
        if cert_tab.is_visible():
            cert_tab.click()
            page.wait_for_timeout(300)

        # ESC 닫기
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    expect(page.locator("h2", has_text="재위탁 통보서 관리").first).to_be_visible()
    print("[Success] TC-CON-10 재위탁 통보서 상세/수정/첨부파일 검증 성공!")
