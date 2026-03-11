import os
import shutil
import time
from robot import run
from dotenv import load_dotenv

# 테스트 스위트 폴더 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

# 환경 변수 로드
load_dotenv(os.path.join(ROOT_DIR, "common", "auth", ".env"))

TEST_SUITE_DIR = os.path.join(SCRIPT_DIR, "testcase") 

# 새로운 결과 저장 경로 (최상위 TestResult 폴더)
BASE_RESULT_DIR = os.path.join(ROOT_DIR, "TestResult")

# 현재 날짜 및 시간 기반으로 폴더 생성
timestamp = time.strftime("%y-%m-%d_%H-%M")
result_dir = os.path.join(BASE_RESULT_DIR, timestamp)
os.makedirs(result_dir, exist_ok=True)

# 최상위 screenshots 폴더 내부에 현재 실행 결과를 위한 폴더 생성
# (기존 logic 유지: result_dir 내부에 screenshots 생성하도록 설정)
screenshots_dir = os.path.join(result_dir, "screenshots")
os.makedirs(screenshots_dir, exist_ok=True)

# Robot Framework 실행
run(TEST_SUITE_DIR, output=os.path.join(result_dir, "output.xml"),
    log=os.path.join(result_dir, "log.html"),
    report=os.path.join(result_dir, "report.html"),
    variable=f"SCREENSHOT_DIR:{screenshots_dir}")


# 디렉토리 확인
print(f"Test results saved in: {result_dir}")
print(f"Screenshots saved in: {screenshots_dir}")

# 마무리
print("==============================================================================")
print("=============================== Test  Finished ===============================")
print("==============================================================================")
