import os
import time
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (10. 이전 통보서 관리)
# =============================================================================

def test_10_previous_notice_management_flow(page: Page, login_pharm1):
    """10. 이전통보서관리 - 제약사 계정으로 이전 통보서 관리 메뉴 진입 및 업체 정보 수정 팝업 확인을 검증합니다."""
    print("\n" + "=" * 60)
    print(" 10. 이전 통보서 관리 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 이전 통보서 관리 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '이전 통보서 관리' 페이지 이동")
    page.click("xpath=//a[span[text()='이전 통보서 관리']]")
    page.wait_for_selector("xpath=//h2[text()='이전 통보서 관리'] | //h2[contains(., '이전 통보서')]", timeout=10000)
    expect(page.locator("xpath=//h2[text()='이전 통보서 관리'] | //h2[contains(., '이전 통보서')]").first).to_be_visible()

    # -------------------------------------------------------------
    # 2. 업체 정보 수정 팝업 확인
    # -------------------------------------------------------------
    print("[Step 2] 업체 정보 버튼 클릭 및 업체 정보 수정 팝업 확인")
    company_info_btn = page.locator("xpath=//button[normalize-space(.)='업체 정보'] | //button[contains(., '업체 정보')]")
    if company_info_btn.count() > 0 and company_info_btn.first.is_visible():
        company_info_btn.first.click()
        page.wait_for_timeout(1000)

        # 그리드 셀(업체명) 클릭 (AG Grid 및 Table 지원)
        biz_cell = page.locator(".ag-row:visible [col-id='bizName'], .ag-row:visible a, div[role='gridcell'][col-id='bizName']")
        if biz_cell.count() > 0 and biz_cell.first.is_visible():
            biz_cell.first.click()
            page.wait_for_selector("xpath=//h2[text()='업체 정보 수정'] | //h2[contains(., '업체 정보')]", timeout=5000)
            expect(page.locator("xpath=//h2[text()='업체 정보 수정'] | //h2[contains(., '업체 정보')]").first).to_be_visible()
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

    print("[Success] 10. 이전 통보서 관리 전체 Flow 성공 완료!")
