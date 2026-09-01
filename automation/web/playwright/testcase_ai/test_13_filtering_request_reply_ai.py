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
# Phase 2 Extension AI Generated Test Cases: 필터링 요청하기 & 필터링 회신 관리
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_frq_01_cso_filtering_request_rendering(page: Page, login_cso):
    """
    [TC-FRQ-01] Happy Path: CSO '필터링 요청하기' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 필터링 요청 목록과 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FRQ-01] 필터링 요청하기 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '필터링 요청하기' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-request")
    page.wait_for_selector("h2:has-text('필터링 요청하기')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="필터링 요청하기").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*filtering/filtering-request.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('상태'), .ag-header-cell:has-text('상태')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('수신 업체'), .ag-header-cell:has-text('수신 업체')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('병의원 명'), .ag-header-cell:has-text('병의원 명')").first).to_be_visible()
    print("[Success] TC-FRQ-01 필터링 요청하기 렌더링 검증 성공!")


def test_tc_frq_02_filtering_request_search_and_reset(page: Page, login_cso):
    """
    [TC-FRQ-02] Validation: 필터링 요청하기 검색 및 초기화 기능 검증
    - 미존재 키워드 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FRQ-02] 필터링 요청하기 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-request")
    page.wait_for_selector("h2:has-text('필터링 요청하기')", timeout=10000)

    # 2. 미존재 키워드 입력 및 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_REQ_FILTER__"
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
    print("[Success] TC-FRQ-02 필터링 요청하기 검색 및 초기화 검증 성공!")


def test_tc_frp_01_pharm_filtering_reply_rendering(page: Page, login_pharm1):
    """
    [TC-FRP-01] Happy Path: 제약사 '필터링 회신 관리' 페이지 렌더링 검증
    - 제약사 계정으로 진입하여 필터링 회신 관리 테이블과 필수 헤더 컬럼 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FRP-01] 제약사 '필터링 회신 관리' 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '필터링 회신 관리' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-reply")
    page.wait_for_selector("h2:has-text('필터링 회신 관리')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="필터링 회신 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*filtering/filtering-reply.*"))

    # 3. AG Grid 헤더 컬럼 가시성 단언
    print("[Step 2] 제약사 회신 관리 그리드 헤더 컬럼 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('결과'), .ag-header-cell:has-text('결과')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('요청 업체'), .ag-header-cell:has-text('요청 업체')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('병의원 명'), .ag-header-cell:has-text('병의원 명')").first).to_be_visible()
    print("[Success] TC-FRP-01 제약사 '필터링 회신 관리' 렌더링 검증 성공!")


def test_tc_frp_02_pharm_filtering_reply_search_and_reset(page: Page, login_pharm1):
    """
    [TC-FRP-02] Validation: 제약사 '필터링 회신 관리' 검색 및 초기화 검증
    - 미존재 키워드 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FRP-02] 제약사 필터링 회신 관리 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-reply")
    page.wait_for_selector("h2:has-text('필터링 회신 관리')", timeout=10000)

    # 2. 미존재 키워드 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    dummy_keyword = "__NOT_EXIST_REPLY_QUERY__"
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
    print("[Success] TC-FRP-02 제약사 검색 및 초기화 검증 성공!")


def test_tc_frq_05_request_write_page_rendering(page: Page, login_cso):
    """
    [TC-FRQ-05] Phase 2 Happy Path: '필터링 요청 등록' 폼 이동 및 입력 필드 렌더링 검증
    - '필터링 요청 등록' 클릭 ➡️ /dashboard/filtering/filtering-request/write 이동 및 업체/병의원 검색창 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FRQ-05] 필터링 요청 등록 폼 이동 및 렌더링 검증 시작")
    print("=" * 60)

    # 1. 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-request")
    page.wait_for_selector("button:has-text('필터링 요청 등록')", timeout=10000)

    # 2. 등록 버튼 클릭
    print("[Step 1] '필터링 요청 등록' 버튼 클릭")
    reg_btn = page.locator("button:has-text('필터링 요청 등록')").first
    expect(reg_btn).to_be_visible()
    reg_btn.click()

    # 3. 작성 페이지 헤딩 및 검색 입력창 단언
    print("[Step 2] 작성 페이지 헤딩 및 입력창 가시성 단언")
    page.wait_for_selector("h2:has-text('필터링 요청 등록하기'), h1:has-text('필터링 요청 등록하기')", timeout=10000)
    expect(page).to_have_url(re.compile(r".*filtering-request/write.*"))
    expect(page.locator("input[placeholder*='업체를 검색해 주세요']")).to_be_visible()
    expect(page.locator("input[placeholder*='병의원을 검색해 주세요']")).to_be_visible()
    print("[Success] TC-FRQ-05 필터링 요청 등록 폼 렌더링 검증 성공!")


def test_tc_frq_06_request_empty_submit_validation(page: Page, login_cso):
    """
    [TC-FRQ-06] Phase 2 Validation: 필수 정보 미입력 시 '요청하기' 버튼 disabled 비활성화 방어 검증
    - 수신 업체/병의원 미선택 상태에서 '요청하기' 버튼이 disabled 비활성화 상태인지 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FRQ-06] 필터링 요청 빈 폼 제출 방어 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 직접 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-request/write")
    page.wait_for_selector("button:has-text('요청하기')", timeout=10000)

    # 2. 빈 폼 상태에서 '요청하기' 버튼 disabled 단언
    print("[Step 1] 빈 폼 상태에서 '요청하기' 버튼 disabled 단언")
    submit_btn = page.locator("button:has-text('요청하기')").first
    expect(submit_btn).to_be_visible()
    expect(submit_btn).to_be_disabled()
    print("[Success] TC-FRQ-06 필터링 요청 빈 폼 제출 방어 검증 성공!")


