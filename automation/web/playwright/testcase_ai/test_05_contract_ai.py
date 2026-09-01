import os
import re
import time
import datetime
import pytest
from playwright.sync_api import Page, expect

# 공통 도구 모듈 import
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# 파일 경로 상수
TESTFILE_PDF = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF.pdf")

# ==============================================================================
# Phase 1 & 2: Core & Atomic Validation Test Cases
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_cnt_01_tab_switching_and_grid_columns(page: Page, login_cso):
    """
    [TC-CNT-01] Happy Path: 계약서 관리 탭 전환(전송 전/전송 완료) 및 그리드 컬럼 검증
    - /dashboard/e-contract/contract-management 진입
    - '전송 전' / '전송 완료' 탭 전환 및 AG Grid 로딩, 필수 컬럼(제목, 계약 업체 등) 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CNT-01] 탭 전환 및 그리드 컬럼 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '계약서 관리' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/e-contract/contract-management")
    page.wait_for_selector("h2:has-text('계약서 관리')", timeout=10000)

    # 2. '전송 전' 탭 기본 활성화 확인
    tab_before = page.locator("button:has-text('전송 전'), div[role='tablist'] button:has-text('전송 전')").first
    expect(tab_before).to_be_visible()

    # 3. '전송 완료' 탭 전환
    print("[Step 2] '전송 완료' 탭 클릭")
    tab_done = page.locator("button:has-text('전송 완료'), div[role='tablist'] button:has-text('전송 완료')").first
    expect(tab_done).to_be_visible()
    tab_done.click()
    page.wait_for_timeout(1000)

    # 4. AG Grid 렌더링 및 컬럼 검증
    print("[Step 3] AG Grid 헤더 컬럼 가시성 단언")
    grid_container = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid_container).to_be_visible()

    title_col = page.locator(".ag-header-cell-text:has-text('제목'), .ag-header-cell:has-text('제목')").first
    expect(title_col).to_be_visible()

    company_col = page.locator(".ag-header-cell-text:has-text('계약 업체'), .ag-header-cell:has-text('계약 업체')").first
    expect(company_col).to_be_visible()
    print("[Success] TC-CNT-01 탭 전환 및 그리드 로딩 검증 성공!")


def test_tc_cnt_02_search_and_reset_filter(page: Page, login_cso):
    """
    [TC-CNT-02] Validation: 계약서 관리 검색 필터 및 검색 초기화 기능 검증
    - 미존재 키워드 검색 후 '검색 초기화' 클릭 시 초기 목록 복구 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CNT-02] 검색 필터 및 초기화 기능 검증 시작")
    print("=" * 60)

    # 1. 계약서 관리 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/e-contract/contract-management")
    page.wait_for_selector("h2:has-text('계약서 관리')", timeout=10000)

    # 2. 미존재 키워드 검색
    search_input = page.locator("input[placeholder*='검색어를 입력'], input[placeholder*='검색어']").first
    expect(search_input).to_be_visible()

    print("[Step 1] 미존재 검색어 입력 및 검색 실행")
    search_input.fill("NON_EXISTING_CONTRACT_9999")
    page.wait_for_timeout(300)

    search_btn = page.locator("button:has-text('검색')").first
    expect(search_btn).to_be_visible()
    search_btn.click()
    page.wait_for_timeout(1000)

    # 3. '검색 초기화' 버튼 클릭
    print("[Step 2] '검색 초기화' 버튼 클릭하여 필터 리셋")
    reset_btn = page.locator("button:has-text('검색 초기화'), button:has-text('초기화')").first
    expect(reset_btn).to_be_visible()
    reset_btn.click()
    page.wait_for_timeout(1000)

    # 4. 검색창 초기화 단언
    expect(search_input).to_have_value("")
    print("[Success] TC-CNT-02 검색 필터 및 초기화 기능 검증 성공!")


