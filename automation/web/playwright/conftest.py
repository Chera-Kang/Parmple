import os
import time
import pytest
from playwright.sync_api import Page, sync_playwright
from dotenv import load_dotenv

# 공통 환경 변수 로드
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv(os.path.join(ROOT_DIR, "common", "auth", ".env"))

BASE_URL = "https://qa.erp.parmple.com/"
ADMIN_URL = "https://qa.admin.parmple.com/"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def credentials():
    return {
        "id_cso": os.environ.get("ID_CSO", ""),
        "id_cso2": os.environ.get("ID_CSO2", ""),
        "id_cso3": os.environ.get("ID_CSO3", ""),
        "id_pharm1": os.environ.get("ID_PHARM_1", ""),
        "id_pharm2": os.environ.get("ID_PHARM_2", ""),
        "admin_email": os.environ.get("ADMIN_EMAIL", ""),
        "password": os.environ.get("PASSWORD", "")
    }

@pytest.fixture(scope="function")
def login_cso(page: Page, credentials):
    """CSO 1 계정으로 로그인하는 공통 fixture"""
    page.goto(BASE_URL)
    page.wait_for_selector("a:has-text('회원가입')", timeout=10000)
    page.fill("input[name='email']", credentials["id_cso"])
    page.fill("input[name='password']", credentials["password"])
    page.click("button:has-text('로그인')")
    page.wait_for_selector("h2:has-text('회원 업체 관리')", timeout=10000)
    return page

@pytest.fixture(scope="function")
def login_cso3(page: Page, credentials):
    """CSO 3 계정으로 로그인하는 공통 fixture"""
    page.goto(BASE_URL)
    page.wait_for_selector("a:has-text('회원가입')", timeout=10000)
    page.fill("input[name='email']", credentials["id_cso3"])
    page.fill("input[name='password']", credentials["password"])
    page.click("button:has-text('로그인')")
    page.wait_for_selector("h2:has-text('회원 업체 관리')", timeout=10000)
    return page

@pytest.fixture(scope="function")
def login_pharm1(page: Page, credentials):
    """제약사 1 계정으로 로그인하는 공통 fixture"""
    page.goto(BASE_URL)
    page.wait_for_selector("a:has-text('회원가입')", timeout=10000)
    page.fill("input[name='email']", credentials["id_pharm1"])
    page.fill("input[name='password']", credentials["password"])
    page.click("button:has-text('로그인')")
    page.wait_for_selector("xpath=//h2[contains(., '회원 업체 관리')] | //h2[contains(., '계약서 관리')] | //h2[contains(., '받은 재위탁 통보서')]", timeout=10000)
    return page


# --------------------------------------------------------------------------
# 실패 시 스크린샷 자동 캡처 및 HTML 리포트 첨부 Hook
# --------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # 테스트 단계가 실행(call) 중 실패(failed)했을 때만 스크린샷 캡처
    if report.when == "call" and report.failed:
        page: Page = item.funcargs.get("page")
        if page:
            # 결과 저장 디렉토리 확인 (run.py에서 지정한 경로 또는 기본 TestResult 경로)
            result_dir = os.environ.get("CURRENT_TEST_RESULT_DIR")
            if not result_dir:
                result_dir = os.path.join(ROOT_DIR, "TestResult", f"{time.strftime('%y-%m-%d_%H-%M')}_playwright")
            
            screenshots_dir = os.path.join(result_dir, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            test_name = item.name.replace("[chromium]", "")
            timestamp = time.strftime("%H-%M-%S")
            screenshot_file = f"fail_{test_name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshots_dir, screenshot_file)
            
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n[Failure Screenshot] 실패 화면이 저장되었습니다: {screenshot_path}")
                
                # pytest-html 리포트가 활성화되어 있다면 HTML 리포트에도 이미지 첨부
                extra = getattr(report, "extra", [])
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    extra.append(pytest_html.extras.image(screenshot_path))
                    report.extra = extra
            except Exception as e:
                print(f"\n[Warning] 실패 스크린샷 저장 실패: {e}")
