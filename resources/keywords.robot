*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    String
Library    Collections
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
${testfile_DIR}    ${EXECDIR}/resources/testfile
${testfile_PATH}   ${testfile_DIR}/Sameple_PDF.pdf
${bizRegNo_DIR}    ${EXECDIR}/resources/bizRegNo
${bizReg_FILE}    ${EXECDIR}/resources/bizRegNo/used_bizRegNo.txt
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


# 사업자번호 찾기 
Get Biz Number
    ${files}=         List Files In Directory    ${bizRegNo_DIR}   pattern=bizRegNo_*.txt
    ${random_index}=  Evaluate    random.randint(0, len(${files}) - 1)    modules=random
    ${file}=          Get From List    ${files}    ${random_index}
    ${path}=          Catenate    SEPARATOR=/    ${bizRegNo_DIR}    ${file}
    
    ${content}=       Get File    ${path}
    ${lines}=         Split To Lines    ${content}
    Run Keyword Unless    ${lines}    Fatal Error    사용 가능한 사업자번호가 없습니다: ${file}

    # 사용한 번호 제거
    ${last}=          Get From List    ${lines}    -1    
    Remove From List  ${lines}    -1
    # 사용한 번호 기록
    ${new_content}=   Catenate    SEPARATOR=\n    @{lines}
    Create File       ${path}    ${new_content}
    
    Log To Console    \n선택된 파일 : ${file}
    Log To Console    사용된 사업자번호 : ${last}

    [Return]          ${last}


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
    Sleep    0.5
    Input Text    name=email    ${id_CSO}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Sleep    2


# 제약사 계정 로그인
Login_pharm_pharm1
    Sleep    0.5
    Input Text    name=email    ${id_pharm_1}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Sleep    2


# 삼익제약 계정 로그인
Login_pharm_samik
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