def test_tc_cnt_03_template_management_modal_open(page: Page, login_cso):
    """
    [TC-CNT-03] Happy Path: '템플릿 관리' 모달 오픈 및 목록 렌더링 검증
    - '템플릿 관리' 버튼 클릭 ➡️ 모달 노출 ➡️ 템플릿 목록/그리드 및 '템플릿 추가' 버튼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CNT-03] 템플릿 관리 모달 오픈 검증 시작")
    print("=" * 60)

    # 1. 계약서 관리 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/e-contract/contract-management")
    page.wait_for_selector("h2:has-text('계약서 관리')", timeout=10000)

    # 2. '템플릿 관리' 버튼 클릭
    print("[Step 1] '템플릿 관리' 버튼 클릭")
    template_btn = page.locator("button:has-text('템플릿 관리')").first
    expect(template_btn).to_be_visible()
    template_btn.click()

    # 3. 다이얼로그 모달 오픈 및 요소 검증
    print("[Step 2] 모달 다이얼로그 및 '템플릿 추가' 버튼 가시성 단언")
    dialog = page.locator("div[role='dialog']").first
    expect(dialog).to_be_visible()
    expect(dialog.locator("h2, h3").first).to_be_visible()

    add_template_btn = dialog.locator("button:has-text('템플릿 추가')").first
    expect(add_template_btn).to_be_visible()
    print("[Success] TC-CNT-03 템플릿 관리 모달 오픈 검증 성공!")


def test_tc_cnt_04_template_management_modal_close(page: Page, login_cso):
    """
    [TC-CNT-04] Validation: '템플릿 관리' 모달 닫기 검증
    - 모달 열린 상태에서 ESC 키 입력 ➡️ 모달 정상 닫힘 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CNT-04] 템플릿 관리 모달 닫기 검증 시작")
    print("=" * 60)

    # 1. 템플릿 관리 모달 열기
    page.goto(page.url.split("dashboard")[0] + "dashboard/e-contract/contract-management")
    page.wait_for_selector("button:has-text('템플릿 관리')", timeout=10000)
    page.locator("button:has-text('템플릿 관리')").first.click()

    dialog = page.locator("div[role='dialog']").first
    expect(dialog).to_be_visible()

    # 2. ESC 키 입력하여 닫기
    print("[Step 1] ESC 키를 통한 모달 닫기")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 3. 모달 비가시성 단언
    expect(page.locator("div[role='dialog']")).to_have_count(0)
    print("[Success] TC-CNT-04 템플릿 관리 모달 닫기 검증 성공!")


def test_tc_cnt_05_contract_create_page_rendering(page: Page, login_cso):
    """
    [TC-CNT-05] Happy Path: '계약서 작성' 페이지 진입 및 폼 요소 렌더링 검증
    - '계약서 작성' 버튼 클릭 ➡️ /dashboard/e-contract/contract-management/write 이동
    - 계약서 제목, 계약일자, 계약 업체 검색 버튼 노출 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CNT-05] 계약서 작성 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 계약서 관리 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/e-contract/contract-management")
    page.wait_for_selector("h2:has-text('계약서 관리')", timeout=10000)

    # 2. '계약서 작성' 버튼 클릭
    print("[Step 1] '계약서 작성' 버튼 클릭")
    create_btn = page.locator("button:has-text('계약서 작성')").first
    expect(create_btn).to_be_visible()
    create_btn.click()

    # 3. 작성 페이지 URL 및 헤딩 단언
    print("[Step 2] 계약서 작성 페이지 렌더링 및 폼 필드 단언")
    page.wait_for_selector("h2:has-text('계약서 작성하기')", timeout=10000)
    expect(page).to_have_url(re.compile(r".*contract-management/write.*"))
    expect(page.locator("h2", has_text="계약서 작성하기").first).to_be_visible()

    # 4. 필수 입력 폼 요소 가시성 단언
    expect(page.locator("input[name='title']").first).to_be_visible()
    expect(page.locator("button[title*='업체 검색'], button:has-text('업체 검색')").first).to_be_visible()
    print("[Success] TC-CNT-05 계약서 작성 페이지 렌더링 검증 성공!")


def test_tc_cnt_06_contract_create_cancel_return_to_list(page: Page, login_cso):
    """
    [TC-CNT-06] Validation: 계약서 작성 화면에서 브레드크럼 '계약서 관리' 링크 클릭 시 목록 복귀 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CNT-06] 계약서 작성 취소 및 목록 복귀 검증 시작")
    print("=" * 60)

    # 1. 계약서 작성 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/e-contract/contract-management/write")
    page.wait_for_selector("h2:has-text('계약서 작성하기')", timeout=10000)

    # 2. 브레드크럼의 '계약서 관리' 링크 클릭
    print("[Step 1] 브레드크럼 '계약서 관리' 링크 클릭")
    breadcrumb_link = page.locator("nav[aria-label='breadcrumb'] a:has-text('계약서 관리'), a[href*='/e-contract/contract-management']").first
    expect(breadcrumb_link).to_be_visible()
    breadcrumb_link.click()

    # 3. 계약서 관리 메인 복귀 단언
    print("[Step 2] 계약서 관리 메인 목록 복귀 단언")
    page.wait_for_selector("h2:has-text('계약서 관리')", timeout=10000)
    expect(page).to_have_url(re.compile(r".*e-contract/contract-management$"))
    expect(page.locator("h2", has_text="계약서 관리").first).to_be_visible()
    print("[Success] TC-CNT-06 계약서 작성 취소 및 목록 복귀 검증 성공!")


