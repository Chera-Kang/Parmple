import os
import subprocess
import shutil

def build_allure_report(allure_raw_dir: str, allure_report_dir: str):
    """수집된 Allure 원천 데이터로부터 Single-file HTML 대시보드를 빌드합니다."""
    if not (os.path.exists(allure_raw_dir) and os.listdir(allure_raw_dir)):
        return

    print("\n[Report] Allure HTML 대시보드 빌드 중 (Single-file 번들링)...")
    try:
        subprocess.run(
            f"npx -y allure-commandline generate \"{allure_raw_dir}\" --clean --single-file -o \"{allure_report_dir}\"",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # 임시 원천 데이터 폴더 정리
        shutil.rmtree(allure_raw_dir, ignore_errors=True)
        print(f" -> Allure 리포트 생성 완료: {allure_report_dir}")
    except Exception as e:
        print(f"[Warning] Allure 리포트 생성 중 오류: {e}")


def generate_launcher_bats(result_dir: str, enable_allure: bool, enable_traces: bool):
    """결과 폴더 내 편리한 1-클릭 실행용 바로가기 배치(.bat) 파일을 생성합니다."""
    # 1. Allure 리포트 열기 배치 파일
    if enable_allure:
        bat_allure_path = os.path.join(result_dir, "열기_Allure리포트.bat")
        with open(bat_allure_path, "w", encoding="utf-8") as f:
            f.write("@echo off\ncd /d \"%~dp0\\allure_report\"\nstart index.html\n")

    # 2. Playwright Trace Viewer 선택기 배치 파일
    if enable_traces:
        bat_trace_path = os.path.join(result_dir, "열기_PlaywrightTrace.bat")
        bat_content = """@echo off
chcp 65001 >nul
title Playwright Trace Viewer Selector
cd /d "%~dp0"
echo ================================================================================
echo                    Playwright Trace Viewer - 테스트 선택
echo ================================================================================
echo.
setlocal enabledelayedexpansion
set count=0
for /d %%d in (traces\\*) do (
    set /a count+=1
    set "folder[!count!]=%%d"
    set "rawname=%%~nxd"
    
    :: 보기 편하도록 긴 경로 접두사 제거
    set "dispname=!rawname:automation-web-playwright-testcase-ai-=!"
    set "dispname=!dispname:automation-web-playwright-testcase-=!"
    set "dispname=!dispname:-chromium=!"
    echo  [!count!] !dispname!
)
echo.
echo ================================================================================
echo  [A] 전체 동시 열기   [Q] 종료
echo ================================================================================
set /p choice="확인할 테스트 번호를 입력하세요: "

if /i "!choice!"=="Q" exit /b
if /i "!choice!"=="A" (
    for /l %%i in (1,1,!count!) do (
        start npx playwright show-trace "!folder[%%i]!\\trace.zip"
    )
    exit /b
)
if defined folder[!choice!] (
    start npx playwright show-trace "!folder[%choice%]!\\trace.zip"
) else (
    echo 잘못된 번호입니다.
    pause
)
"""
        with open(bat_trace_path, "w", encoding="utf-8") as f:
            f.write(bat_content)


def print_test_summary(exit_code: int, result_dir: str, report_html: str, allure_report_dir: str,
                       enable_pytest: bool, enable_allure: bool, enable_traces: bool):
    """최종 실행 결과 및 리포트 파일 위치를 터미널에 요약 출력합니다."""
    print("\n" + "=" * 80)
    print(f"Test Finished with Exit Code: {exit_code}")
    print(f"Test Results & Reports saved in: {result_dir}")
    if enable_pytest:
        print(f" - [1] Pytest HTML : {report_html}")
    if enable_allure:
        print(f" - [2] Allure Report : {os.path.join(allure_report_dir, 'index.html')}")
    if enable_traces:
        print(f" - [3] Playwright Trace : {os.path.join(result_dir, '열기_PlaywrightTrace.bat')}")
    print("=" * 80 + "\n")
