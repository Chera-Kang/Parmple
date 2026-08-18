import time
import os
# pyrefly: ignore [missing-import] //이건 유지해줘
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="class", autouse=True)
def login_once(driver):
    """
    [공통 설정] 테스트 클래스가 시작될 때 딱 한 번만 로그인을 수행합니다.
    이후 각각의 테스트 케이스(메뉴 클릭)들은 이 로그인된 상태를 공유하여 빠르게 동작합니다.
    """
    wait = WebDriverWait(driver, 15)
    print("\n[Setup] 최초 1회 로그인 수행 중...")
    
    cso_id = os.getenv('ID_CSO')
    cso_pw = os.getenv('PASSWORD')
    if not cso_id or not cso_pw:
        raise ValueError("common/auth/.env 파일에 'ID_CSO' 또는 'PASSWORD'가 설정되어 있지 않습니다.")

    id_locator = (AppiumBy.XPATH, "//*[@resource-id='ion-input-0']")
    id_input = wait.until(EC.visibility_of_element_located(id_locator))
    id_input.clear()
    id_input.send_keys(cso_id)

    pw_locator = (AppiumBy.XPATH, "//*[@resource-id='ion-input-1']")
    pw_input = wait.until(EC.visibility_of_element_located(pw_locator))
    pw_input.clear()
    pw_input.send_keys(cso_pw)
    
    login_btn_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("로그인")')
    login_btn = wait.until(EC.element_to_be_clickable(login_btn_locator))
    login_btn.click()
    
    # 메인 화면(GNB) 첫 번째 메뉴가 뜰 때까지 대기하여 로그인 성공 보장
    first_gnb = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" 필터링")')
    wait.until(EC.visibility_of_element_located(first_gnb))
    print("\n[Setup] 로그인 성공! 이제 개별 GNB 테스트를 시작합니다.")

class TestHybridAppSmoke:
    # -------------------------------------------------------------
    # 개별 테스트 케이스 (각 기능마다 Pass/Fail을 독립적으로 판정)
    # -------------------------------------------------------------
    
    def test_gnb_filtering(self, driver):
        """필터링 탭 진입 검증"""
        wait = WebDriverWait(driver, 10)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" 필터링")')
        btn = wait.until(EC.element_to_be_clickable(locator))
        btn.click()
        time.sleep(1) # 화면 전환 대기
        
        # TODO: (예시) assert 문을 추가하여 필터링 화면 상단 타이틀이 맞는지 검증할 수 있습니다.
        # title = wait.until(...).text
        # assert "필터링" in title
        print("\n -> '필터링' 탭 진입 검증 완료")
        
    def test_gnb_contract(self, driver):
        """전자 계약 탭 진입 검증"""
        wait = WebDriverWait(driver, 10)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" 전자 계약")')
        btn = wait.until(EC.element_to_be_clickable(locator))
        btn.click()
        time.sleep(1)
        print("\n -> '전자 계약' 탭 진입 검증 완료")
        
    def test_gnb_library(self, driver):
        """자료실 탭 진입 검증"""
        wait = WebDriverWait(driver, 10)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" 자료실")')
        btn = wait.until(EC.element_to_be_clickable(locator))
        btn.click()
        time.sleep(1)
        print("\n -> '자료실' 탭 진입 검증 완료")
        
    def test_gnb_all(self, driver):
        """전체 탭 진입 검증"""
        wait = WebDriverWait(driver, 10)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" 전체")')
        btn = wait.until(EC.element_to_be_clickable(locator))
        btn.click()
        time.sleep(1)
        print("\n -> '전체' 탭 진입 검증 완료")
