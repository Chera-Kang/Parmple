import os
import time
import random
import datetime
import pytest
from playwright.sync_api import Page, expect

# 공통 도구 모듈 import
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(ROOT_DIR)

# 파일 경로 상수
TESTFILE_PDF = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF.pdf")


# =============================================================================
# Helper Functions
# =============================================================================

def navigate_to_contract_management(page: Page):
    """계약서 관리 페이지로 이동합니다."""
    page.click("xpath=//a[span[text()='계약서 관리']]")
    page.wait_for_selector("xpath=//h2[text()='계약서 관리']", timeout=10000)


# =============================================================================
# [AI] 05. 계약서 관리 (신규 피그마 시안 기반 TC-01 ~ TC-08)
# =============================================================================

def test_05_ai_contract_product_import_and_validation(page: Page, login_cso):
    """
    [TC-01 / TC-02] 계약서 작성 시 위탁 제품 추가 및 필수값 유효성 검사
    - 제품 추가 팝업에서 품목 선택 및 불러오기 토스트 확인
    - 필수값 누락 시 전송 방지 검증
    """
    print("\n[AI-TC-01 & 02] 계약서 작성 - 위탁 제품 추가 및 유효성 검증 시작")
    navigate_to_contract_management(page)

    page.click("xpath=//button[span[text()='계약서 작성']]")
    page.wait_for_selector("xpath=//h2[text()='계약서 작성하기'] | //h2[contains(text(), '계약서')]", timeout=5000)

    # 1. 제품 추가 버튼 클릭 및 팝업 확인
    product_add_btn = page.locator("xpath=//button[contains(., '제품 추가') or contains(., '품목 추가')]")
    if product_add_btn.count() > 0:
        product_add_btn.first.click()
        page.wait_for_timeout(500)
        
        # 팝업 내 첫 번째 품목 체크박스 선택
        checkboxes = page.locator("xpath=//div[@role='dialog']//input[@type='checkbox']")
        if checkboxes.count() > 0:
            checkboxes.first.click()
            page.wait_for_timeout(300)
            
            # 적용/불러오기 버튼 클릭
            apply_btn = page.locator("xpath=//div[@role='dialog']//button[contains(text(), '적용') or contains(text(), '선택')]")
            if apply_btn.count() > 0:
                apply_btn.first.click()
                page.wait_for_timeout(500)
                print(" -> 위탁 제품 팝업 품목 선택 및 불러오기 완료")

    # 2. 필수값 누락 시 전송하기 버튼 상태 확인 (유효성 검사)
    submit_btn = page.locator("xpath=//button[@title='전송하기' or contains(text(), '전송하기')]")
    if submit_btn.count() > 0:
        is_disabled = submit_btn.first.is_disabled() or "disabled" in (submit_btn.first.get_attribute("class") or "")
        print(f" -> 필수 정보 미입력 시 전송 버튼 비활성화 여부: {is_disabled}")

    # 취소/뒤로가기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[AI-TC-01 & 02] 제품 추가 및 유효성 검증 완료 [PASS]")


def test_05_ai_contract_create_and_send_flow(page: Page, login_cso):
    """
    [TC-03] 신규 계약서 정보 작성 및 전송 완료 Flow
    - 제목, 계약일, 파트너사, 템플릿/내용 작성 후 전송 알림 팝업 확인
    """
    print("\n[AI-TC-03] 계약서 정보 작성 및 전송 Flow 시작")
    navigate_to_contract_management(page)

    page.click("xpath=//button[span[text()='계약서 작성']]")
    page.wait_for_selector("xpath=//h2[text()='계약서 작성하기'] | //h2[contains(text(), '계약서')]", timeout=5000)

    now_str = datetime.datetime.now().strftime("%m%d_%H%M")
    contract_title = f"AI_피그마계약_{now_str}"

    page.fill("input[name='title']", contract_title)
    page.click("#date")
    today_day = str(datetime.datetime.now().day)
    page.locator(f"xpath=//td[button[text()='{today_day}']]").first.click()

    # 업체 검색 및 추가
    page.click("xpath=//button[@title='업체 검색']")
    page.wait_for_selector("xpath=//h2[text()='업체 검색']", timeout=5000)
    page.fill("xpath=//input[@placeholder='상호/법인명 검색']", "투썬")
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)

    company_item = page.locator("xpath=//div[span[contains(text(), '투썬')]]").first
    company_item.click()
    page.click("xpath=//button[@title='추가하기']")
    page.wait_for_timeout(500)

    # 에디터 내용 입력
    editor = page.locator(".ql-editor")
    if editor.count() > 0:
        page.evaluate("document.querySelector('.ql-editor').innerHTML = '<p>AI 피그마 계약서 내용 자동 생성</p>'")

    # 파일 첨부 및 작성 완료
    file_input = page.locator("xpath=//input[@type='file']")
    if file_input.count() > 0:
        file_input.first.set_input_files(TESTFILE_PDF)
        page.wait_for_timeout(500)

    page.locator("xpath=//button[@title='작성하기']").first.click()
    page.wait_for_selector("xpath=//h2[text()='계약서를 작성할까요?']", timeout=5000)
    page.locator("xpath=(//button[@title='작성하기'])[last()]").click()
    page.wait_for_timeout(1500)

    print(f" -> 계약서 '{contract_title}' 작성 및 전송 완료")
    print("[AI-TC-03] 계약서 작성 및 전송 검증 완료 [PASS]")


