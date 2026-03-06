*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    String
Library    Collections

*** Variables ***
${URL1}               https://qa.erp.parmple.com/
${URL2}               https://qa.renew.parmple.com/
${SCREENSHOT_DIR}     ../screenshots
${GENERATOR}    file:///C:/Dev/parmple/resources/GENERATOR.html
${VALIDATOR}    file:///C:/Dev/parmple/resources/VALIDATOR.html
${USER_1_ID}    chera-m1@twosun.com
${USER_1_PW}    asdf1234
${USER_2_ID}    chera@twosun.com
${USER_2_PW}    dummy_password123!

# ▲ 기존 버전
# ▼ 리뉴얼 버전

${id_1}    chera+1@twosun.com
${id_2}    pharm1@parmple.com
${id_3}    pharm_manager@example.com
${password}    password123!

${API}               https://qa.api.parmple.com
${bizRegNo_DIR}      resources/bizRegNo
${unused_bizRegNo_DIR}      resources/unused_bizRegNo
${testfile_DIR}    ${EXECDIR}/resources/testfile
${testfile_PATH}   ${EXECDIR}/resources/testfile/Test_Sameple_PDF.pdf

${MAX_RETRY}         5

${BIZREG_FILE}    ${CURDIR}/../resources/used_bizRegNo.txt

*** Keywords ***
Initialize Test Suite
    Log To Console    Initialzing Test Suite
    Log To Console    Opening Browser
    Open Browser    ${URL1}    Chrome
    Maximize Browser Window

Finalize Test Suite
    Log To Console    Closing Browser
    Close Browser

Screenshot
    ${SetTime}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
    Sleep    0.5
    Capture Page Screenshot    ${SCREENSHOT_DIR}/screenshot_${SetTime}.png
    Sleep    0.5

MainMenu Mouse Over
    Mouse Over    class=menu-link
    Sleep    0.5

Open New Tab
    Execute JavaScript    window.open();  # 새로운 탭 열기
    sleep    0.5
    Switch Window    NEW                 # 새로 열린 탭으로 전환
    sleep    0.5

Switch To Tab
    [Arguments]    ${index}
    ${handles}=    Get Window Handles
    Switch Window    ${handles[${index}]}
    sleep    0.5 


Generaotr & Validator
    Open New Tab
    Go To    ${GENERATOR}
    Wait Until Element Is Visible    id=count    5
    Input Text    count    1
    Sleep    0.5

    Open New Tab 
    Go To    ${VALIDATOR}
    Wait Until Element Is Visible    id=numbers    5

    ${is_valid}=    Set Variable    False

    WHILE    not ${is_valid}
        Switch To Tab    1
        Click Element    xpath=//button[@onclick='generateBusinessNumbers()']
        Screenshot
        ${GENERATOR_Number}=    Get Text    id=result

        Switch To Tab    2
        Input Text    numbers    ${GENERATOR_Number}
        Click Element    xpath=//button[@onclick='validateBizRegNos()']
        Wait Until Element Is Visible    class=summary    5
        ${validation_result}=    Get Text    class=summary

        Run Keyword If    '${validation_result}' == '모든 사업자등록번호가 유효합니다.'    Set Global Variable    ${is_valid}    True
        Run Keyword If    not $is_valid    Log To Console    Number invalid, retrying...
    END
    Screenshot
    # Switch To Tab    2
    # Close Window
    # Sleep    0.5
    # Switch To Tab    1
    # Close Window
    # Sleep    0.5
    Switch To Tab    0

    
    # Global 변수 설정
    Set Global Variable    ${GENERATOR_Number}    ${GENERATOR_Number}



# 사업자번호 찾기 
Get Biz Number
    ${files}=         List Files In Directory    ${bizRegNo_DIR}   pattern=bizRegNo_*.txt
    ${random_index}=  Evaluate    random.randint(0, len(${files}) - 1)    modules=random
    ${file}=          Get From List    ${files}    ${random_index}
    ${path}=          Catenate    SEPARATOR=/    ${bizRegNo_DIR}    ${file}
    
    ${content}=       Get File    ${path}
    ${lines}=         Split To Lines    ${content}
    Run Keyword Unless    ${lines}    Fatal Error    사용 가능한 사업자번호가 없습니다: ${file}

    ${last}=          Get From List    ${lines}    -1
    Remove From List  ${lines}    -1
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


# 사용했던 사업자 번호 추출 
Get Last BizRegNo From File
    ${content}=    Get File    ${BIZREG_FILE}
    ${lines}=    Split String    ${content}    \n
    ${line_count}=    Get Length    ${lines}
    Run Keyword If    ${line_count} < 2    Fail    No bizRegNo found in file
    ${last_bizRegNo}=    Get From List    ${lines}    -2
    [Return]    ${last_bizRegNo}

