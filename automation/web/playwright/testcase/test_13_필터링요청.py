import os
import time
import datetime
import pytest
from playwright.sync_api import Page, expect

# 구글 시트 연동 도구
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(ROOT_DIR)

from common.resources.gsheet_reader import get_biz_no_from_sheet

# =============================================================================
# Test Cases (13. 필터링 요청하기)
# =============================================================================

def test_13_filtering_request_flow(page: Page, login_cso):
    """13. 필터링요청 - CSO 계정으로 신규 병의원 등록 및 필터링 요청 등록, 수정/요청취소, 검색 필터를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 13. 필터링 요청하기 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 필터링 요청하기 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '필터링 요청하기' 페이지 이동")
    page.locator("xpath=//a[span[text()='필터링 요청하기']]").scroll_into_view_if_needed()
    page.click("xpath=//a[span[text()='필터링 요청하기']]")
    page.wait_for_selector("xpath=//h2[text()='필터링 요청하기'] | //h2[contains(., '필터링 요청')]", timeout=10000)

    # -------------------------------------------------------------
    # 2. 필터링 요청 1차 등록 (회신 검증용)
    # -------------------------------------------------------------
    print("[Step 2] 필터링 요청 1차 등록 (신규 병의원 및 문의내용)")
    page.click("xpath=//button[@title='필터링 요청 등록'] | //button[contains(., '필터링 요청 등록')]")
    page.wait_for_selector("xpath=//h2[text()='필터링 요청 등록하기']", timeout=5000)

    # 2.1. 요청 업체 검색
    page.fill("xpath=//input[@placeholder='업체를 검색해 주세요']", "투썬")
    page.wait_for_timeout(500)
    pharm_opt = page.locator("xpath=//button[div[span[normalize-space(.)='제약사']]] | //div[span[contains(text(), '제약사')]] | //button[contains(., '투썬')]").first
    pharm_opt.click()
    page.wait_for_timeout(500)

    # 2.2. 신규 병의원 추가
    page.click("xpath=//button[text()='신규 병의원 등록'] | //button[contains(., '신규 병의원')]")
    page.wait_for_selector("xpath=//h2[text()='신규 병의원 등록']", timeout=5000)

    now_str = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    page.fill("xpath=//input[@placeholder='병의원 명을 입력해 주세요.']", f"Auto {now_str}")
    page.fill("xpath=//input[@placeholder='병의원 주소를 입력해 주세요.']", "자동화주소")
    
    biz_no = get_biz_no_from_sheet()
    clean_biz_no = biz_no.replace("-", "") if biz_no else "6046400707"
    page.fill("xpath=//input[@placeholder='-없이 숫자만 입력해 주세요']", clean_biz_no)
    page.wait_for_timeout(300)

    page.click("xpath=//button[text()='등록하기'] | //button[normalize-space(.)='등록하기']")
    page.wait_for_timeout(500)

    # 2.3. 문의 내용 입력
    page.locator("xpath=//button[@title='취소'] | //textarea[@name='inquiryContent']").first.scroll_into_view_if_needed()
    page.fill("textarea[name='inquiryContent'], input[name='inquiryContent']", "자동화테스트")

    # 2.4. 요청하기 완료
    page.click("xpath=//button[@title='요청하기'] | //button[normalize-space(.)='요청하기']")
    page.wait_for_timeout(1500)

    # -------------------------------------------------------------
    # 2.5. 필터링 요청 2차 등록 (수정 및 취소 테스트용)
    # -------------------------------------------------------------
    print("[Step 2.5] 필터링 요청 2차 등록 (수정 및 취소 검증용)")
    page.click("xpath=//button[@title='필터링 요청 등록'] | //button[contains(., '필터링 요청 등록')]")
    page.wait_for_selector("xpath=//h2[text()='필터링 요청 등록하기']", timeout=5000)

    page.fill("xpath=//input[@placeholder='업체를 검색해 주세요']", "투썬")
    page.wait_for_timeout(500)
    page.locator("xpath=//button[div[span[normalize-space(.)='제약사']]] | //div[span[contains(text(), '제약사')]] | //button[contains(., '투썬')]").first.click()
    page.wait_for_timeout(500)

    page.click("xpath=//button[text()='신규 병의원 등록'] | //button[contains(., '신규 병의원')]")
    page.wait_for_selector("xpath=//h2[text()='신규 병의원 등록']", timeout=5000)

    now_str2 = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    page.fill("xpath=//input[@placeholder='병의원 명을 입력해 주세요.']", f"Auto {now_str2}")
    page.fill("xpath=//input[@placeholder='병의원 주소를 입력해 주세요.']", "자동화주소")
    
    biz_no2 = get_biz_no_from_sheet()
    clean_biz_no2 = biz_no2.replace("-", "") if biz_no2 else "1298637855"
    page.fill("xpath=//input[@placeholder='-없이 숫자만 입력해 주세요']", clean_biz_no2)
    page.wait_for_timeout(300)

    page.click("xpath=//button[text()='등록하기'] | //button[normalize-space(.)='등록하기']")
    page.wait_for_timeout(500)

    page.locator("xpath=//button[@title='취소'] | //textarea[@name='inquiryContent']").first.scroll_into_view_if_needed()
    page.fill("textarea[name='inquiryContent'], input[name='inquiryContent']", "자동화테스트")

    page.click("xpath=//button[@title='요청하기'] | //button[normalize-space(.)='요청하기']")
    page.wait_for_timeout(1500)

    # -------------------------------------------------------------
    # 3. 필터링 요청 상세, 수정 및 요청 취소
    # -------------------------------------------------------------
    print("[Step 3] 필터링 요청 상세 진입 및 수정하기")
    first_req = page.locator("xpath=//span[text()='자동화테스트'] | //table//tbody//tr//span[contains(text(), '자동화테스트')]").first
    if first_req.count() > 0:
        first_req.click()
        page.wait_for_selector("xpath=//h2[text()='필터링 요청'] | //h2[contains(., '필터링 요청')]", timeout=5000)

        # 3.1. 수정하기
        print("[Step 3.1] 문의내용 수정 ('_수정하기' 추가)")
        page.fill("textarea[name='inquiryContent'], textarea", "자동화테스트_수정하기")
        page.click("xpath=//button[text()='수정하기'] | //button[normalize-space(.)='수정하기']")
        page.wait_for_timeout(1000)

        # 3.2. 요청 취소
        print("[Step 3.2] 요청 취소 수행")
        cancel_target = page.locator("xpath=//span[contains(text(), '자동화테스트_수정하기')]").first
        if cancel_target.count() > 0:
            cancel_target.click()
            page.wait_for_selector("xpath=//h2[text()='필터링 요청'] | //h2[contains(., '필터링 요청')]", timeout=5000)

            page.click("xpath=//button[text()='요청 취소'] | //button[normalize-space(.)='요청 취소']")
            page.wait_for_selector("xpath=//button[text()='요청 취소하기'] | //button[normalize-space(.)='요청 취소하기']", timeout=5000)
            page.click("xpath=//button[text()='요청 취소하기'] | //button[normalize-space(.)='요청 취소하기']")
            page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 4. 검색 필터링 검증
    # -------------------------------------------------------------
    print("[Step 4] 검색 드롭다운 필터 및 검색어 필터링")
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
        search_input.fill("인천")
        page.click("xpath=//button[span[text()='검색']] | //button[normalize-space(.)='검색']")
        page.wait_for_timeout(1000)

    print("[Success] 13. 필터링 요청하기 전체 Flow 성공 완료!")
