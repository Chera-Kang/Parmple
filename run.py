import os
import shutil
import time
from robot import run

# 테스트 스위트 폴더 (실제 테스트 폴더 경로 설정)
TEST_SUITE_DIR = "Web/TC" 

# 새로운 결과 저장 경로
BASE_RESULT_DIR = r"C:\Dev\TestResult"

# 현재 날짜 및 시간 기반으로 폴더 생성
timestamp = time.strftime("%y-%m-%d_%H-%M")
result_dir = os.path.join(BASE_RESULT_DIR, timestamp)
os.makedirs(result_dir, exist_ok=True)

# screenshots 폴더를 실행 결과 폴더 내부에 생성
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
