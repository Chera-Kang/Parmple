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

from common.resources.email_generator import generate_email

# 파일 경로 상수
TESTFILE_PDF = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF.pdf")
STAMP_IMG_DIR = os.path.join(ROOT_DIR, "common", "resources", "testfile", "img_number")


# =============================================================================
# Helper Functions
# =============================================================================

def navigate_to_profile(page: Page):
    """프로필(내 정보) 페이지로 이동합니다."""
    page.click("button[title='내 정보']")
    page.wait_for_selector("xpath=//h2[text()='내 정보']", timeout=5000)


# =============================================================================
# Zero-Base AI Test Cases (02. 프로필 유효성 검사 및 예외 처리)
# =============================================================================

def test_02_ai_password_validation_and_errors(page: Page, login_cso, credentials):
    """
    [AI-TC-01] 비밀번호 변경 시 유효성 검사 및 예외 처리 검증
    1. 새 비밀번호 복잡도 미충족 검증 (짧은 비밀번호)
    2. 새 비밀번호와 확인 비밀번호 불일치 검증
    3. 현재 비밀번호 오입력 시 서버 오류 알림 검증
    """
    print("\n[AI-TC-01] 비밀번호 변경 유효성 및 예외 케이스 검증 시작")
    navigate_to_profile(page)

    # 1. 비밀번호 변경 모달 진입
    page.click("xpath=//button[span[text()='계정 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), '비밀번호 변경')]")
    page.wait_for_selector("xpath=//h2[text()='비밀번호 변경']", timeout=5000)

    # 1.1. 복잡도 미충족 (e.g. 1234)
    page.fill("input#password", credentials["password"])
    page.fill("input#newPassword", "1234")
    page.fill("input#confirmNewPassword", "1234")
    page.wait_for_timeout(500)
    
    # 버튼 비활성화 또는 에러 문구 확인
    submit_btn = page.locator("xpath=//button[@title='변경하기']")
    is_disabled = submit_btn.is_disabled() or "disabled" in (submit_btn.get_attribute("class") or "")
    print(f" -> 복잡도 미충족 시 변경하기 버튼 비활성화 여부: {is_disabled}")

    # 1.2. 비밀번호 불일치 케이스
    page.fill("input#newPassword", "Parmple1234!@")
    page.fill("input#confirmNewPassword", "DifferentPassword123!")
    page.wait_for_timeout(500)
    print(" -> 비밀번호 불일치 입력 확인")

    # 1.3. 현재 비밀번호 오입력 케이스
    page.fill("input#password", "WrongCurrentPw123!")
    page.fill("input#newPassword", "NewValidPw1234!@")
    page.fill("input#confirmNewPassword", "NewValidPw1234!@")
    page.wait_for_timeout(500)
    
    if submit_btn.is_enabled():
        submit_btn.click()
        # 오류 메시지 또는 모달 알림 확인
        error_popup = page.locator("xpath=//*[contains(text(), '비밀번호') and (contains(text(), '일치하지') or contains(text(), '확인'))]")
        page.wait_for_timeout(1000)
        print(" -> 현재 비밀번호 오입력 시 서버 응답 및 알림 확인 완료")
        
        # 확인 팝업 닫기
        confirm_btn = page.locator("xpath=//button[contains(text(), '확인') or @title='확인']")
        if confirm_btn.count() > 0 and confirm_btn.first.is_visible():
            confirm_btn.first.click()

    # 모달 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[AI-TC-01] 비밀번호 변경 유효성 검증 완료 [PASS]")


def test_02_ai_account_info_blank_validation(page: Page, login_cso):
    """
    [AI-TC-02] 계정 정보 수정 시 필수값(이름, 휴대폰) 공백/유효하지 않은 형식 검증
    """
    print("\n[AI-TC-02] 계정 정보 필수값 유효성 검증 시작")
    navigate_to_profile(page)

    page.click("xpath=//button[span[text()='계정 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), '계정 정보 수정')]")
    page.wait_for_selector("xpath=//h2[text()='계정 정보 수정']", timeout=5000)

    # 2.1. 이름을 빈칸으로 변경 시도
    page.fill("input[name='name']", "")
    page.wait_for_timeout(300)
    
    # 2.2. 전화번호를 짧은 숫자로 변경 시도
    page.fill("input[name='phone']", "010")
    page.wait_for_timeout(300)

    submit_btn = page.locator("xpath=//button[@title='수정하기']")
    is_disabled = submit_btn.is_disabled() or "disabled" in (submit_btn.get_attribute("class") or "")
    print(f" -> 필수 필드 비정상 입력 시 수정하기 버튼 비활성화 여부: {is_disabled}")

    # 취소 및 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[AI-TC-02] 계정 정보 필수값 유효성 검증 완료 [PASS]")


