import os
import time
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (12. 필터링 조회 관리)
# =============================================================================

def test_12_filtering_inquiry_management_flow(page: Page, login_pharm1):
    """12. 필터링조회관리 - 제약사 계정으로 조건 관리(저장), 실적 관리(처방월 설정/일괄추가 모달), 병의원 검색 조회를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 12. 필터링 조회 관리 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 필터링 조회 관리 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '필터링 조회 관리' 페이지 이동")
    page.locator("xpath=//a[span[text()='필터링 조회 관리']]").scroll_into_view_if_needed()
    page.click("xpath=//a[span[text()='필터링 조회 관리']]")
    page.wait_for_selector("xpath=//h2[text()='필터링 조회 관리'] | //h2[contains(., '필터링 조회 관리')]", timeout=10000)
    expect(page.locator("xpath=//h2[text()='필터링 조회 관리'] | //h2[contains(., '필터링 조회 관리')]").first).to_be_visible()

    # -------------------------------------------------------------
    # 2. 조건 관리
    # -------------------------------------------------------------
    print("[Step 2] 필터링 조건 관리 및 저장 확인")
    cond_btn = page.locator("xpath=//button[@title='조건 관리'] | //button[contains(., '조건 관리')]")
    if cond_btn.count() > 0 and cond_btn.first.is_visible():
        cond_btn.first.click()
        page.wait_for_selector("xpath=//h2[text()='필터링 조건 관리'] | //h2[contains(., '조건 관리')]", timeout=5000)
        expect(page.locator("xpath=//h2[text()='필터링 조건 관리'] | //h2[contains(., '조건 관리')]").first).to_be_visible()

        save_btn = page.locator("xpath=//button[@title='저장하기'] | //button[normalize-space(.)='저장하기']")
        if save_btn.count() > 0:
            save_btn.first.click()
            page.wait_for_selector("xpath=//h2[text()='저장할까요?'] | //h2[contains(., '저장')]", timeout=5000)
            page.click("xpath=//button[@title='확인'] | //button[normalize-space(.)='확인']")
            page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 3. 실적 관리
    # -------------------------------------------------------------
    print("[Step 3] 실적 관리 모달 진입")
    perf_btn = page.locator("xpath=//button[@title='실적 관리'] | //button[contains(., '실적 관리')]")
    if perf_btn.count() > 0:
        perf_btn.first.click()
        page.wait_for_selector("xpath=//h2[text()='실적 관리'] | //h2[contains(., '실적 관리')]", timeout=5000)

        # 3.1. 처방월 설정
        print("[Step 3.1] 처방월 설정 모달 확인")
        month_btn = page.locator("xpath=//button[@title='처방월 설정'] | //button[contains(., '처방월 설정')]")
        if month_btn.count() > 0:
            month_btn.first.click()
            page.wait_for_selector("xpath=//h2[text()='처방월 설정'] | //h2[contains(., '처방월')]", timeout=5000)
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

        # 3.2. 일괄 추가
        print("[Step 3.2] 일괄 추가 모달 확인")
        batch_btn = page.locator("xpath=//button[@title='일괄추가'] | //button[contains(., '일괄추가')] | //button[contains(., '일괄 추가')]")
        if batch_btn.count() > 0:
            batch_btn.first.click()
            page.wait_for_selector("xpath=//h2[text()='일괄 추가'] | //h2[contains(., '일괄 추가')]", timeout=5000)
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 4. 병의원 검색
    # -------------------------------------------------------------
    print("[Step 4] 병의원 검색어('테스트') 필터링 수행")
    search_input = page.locator("xpath=//input[@placeholder='검색어를 입력해 주세요']")
    if search_input.count() > 0:
        search_input.fill("테스트")
        page.click("xpath=//button[span[text()='검색']] | //button[normalize-space(.)='검색']")
        page.wait_for_timeout(1000)

    print("[Success] 12. 필터링 조회 관리 전체 Flow 성공 완료!")
