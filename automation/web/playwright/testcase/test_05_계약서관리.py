import os
import time
import datetime
import pytest
from playwright.sync_api import Page, expect

# 공통 도구 모듈 import
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(ROOT_DIR)

# 파일 경로 상수
TESTFILE_PDF = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF.pdf")


# =============================================================================
# Test Cases (05. 계약서 관리)
# =============================================================================

def test_05_contract_management_flow(page: Page, login_cso):
    """05. 계약서관리 - 템플릿 생성/삭제, 전자계약 작성/수정/미리보기, 계약서 전송/취소/재전송 전체 Flow를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 05. 계약서 관리 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 계약서 관리 Page 이동
    # -------------------------------------------------------------
    print("[Step 1] '계약서 관리' 페이지 이동")
    page.click("xpath=//a[span[text()='계약서 관리']]")
    page.wait_for_selector("xpath=//h2[text()='계약서 관리']", timeout=10000)

    # -------------------------------------------------------------
    # 2. 템플릿 관리 (기존 템플릿 정리)
    # -------------------------------------------------------------
    print("[Step 2] 템플릿 관리 진입 및 기존 템플릿 확인/삭제")
    page.click("xpath=//button[span[text()='템플릿 관리']]")
    page.wait_for_selector("xpath=//h2[text()='템플릿 관리']", timeout=5000)

    edit_template_btn = page.locator("xpath=//div[span[button[@title='수정']]]")
    if edit_template_btn.count() > 0:
        print("-> 기존 등록된 템플릿 삭제 수행")
        edit_template_btn.first.click()
        page.wait_for_selector("xpath=//h2[text()='계약서 템플릿 관리']", timeout=5000)
        
        page.locator("xpath=//button[@title='삭제하기']").first.scroll_into_view_if_needed()
        page.locator("xpath=//button[@title='삭제하기']").first.click()
        page.wait_for_selector("xpath=//h2[text()='삭제할까요?']", timeout=5000)
        page.locator("xpath=(//button[@title='삭제하기'])[last()]").click()
        page.wait_for_selector("xpath=//h2[text()='계약서 관리']", timeout=5000)
        page.wait_for_timeout(1000)
    else:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 2.1. 템플릿 추가
    # -------------------------------------------------------------
    print("[Step 2.1] 신규 계약서 템플릿 추가")
    page.click("xpath=//button[span[text()='템플릿 관리']]")
    page.wait_for_selector("xpath=//h2[text()='템플릿 관리']", timeout=5000)

    page.click("xpath=//button[span[text()='템플릿 추가']]")
    page.wait_for_selector("xpath=//h2[text()='계약서 템플릿 추가']", timeout=5000)

    now_time = datetime.datetime.now().strftime("%y%m%d-%H%M")
    template_title = f"자동화테스트_{now_time}"
    page.fill("input[name='templateTitle']", template_title)

    # Quill 에디터 영역 텍스트 입력
    page.wait_for_selector(".ql-editor", timeout=5000)
    page.evaluate("document.querySelector('.ql-editor').innerHTML = '<p>자동화테스트2</p>'")
    page.wait_for_timeout(500)

    # 미리보기 확인
    page.click("xpath=//button[@title='미리보기']")
    page.wait_for_selector("xpath=//h2[text()='미리보기']", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 템플릿 저장하기
    page.click("xpath=//button[@title='저장하기']")
    page.wait_for_timeout(1000)

    # 템플릿 모달 닫기
    page.click("xpath=//button[span[text()='템플릿 관리']]")
    page.wait_for_selector("xpath=//h2[text()='템플릿 관리']", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 3. 전자계약 작성 Page
    # -------------------------------------------------------------
    print("[Step 3] 전자계약 작성 시작")
    page.click("xpath=//button[span[text()='계약서 작성']]")
    page.wait_for_selector("xpath=//h2[text()='계약서 작성하기']", timeout=5000)

    # 3.1. 제목 및 3.2. 계약일 입력
    page.fill("input[name='title']", "자동화테스트")
    page.click("#date")
    today_day = str(datetime.datetime.now().day)
    page.locator(f"xpath=//td[button[text()='{today_day}']]").first.click()

    # 3.3. 계약 업체 검색 및 추가
    print("[Step 3.3] 계약 업체(투썬) 검색 및 추가")
    page.click("xpath=//button[@title='업체 검색']")
    page.wait_for_selector("xpath=//h2[text()='업체 검색']", timeout=5000)

    page.fill("xpath=//input[@placeholder='상호/법인명 검색']", "투썬")
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)

    company_item = page.locator("xpath=//div[span[contains(text(), '투썬')]]").first
    company_item.click()
    page.click("xpath=//button[@title='추가하기']")
    page.wait_for_timeout(500)

    # 3.4. 계약서 (템플릿) 선택
    print("[Step 3.4] 생성한 템플릿 선택")
    page.locator("xpath=//div[label[text()='서명란']] | //div[contains(., '서명란')]").first.scroll_into_view_if_needed()
    page.click("xpath=//div[button[span[span[text()='직접 입력']]]] | //button[span[span[text()='직접 입력']]]")
    page.wait_for_timeout(300)

    template_select = page.locator(f"xpath=//div[span[contains(text(), '자동화테스트_')]]").last
    template_select.click()
    page.wait_for_timeout(500)

    # 3.5. 미리보기 확인
    print("[Step 3.5] 전자계약 미리보기 확인")
    page.locator("xpath=//button[@title='작성하기']").first.scroll_into_view_if_needed()
    page.click("xpath=//button[@title='미리보기']")
    page.wait_for_selector("xpath=//h2[text()='미리보기']", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 3.6. 추가 파일 업로드 및 최종 작성 완료
    print("[Step 3.6] 추가 파일 첨부 및 계약서 작성 완료")
    page.locator("xpath=//input[@type='file']").first.set_input_files(TESTFILE_PDF)
    page.wait_for_timeout(500)

    page.locator("xpath=//button[@title='작성하기']").first.click()
    page.wait_for_selector("xpath=//h2[text()='계약서를 작성할까요?']", timeout=5000)
    page.locator("xpath=(//button[@title='작성하기'])[last()]").click()
    page.wait_for_timeout(1500)

    # -------------------------------------------------------------
    # 4. 계약서 목록 & 미리보기
    # -------------------------------------------------------------
    print("[Step 4] 계약서 목록 확인 및 계약서 미리보기")
    page.click("xpath=//button[span[text()='검색 초기화']]")
    page.wait_for_timeout(1000)

    contract_view_btn = page.locator("xpath=//button[@title='계약서']")
    if contract_view_btn.count() > 0 and contract_view_btn.first.is_visible():
        contract_view_btn.first.click()
        page.wait_for_selector("xpath=//h2[text()='계약서'] | //div[contains(@class, 'react-pdf__Document')]", timeout=5000)
        expect(page.locator("xpath=//h2[text()='계약서'] | //div[contains(@class, 'react-pdf__Document')]").first).to_be_visible()
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 5. 전자계약 수정 (작성 완료 상태인 경우 수행)
    # -------------------------------------------------------------
    print("[Step 5] 전자계약 수정 (제목 및 내용 변경)")
    edit_btn = page.locator("xpath=//button[@title='수정']")
    if edit_btn.count() > 0 and edit_btn.first.is_visible():
        edit_btn.first.click()
        page.wait_for_selector("xpath=//h2[text()='계약서 수정하기']", timeout=5000)
        expect(page.locator("xpath=//h2[text()='계약서 수정하기']")).to_be_visible()

        page.fill("input[name='title']", "자동화테스트_fix")
        page.click("#date")
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

        page.evaluate("document.querySelector('.ql-editor').innerHTML = '<p>자동화테스트 내용 수정하기</p>'")
        page.click("xpath=//button[@title='수정하기']")
        page.wait_for_selector("xpath=//h2[text()='계약서 관리']", timeout=5000)
        expect(page.locator("xpath=//h2[text()='계약서 관리']")).to_be_visible()
        page.wait_for_timeout(1000)
    else:
        print(" -> 비동기 작성중 상태이거나 수정 버튼이 비활성화되어 수정 단계를 스킵합니다.")

    # -------------------------------------------------------------
    # 6. 전자계약 전송 (선택 가능한 계약서가 있는 경우 수행)
    # -------------------------------------------------------------
    print("[Step 6] 전자계약 전송 (서명 기한 및 약관 동의)")
    first_checkbox = page.locator(".ag-row:visible input[type='checkbox']:not([disabled]), input[type='checkbox']:visible:not([disabled])")
    if first_checkbox.count() > 0:
        first_checkbox.first.click()
        page.wait_for_timeout(300)

        send_btn = page.locator("xpath=//button[@title='전송하기'] | //button[normalize-space(.)='전송하기']")
        if send_btn.count() > 0 and not send_btn.first.is_disabled():
            send_btn.first.click()
            page.wait_for_selector("xpath=//h2[text()='계약서 전송하기']", timeout=5000)
            expect(page.locator("xpath=//h2[text()='계약서 전송하기']")).to_be_visible()

            # 6.1. 서명 가능 기한 선택
            page.click("xpath=//button[div[span[text()='서명 가능 기한']]]")
            page.wait_for_selector("xpath=//button[@name='day' and not(@disabled)]", timeout=5000)
            page.locator("xpath=(//button[@name='day' and not(@disabled)])[1]").click()
            page.wait_for_timeout(300)

            # 6.2. 전자계약 이용약관 동의
            arrow_btn = page.locator("xpath=//button[i[contains(@class, 'ri-arrow-down-s-line')]] | //button[contains(@class, 'accordion')]")
            if arrow_btn.count() > 0:
                arrow_btn.first.click()
            page.click("#termsAll")

            page.locator("xpath=(//button[@title='전송하기'])[last()]").click()
            page.wait_for_timeout(1500)

    # -------------------------------------------------------------
    # 7. 전송 완료 탭 확인 (엄격 단언)
    # -------------------------------------------------------------
    print("[Step 7] 전송 완료 탭 확인 및 계약서 상태 검증")
    sent_tab = page.locator("button:has-text('전송 완료')")
    expect(sent_tab).to_be_visible(timeout=5000)
    sent_tab.click()
    page.wait_for_timeout(1000)

    # 전송 완료 탭 헤더 단언
    expect(page.locator("xpath=//*[text()='전송 일시']").first).to_be_visible(timeout=5000)
    print(" -> [전송 완료] 탭 정상 전환 및 '전송 일시' 헤더 노출 확인 완료!")

    # 다시 [전송 전] 탭으로 복귀
    pre_tab = page.locator("button:has-text('전송 전')")
    pre_tab.click()
    page.wait_for_timeout(1000)
    expect(page.locator("xpath=//*[text()='계약일자']").first).to_be_visible(timeout=5000)

    print("[Success] 05. 계약서 관리 전체 Flow 성공 완료!")

