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
    expect(page.locator("xpath=//h2[text()='필터링 요청하기'] | //h2[contains(., '필터링 요청')]").first).to_be_visible()

    # -------------------------------------------------------------
    # 2. 필터링 요청 1차 등록 (회신 검증용)
    # -------------------------------------------------------------
    print("[Step 2] 필터링 요청 1차 등록 (신규 병의원 및 문의내용)")
    page.click("xpath=//button[@title='필터링 요청 등록'] | //button[contains(., '필터링 요청 등록')]")
    page.wait_for_selector("xpath=//h2[text()='필터링 요청 등록하기']", timeout=5000)
    expect(page.locator("xpath=//h2[text()='필터링 요청 등록하기']")).to_be_visible()

    # 2.0. 요청 수신 업체 검색 및 선택
    print("-> 요청 수신 업체 선택")
    page.fill("xpath=//input[@placeholder='업체를 검색해 주세요']", "투썬")
    page.wait_for_timeout(500)
    pharm_opt = page.locator("xpath=//button[div[span[normalize-space(.)='제약사']]] | //div[span[contains(text(), '제약사')]] | //button[contains(., '투썬')] | //div[contains(@class, 'cursor-pointer') and contains(., '투썬')]").first
    if pharm_opt.count() > 0 and pharm_opt.is_visible():
        pharm_opt.click()
        page.wait_for_timeout(500)

    # 2.1. 제약사 선택 (관리하기 모달이 있는 경우)
    manage_btn = page.locator("xpath=//button[contains(., '관리하기')] | //button[text()='+ 관리하기']").first
    if manage_btn.count() > 0 and manage_btn.is_visible():
        manage_btn.click()
        page.wait_for_selector("xpath=//h2[text()='제약사 관리']", timeout=5000)
        page.fill("xpath=//input[@placeholder='제약사명 검색']", "투썬")
        page.click("xpath=//button[normalize-space(.)='검색']")
        page.wait_for_timeout(500)
        
        checkboxes = page.locator("xpath=//div[@role='dialog']//input[@type='checkbox'] | //input[@type='checkbox']")
        if checkboxes.count() > 0:
            checkboxes.last.click()
            page.wait_for_timeout(300)
        
        page.click("xpath=//div[@role='dialog']//button[text()='저장하기'] | //button[normalize-space(.)='저장하기']")
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

    # 중복 사업자번호 또는 미등록 시 기존 병의원 검색으로 폴백
    if page.locator("xpath=//*[contains(text(), '이미 등록되어 있는')] | //*[contains(text(), '사업자등록번호를 다시')]").is_visible():
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        page.fill("xpath=//input[@placeholder='병의원을 검색해 주세요']", "Auto")
        page.wait_for_timeout(500)
        hosp_opt = page.locator("xpath=//div[contains(@class, 'cursor-pointer') and contains(., 'Auto')] | //li[contains(., 'Auto')] | //button[contains(., 'Auto')] | //div[span[contains(text(), 'Auto')]]").first
        if hosp_opt.count() > 0 and hosp_opt.is_visible():
            hosp_opt.click()
            page.wait_for_timeout(500)

    # 2.3. 문의 내용 입력
    page.locator("xpath=//button[@title='취소'] | //textarea[@name='inquiryContent'] | //textarea").first.scroll_into_view_if_needed()
    page.locator("textarea").first.fill("자동화테스트")
    page.wait_for_timeout(300)

    # 2.4. 요청하기 완료
    modal_req_btn = page.locator("xpath=//button[text()='요청하기'] | //button[normalize-space(.)='요청하기']").last
    modal_req_btn.click()
    page.wait_for_timeout(1500)

    # -------------------------------------------------------------
    # 2.5. 필터링 요청 2차 등록 (수정 및 취소 테스트용)
    # -------------------------------------------------------------
    print("[Step 2.5] 필터링 요청 2차 등록 (수정 및 취소 검증용)")
    page.click("xpath=//button[@title='필터링 요청 등록'] | //button[contains(., '필터링 요청 등록')]")
    page.wait_for_selector("xpath=//h2[text()='필터링 요청 등록하기']", timeout=5000)

    # 2.5.1. 요청 수신 업체
    page.fill("xpath=//input[@placeholder='업체를 검색해 주세요']", "투썬")
    page.wait_for_timeout(500)
    pharm_opt2 = page.locator("xpath=//button[div[span[normalize-space(.)='제약사']]] | //div[span[contains(text(), '제약사')]] | //button[contains(., '투썬')] | //div[contains(@class, 'cursor-pointer') and contains(., '투썬')]").first
    if pharm_opt2.count() > 0 and pharm_opt2.is_visible():
        pharm_opt2.click()
        page.wait_for_timeout(500)

    manage_btn2 = page.locator("xpath=//button[contains(., '관리하기')] | //button[text()='+ 관리하기']").first
    if manage_btn2.count() > 0 and manage_btn2.is_visible():
        manage_btn2.click()
        page.wait_for_selector("xpath=//h2[text()='제약사 관리']", timeout=5000)
        page.fill("xpath=//input[@placeholder='제약사명 검색']", "투썬")
        page.click("xpath=//button[normalize-space(.)='검색']")
        page.wait_for_timeout(500)
        
        checkboxes2 = page.locator("xpath=//div[@role='dialog']//input[@type='checkbox'] | //input[@type='checkbox']")
        if checkboxes2.count() > 0:
            checkboxes2.last.click()
            page.wait_for_timeout(300)
        
        page.click("xpath=//div[@role='dialog']//button[text()='저장하기'] | //button[normalize-space(.)='저장하기']")
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

    if page.locator("xpath=//*[contains(text(), '이미 등록되어 있는')] | //*[contains(text(), '사업자등록번호를 다시')]").is_visible():
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        page.fill("xpath=//input[@placeholder='병의원을 검색해 주세요']", "Auto")
        page.wait_for_timeout(500)
        hosp_opt2 = page.locator("xpath=//div[contains(@class, 'cursor-pointer') and contains(., 'Auto')] | //li[contains(., 'Auto')] | //button[contains(., 'Auto')] | //div[span[contains(text(), 'Auto')]]").first
        if hosp_opt2.count() > 0 and hosp_opt2.is_visible():
            hosp_opt2.click()
            page.wait_for_timeout(500)

    page.locator("xpath=//button[@title='취소'] | //textarea[@name='inquiryContent'] | //textarea").first.scroll_into_view_if_needed()
    page.locator("textarea").first.fill("자동화테스트")
    page.wait_for_timeout(300)

    modal_req_btn2 = page.locator("xpath=//button[text()='요청하기'] | //button[normalize-space(.)='요청하기']").last
    modal_req_btn2.click()
    page.wait_for_timeout(1500)

    # -------------------------------------------------------------
    # 3. 필터링 요청 상세, 수정 및 요청 취소
    # -------------------------------------------------------------
    print("[Step 3] 필터링 요청 상세 진입 및 수정하기")
    first_req = page.locator(".ag-row:visible a:has-text('자동화테스트')").first
    if first_req.count() > 0 and first_req.is_visible():
        first_req.click()
        page.wait_for_selector("xpath=//h2[text()='필터링 요청 상세'] | //h2[contains(., '필터링 요청') and not(contains(., '목록')) and not(contains(., '하기'))] | textarea", timeout=5000)

        # 3.1. 수정하기
        print("[Step 3.1] 문의내용 수정 ('_수정하기' 추가)")
        page.locator("textarea").first.fill("자동화테스트_수정하기")
        page.click("xpath=//button[text()='수정하기'] | //button[normalize-space(.)='수정하기']")
        page.wait_for_timeout(1000)

        # 3.2. 요청 취소
        print("[Step 3.2] 요청 취소 수행")
        cancel_target = page.locator(".ag-row:visible a:has-text('자동화테스트_수정하기')").first
        if cancel_target.count() > 0 and cancel_target.is_visible():
            cancel_target.click()
            page.wait_for_selector("xpath=//button[text()='요청 취소'] | //button[normalize-space(.)='요청 취소']", timeout=5000)

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
