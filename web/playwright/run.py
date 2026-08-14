import os
import sys
import time
# pyrefly: ignore [missing-import]
import pytest
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# 디렉토리 경로 설정
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

# 환경 변수 로드 (공통 계정 정보 및 Gemini API 키 등)
env_path = os.path.join(ROOT_DIR, "common", "auth", ".env")
load_dotenv(env_path)

# 테스트 케이스 경로
TEST_DIR = os.path.join(SCRIPT_DIR, "testcase")
if not os.path.exists(TEST_DIR):
    os.makedirs(TEST_DIR, exist_ok=True)

# 테스트 결과 저장 경로 (TestResult/날짜_시간_playwright)
BASE_RESULT_DIR = os.path.join(ROOT_DIR, "TestResult")
timestamp = time.strftime("%y-%m-%d_%H-%M")
result_dir = os.path.join(BASE_RESULT_DIR, f"{timestamp}_playwright")
os.makedirs(result_dir, exist_ok=True)

# 실패 시 스크린샷 저장을 위해 환경 변수에 현재 결과 디렉토리 전달
os.environ["CURRENT_TEST_RESULT_DIR"] = result_dir

report_html = os.path.join(result_dir, "report.html")

print("=" * 80)
print("              Starting Playwright E2E Regression Test Suites")
print("=" * 80)
print(f"Test Suite Directory: {TEST_DIR}")
print(f"Report Output Path: {report_html}")
print(f"Browser Mode: Headed (실제 브라우저 화면 표시, 0.5초 슬로우모션)")
print("-" * 80)

# pytest 실행 옵션
# --headed : 실제 브라우저 창을 띄움
# --slowmo=500 : 사람이 눈으로 확인할 수 있도록 각 동작 간 0.5초 대기
target_tests = sys.argv[1:] if len(sys.argv) > 1 else [TEST_DIR]

pytest_args = [
    *target_tests,
    "--headed",
    "--slowmo=500",
    f"--html={report_html}",
    "--self-contained-html",
    "-v",
    "-s"
]

exit_code = pytest.main(pytest_args)

print("=" * 80)
print(f"Test Finished with Exit Code: {exit_code}")
print(f"Test results saved in: {result_dir}")
print("=" * 80)

sys.exit(exit_code)
