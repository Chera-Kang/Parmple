*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    String
Library    Collections
Library    DateTime
Library    Process

*** Variables ***
# Service URL
${URL}    https://qa.erp.parmple.com/

# Account
${id_CSO}        %{ID_CSO=}
${id_pharm_1}    %{ID_PHARM_1=}
${id_pharm_2}    %{ID_PHARM_2=}
${ADMIN_EMAIL}    %{ADMIN_EMAIL=}
${password}       %{PASSWORD=}

# DIR
${ROOT_DIR}           ${{os.path.abspath(os.path.join(r'${CURDIR}', '../../'))}}
${RES_DIR}            ${ROOT_DIR}/common/resources
${SCREENSHOT_DIR}     ${ROOT_DIR}/screenshots
${TESTFILE_DIR}       ${RES_DIR}/testfile
${TESTFILE_PATH}      ${TESTFILE_DIR}/Sameple_PDF.pdf
${BIZNO_FILE}         ${RES_DIR}/used_bizgNo.txt
${PYTHON_EXE}         ${ROOT_DIR}/.venv/Scripts/python.exe
${GSHEET_READER_PY}   ${RES_DIR}/gsheet_reader.py
${EMAIL_READER_PY}    ${RES_DIR}/email_reader.py
${EMAIL_GEN_PY}       ${RES_DIR}/email_generator.py
${ADMIN_API_PY}       ${RES_DIR}/admin_api.py


*** Keywords ***
# Test Suite 실행
Initialize Test Suite
    Load Login Credentials        # 환경변수 강제 로드 (단일 파일 실행 및 run.py 모두 대응)
    Log To Console    Initialzing Test Suite
    Log To Console    Opening Browser
    Open Browser    ${URL}    Chrome
    Maximize Browser Window

# Test Suite 종료
Finalize Test Suite
    Log To Console    Closing Browser
    Close Browser

# 스크린샷
Screenshot
    ${SetTime}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
    Sleep    0.5
    Capture Page Screenshot    ${screenshot_DIR}/screenshot_${SetTime}.png
    Sleep    0.5

# 새로운 사업자번호 조회 (Google Sheet에서 가져오기)
Get Biz Number
    # Google Sheet에서 사업자번호 가져오기
    ${result}=    Run Process    ${PYTHON_EXE}    ${GSHEET_READER_PY}    stdout=PIPE    stderr=PIPE
    ${biz_no}=    Set Variable   ${result.stdout.strip()}
    
    # 에러 및 결과 확인
    Should Not Contain    ${biz_no}    ERROR    msg=Google Sheet 처리 중 오류 발생: ${biz_no}
    Should Not Be Equal   ${biz_no}    NO_BIZ_NO    msg=사용 가능한 사업자번호가 스프레드시트에 없습니다.
    
    Log To Console    \n[Google Sheet] 선택된 사업자번호 : ${biz_no}
    [Return]    ${biz_no}

# 사업자번호 하이픈 제거 및 파일 기록
Record Biz Number
    [Arguments]    ${raw_biz_no}
    # 1. 하이픈 제거
    ${clean_biz_no}=    Replace String    ${raw_biz_no}    -    ${EMPTY}

    # 2. 파일에 기록
    Append To File    ${bizNo_FILE}    ${clean_biz_no}\n
    Log    기록된 사업자번호: ${clean_biz_no}

    [Return]    ${clean_biz_no}

# 마지막으로 사용했던 사업자 번호 찾기 
Get Last Biz Number
    ${content}=    Get File    ${bizNo_FILE}
    ${lines}=    Split String    ${content}    \n
    ${line_count}=    Get Length    ${lines}
    Run Keyword If    ${line_count} < 2    Fail    No bizNo found in file
    ${last_bizNo}=    Get From List    ${lines}    -2
    [Return]    ${last_bizNo}

# CSO 계정 로그인
Login_CSO
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Sleep    0.5
    Input Text    name=email    ${id_CSO}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Sleep    2

# 제약사 계정 로그인
Login_pharm_pharm1
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Sleep    0.5
    Input Text    name=email    ${id_pharm_1}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Sleep    2

# 삼익제약 계정 로그인
Login_pharm_samik
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Sleep    0.5
    Input Text    name=email    ${id_pharm_2}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Sleep    2

# 로그아웃 
Logout
    Sleep    0.5
    Click Element    xpath=//button[@aria-haspopup='menu']
    Wait Until Element Is Visible    xpath=//div[@title='로그아웃']    5
    Screenshot
    Click Element    xpath=//div[@title='로그아웃']
    Screenshot
    Sleep    1



# [Common] .env 파일에서 변수 강제 로드 (개별 파일 실행용)
Load Login Credentials
    ${env_path}=    Normalize Path    ${CURDIR}/../../common/auth/.env
    ${content}=     Get File    ${env_path}
    ${lines}=       Split To Lines    ${content}
    FOR    ${line}    IN    @{lines}
        ${is_empty}=    Evaluate    '${line}'.strip() == ''
        ${is_comment}=  Evaluate    '${line}'.strip().startswith('#')
        Continue For Loop If    ${is_empty} or ${is_comment}
        
        ${key}    ${val}=    Split String    ${line}    separator==    max_split=1
        Set Global Variable    \${${key.strip()}}    ${val.strip()}
    END
