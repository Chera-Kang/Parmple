import os
import subprocess
import time
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

# 공통 .env 파일 로드
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'common', 'auth', '.env'))
load_dotenv(dotenv_path=env_path)

def kill_process_on_port(port):
    """지정된 포트를 사용 중인 프로세스를 찾아 강제 종료합니다 (Windows 환경)"""
    try:
        # netstat 결과에서 LISTENING 상태인 해당 포트의 PID 추출
        result = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True, text=True)
        for line in result.strip().split('\n'):
            if 'LISTENING' in line:
                pid = line.strip().split()[-1]
                if pid and pid != "0":
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        # 해당 포트를 점유하는 프로세스가 없는 경우 (정상)
        pass

@pytest.fixture(scope="module")
def driver():
    """
    Appium WebDriver 인스턴스를 생성하고 관리하는 Fixture (Setup & Teardown)
    pytest는 conftest.py 파일에 정의된 fixture를 자동으로 모든 테스트 파일에서 사용할 수 있게 해줍니다.
    """
    appium_port = 4723
    
    # [Setup] 1. 앱피움 서버 종료 (살아있을 수 있으니)
    print(f"\n[Setup] {appium_port} 포트를 점유중인 이전 Appium 서버 프로세스 종료 중...")
    kill_process_on_port(appium_port)
    
    # [Setup] 2. 앱피움 서버 실행
    print("[Setup] 새 Appium 서버 구동 중...")
    appium_log = open('appium_server.log', 'w')
    appium_process = subprocess.Popen(
        f"appium -p {appium_port}", 
        shell=True, 
        stdout=appium_log, 
        stderr=appium_log
    )
    # 서버가 완전히 구동될 때까지 대기 (최대 25초 대기)
    import urllib.request
    server_ready = False
    for _ in range(25):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{appium_port}/status", timeout=1) as resp:
                if resp.status == 200:
                    server_ready = True
                    break
        except Exception:
            time.sleep(1)
            
    if not server_ready:
        print("[Warning] Appium 서버 응답 대기 시간 초과, 기본 대기 후 시도합니다.")
        time.sleep(3)
    
    # Appium 서버 주소 설정
    appium_server_url = f'http://127.0.0.1:{appium_port}'

    # UiAutomator2Options를 활용한 Capabilities 설정
    options = UiAutomator2Options()
    
    # OS 권한 팝업(알림 허용, 위치 허용 등) 자동 허용 설정
    options.auto_grant_permissions = True
    
    # 디바이스 정보 및 앱 패키지명 설정
    options.platform_name = 'Android'
    
    # 디바이스 UDID (adb devices로 확인된 Pixel 4 XL 기기 설정)
    options.udid = '9A271FFBA005AZ'
    
    options.app_package = 'com.parmple.app'
    
    # TODO: 앱의 메인 액티비티 입력 (앱 개발자에게 문의하거나 apk 분석 툴 사용)
    options.app_activity = '.MainActivity' 
    
    # 하이브리드 앱 테스트를 위해 ChromeDriver가 필요할 수 있습니다. 
    # 웹뷰 버전에 맞는 ChromeDriver 경로를 명시해야 할 수도 있습니다.
    # options.chromedriver_executable = '/path/to/chromedriver'
    
    # 1. 앱 구동 (App Launch)
    driver = webdriver.Remote(appium_server_url, options=options)
    
    yield driver
    
    # [Teardown] 1. 테스트 종료 후 앱 종료
    driver.quit()
    
    # [Teardown] 2. 앱피움 서버 종료
    print("\n[Teardown] Appium 서버 프로세스 종료 중...")
    appium_process.terminate()
    kill_process_on_port(appium_port) # 확실한 종료를 위해 포트 단위로 한 번 더 킬
    appium_log.close()
