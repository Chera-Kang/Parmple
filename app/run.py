import sys
import os
# pyrefly: ignore [missing-import]
import pytest

if __name__ == "__main__":
    """
    모든 Appium 테스트 케이스를 모아서 한 번에 실행하는 Entry Point (실행 파일)입니다.
    """
    # 현재 파일(run.py)이 있는 디렉토리 기준 app 폴더 경로
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 실행할 테스트 케이스가 모여있는 폴더 경로 지정
    testcase_dir = os.path.join(base_dir, 'testcase')
    
    # 리포트 폴더명 동적 생성: 26-08-12_09-45 (App) 형식
    import datetime
    now_str = datetime.datetime.now().strftime("%y-%m-%d_%H-%M")
    
    # 최상위 폴더인 Parmple 아래 TestResult 폴더 경로 구성
    report_dir = os.path.abspath(os.path.join(base_dir, '..', 'TestResult', f"{now_str} (App)"))
    
    # 해당 결과 폴더가 없으면 자동 생성
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        
    # 리포트 파일 최종 경로
    report_path = os.path.join(report_dir, 'report.html')
    
    # pytest 실행 인자 설정
    # -v: 테스트 결과를 상세히 출력
    # -s: 테스트 코드 내의 print() 출력문을 콘솔에 표시
    # --html: pytest-html 플러그인을 사용하여 리포트 생성
    # --self-contained-html: CSS, JS 등을 리포트 파일 하나에 모두 내장시킴
    args = [
        '-v', 
        '-s', 
        f'--html={report_path}', 
        '--self-contained-html', 
        testcase_dir
    ]
    
    print(f"============================================================")
    print(f"앱 테스트 구동을 시작합니다. (대상 폴더: {testcase_dir})")
    print(f"============================================================")
    
    # pytest.main()을 통해 testcase 폴더 내의 모든 테스트 스크립트 일괄 실행
    exit_code = pytest.main(args)
    sys.exit(exit_code)
