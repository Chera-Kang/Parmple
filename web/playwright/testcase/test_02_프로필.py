import os
import time
import random
import datetime
import pytest
from playwright.sync_api import Page, expect

# 공통 도구 모듈 import
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(ROOT_DIR)

from common.resources.email_generator import generate_email

# 파일 경로 상수
TESTFILE_PDF = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF.pdf")
STAMP_IMG_DIR = os.path.join(ROOT_DIR, "common", "resources", "testfile", "img_number")


# =============================================================================
# Helper Functions
# =============================================================================

def get_random_stamp_image_path() -> str:
    """도장 업로드를 위한 랜덤 이미지(.png) 파일 경로를 반환합니다."""
    files = [f for f in os.listdir(STAMP_IMG_DIR) if f.endswith(".png")]
    if not files:
        raise FileNotFoundError(f"도장 이미지 폴더가 비어있습니다: {STAMP_IMG_DIR}")
    return os.path.join(STAMP_IMG_DIR, random.choice(files))


# =============================================================================
# Test Cases (02. 프로필 및 내 정보 관리)
# =============================================================================

def test_02_profile_full_management_flow(page: Page, login_cso, credentials):
    """02. 프로필 - 내 정보 조회, 계정 수정, 증빙 확인, 서브계정/수료증/도장 관리 및 로그아웃 전체 Flow를 검증합니다."""
    print("\n" + "=" * 60)
    print(" 02. 프로필 전체 관리 Flow 시작")
    print("=" * 60)

    # -------------------------------------------------------------
    # 2. 내 정보 Page 이동
    # -------------------------------------------------------------
    print("[Step 2] '내 정보' 페이지 이동")
    page.click("button[title='내 정보']")
    page.wait_for_selector("xpath=//h2[text()='내 정보']", timeout=5000)

    # -------------------------------------------------------------
    # 2.2. 비밀번호 변경
    # -------------------------------------------------------------
    print("[Step 2.2] 비밀번호 변경 수행")
    page.click("xpath=//button[span[text()='계정 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), '비밀번호 변경')]")
    page.wait_for_selector("xpath=//h2[text()='비밀번호 변경']", timeout=5000)

    pwd = credentials["password"]
    page.fill("input#password", pwd)
    page.fill("input#newPassword", pwd)
    page.fill("input#confirmNewPassword", pwd)
    page.click("xpath=//button[@title='변경하기']")

    page.wait_for_selector("xpath=//h2[text()='비밀번호가 변경되었습니다.']", timeout=5000)
    page.click("xpath=//button[@title='확인']")
    page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 2.3. 계정 정보 수정
    # -------------------------------------------------------------
    print("[Step 2.3] 계정 정보(이름, 휴대폰) 수정")
    page.click("xpath=//button[span[text()='계정 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), '계정 정보 수정')]")
    page.wait_for_selector("xpath=//h2[text()='계정 정보 수정']", timeout=5000)

    now_str = datetime.datetime.now().strftime("%m%d-%H%M")
    new_name = f"테스트_{now_str}"
    random_phone = f"010{random.randint(10000000, 99999999)}"

    page.fill("input[name='name']", new_name)
    page.fill("input[name='phone']", random_phone)
    page.click("xpath=//button[@title='수정하기']")
    page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 3. 사업자 정보 (사업자등록증 / CSO신고증 보기)
    # -------------------------------------------------------------
    print("[Step 3] 사업자등록증 및 CSO신고증 미리보기")
    page.locator("xpath=//img[@alt='도장이미지']").scroll_into_view_if_needed()
    
    # 3.1. 사업자등록증 보기
    page.locator("xpath=//button[text()='보기']").first.click()
    page.wait_for_selector("xpath=//img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]", timeout=10000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 3.2. 의약품 판촉영업 신고증 보기
    page.locator("xpath=(//button[text()='보기'])[last()]").click()
    page.wait_for_selector("xpath=//img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]", timeout=10000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 4. 업체 계정 관리 (서브 계정 삭제 & 생성)
    # -------------------------------------------------------------
    print("[Step 4] 업체 계정 관리 (계정 삭제 및 신규 계정 생성)")
    page.click("xpath=//button[span[text()='업체 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), '업체 계정 관리')]")
    page.wait_for_selector("xpath=//h2[text()='업체 계정 관리']", timeout=5000)

    # 4.2. 마지막 계정 삭제
    delete_buttons = page.locator("xpath=//button[@title='삭제']")
    if delete_buttons.count() > 0:
        delete_buttons.last.scroll_into_view_if_needed()
        delete_buttons.last.click()
        page.wait_for_selector("xpath=//h2[text()='삭제할까요?']", timeout=5000)
        page.click("xpath=//button[@title='확인']")
        page.wait_for_timeout(1000)

    # 4.3. 계정 생성
    page.click("xpath=//button[@title='계정 생성하기']")
    page.wait_for_selector("xpath=//h2[text()='계정 생성하기']", timeout=5000)

    sub_email = generate_email(prefix="subuser")
    random_phone = f"010{random.randint(10000000, 99999999)}"

    page.fill("input[name='email']", sub_email)
    page.fill("input[name='name']", "xptmxm")
    page.fill("input[name='phone']", random_phone)
    page.click("xpath=//button[text()='생성하기']")
    page.wait_for_timeout(1000)

    # 내 정보 메인으로 복귀
    page.click("button[title='내 정보']")
    page.wait_for_selector("xpath=//h2[text()='내 정보']", timeout=5000)

    # -------------------------------------------------------------
    # 5. CSO 교육 수료증 등록
    # -------------------------------------------------------------
    print("[Step 5] CSO 교육 수료증 첨부 및 등록")
    page.click("xpath=//button[span[text()='업체 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), 'CSO 교육 수료증 등록')]")
    page.wait_for_selector("xpath=//h2[text()='CSO 교육 수료증 등록하기']", timeout=5000)

    # 5.1. 수료증 첨부
    page.locator("xpath=//*[@id='fileUuid']//input").set_input_files(TESTFILE_PDF)
    page.wait_for_selector("xpath=//button[@title='삭제']", timeout=5000)

    # 5.2. 수료일자
    page.click("xpath=//div[span[text()='수료증 기재일']]")
    today_day = str(datetime.datetime.now().day)
    page.locator(f"xpath=//td[button[text()='{today_day}']]").first.click()

    # 5.3. 발급번호
    doc_no = datetime.datetime.now().strftime("%Y-%m%d-%H%M%S")
    page.fill("xpath=//input[@placeholder='발급번호를 입력해 주세요']", doc_no)
    page.click("xpath=//button[text()='등록하기']")
    page.wait_for_timeout(1000)

    # 5.4. 수료증 업데이트 확인 이력 팝업
    page.locator("xpath=//dl[dt[text()='CSO 교육 수료증']]//button").first.click()
    page.wait_for_selector("xpath=//div[h2[text()='CSO 교육 수료 이력']]", timeout=5000)
    page.click("xpath=//button[@title='수료증']")
    page.wait_for_selector("xpath=//img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]", timeout=10000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 6. 도장 정보 관리 (직접 만들기 & 파일 업로드)
    # -------------------------------------------------------------
    print("[Step 6.1] 도장 직접 만들기")
    page.click("xpath=//button[span[text()='업체 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), '도장 정보 관리')]")
    page.wait_for_selector("xpath=//h2[text()='도장 정보 관리']", timeout=5000)

    page.fill("id=stampName", "테스트")
    page.click("xpath=//button[text()='만들기']")
    page.wait_for_selector("xpath=//img[@alt='도장 미리보기']", timeout=5000)
    page.click("xpath=//button[@title='저장하기']")
    page.wait_for_timeout(1000)

    print("[Step 6.2] 도장 파일 업로드")
    page.click("xpath=//button[span[text()='업체 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), '도장 정보 관리')]")
    page.wait_for_selector("xpath=//h2[text()='도장 정보 관리']", timeout=5000)

    page.click("xpath=//button[text()='파일 업로드']")
    random_stamp_path = get_random_stamp_image_path()
    page.locator("xpath=//input[@type='file']").set_input_files(random_stamp_path)
    page.wait_for_selector("xpath=//button[@title='삭제']", timeout=5000)
    page.click("xpath=//button[@title='저장하기']")
    page.wait_for_timeout(1000)

    # -------------------------------------------------------------
    # 7. 추가 메뉴 (약관 / 매뉴얼)
    # -------------------------------------------------------------
    print("[Step 7] 추가 메뉴(서비스 이용 매뉴얼, 이용약관, 개인정보처리방침) 확인")
    
    # 7.1. 서비스 이용 매뉴얼
    page.click("xpath=//button[@aria-haspopup='menu']")
    page.wait_for_selector("xpath=//div[@title='서비스 이용 매뉴얼']", timeout=5000)
    page.click("xpath=//div[@title='서비스 이용 매뉴얼']")
    page.wait_for_selector("xpath=//h2[text()='서비스 이용 매뉴얼']", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 7.2. 서비스 이용약관
    page.click("xpath=//button[@aria-haspopup='menu']")
    page.wait_for_selector("xpath=//div[@title='서비스 이용약관']", timeout=5000)
    page.click("xpath=//div[@title='서비스 이용약관']")
    page.wait_for_selector("xpath=//h2[text()='서비스 이용약관']", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 7.3. 개인정보처리방침
    page.click("xpath=//button[@aria-haspopup='menu']")
    page.wait_for_selector("xpath=//div[@title='개인정보처리방침']", timeout=5000)
    page.click("xpath=//div[@title='개인정보처리방침']")
    page.wait_for_selector("xpath=//h2[text()='개인정보처리방침']", timeout=5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # -------------------------------------------------------------
    # 8. 최종 로그아웃
    # -------------------------------------------------------------
    print("[Step 8] 내 정보 페이지 하단 로그아웃 수행")
    page.click("button[title='내 정보']")
    page.wait_for_selector("xpath=//h2[text()='내 정보']", timeout=5000)
    
    logout_btn = page.locator("xpath=//button[contains(text(), '로그아웃')]")
    logout_btn.scroll_into_view_if_needed()
    logout_btn.click()

    page.wait_for_selector("xpath=//a[normalize-space(.)='회원가입']", timeout=5000)
    print("[Success] 02. 프로필 전체 관리 Flow 성공 완료!")
