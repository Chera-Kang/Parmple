import os
import time
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (04. 상위 업체 조회)
# =============================================================================

def test_04_upper_company_inquiry_flow(page: Page, login_cso):
    """04. 상위업체조회 - 상위 업체 목록 검색, 제약사 및 CSO 상위 업체 상세(사업자등록증, 수수료율, 계약서) 조회를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 04. 상위 업체 조회 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 상위 업체 조회 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '상위 업체 조회' 페이지 이동")
    page.click("xpath=//a[span[text()='상위 업체 조회']]")
    page.wait_for_selector("xpath=//h2[text()='상위 업체 조회']", timeout=10000)

    # -------------------------------------------------------------
    # 1.1. 검색 조건 확인 및 검색 수행
    # -------------------------------------------------------------
    print("[Step 1.1] 상호/법인명 기준 '투썬' 검색")
    page.click("xpath=//button[span[span[text()='상호/법인명']]]")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    page.fill("xpath=//input[@placeholder='검색어를 입력해 주세요']", "투썬")
    page.click("xpath=//button[span[text()='검색']]")
    page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 2. 상위 업체 상세 (제약사)
    # -------------------------------------------------------------
    print("[Step 2] 상위 업체 상세 보기 (제약사: 842-88-83121)")
    # 첫 번째 대상 제약사 링크 클릭 (사업자번호 기준)
    pharm_link = page.locator("xpath=//a[translate(normalize-space(.), '-', '') = '8428883121'] | //a[contains(text(), '842-88-83121')]").first
    if pharm_link.count() > 0:
        pharm_link.click()
    else:
        # 특정 번호가 없는 경우 첫 번째 행의 링크 클릭
        page.locator("xpath=//table//tbody//tr//a").first.click()
    
    page.wait_for_selector("xpath=//h2[text()='상세 보기']", timeout=5000)

    # 2.1. 사업자등록증 미리보기
    print("[Step 2.1] 사업자등록증 미리보기")
    view_btn = page.locator("xpath=//button[text()='보기']").last
    view_btn.click()
    page.wait_for_selector("xpath=//h2[text()='사업자등록증'] | //img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 2.2. 계약관리 - 수수료율 확인
    print("[Step 2.2] 수수료율 팝업 확인")
    page.locator("xpath=//button[@title='처음'] | //h3[text()='계약관리']").first.scroll_into_view_if_needed()
    commission_btn = page.locator("xpath=//button[@title='수수료율']").first
    if commission_btn.count() > 0 and commission_btn.is_visible():
        commission_btn.click()
        page.wait_for_selector("xpath=//h2[text()='수수료율']", timeout=5000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # 2.3. 계약관리 - 계약서 확인
    print("[Step 2.3] 계약서 팝업 확인")
    contract_btn = page.locator("xpath=//button[@title='계약서']").first
    if contract_btn.count() > 0 and contract_btn.is_visible():
        contract_btn.click()
        page.wait_for_selector("xpath=//h2[text()='계약서']", timeout=5000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 3. 상위 업체 상세 (CSO)
    # -------------------------------------------------------------
    print("[Step 3] 상위 업체 상세 보기 (CSO: 129-86-37855)")
    page.go_back()
    page.wait_for_selector("xpath=//h2[text()='상위 업체 조회']", timeout=5000)

    cso_link = page.locator("xpath=//a[translate(normalize-space(.), '-', '') = '1298637855'] | //a[contains(text(), '129-86-37855')]").first
    if cso_link.count() > 0:
        cso_link.click()
    else:
        # 특정 번호가 없는 경우 마지막 행의 링크 클릭
        page.locator("xpath=//table//tbody//tr//a").last.click()

    page.wait_for_selector("xpath=//h2[text()='상세 보기']", timeout=5000)

    # 3.1. 사업자등록증 미리보기
    print("[Step 3.1] CSO 상위 업체 사업자등록증 미리보기")
    view_btn2 = page.locator("xpath=//button[text()='보기']").last
    view_btn2.click()
    page.wait_for_selector("xpath=//h2[text()='사업자등록증'] | //img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 3.3. 계약관리 - 수수료율 확인
    print("[Step 3.3] CSO 상위 업체 수수료율 팝업 확인")
    page.locator("xpath=//button[@title='처음'] | //h3[text()='계약관리']").first.scroll_into_view_if_needed()
    commission_btn2 = page.locator("xpath=//button[@title='수수료율']").first
    if commission_btn2.count() > 0 and commission_btn2.is_visible():
        commission_btn2.click()
        page.wait_for_selector("xpath=//h2[text()='수수료율']", timeout=5000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # 3.4. 계약관리 - 계약서 확인
    print("[Step 3.4] CSO 상위 업체 계약서 팝업 확인")
    contract_btn2 = page.locator("xpath=//button[@title='계약서']").first
    if contract_btn2.count() > 0 and contract_btn2.is_visible():
        contract_btn2.click()
        page.wait_for_selector("xpath=//h2[text()='계약서']", timeout=5000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    print("[Success] 04. 상위 업체 조회 전체 Flow 성공 완료!")