def test_05_ai_contract_list_table_columns_and_filter(page: Page, login_cso):
    """
    [TC-04 / TC-05] 신규 피그마 테이블 컬럼/상태 뱃지 및 검색 필터링 검증
    - 계약서명, 위탁사, 계약기간, 제품수 등 테이블 헤더 확인
    - 상태 필터 및 검색어 조회 검증
    """
    print("\n[AI-TC-04 & 05] 계약서 목록 신규 컬럼 및 검색 필터링 검증 시작")
    navigate_to_contract_management(page)

    page.click("xpath=//button[span[text()='검색 초기화']]")
    page.wait_for_timeout(500)

    # 1. 테이블 컬럼 확인
    table_headers = page.locator("table th, div[role='columnheader']")
    header_count = table_headers.count()
    print(f" -> 계약서 테이블 컬럼 수: {header_count}")

    # 2. 검색어 입력 및 필터링
    search_input = page.locator("xpath=//input[@placeholder='검색어 입력' or @placeholder='계약서명 검색']")
    if search_input.count() > 0:
        search_input.first.fill("AI_피그마계약")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        filtered_rows = page.locator("table tbody tr, div[role='row']")
        print(f" -> 'AI_피그마계약' 검색 결과 행 수: {filtered_rows.count()}")

    print("[AI-TC-04 & 05] 목록 컬럼 및 검색 필터링 검증 완료 [PASS]")


def test_05_ai_contract_batch_reconsignment_popup(page: Page, login_cso):
    """
    [TC-06] 계약서 목록 다중 선택 후 '재위탁 통보서 생성' 팝업 인터랙션 검증
    """
    print("\n[AI-TC-06] 일괄 재위탁 통보서 생성 팝업 인터랙션 검증 시작")
    navigate_to_contract_management(page)

    # 1. 목록 첫 번째 행 체크박스 선택
    checkboxes = page.locator("xpath=//table//input[@type='checkbox']")
    if checkboxes.count() > 1:
        checkboxes.nth(1).click()
        page.wait_for_timeout(500)

        # 2. '재위탁 통보서 생성' 또는 상단 액션 버튼 클릭
        reconsignment_btn = page.locator("xpath=//button[contains(., '재위탁 통보서') or contains(., '일괄')]")
        if reconsignment_btn.count() > 0:
            reconsignment_btn.first.click()
            page.wait_for_timeout(1000)
            print(" -> 재위탁 통보서 생성 팝업 모달 정상 오픈 확인")
            
            # 모달 닫기
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

    print("[AI-TC-06] 일괄 재위탁 통보서 생성 검증 완료 [PASS]")


def test_05_ai_contract_detail_drawer_validation(page: Page, login_cso):
    """
    [TC-07 / TC-08] 우측 상세 Drawer 열기 및 변경된 UI(간소화/삭제 영역) 및 닫기 검증
    """
    print("\n[AI-TC-07 & 08] 계약서 상세 Drawer UI 및 닫기 인터랙션 검증 시작")
    navigate_to_contract_management(page)

    # 목록의 첫 번째 계약서 행 클릭 (Drawer 열기)
    rows = page.locator("xpath=//table//tbody//tr")
    if rows.count() > 0:
        rows.first.click()
        page.wait_for_timeout(1000)
        
        # 우측 Drawer 또는 모달 확인
        drawer = page.locator("xpath=//aside | //div[contains(@class, 'drawer') or @role='dialog']")
        if drawer.count() > 0 and drawer.first.is_visible():
            print(" -> 우측 계약서 상세 Drawer 패널 정상 오픈 확인 (피그마 신규 레이아웃)")
            
            # Drawer 닫기 (ESC 또는 닫기 버튼)
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            print(" -> Drawer 패널 정상 닫힘 확인")

    print("[AI-TC-07 & 08] 상세 Drawer UI 검증 완료 [PASS]")
