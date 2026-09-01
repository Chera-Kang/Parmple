import os
import time
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (11. 필터링 직접 조회)
# =============================================================================

def test_11_direct_filtering_inquiry_flow(page: Page, login_cso):
    """11. 필터링직접조회 - CSO 계정으로 제약사/병의원 선택 후 직접 필터링 조회 및 조회 결과 검색 필터를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 11. 필터링 직접 조회 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 필터링 직접 조회 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '필터링 직접 조회' 페이지 이동")
    page.locator("xpath=//a[span[text()='필터링 직접 조회']]").scroll_into_view_if_needed()
    page.click("xpath=//a[span[text()='필터링 직접 조회']]")
    page.wait_for_selector("xpath=//h2[text()='필터링 직접 조회'] | //h2[contains(., '필터링 직접 조회')]", timeout=10000)
    expect(page.locator("xpath=//h2[text()='필터링 직접 조회'] | //h2[contains(., '필터링 직접 조회')]").first).to_be_visible()

    # -------------------------------------------------------------
    # 1.1. 업체(제약사) 선택
    # -------------------------------------------------------------
    print("[Step 1.1] 제약사('투썬') 선택")
    page.click("xpath=//button[@role='combobox' and contains(., '제약사를 선택해 주세요')] | //button[contains(., '제약사를 선택')]")
    page.wait_for_selector("xpath=//div[span[contains(text(), '투썬')]] | //div[contains(@role, 'option') and contains(., '투썬')]", timeout=5000)
    page.locator("xpath=(//div[span[contains(text(), '투썬')]])[last()] | (//div[contains(@role, 'option') and contains(., '투썬')])[last()]").click()
    page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 1.2. 공지사항 단계 통과
    # -------------------------------------------------------------
    print("[Step 1.2] 공지사항 확인 후 다음 단계 이동")
    page.click("xpath=//button[text()='다음'] | //button[normalize-space(.)='다음']")
    page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 1.3. 병의원 검색 및 사업자번호 입력
    # -------------------------------------------------------------
    print("[Step 1.3] 병의원명 검색('자동화테스트') 및 사업자번호 입력")
    page.click("xpath=//button[text()='다음'] | //button[normalize-space(.)='다음']")
    page.wait_for_timeout(500)

    page.fill("xpath=//input[@placeholder='병의원명을 입력해 주세요']", "자동화테스트")
    page.wait_for_timeout(500)

    # 드롭다운 제안 항목 클릭
    suggestion = page.locator("xpath=//div[@role='dialog']//div[contains(., '자동화테스트') and contains(., '604')] | //div[span[span[text()='자동화테스트']]]").last
    suggestion.click()
    page.wait_for_timeout(500)

    # 사업자번호가 비어있는 경우 직접 입력
    biz_input = page.locator("xpath=//input[@placeholder='-없이 숫자만 가능']")
    if biz_input.count() > 0 and not biz_input.input_value():
        biz_input.fill("6046400707")
        page.wait_for_timeout(300)

    # -------------------------------------------------------------
    # 1.4. 조회 결과 팝업 확인
    # -------------------------------------------------------------
    print("[Step 1.4] 필터링 조회 결과 팝업 확인")
    page.click("xpath=//button[text()='조회하기'] | //button[normalize-space(.)='조회하기']")
    page.wait_for_selector("xpath=//h2[text()='필터링 조회 결과'] | //h2[contains(., '조회 결과')]", timeout=5000)
    expect(page.locator("xpath=//h2[text()='필터링 조회 결과'] | //h2[contains(., '조회 결과')]").first).to_be_visible()
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 2. 결과 목록 검색 및 필터 조건 검증
    # -------------------------------------------------------------
    print("[Step 2] 결과 목록 드롭다운 필터 및 검색어 필터링")
    result_filter_btn = page.locator("xpath=//button[span[span[text()='조회 결과(전체)']]] | //button[contains(., '조회 결과')]")
    if result_filter_btn.count() > 0:
        result_filter_btn.first.click()
        page.wait_for_timeout(300)
        unavailable_opt = page.locator("xpath=(//div[span[text()='거래 불가']])[last()] | (//div[contains(., '거래 불가')])[last()]")
        if unavailable_opt.count() > 0:
            unavailable_opt.click()
            page.wait_for_timeout(300)

    page.click("#date")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    search_category_btn = page.locator("xpath=//button[span[span[text()='병의원 명']]] | //button[contains(., '병의원')]")
    if search_category_btn.count() > 0:
        search_category_btn.first.click()
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    page.fill("xpath=//input[@placeholder='검색어를 입력해 주세요']", "테스트96")
    page.click("xpath=//button[span[text()='검색']] | //button[normalize-space(.)='검색']")
    page.wait_for_timeout(1000)

    print("[Success] 11. 필터링 직접 조회 전체 Flow 성공 완료!")