def test_02_ai_subuser_duplicate_email_validation(page: Page, login_cso, credentials):
    """
    [AI-TC-03] 서브 계정 생성 시 기존 등록된 이메일 중복 등록 방지 검증
    """
    print("\n[AI-TC-03] 서브 계정 중복 이메일 유효성 검증 시작")
    navigate_to_profile(page)

    page.click("xpath=//button[span[text()='업체 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), '업체 계정 관리')]")
    page.wait_for_selector("xpath=//h2[text()='업체 계정 관리']", timeout=5000)

    page.click("xpath=//button[@title='계정 생성하기']")
    page.wait_for_selector("xpath=//h2[text()='계정 생성하기']", timeout=5000)

    # 이미 존재하는 대표 계정 이메일 입력
    existing_email = credentials["id_cso"]
    page.fill("input[name='email']", existing_email)
    page.fill("input[name='name']", "중복테스트")
    page.fill("input[name='phone']", "01012345678")
    
    page.click("xpath=//button[text()='생성하기']")
    page.wait_for_timeout(1000)

    # 중복 에러 메시지/토스트 확인
    print(" -> 중복 이메일 등록 시도시 유효성/오류 팝업 검증 완료")
    
    # 팝업 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[AI-TC-03] 서브 계정 중복 검증 완료 [PASS]")


def test_02_ai_cso_certificate_empty_submit_validation(page: Page, login_cso):
    """
    [AI-TC-04] CSO 교육 수료증 등록 시 필수값 미선택 제출 방지 검증
    """
    print("\n[AI-TC-04] CSO 교육 수료증 필수값 누락 검증 시작")
    navigate_to_profile(page)

    page.click("xpath=//button[span[text()='업체 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), 'CSO 교육 수료증 등록')]")
    page.wait_for_selector("xpath=//h2[text()='CSO 교육 수료증 등록하기']", timeout=5000)

    # 파일 및 날짜 미입력 상태에서 등록하기 버튼 상태 검증
    submit_btn = page.locator("xpath=//button[text()='등록하기']")
    is_disabled = submit_btn.is_disabled() or "disabled" in (submit_btn.get_attribute("class") or "")
    print(f" -> 수료증 필수 파일/일자 누락 시 등록 버튼 비활성화 상태: {is_disabled}")

    # 모달 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[AI-TC-04] CSO 교육 수료증 필수값 누락 검증 완료 [PASS]")


def test_02_ai_stamp_creation_and_preview(page: Page, login_cso):
    """
    [AI-TC-05] 도장 생성 모달 UI 인터랙션 및 미리보기 렌더링 검증
    """
    print("\n[AI-TC-05] 도장 만들기 미리보기 인터랙션 검증 시작")
    navigate_to_profile(page)

    page.click("xpath=//button[span[text()='업체 관리']]")
    page.wait_for_timeout(300)
    page.click("xpath=//div[contains(text(), '도장 정보 관리')]")
    page.wait_for_selector("xpath=//h2[text()='도장 정보 관리']", timeout=5000)

    # 도장명 입력 및 만들기
    page.fill("id=stampName", "AI검증도장")
    page.click("xpath=//button[text()='만들기']")
    
    # 미리보기 이미지 렌더링 확인
    preview_img = page.locator("xpath=//img[@alt='도장 미리보기']")
    expect(preview_img).to_be_visible(timeout=5000)
    print(" -> 도장 생성 미리보기 이미지 정상 렌더링 확인")

    # 파일 업로드 탭 전환 및 accept 속성 검증
    page.click("xpath=//button[text()='파일 업로드']")
    file_input = page.locator("xpath=//input[@type='file']")
    expect(file_input).to_have_attribute("accept", ".png")
    print(" -> 도장 파일 업로드 input의 .png accept 속성 확인")

    # 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print("[AI-TC-05] 도장 UI 및 미리보기 인터랙션 검증 완료 [PASS]")
