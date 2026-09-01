import os
import sys
import time
# pyrefly: ignore [missing-import]
import pytest
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# 리포트 관리 모듈 import
from report_manager import build_allure_report, generate_launcher_bats, print_test_summary

# =============================================================================
# 1. 리포트 생성 설정 (True / False 로 On/Off 가능)
# =============================================================================
ENABLE_PYTEST_HTML = True       # 1) Pytest HTML 리포트 (report.html)
ENABLE_PLAYWRIGHT_TRACES = True # 2) Playwright Trace Viewer (traces/)
ENABLE_ALLURE_REPORT = True     # 3) Allure 대시보드 (allure_report/)

# =============================================================================
# 2. 경로 및 환경 설정
# =============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))

# 환경 변수 로드
env_path = os.path.join(ROOT_DIR, "common", "auth", ".env")
load_dotenv(env_path)

# 기본 테스트 대상 디렉토리 (testcase 또는 testcase_ai)
# DEFAULT_TEST_DIR = os.path.join(SCRIPT_DIR, "testcase")
DEFAULT_TEST_DIR = os.path.join(SCRIPT_DIR, "testcase_ai")

# 결과 디렉토리 설정: TestResult/YY-MM-DD_HH-MM
BASE_RESULT_DIR = os.path.join(ROOT_DIR, "TestResult")
timestamp = time.strftime("%y-%m-%d_%H-%M")
result_dir = os.path.join(BASE_RESULT_DIR, timestamp)
os.makedirs(result_dir, exist_ok=True)
os.environ["CURRENT_TEST_RESULT_DIR"] = result_dir

# 서브 경로 정의
report_html = os.path.join(result_dir, "report.html")
traces_dir = os.path.join(result_dir, "traces")
allure_raw_dir = os.path.join(result_dir, ".allure_raw")
allure_report_dir = os.path.join(result_dir, "allure_report")

target_tests = sys.argv[1:] if len(sys.argv) > 1 else [DEFAULT_TEST_DIR]

print("=" * 80)
print("              Starting Playwright E2E Regression Test Suites")
print("=" * 80)
print(f"Target Tests: {target_tests}")
print(f"Result Directory: {result_dir}")
print(f"Browser Mode: Headed (0.5s SlowMo)")
print("-" * 80)

# =============================================================================
# 3. Pytest 실행 인자 구성 및 실행
# =============================================================================
pytest_args = [
    *target_tests,
    "--headed",
    "--slowmo=500",
    "-v",
    "-s",
    "-W", "ignore"
]

if ENABLE_PYTEST_HTML:
    pytest_args.extend([f"--html={report_html}", "--self-contained-html"])

if ENABLE_PLAYWRIGHT_TRACES:
    os.makedirs(traces_dir, exist_ok=True)
    pytest_args.extend(["--tracing=on", f"--output={traces_dir}"])

if ENABLE_ALLURE_REPORT:
    os.makedirs(allure_raw_dir, exist_ok=True)
    pytest_args.extend([f"--alluredir={allure_raw_dir}"])

exit_code = pytest.main(pytest_args)

# =============================================================================
# 4. 후처리 및 리포트/배치 생성
# =============================================================================
if ENABLE_ALLURE_REPORT:
    build_allure_report(allure_raw_dir, allure_report_dir)

generate_launcher_bats(result_dir, ENABLE_ALLURE_REPORT, ENABLE_PLAYWRIGHT_TRACES)

print_test_summary(
    exit_code, result_dir, report_html, allure_report_dir,
    ENABLE_PYTEST_HTML, ENABLE_ALLURE_REPORT, ENABLE_PLAYWRIGHT_TRACES
)

sys.exit(exit_code)
