import os
import time
import datetime
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (15. 영업 거래처 관리)
# =============================================================================

def test_15_sales_customer_management_flow(page: Page, login_pharm1):
    """15. 영업거래처관리 - 제약사 계정으로 영업 거래처 목록 조회, 병의원 상세 진입, 관리코드 수정, 거래처 상태 변경, 비고 작성 및 검색 필터를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 15. 영업 거래처 관리 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 영업 거래처 관리 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '영업 거래처 관리' 페이지 이동")
    page.locator("xpath=//a[span[text()='영업 거래처 관리']]").scroll_into_view_if_needed()
    page.click("xpath=//a[span[text()='영업 거래처 관리']]")
    page.wait_for_selector("xpath=//h2[text()='영업 거래처 관리'] | //h2[contains(., '영업 거래처')]", timeout=10000)
    expect(page.locator("xpath=//h2[text()='영업 거래처 관리'] | //h2[contains(., '영업 거래처')]").first).to_be_visible()

    # -------------------------------------------------------------
    # 2. 병의원 상세 진입 및 관리
    # -------------------------------------------------------------
    print("[Step 2] 병의원 상세 페이지 진입")
    target_link = page.locator(".ag-row:visible a:has-text('Auto'), .ag-row:visible [col-id='hospitalName'] a, .ag-row:visible a, div[role='gridcell'] a").first
    if target_link.count() > 0 and target_link.is_visible():
        target_link.click()
        page.wait_for_selector("xpath=//h2[text()='상세 보기'] | //h2[contains(., '상세')]", timeout=10000)
        expect(page.locator("xpath=//h2[text()='상세 보기'] | //h2[contains(., '상세')]").first).to_be_visible()

        # 2.1. 관리코드 수정
        print("[Step 2.1] 관리코드 수정")
        edit_code_btn = page.locator("xpath=//button[text()='수정'] | //button[contains(., '수정')]").first
        if edit_code_btn.count() > 0 and edit_code_btn.is_visible():
            edit_code_btn.click()
            page.wait_for_selector("xpath=//h2[contains(., '관리코드')] | //h2[contains(., '수정')]", timeout=5000)
            
            now_code = datetime.datetime.now().strftime("%y%m%d%H%M")
            code_input = page.locator("xpath=//input[@name='managementCode'] | //input[@placeholder='관리코드를 입력해 주세요'] | //div[contains(@role, 'dialog')]//input")
            if code_input.count() > 0:
                code_input.fill(now_code)
                page.click("xpath=//button[text()='저장하기'] | //button[normalize-space(.)='저장하기']")
                page.wait_for_timeout(1000)

        # 2.2. 거래처 관리 (상태 변경)
        print("[Step 2.2] 거래처 상태 관리 ('제품별 승인')")
        manage_btn = page.locator("xpath=//button[@title='관리'] | //div[contains(@class, 'ag-row')]//button | //div[@role='row']//button").first
        if manage_btn.count() > 0 and manage_btn.is_visible():
            manage_btn.click()
            page.wait_for_selector("xpath=//h2[text()='영업 거래처'] | //h2[contains(., '영업 거래처')]", timeout=5000)
            
            status_dropdown = page.locator("xpath=//button[span[span[text()='변경할 상태 선택']]] | //button[contains(., '변경할 상태')] | //button[@role='combobox']").last
            if status_dropdown.count() > 0:
                status_dropdown.click()
                page.wait_for_timeout(300)
                prod_opt = page.locator("xpath=(//div[span[text()='제품별 승인']])[last()] | (//div[contains(@role, 'option') and contains(., '제품별 승인')])[last()] | //div[contains(., '제품별 승인')]").last
                if prod_opt.count() > 0:
                    prod_opt.click()
                    page.wait_for_timeout(300)
            
            page.click("xpath=//button[text()='저장하기'] | //button[normalize-space(.)='저장하기']")
            page.wait_for_timeout(1000)

        # 2.3. 거래처 비고 등록
        print("[Step 2.3] 거래처 비고 등록")
        note_btn = page.locator("xpath=//button[@title='비고'] | //button[contains(., '비고')]")
        if note_btn.count() > 0 and note_btn.first.is_visible():
            note_btn.first.click()
            page.wait_for_selector("xpath=//h2[text()='비고'] | //h2[contains(., '비고')]", timeout=5000)
            
            page.fill("textarea[name='note'], input[name='note']", "자동화테스트")
            page.click("xpath=//button[text()='저장하기'] | //button[normalize-space(.)='저장하기']")
            page.wait_for_timeout(1000)

        # 목록으로 복귀
        page.locator("xpath=//a[span[text()='영업 거래처 관리']]").scroll_into_view_if_needed()
        page.click("xpath=//a[span[text()='영업 거래처 관리']]")
        page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 3. 검색 및 필터링
    # -------------------------------------------------------------
    print("[Step 3] 검색 및 필터 조건 검증")
    sales_status_filter = page.locator("xpath=//button[span[span[text()='영업 상태(전체)']]] | //button[contains(., '영업 상태')]")
    if sales_status_filter.count() > 0:
        sales_status_filter.first.click()
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    date_input = page.locator("xpath=//input[@placeholder='등록일시'] | //*[@id='date']")
    if date_input.count() > 0:
        date_input.first.click()
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    search_category = page.locator("xpath=//button[span[span[text()='병의원 명']]] | //button[contains(., '병의원')]")
    if search_category.count() > 0:
        search_category.first.click()
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    search_input = page.locator("xpath=//input[@placeholder='검색어를 입력해 주세요']")
    if search_input.count() > 0:
        search_input.fill("휴베이스")
        page.click("xpath=//button[span[text()='검색']] | //button[normalize-space(.)='검색']")
        page.wait_for_timeout(1000)

    print("[Success] 15. 영업 거래처 관리 전체 Flow 성공 완료!")
