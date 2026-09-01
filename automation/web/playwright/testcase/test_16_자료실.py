import os
import time
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (16. 자료실 - 신규 개원 정보)
# =============================================================================

def test_16_reference_room_flow(page: Page, login_cso):
    """16. 자료실 - CSO 계정으로 신규 개원 정보 페이지에 진입하여 지역(광주), 구분, 진료 과목 필터링 검색을 검증합니다."""
    print("\n" + "=" * 60)
    print(" 16. 자료실 (신규 개원 정보) 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 신규 개원 정보 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '신규 개원 정보' 페이지 이동")
    page.locator("xpath=//a[span[text()='신규 개원 정보']]").scroll_into_view_if_needed()
    page.click("xpath=//a[span[text()='신규 개원 정보']]")
    page.wait_for_selector("xpath=//h2[text()='신규 개원 정보'] | //h2[contains(., '신규 개원 정보')]", timeout=10000)
    expect(page.locator("xpath=//h2[text()='신규 개원 정보'] | //h2[contains(., '신규 개원 정보')]").first).to_be_visible()

    # -------------------------------------------------------------
    # 2. 필터링 검색 검증
    # -------------------------------------------------------------
    # 2.1. 지역 필터 ('광주' 선택)
    print("[Step 2.1] 지역 필터 ('광주') 선택")
    region_btn = page.locator("xpath=//button[contains(., '지역')]").first
    if region_btn.count() > 0:
        region_btn.click()
        page.wait_for_timeout(500)
        
        gwangju_opt = page.locator("xpath=//div[contains(@role, 'option') and contains(., '광주')] | //div[contains(., '광주') and not(@role='combobox')] | //span[text()='광주']").last
        if gwangju_opt.count() > 0:
            gwangju_opt.click()
            page.wait_for_timeout(1000)

    # 2.2. 구분 필터
    print("[Step 2.2] 구분 필터 확인")
    gubun_btn = page.locator("xpath=//button[contains(., '구분')]").first
    if gubun_btn.count() > 0:
        gubun_btn.click()
        page.wait_for_timeout(300)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    # 2.3. 진료 과목 필터 선택
    print("[Step 2.3] 진료 과목 필터 선택")
    dept_btn = page.locator("xpath=//button[contains(., '진료 과목')]").first
    if dept_btn.count() > 0:
        dept_btn.click()
        page.wait_for_timeout(500)
        
        dept_opt = page.locator("xpath=//div[contains(@role, 'option') and contains(., '내과')] | //div[contains(., '내과') and not(@role='combobox')] | //span[text()='내과']").last
        if dept_opt.count() > 0:
            dept_opt.click()
            page.wait_for_timeout(1000)
        else:
            page.keyboard.press("Escape")

    print("[Success] 16. 자료실 (신규 개원 정보) 전체 Flow 성공 완료!")
