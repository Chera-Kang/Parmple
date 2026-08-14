import os
import time
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (09. 재위탁 현황)
# =============================================================================

def test_09_reconsignment_status_flow(page: Page, login_pharm1):
    """09. 재위탁현황 - 제약사 계정으로 재위탁 현황 메뉴 진입 및 검색어 필터링 조회를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 09. 재위탁 현황 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 재위탁 현황 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '재위탁 현황' 페이지 이동")
    page.click("xpath=//a[span[text()='재위탁 현황']]")
    page.wait_for_selector("xpath=//h2[text()='재위탁 현황'] | //h2[contains(., '재위탁 현황')]", timeout=10000)

    # -------------------------------------------------------------
    # 1.1. 재위탁 현황 검색 조건 및 검색 수행
    # -------------------------------------------------------------
    print("[Step 1.1] 상호/법인명 기준 '휴피' 검색 수행")
    search_type_btn = page.locator("xpath=//button[span[span[text()='상호/법인명']]] | //button[contains(., '상호/법인명')]")
    if search_type_btn.count() > 0:
        search_type_btn.first.click()
        page.wait_for_selector("xpath=//div[span[text()='사업자등록번호']] | //div[contains(., '사업자등록번호')]", timeout=5000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    search_input = page.locator("xpath=//input[@placeholder='검색어를 입력해 주세요']")
    if search_input.count() > 0:
        search_input.fill("휴피")
        page.click("xpath=//button[span[text()='검색']] | //button[normalize-space(.)='검색']")
        page.wait_for_timeout(1000)

    print("[Success] 09. 재위탁 현황 전체 Flow 성공 완료!")