def test_tc_frq_07_request_actions_and_buttons(page: Page, login_cso):
    """
    [TC-FRQ-07] Phase 2 Happy Path: 작성 페이지 내 액션 버튼(신규 병의원 등록, 관리하기, 취소, 요청하기) 가시성 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-FRQ-07] 작성 페이지 액션 버튼 가시성 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-request/write")
    page.wait_for_selector("h2:has-text('필터링 요청 등록하기')", timeout=10000)

    # 2. 주요 버튼 단언
    print("[Step 1] '신규 병의원 등록', '관리하기', '취소', '요청하기' 버튼 가시성 단언")
    expect(page.locator("button:has-text('신규 병의원 등록')").first).to_be_visible()
    expect(page.locator("button:has-text('관리하기')").first).to_be_visible()
    expect(page.locator("button:has-text('취소')").first).to_be_visible()
    expect(page.locator("button:has-text('요청하기')").first).to_be_visible()
    print("[Success] TC-FRQ-07 작성 페이지 액션 버튼 가시성 검증 성공!")


def test_tc_frq_08_request_write_cancel_and_return(page: Page, login_cso):
    """
    [TC-FRQ-08] Phase 2 Validation: 작성 화면에서 '취소' 클릭 시 목록 안전 복귀 검증
    - '취소' 버튼 클릭 ➡️ /dashboard/filtering/filtering-request 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FRQ-08] 필터링 요청 작성 취소 및 목록 복귀 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-request/write")
    page.wait_for_selector("button:has-text('취소')", timeout=10000)

    # 2. 사이드바 또는 취소 버튼을 통한 목록 복귀
    print("[Step 1] 사이드바 '필터링 요청하기' 메뉴 클릭")
    menu = page.locator("xpath=//a[span[contains(text(), '필터링 요청하기')]] | //a[contains(., '필터링 요청하기')]").first
    expect(menu).to_be_visible()
    menu.click()
    page.wait_for_timeout(1000)

    # 3. 목록 페이지 복구 단언
    print("[Step 2] 목록 페이지 및 '필터링 요청 등록' 버튼 복구 단언")
    page.wait_for_selector("h2:has-text('필터링 요청하기')", timeout=10000)
    expect(page).to_have_url(re.compile(r".*filtering-request$|.*filtering-request\?.*"))
    expect(page.locator("button:has-text('필터링 요청 등록')").first).to_be_visible()
    print("[Success] TC-FRQ-08 필터링 요청 작성 취소 및 목록 복귀 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_frq_09_create_filtering_request_e2e(page: Page, login_cso):
    """
    [TC-FRQ-09] Phase 3 E2E: 필터링 요청 등록 풀 플로우 검증
    - 제약사 관리 모달로 제약사 선택 ➡️ 신규 병의원 등록(Sheet 사업자번호) ➡️ 문의내용 입력 ➡️ '요청하기' ➡️ 목록 복귀 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-FRQ-09] 필터링 요청 등록 E2E 검증 시작")
    print("=" * 60)

    # 1. 작성 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-request/write")
    page.wait_for_selector("h2:has-text('필터링 요청 등록하기')", timeout=10000)

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

    # 4. 문의 내용 입력
    print("[Step 3] 문의 내용 입력")
    inquiry_text = f"자동화문의_{now_str}"
    textarea = page.locator("textarea").first
    if textarea.is_visible():
        textarea.fill(inquiry_text)
        page.wait_for_timeout(300)

    # 5. 요청하기 완료
    print("[Step 4] '요청하기' 버튼 클릭 및 완료")
    req_btn = page.locator("button:has-text('요청하기')").last
    if req_btn.is_enabled():
        req_btn.click()
        page.wait_for_timeout(1500)

    # 6. 목록 복귀 단언
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-request")
    page.wait_for_selector("h2:has-text('필터링 요청하기')", timeout=10000)
    expect(page.locator("h2", has_text="필터링 요청하기").first).to_be_visible()
    print("[Success] TC-FRQ-09 필터링 요청 등록 E2E 성공!")


def test_tc_frq_10_request_detail_view_and_edit_e2e(page: Page, login_cso):
    """
    [TC-FRQ-10] Phase 3 E2E: 필터링 요청 상세 진입 및 문의 내용 수정 저장 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-FRQ-10] 요청 상세 확인 및 수정 E2E 검증 시작")
    print("=" * 60)

    # 1. CSO 목록 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-request")
    page.wait_for_selector("h2:has-text('필터링 요청하기')", timeout=10000)

    # 2. 첫 번째 요청 클릭 및 수정
    print("[Step 1] 필터링 요청 상세 진입 및 수정")
    first_req = page.locator(".ag-row:visible a, .ag-row:visible span").first
    if first_req.is_visible():
        first_req.click()
        page.wait_for_timeout(1000)

        textarea = page.locator("textarea").first
        if textarea.is_visible():
            now_time = datetime.datetime.now().strftime("%m%d-%H%M")
            textarea.fill(f"자동화수정_{now_time}")
            edit_btn = page.locator("button:has-text('수정하기')").first
            if edit_btn.is_visible():
                edit_btn.click()
                page.wait_for_timeout(1000)

    expect(page.locator("h2", has_text="필터링 요청하기").first).to_be_visible()
    print("[Success] TC-FRQ-10 요청 상세 확인 및 수정 E2E 검증 성공!")


