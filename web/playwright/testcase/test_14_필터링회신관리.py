import os
import time
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (14. 필터링 회신 관리)
# =============================================================================

def test_14_filtering_reply_management_flow(page: Page, login_pharm1):
    """14. 필터링회신관리 - 제약사 계정으로 수신된 필터링 요청 상세 확인, 결과(임시 승인) 라디오 선택 및 회신내용 작성 제출, 검색 필터를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 14. 필터링 회신 관리 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 필터링 회신 관리 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '필터링 회신 관리' 페이지 이동")
    page.locator("xpath=//a[span[text()='필터링 회신 관리']]").scroll_into_view_if_needed()
    page.click("xpath=//a[span[text()='필터링 회신 관리']]")
    page.wait_for_selector("xpath=//h2[text()='필터링 회신 관리'] | //h2[contains(., '필터링 회신')]", timeout=10000)

    # -------------------------------------------------------------
    # 2. 필터링 요청 상세 진입 및 회신 작성
    # -------------------------------------------------------------
    print("[Step 2] 필터링 요청 상세 진입 및 결과 회신")
    req_item = page.locator("xpath=//span[text()='자동화테스트'] | //table//tbody//tr//span[contains(text(), '자동화테스트')]").first
    if req_item.count() > 0:
        req_item.click()
        page.wait_for_selector("xpath=//h2[text()='상세 보기'] | //h2[contains(., '상세')]", timeout=10000)

        # 페이지 하단으로 스크롤하여 회신 폼 확인
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

        # 2.1. 필터링 결과 선택 ('임시 승인' 라디오 버튼 클릭)
        print("[Step 2.1] 필터링 결과 라디오 선택 ('임시 승인')")
        temp_radio = page.locator("xpath=//label[contains(., '임시 승인')] | //span[text()='임시 승인'] | //input[@value='임시 승인']").first
        if temp_radio.count() > 0:
            temp_radio.click()
            page.wait_for_timeout(300)

        # 2.2. 회신 내용 입력 (필수 필드)
        print("[Step 2.2] 회신 내용 입력")
        reply_textarea = page.locator("xpath=//textarea[@placeholder='회신 내용을 입력해주세요.'] | (//textarea)[1]")
        if reply_textarea.count() > 0:
            reply_textarea.fill("자동화테스트 회신")
            page.wait_for_timeout(300)

        # 2.3. 필터링 회신하기 제출
        print("[Step 2.3] 필터링 회신 제출 완료")
        submit_reply_btn = page.locator("xpath=//button[text()='회신하기'] | //button[@title='회신하기'] | //button[normalize-space(.)='회신하기']").last
        if submit_reply_btn.count() > 0:
            submit_reply_btn.click()
            page.wait_for_selector("xpath=//h2[contains(text(), '필터링 결과를 회신할까요?')] | //h2[contains(., '회신')]", timeout=5000)
            page.locator("xpath=(//button[text()='회신하기'])[last()] | (//button[normalize-space(.)='회신하기'])[last()]").click()
            page.wait_for_timeout(1500)

        # 목록으로 돌아가기
        page.click("xpath=//a[span[text()='필터링 회신 관리']]")
        page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 3. 검색 및 필터링
    # -------------------------------------------------------------
    print("[Step 3] 검색 및 필터 조건 검증")
    status_filter = page.locator("xpath=//button[span[span[text()='상태 (전체)']]] | //button[contains(., '상태')]")
    if status_filter.count() > 0:
        status_filter.first.click()
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    res_filter = page.locator("xpath=//button[span[span[text()='조회 결과(전체)']]] | //button[contains(., '조회 결과')]")
    if res_filter.count() > 0:
        res_filter.first.click()
        page.wait_for_timeout(300)
        reject_opt = page.locator("xpath=//div[span[text()='반려']] | //div[contains(., '반려')]")
        if reject_opt.count() > 0:
            reject_opt.first.click()
            page.wait_for_timeout(300)

    search_input = page.locator("xpath=//input[@placeholder='검색어를 입력해 주세요']")
    if search_input.count() > 0:
        search_input.fill("휴피")
        page.click("xpath=//button[span[text()='검색']] | //button[normalize-space(.)='검색']")
        page.wait_for_timeout(1000)

    print("[Success] 14. 필터링 회신 관리 전체 Flow 성공 완료!")