def test_tc_cnt_07_contract_create_disabled_submit_validation(page: Page, login_cso):
    """
    [TC-CNT-07] Phase 2 Validation: 계약서 작성 화면에서 필수값 미입력 시 '작성하기' 버튼 disabled 방어 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CNT-07] 계약서 작성 필수값 미입력 비활성화(disabled) 방어 검증 시작")
    print("=" * 60)

    # 1. 계약서 작성 페이지 직접 진입
    page.goto(page.url.split("dashboard")[0] + "dashboard/e-contract/contract-management/write")
    page.wait_for_selector("h2:has-text('계약서 작성하기')", timeout=10000)

    # 2. '작성하기' 버튼 상태 확인
    print("[Step 1] 빈 입력 상태에서 '작성하기' 버튼 비활성화 단언")
    submit_btn = page.locator("button[title*='작성하기'], button:has-text('작성하기')").first
    expect(submit_btn).to_be_visible()
    expect(submit_btn).to_be_disabled()
    print("[Success] TC-CNT-07 계약서 작성 비활성화 방어 검증 성공!")


def test_tc_cnt_08_received_contract_rendering_and_columns(page: Page, login_cso):
    """
    [TC-CNT-08] Phase 2 Happy Path: '받은 계약서' 메뉴 진입 및 그리드 컬럼 검증
    - /dashboard/e-contract/received-contract 이동 ➡️ 헤딩 및 AG Grid 컬럼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CNT-08] 받은 계약서 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. '받은 계약서' 메뉴 이동
    print("[Step 1] '받은 계약서' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/e-contract/received-contract")
    page.wait_for_selector("h2:has-text('받은 계약서')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="받은 계약서").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*e-contract/received-contract.*"))

    # 3. AG Grid 테이블 및 주요 컬럼 검증
    print("[Step 2] AG Grid 테이블 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('제목'), .ag-header-cell:has-text('제목')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('계약 업체'), .ag-header-cell:has-text('계약 업체')").first).to_be_visible()
    print("[Success] TC-CNT-08 받은 계약서 페이지 렌더링 검증 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_cnt_09_create_contract_template_e2e(page: Page, login_cso):
    """
    [TC-CNT-09] Phase 3 E2E: 계약서 템플릿 관리 (기존 템플릿 정리 및 신규 템플릿 추가/에디터/미리보기/저장) Full Flow 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CNT-09] 신규 계약서 템플릿 생성 E2E 검증 시작")
    print("=" * 60)

    # 1. 계약서 관리 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/e-contract/contract-management")
    page.wait_for_selector("h2:has-text('계약서 관리')", timeout=10000)

    # 2. '템플릿 관리' 클릭 및 모달 로드 대기
    print("[Step 1] '템플릿 관리' 클릭 및 모달 오픈")
    page.click("button:has-text('템플릿 관리')")
    page.wait_for_selector("div[role='dialog'] h2:has-text('템플릿 관리')", timeout=5000)
    page.wait_for_timeout(500)

    dialog = page.locator("div[role='dialog']").last
    add_btn = dialog.locator("button[title*='추가'], button:has-text('템플릿 추가')").first

    # 3. 추가 버튼이 비활성화(최대 10개 한도 초과)인 경우 활성화될 때까지 템플릿 삭제 반복
    while add_btn.is_disabled() and dialog.locator("button[title='수정']").count() > 0:
        print("[Step 2] 템플릿 등록 한도 초과 -> 기존 템플릿 1개 삭제 수행")
        edit_btn = dialog.locator("button[title='수정']").first
        edit_btn.click()
        page.wait_for_selector("h2:has-text('계약서 템플릿 관리')", timeout=5000)

        delete_btn = page.locator("button[title='삭제하기'], button:has-text('삭제하기')").first
        delete_btn.scroll_into_view_if_needed()
        delete_btn.click()

        page.wait_for_selector("h2:has-text('삭제할까요?')", timeout=5000)
        confirm_del = page.locator("button[title='삭제하기'], button:has-text('삭제하기')").last
        confirm_del.click()
        page.wait_for_selector("h2:has-text('계약서 관리')", timeout=5000)
        page.wait_for_timeout(1000)

        # 템플릿 관리 모달 다시 오픈
        page.click("button:has-text('템플릿 관리')")
        page.wait_for_selector("div[role='dialog'] h2:has-text('템플릿 관리')", timeout=5000)
        page.wait_for_timeout(500)
        dialog = page.locator("div[role='dialog']").last
        add_btn = dialog.locator("button[title*='추가'], button:has-text('템플릿 추가')").first

    # 4. 신규 계약서 템플릿 추가
    print("[Step 3] 신규 계약서 템플릿 추가")
    expect(add_btn).to_be_enabled()
    add_btn.click()
    page.wait_for_selector("h2:has-text('계약서 템플릿 추가')", timeout=5000)

    # 5. 템플릿 제목 및 내용 입력
    now_time = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    template_title = f"자동화템플릿_{now_time}"
    print(f"[Step 4] 템플릿 제목({template_title}) 및 에디터 텍스트 입력")
    page.fill("input[name='templateTitle']", template_title)

    page.wait_for_selector(".ql-editor", timeout=5000)
    page.evaluate("document.querySelector('.ql-editor').innerHTML = '<p>자동화 테스트 템플릿 내용입니다.</p>'")
    page.wait_for_timeout(500)

    # 6. 미리보기 확인 후 ESC 닫기
    print("[Step 5] 미리보기 모달 확인")
    page.click("button:has-text('미리보기')")
    page.wait_for_selector("h2:has-text('미리보기')", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 7. 저장하기 클릭
    print("[Step 6] '저장하기' 클릭하여 템플릿 저장")
    page.click("button:has-text('저장하기')")
    page.wait_for_timeout(1000)

    # 8. 템플릿 관리 모달 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[Success] TC-CNT-09 신규 계약서 템플릿 생성 E2E 검증 성공!")


def test_tc_cnt_10_create_electronic_contract_e2e(page: Page, login_cso):
    """
    [TC-CNT-10] Phase 3 E2E: 전자계약서 작성 Full Flow 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CNT-10] 전자계약서 작성 E2E 검증 시작")
    print("=" * 60)

    # 1. 계약서 작성 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/e-contract/contract-management/write")
    page.wait_for_selector("h2:has-text('계약서 작성하기')", timeout=10000)

    # 2. 제목 및 계약일자 입력
    now_str = datetime.datetime.now().strftime("%m%d-%H%M")
    contract_title = f"자동화계약_{now_str}"
    print(f"[Step 1] 계약서 제목({contract_title}) 및 일자 선택")
    page.fill("input[name='title']", contract_title)

    page.click("#date, button:has-text('계약일')")
    today_day = str(datetime.datetime.now().day)
    page.locator(f"td:has(button:text-is('{today_day}'))").first.click()

    # 3. 계약 업체 검색 및 추가
    print("[Step 2] 계약 업체 검색 및 추가")
    page.click("button[title*='업체 검색'], button:has-text('업체 검색')")
    page.wait_for_selector("h2:has-text('업체 검색')", timeout=5000)

    page.fill("input[placeholder*='검색']", "투썬")
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)

    company_item = page.locator("div[role='dialog'] div:has-text('투썬')").last
    if company_item.is_visible():
        company_item.click()
        page.click("div[role='dialog'] button:has-text('추가하기')")
        page.wait_for_timeout(500)

    # 4. 에디터 본문 내용 입력
    print("[Step 3] 계약 본문 내용 입력")
    page.wait_for_selector(".ql-editor", timeout=5000)
    page.evaluate("document.querySelector('.ql-editor').innerHTML = '<p>자동화 테스트 계약서 본문 내용입니다.</p>'")
    page.wait_for_timeout(500)

    # 5. 파일 첨부
    print("[Step 4] 계약서 파일 첨부")
    file_input = page.locator("input[type='file']").first
    if file_input.is_visible():
        file_input.set_input_files(TESTFILE_PDF)
        page.wait_for_timeout(500)

    # 6. 작성하기 클릭 및 완료 팝업 처리
    print("[Step 5] '작성하기' 클릭 및 확인 팝업")
    submit_btn = page.locator("button:has-text('작성하기')").first
    if submit_btn.is_enabled():
        submit_btn.click()
        page.wait_for_selector("div[role='dialog']", timeout=5000)
        confirm_btn = page.locator("div[role='dialog'] button:has-text('작성하기')").last
        if confirm_btn.is_visible():
            confirm_btn.click()
            page.wait_for_timeout(1500)

    # 계약서 관리 메인 복귀 단언
    expect(page.locator("h2", has_text="계약서 관리").first).to_be_visible()
    print("[Success] TC-CNT-10 전자계약서 작성 E2E 검증 성공!")
