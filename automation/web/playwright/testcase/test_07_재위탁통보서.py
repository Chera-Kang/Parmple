import os
import time
import datetime
import pytest
from playwright.sync_api import Page, expect

# =============================================================================
# Test Cases (07. 재위탁 통보서)
# =============================================================================

def test_07_reconsignment_notice_flow(page: Page, login_cso):
    """07. 재위탁통보서 - 작성하기(제약사/사유/업체선택), 삭제/수정, 첨부파일(계약서/수수료율/수료증) 확인 및 전송 전체 Flow를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 07. 재위탁 통보서 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 재위탁 통보서 관리 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '재위탁 통보서 관리' 페이지 이동")
    page.click("xpath=//a[span[text()='재위탁 통보서 관리']]")
    page.wait_for_selector("xpath=//h2[text()='재위탁 통보서 관리'] | //h2[contains(., '재위탁 통보서')]", timeout=10000)

    # -------------------------------------------------------------
    # 1.1. 재위탁통보서 작성하기 (첫 번째 통보서 생성)
    # -------------------------------------------------------------
    print("[Step 1.1] 재위탁 통보서 작성하기 진입")
    page.click("xpath=//button[@title='작성하기'] | //button[contains(., '작성하기')]")
    page.wait_for_selector("xpath=//h2[text()='재위탁 통보서 작성하기']", timeout=5000)

    # 1.2. 제약사 선택
    print("[Step 1.2] 제약사('투썬') 검색 및 선택")
    page.fill("xpath=//input[@placeholder='제약사 명 검색']", "투썬")
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)

    # 1.3. 재위탁 사유 및 기타 입력
    print("[Step 1.3] 재위탁 사유 및 비고 입력")
    page.fill("input[name='reason']", "automation test reason")
    page.fill("input[name='note']", "automation test note")

    # 1.4. 통보서 기재일 확인
    page.locator("xpath=//button[@title='추가하기'] | //button[@id='date']").first.scroll_into_view_if_needed()
    page.click("#date")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    # 1.6. 재위탁 업체 추가
    print("[Step 1.6] 재위탁 업체 모달에서 업체 추가 및 삭제")
    page.click("xpath=//button[@title='추가하기']")
    page.wait_for_selector("xpath=//h2[text()='재위탁 업체 추가하기']", timeout=5000)

    # ag-grid 행 또는 체크박스 영역 클릭
    rows = page.locator("xpath=//div[contains(@class, 'ag-center-cols-container')]//div[contains(@class, 'ag-row')] | //div[contains(@class, 'ag-row-level-0')]")
    count = min(rows.count(), 3)
    for i in range(count):
        checkbox_elem = rows.nth(i).locator(".ag-selection-checkbox, [role='checkbox'], div.ag-cell-first-right-pinned, div.ag-cell").first
        if checkbox_elem.count() > 0:
            checkbox_elem.click()
        else:
            rows.nth(i).click()
        page.wait_for_timeout(300)

    # 모달 내 추가하기 버튼 클릭
    page.locator("xpath=(//button[@title='추가하기'])[last()] | (//button[normalize-space(.)='추가하기'])[last()]").click()
    page.wait_for_timeout(1000)

    # 추가한 업체 1건 삭제
    delete_item_btn = page.locator("xpath=//button[@title='삭제'] | //button[contains(., '삭제')]")
    if delete_item_btn.count() > 0:
        delete_item_btn.first.click()
        page.wait_for_timeout(300)

    # 1.7. 재위탁통보서 최종 작성하기
    print("[Step 1.7] 재위탁 통보서 작성 완료")
    page.locator("xpath=//button[@title='작성하기'] | //button[normalize-space(.)='작성하기']").first.click()
    page.wait_for_selector("xpath=//h2[text()='재위탁 통보서를 작성할까요?']", timeout=5000)
    page.locator("xpath=(//button[@title='작성하기'])[last()] | (//button[normalize-space(.)='작성하기'])[last()]").click()
    page.wait_for_timeout(1500)

    # -------------------------------------------------------------
    # 2. 재위탁통보서 삭제 및 수정
    # -------------------------------------------------------------
    print("[Step 2] 작성된 재위탁 통보서 상세 열기")
    notice_btn = page.locator("xpath=(//button[@title='재위탁통보서'])[1] | (//button[contains(@title, '통보서')])[1]")
    if notice_btn.count() > 0:
        notice_btn.click()
        page.wait_for_selector("xpath=//h2[text()='재위탁 통보서']", timeout=5000)

        # 2.2. 수정하기 (사유 및 비고 수정)
        print("[Step 2.2] 재위탁 통보서 정보 수정")
        now_time = datetime.datetime.now().strftime("%m%d-%H%M")
        page.fill("input[name='reason']", f"자동화_{now_time}")

        page.locator("xpath=//div[text()='(서명 또는 인)'] | //input[@name='note']").first.scroll_into_view_if_needed()
        page.fill("input[name='note']", f"자동화_{now_time}")

        page.click("xpath=//button[text()='수정하기'] | //button[@title='수정하기']")
        page.wait_for_selector("xpath=//h2[text()='수정 완료'] | //h2[contains(., '완료')]", timeout=5000)
        page.locator("xpath=(//button[@title='확인'])[last()] | (//button[text()='확인'])[last()]").click()
        page.wait_for_timeout(500)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 3. 첨부파일 확인
    # -------------------------------------------------------------
    print("[Step 3] 첨부파일 팝업 확인 (계약서, 수수료율, 수료증)")
    file_btn = page.locator("xpath=(//button[@title='파일'])[1] | (//button[contains(@title, '파일')])[1]")
    if file_btn.count() > 0:
        file_btn.click()
        page.wait_for_selector("xpath=//h2[text()='파일']", timeout=5000)

        # 3.2. 수수료율 탭
        fee_tab = page.locator("xpath=//button[normalize-space(.)='수수료율']")
        if fee_tab.count() > 0:
            fee_tab.click()
            page.wait_for_timeout(500)

        # 3.3. 수료증 탭
        cert_tab = page.locator("xpath=//button[normalize-space(.)='수료증']")
        if cert_tab.count() > 0:
            cert_tab.click()
            page.wait_for_timeout(500)

        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 4. 재위탁 통보서 전송
    # -------------------------------------------------------------
    print("[Step 4] 재위탁 통보서 전송 수행")
    rows_to_send = page.locator("xpath=//div[contains(@class, 'ag-center-cols-container')]//div[contains(@class, 'ag-row')] | (//table//tbody//tr)")
    if rows_to_send.count() > 0:
        checkbox_send = rows_to_send.first.locator(".ag-selection-checkbox, input[type='checkbox'], [role='checkbox'], div.ag-cell").first
        if checkbox_send.count() > 0:
            checkbox_send.click()
        else:
            rows_to_send.first.click()
        page.wait_for_timeout(300)

        page.click("xpath=//button[@title='전송하기'] | //button[normalize-space(.)='전송하기']")
        page.wait_for_selector("xpath=//h2[contains(text(), '통보서를 전송할까요?')]", timeout=5000)
        page.locator("xpath=(//button[@title='전송하기'])[last()] | (//button[normalize-space(.)='전송하기'])[last()]").click()
        page.wait_for_timeout(1500)

    print("[Success] 07. 재위탁 통보서 전체 Flow 성공 완료!")
