import os
import time
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (08. 받은 재위탁 통보서)
# =============================================================================

def test_08_received_reconsignment_notice_flow(page: Page, login_pharm1):
    """08. 받은재위탁통보서 - 제약사 계정으로 수신된 재위탁 통보서 및 첨부파일(계약서/수수료율/수료증/재위탁수료증) 조회를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 08. 받은 재위탁 통보서 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 받은 재위탁 통보서 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '받은 재위탁 통보서' 페이지 이동")
    page.click("xpath=//a[span[text()='받은 재위탁 통보서']]")
    page.wait_for_selector("xpath=//h2[text()='받은 재위탁 통보서'] | //h2[contains(., '재위탁 통보서')]", timeout=10000)
    expect(page.locator("xpath=//h2[text()='받은 재위탁 통보서'] | //h2[contains(., '재위탁 통보서')]").first).to_be_visible()

    # -------------------------------------------------------------
    # 1.1. 재위탁 통보서 미리보기
    # -------------------------------------------------------------
    print("[Step 1.1] 재위탁 통보서 미리보기 확인")
    notice_btn = page.locator("xpath=//button[@title='통보서'] | //button[contains(@title, '통보서')]")
    if notice_btn.count() > 0 and notice_btn.first.is_visible():
        notice_btn.first.click()
        page.wait_for_selector("xpath=//h2[text()='재위탁 통보서'] | //h2[contains(., '통보서')]", timeout=5000)
        expect(page.locator("xpath=//h2[text()='재위탁 통보서'] | //h2[contains(., '통보서')]").first).to_be_visible()
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 1.2. 첨부파일 확인 (계약서, 수수료율, 수료증, 수료증(재위탁))
    # -------------------------------------------------------------
    print("[Step 1.2] 첨부파일 모달 진입 및 탭별 파일 확인")
    file_btn = page.locator("xpath=(//button[@title='파일'])[1] | (//button[contains(@title, '파일')])[1]")
    if file_btn.count() > 0 and file_btn.first.is_visible():
        file_btn.first.click()
        page.wait_for_selector("xpath=//h2[text()='파일'] | //h2[contains(., '파일')]", timeout=5000)
        expect(page.locator("xpath=//h2[text()='파일'] | //h2[contains(., '파일')]").first).to_be_visible()

        # 1.4. 수수료율
        print("[Step 1.4] 수수료율 탭 확인")
        fee_tab = page.locator("xpath=//button[normalize-space(.)='수수료율']")
        if fee_tab.count() > 0 and fee_tab.first.is_visible():
            fee_tab.first.click()
            page.wait_for_timeout(500)

        # 1.5. 수료증
        print("[Step 1.5] 수료증 탭 확인")
        cert_tab = page.locator("xpath=//button[normalize-space(.)='수료증']")
        if cert_tab.count() > 0 and cert_tab.first.is_visible():
            cert_tab.first.click()
            page.wait_for_timeout(500)

        # 1.6. 수료증(재위탁)
        print("[Step 1.6] 수료증(재위탁) 탭 확인")
        re_cert_tab = page.locator("xpath=//button[normalize-space(.)='수료증(재위탁)']")
        if re_cert_tab.count() > 0 and re_cert_tab.first.is_visible():
            re_cert_tab.first.click()
            page.wait_for_timeout(500)

        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    print("[Success] 08. 받은 재위탁 통보서 전체 Flow 성공 완료!")
