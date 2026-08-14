import os
import time
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (06. 받은 계약서)
# =============================================================================

def test_06_received_contract_flow(page: Page, login_cso3):
    """06. 받은계약서 - 수신된 계약서 확인 및 전자서명(약관 동의 및 서명 완료) 전체 Flow를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 06. 받은 계약서 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 받은 계약서 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '받은 계약서' 페이지 이동")
    page.click("xpath=//a[span[text()='받은 계약서']]")
    page.wait_for_selector("xpath=//h2[text()='받은 계약서']", timeout=10000)

    # -------------------------------------------------------------
    # 1.1. 계약서 미리보기 확인
    # -------------------------------------------------------------
    print("[Step 1.1] 수신된 계약서 미리보기 확인")
    contract_btn = page.locator("xpath=//button[@title='계약서']")
    if contract_btn.count() > 0:
        contract_btn.first.click()
        page.wait_for_selector("xpath=//h2[text()='계약서'] | //div[contains(@class, 'react-pdf__Document')]", timeout=5000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 2. 서명하기 Flow
    # -------------------------------------------------------------
    print("[Step 2] 계약서 서명하기 모달 진입")
    sign_open_btn = page.locator("xpath=//button[@title='서명하기']")
    if sign_open_btn.count() > 0:
        sign_open_btn.first.click()
        page.wait_for_selector("xpath=//h2[text()='계약서']", timeout=5000)

        # 계약서 확인 팝업 내 노출된 서명하기 버튼 클릭
        page.locator("button:visible:has-text('서명하기')").last.click()
        page.wait_for_selector("xpath=//h2[text()='서명하기']", timeout=5000)

        # 2.1. 전자계약 이용약관 전체 동의
        print("[Step 2.1] 전자계약 이용약관 동의")
        arrow_btn = page.locator("xpath=//button[i[contains(@class, 'ri-arrow-down-s-line')]] | //button[contains(@class, 'accordion')]")
        if arrow_btn.count() > 0:
            arrow_btn.first.click()
        page.click("#termsAll")

        # 2.2. 전자계약 서명 완료
        print("[Step 2.2] 전자계약 서명 완료 처리")
        page.evaluate("""
            var btns = document.querySelectorAll("button[title='서명하기'][type='submit']");
            if(btns.length > 0) btns[btns.length - 1].click();
            else {
                var submitBtns = document.querySelectorAll("button[type='submit']");
                if(submitBtns.length > 0) submitBtns[submitBtns.length - 1].click();
            }
        """)
        
        page.wait_for_selector("xpath=//h2[text()='계약서에 서명하였습니다'] | //h2[contains(text(), '서명')]", timeout=10000)
        page.locator("button:visible:has-text('확인')").last.click()
        page.wait_for_timeout(1000)
    else:
        print("-> 대기 중인 서명 대상 계약서가 없습니다.")

    print("[Success] 06. 받은 계약서 전체 Flow 성공 완료!")
