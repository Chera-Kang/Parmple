*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    String
Library    Collections
Library    DateTime
Library    Process
Resource    ../resources/.secrets.robot

*** Variables ***
# Service URL
${URL}    https://qa.erp.parmple.com/
# Account
${id_CSO}    chera+1@twosun.com
${id_pharm_1}    pharm1@parmple.com
${id_pharm_2}    pharm_manager@example.com
# API
${API}               https://qa.api.parmple.com
# DIR
${screenshot_DIR}     ../screenshots
${testfile_DIR}    ${CURDIR}/testfile
${testfile_PATH}   ${testfile_DIR}/Sameple_PDF.pdf
${bizRegNo_DIR}    ${CURDIR}/bizRegNo
${bizReg_FILE}    ${CURDIR}/used_bizRegNo.txt
${PYTHON_EXE}    ${CURDIR}/../.venv/Scripts/python.exe
${GSHEET_READER_PY}    ${CURDIR}/gsheet_reader.py
${MAX_RETRY}         5


*** Keywords ***
# Test Suite 실행
Initialize Test Suite
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
    Capture Page Screenshot    ${SCREENSHOT_DIR}/screenshot_${SetTime}.png
    Sleep    0.5


# 사업자번호 찾기 (Google Sheet)
Get Biz Number
    # Google Sheet에서 사업자번호 가져오기 (A열 체크박스=FALSE인 행 중 F열 데이터)
    ${result}=    Run Process    ${PYTHON_EXE}    ${GSHEET_READER_PY}    stdout=PIPE    stderr=PIPE
    ${biz_no}=    Set Variable   ${result.stdout.strip()}
    
    # 에러 및 결과 확인
    Should Not Contain    ${biz_no}    ERROR    msg=Google Sheet 처리 중 오류 발생: ${biz_no}
    Should Not Be Equal   ${biz_no}    NO_BIZ_NO    msg=사용 가능한 사업자번호가 스프레드시트에 없습니다.
    
    Log To Console    \n[Google Sheet] 선택된 사업자번호 : ${biz_no}
    [Return]          ${biz_no}


# 사업자번호 하이픈 제거
Remove Hyphen From BizNo
    [Arguments]    ${rawBizNo}
    ${cleaned}=    Replace String    ${rawBizNo}    -    ${EMPTY}
    [Return]    ${cleaned}


# 사용한 사업자번호 기록
Record BizRegNo To File
    [Arguments]    ${bizRegNo}
    Append To File    ${BIZREG_FILE}    ${bizRegNo}\n
    Log    기록된 사업자번호: ${bizRegNo}


# 마지막으로 사용했던 사업자 번호 찾기 
Get Last BizRegNo From File
    ${content}=    Get File    ${BIZREG_FILE}
    ${lines}=    Split String    ${content}    \n
    ${line_count}=    Get Length    ${lines}
    Run Keyword If    ${line_count} < 2    Fail    No bizRegNo found in file
    ${last_bizRegNo}=    Get From List    ${lines}    -2
    [Return]    ${last_bizRegNo}


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