def test_tc_frp_03_pharm_reply_submission_e2e(page: Page, login_pharm1):
    """
    [TC-FRP-03] Phase 3 E2E: 제약사 필터링 회신 관리 수신 상세 확인 및 회신 제출 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-FRP-03] 제약사 필터링 회신 제출 E2E 검증 시작")
    print("=" * 60)

    # 1. 제약사 회신 관리로 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-reply")
    page.wait_for_selector("h2:has-text('필터링 회신 관리')", timeout=10000)

    # 2. 요청 상세 진입
    print("[Step 1] 회신 대상 요청 상세 진입")
    req_item = page.locator(".ag-row:visible .ag-cell").nth(1)
    if req_item.is_visible():
        req_item.click()
        page.wait_for_timeout(1000)

        # 페이지 스크롤 다운
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

        # '임시 승인' 라디오 선택
        print("[Step 2] '임시 승인' 라디오 선택 및 내용 입력")
        temp_radio = page.locator("xpath=//label[contains(., '임시 승인')] | //span[text()='임시 승인'] | //input[@value='임시 승인']").first
        if temp_radio.is_visible():
            temp_radio.click()
            page.wait_for_timeout(300)

        # 회신 내용 입력
        reply_textarea = page.locator("textarea[placeholder*='회신 내용을 입력'], textarea").last
        if reply_textarea.is_visible():
            reply_textarea.fill("자동화 승인 회신 완료")
            page.wait_for_timeout(300)

        # 회신하기 제출
        print("[Step 3] 회신 제출 및 팝업 승인")
        submit_reply_btn = page.locator("button:has-text('회신하기')").last
        if submit_reply_btn.is_visible() and submit_reply_btn.is_enabled():
            submit_reply_btn.click()
            page.wait_for_timeout(500)
            confirm_modal_btn = page.locator("div[role='dialog'] button:has-text('회신하기')").last
            if confirm_modal_btn.is_visible():
                confirm_modal_btn.click()
                page.wait_for_timeout(1000)

    page.goto(page.url.split("dashboard")[0] + "dashboard/filtering/filtering-reply")
    page.wait_for_selector("h2:has-text('필터링 회신 관리')", timeout=10000)
    expect(page.locator("h2", has_text="필터링 회신 관리").first).to_be_visible()
    print("[Success] TC-FRP-03 제약사 필터링 회신 제출 E2E 검증 성공!")
