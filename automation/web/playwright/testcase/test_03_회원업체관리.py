import os
import time
import random
import datetime
import pytest
from playwright.sync_api import Page, expect

# 공통 도구 모듈 import
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(ROOT_DIR)

from common.resources.gsheet_reader import get_biz_no_from_sheet

# 파일 경로 상수
BIZNO_FILE = os.path.join(ROOT_DIR, "common", "resources", "used_bizNo.txt")
TESTFILE_PDF = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF.pdf")
TESTFILE_PDF2 = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF_2.pdf")


# =============================================================================
# Helper Functions
# =============================================================================

def get_last_biz_number() -> str:
    """used_bizNo.txt 파일에서 마지막으로 사용된(가입된) 사업자번호를 조회합니다."""
    if not os.path.exists(BIZNO_FILE):
        raise FileNotFoundError(f"사업자번호 파일이 없습니다: {BIZNO_FILE}")
    with open(BIZNO_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        raise ValueError("used_bizNo.txt에 기록된 사업자번호가 없습니다.")
    return lines[-1]


# =============================================================================
# Test Cases (03. 회원 업체 관리)
# =============================================================================

def test_03_member_company_management_flow(page: Page, login_cso):
    """03. 회원업체관리 - 가입/미가입 업체 추가, 상세 정보/수료증/계약서/재위탁통보서 관리 및 검색 전체 Flow를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 03. 회원 업체 관리 전체 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. 회원 업체 관리 메인 화면 진입
    # -------------------------------------------------------------
    print("[Step 1] 회원 업체 관리 메인 화면 확인")
    page.wait_for_selector("xpath=//h2[contains(text(), '회원 업체 관리')]", timeout=10000)
    expect(page.locator("xpath=//h2[contains(text(), '회원 업체 관리')]")).to_be_visible()

    # -------------------------------------------------------------
    # 1.1. 가입된 업체 추가하기
    # -------------------------------------------------------------
    print("[Step 1.1] 가입된 업체 추가 (직전 가입 사업자번호 사용)")
    page.click("xpath=//button[normalize-space(.)='추가하기']")
    page.wait_for_selector("xpath=//h2[text()='회원 업체 추가']", timeout=5000)
    expect(page.locator("xpath=//h2[text()='회원 업체 추가']")).to_be_visible()

    last_biz_no = get_last_biz_number()
    print(f"-> 사용할 가입 업체 사업자번호: {last_biz_no}")
    page.fill("#bizNumber", last_biz_no)
    page.click("xpath=//button[text()='확인하기']")
    page.wait_for_selector("xpath=//h2[text()='회원 업체 추가']", timeout=5000)

    # 관리코드 및 담당자 정보 입력
    now_code = datetime.datetime.now().strftime("%m%d-%H%M")
    random_phone = f"010{random.randint(10000000, 99999999)}"

    page.fill("input[name='managementCode']", now_code)
    page.fill("input[name='managerName']", "자동화")
    page.fill("input[name='managerPhone']", random_phone)
    page.fill("input[name='managerEmail']", "auto@mation.com")

    # 추가하기 클릭 및 계약서 등록 확인 팝업 (이미 등록된 업체 팝업 포함)
    page.locator("xpath=//button[text()='추가하기']").last.click()
    page.wait_for_selector("xpath=//h2[text()='계약서를 등록할까요?'] | //h2[contains(text(), '이미 등록된')]", timeout=8000)
    
    if page.locator("xpath=//h2[contains(text(), '이미 등록된')]").is_visible():
        print("-> 이미 등록된 위탁 업체 알림 확인")
        page.click("xpath=//button[normalize-space(.)='확인']")
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
    else:
        page.click("xpath=//button[normalize-space(.)='나중에']")
        page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 2. 미가입 업체 추가하기
    # -------------------------------------------------------------
    print("[Step 2] 미가입 업체 추가 (Google Sheet에서 신규 사업자번호 추출)")
    page.click("xpath=//button[normalize-space(.)='추가하기']")
    page.wait_for_selector("xpath=//h2[text()='회원 업체 추가']", timeout=5000)

    biz_no = get_biz_no_from_sheet()
    if biz_no.startswith("ERROR") or biz_no == "NO_BIZ_NO":
        pytest.fail(f"사용 가능한 사업자번호를 가져오지 못했습니다: {biz_no}")
    
    clean_biz_no = biz_no.replace("-", "").strip()
    print(f"-> 사용할 미가입 업체 사업자번호: {biz_no} (정제: {clean_biz_no})")

    page.fill("#bizNumber", clean_biz_no)
    page.click("xpath=//button[text()='확인하기']")
    page.wait_for_selector("xpath=//h2[text()='회원 업체 추가']", timeout=5000)

    # 파일 첨부 (사업자등록증, CSO신고증)
    page.locator("xpath=//*[@id='bizRegCertFileUuid']//input").set_input_files(TESTFILE_PDF)
    page.wait_for_timeout(500)
    page.locator("xpath=//*[@id='salesCertFileUuid']//input").set_input_files(TESTFILE_PDF2)
    page.wait_for_timeout(500)

    # 관리코드 및 담당자 정보 입력
    page.fill("input[name='managementCode']", f"{now_code}.")
    page.fill("input[name='managerName']", "자동화")
    random_phone2 = f"010{random.randint(10000000, 99999999)}"
    page.fill("input[name='managerPhone']", random_phone2)
    page.fill("input[name='managerEmail']", "auto@mation.com")

    # 추가하기 클릭 및 완료 확인 팝업
    page.locator("xpath=//button[text()='추가하기']").last.click()
    page.wait_for_selector("xpath=//h2[text()='업체 등록 요청이 완료되었습니다']", timeout=5000)
    page.click("xpath=//button[normalize-space(.)='확인']")
    page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 3. 상세 Page (미가입 업체 - CSO 교육 수료증 등록)
    # -------------------------------------------------------------
    print("[Step 3] 미가입 업체 상세 보기 및 CSO 교육 수료증 등록")
    # 방금 추가한 미가입 업체 사업자번호 링크 클릭
    target_link = page.locator(f"xpath=//a[translate(normalize-space(.), '-', '') = '{clean_biz_no}']")
    target_link.wait_for(timeout=10000)
    target_link.click()
    page.wait_for_selector("xpath=//h2[text()='상세 보기']", timeout=5000)

    # CSO 교육 수료증 등록 모달 열기 (화면에 보이는 버튼 대상)
    reg_btn = page.locator("xpath=//tr[contains(@class, 'lg:table-row') and .//th[text()='CSO 교육 수료증']]//button[text()='등록'] | //button[text()='등록']").last
    reg_btn.wait_for(timeout=10000)
    reg_btn.click()
    page.wait_for_selector("xpath=//h2[text()='CSO 교육 수료증 등록하기']", timeout=5000)

    # 파일 첨부 및 날짜 선택, 발급번호 입력
    page.locator("xpath=//*[@id='fileUuid']//input").set_input_files(TESTFILE_PDF)
    page.wait_for_timeout(500)
    page.click("xpath=//div[span[text()='수료증 기재일']]")
    today_day = str(datetime.datetime.now().day)
    page.locator(f"xpath=//td[button[text()='{today_day}']]").first.click()

    doc_no = datetime.datetime.now().strftime("%Y-%m%d-%H%M%S")
    page.fill("xpath=//input[@placeholder='발급번호를 입력해 주세요']", doc_no)
    page.click("#isNoticeConfirmed")
    page.click("xpath=//button[text()='등록하기']")
    page.wait_for_timeout(1000)

    # 메인 목록으로 복귀
    page.go_back()
    page.wait_for_selector("xpath=//h2[contains(text(), '회원 업체 관리')]", timeout=5000)

    # -------------------------------------------------------------
    # 4. 상세 Page (가입 업체 - 정보 수정 & 계약/재위탁통보서 관리)
    # -------------------------------------------------------------
    print("[Step 4] 가입 업체 상세 보기 및 계약/재위탁통보서 관리")
    clean_last_biz_no = last_biz_no.replace("-", "").strip()
    page.click(f"xpath=//a[translate(normalize-space(.), '-', '') = '{clean_last_biz_no}']")
    page.wait_for_selector("xpath=//h2[text()='상세 보기']", timeout=5000)

    # 4.2. 관리코드 수정
    print("[Step 4.2] 관리코드 수정")
    page.locator("xpath=//button[text()='수정']").last.click()
    page.wait_for_selector("xpath=//h2[text()='관리 코드 수정']", timeout=5000)
    page.fill("input[name='managementCode']", f"{now_code}F")
    page.click("xpath=//button[normalize-space(.)='저장하기']")
    page.wait_for_timeout(1000)

    # 4.3. 사업자등록증 / 영업신고증 보기
    print("[Step 4.3] 사업자등록증 및 영업신고증 미리보기")
    view_buttons = page.locator("xpath=//button[text()='보기']")
    if view_buttons.count() >= 2:
        view_buttons.nth(view_buttons.count() - 2).click()
        page.wait_for_selector("xpath=//h2[text()='사업자등록증'] | //img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]", timeout=5000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        view_buttons.last.click()
        page.wait_for_selector("xpath=//h2[text()='영업신고증'] | //img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]", timeout=5000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # 4.4. 담당자 정보 수정
    print("[Step 4.4] 담당자 정보 수정")
    page.locator("xpath=//button[@title='수정']").first.click()
    page.wait_for_selector("xpath=//h2[text()='담당자 정보 수정']", timeout=5000)

    page.fill("input[name='name']", "자동화테스트")
    page.fill("input[name='phone']", f"010{random.randint(10000000, 99999999)}")
    page.fill("input[name='email']", "automation@test.com")
    page.click("xpath=//button[normalize-space(.)='저장하기']")
    page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 5. 계약 관리 (계약 추가, 수수료율/계약서 확인, 삭제)
    # -------------------------------------------------------------
    print("[Step 5] 계약 추가 및 관리")
    page.locator("xpath=//h3[text()='계약관리']").scroll_into_view_if_needed()

    # 5.1. 계약 1 추가
    page.click("xpath=//button[normalize-space(.)='계약 추가']")
    page.wait_for_selector("xpath=//h2[text()='계약 추가']", timeout=5000)

    page.fill("input[name='contractTitle']", f"자동화테스트 {now_code}")
    page.locator("xpath=//*[@id='contractFile']//input").set_input_files(TESTFILE_PDF)
    page.click("xpath=//input[@id='direct'] | //label[contains(., '직접 입력')]")
    page.wait_for_timeout(300)
    page.fill("xpath=//textarea[@placeholder='수수료율을 입력해 주세요'] | //input[@name='commissionText'] | //textarea[@name='commissionText']", f"자동화테스트 {now_code}")
    page.click("xpath=//button[normalize-space(.)='추가하기']")
    page.wait_for_selector("xpath=//h2[text()='재위탁 통보서를 작성할까요?']", timeout=5000)
    page.click("xpath=//button[normalize-space(.)='나중에']")
    page.wait_for_timeout(1000)

    # 5.2. 계약 2 추가
    page.click("xpath=//button[normalize-space(.)='계약 추가']")
    page.wait_for_selector("xpath=//h2[text()='계약 추가']", timeout=5000)

    page.fill("input[name='contractTitle']", f"자동화테스트 {now_code} 2")
    page.locator("xpath=//*[@id='contractFile']//input").set_input_files(TESTFILE_PDF)
    page.click("xpath=//button[normalize-space(.)='추가하기']")
    page.wait_for_selector("xpath=//h2[text()='재위탁 통보서를 작성할까요?']", timeout=5000)
    page.click("xpath=//button[normalize-space(.)='나중에']")
    page.wait_for_timeout(1000)

    # 5.5. 수수료율 확인
    page.locator("xpath=//button[@title='수수료율']").first.click()
    page.wait_for_selector("xpath=//h2[text()='수수료율']", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 5.6. 계약서 확인
    page.locator("xpath=//button[@title='계약서']").first.click()
    page.wait_for_selector("xpath=//h2[text()='계약서']", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 5.7. 계약 삭제
    page.locator("xpath=//button[@title='삭제']").first.click()
    page.wait_for_selector("xpath=//h2[text()='삭제할까요?']", timeout=5000)
    page.click("xpath=//button[normalize-space(.)='삭제하기']")
    page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 6. 재위탁통보서 작성
    # -------------------------------------------------------------
    print("[Step 6] 재위탁통보서 작성 및 제약사(투썬) 추가")
    page.locator("xpath=//button[@title='재위탁 통보서']").first.click()
    page.wait_for_selector("xpath=//h2[text()='재위탁 통보서']", timeout=5000)
    page.click("xpath=//button[text()='통보서 작성하기']")
    page.wait_for_selector("xpath=//h2[text()='재위탁 통보서 작성하기']", timeout=5000)

    page.fill("input[name='reason']", "automation test")
    page.fill("input[name='note']", "automation test")

    # 제약사 추가하기 모달
    page.locator("xpath=//button[text()='추가하기']").last.click()
    page.wait_for_selector("xpath=//h2[text()='제약사 추가하기']", timeout=5000)

    page.fill("xpath=//input[@placeholder='제약사명 검색']", "투썬")
    page.click("xpath=//button[@title='검색']")
    page.wait_for_timeout(500)

    # '투썬제약' 행 체크박스 선택
    page.locator("xpath=//div[@role='row' and contains(., '투썬')]//div[contains(@class, 'ag-selection-checkbox')]").first.click()
    page.locator("xpath=//button[text()='추가하기']").last.click()
    page.wait_for_timeout(500)

    # 통보서 작성 완료
    page.click("xpath=//button[text()='작성하기']")
    page.wait_for_selector("xpath=//h2[text()='재위탁 통보서를 작성할까요?']", timeout=5000)
    page.locator("xpath=//button[text()='작성하기']").last.click()
    page.wait_for_timeout(1000)

    # 메인 목록으로 복귀
    page.click("xpath=//a[span[text()='회원 업체 관리']]")
    page.wait_for_selector("xpath=//h2[contains(text(), '회원 업체 관리')]", timeout=5000)

    # -------------------------------------------------------------
    # 7. 검색 필터 검증
    # -------------------------------------------------------------
    print("[Step 7] 회원 업체 목록 검색 및 필터링 검증")
    # 구분 (등록) 필터 선택
    page.click("xpath=//button[span[span[contains(text(), '구분')]]]")
    page.wait_for_selector("xpath=//div[span[text()='등록']]", timeout=5000)
    page.click("xpath=//div[span[text()='등록']]")
    page.wait_for_timeout(500)

    # 영업 상태 드롭다운 열기 및 닫기
    page.click("xpath=//button[span[span[contains(text(), '영업 상태')]]]")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    # 계약 상태 드롭다운 열기 및 닫기
    page.click("xpath=//button[span[span[contains(text(), '계약 상태')]]]")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    # 검색 구분 (관리코드) 선택 후 오늘 날짜 검색
    page.click("xpath=//button[span[span[text()='상호/법인명']] | span[span[contains(text(), '관리코드')]]]")
    page.wait_for_selector("xpath=//div[span[text()='관리코드']]", timeout=5000)
    page.locator("xpath=//div[span[text()='관리코드']]").last.click()
    page.wait_for_timeout(300)

    today_monthday = datetime.datetime.now().strftime("%m%d")
    page.fill("xpath=//input[@placeholder='검색어를 입력해 주세요']", today_monthday)
    page.click("xpath=//button[span[text()='검색']]")
    page.wait_for_timeout(1000)

    print("[Success] 03. 회원 업체 관리 전체 Flow 성공 완료!")
