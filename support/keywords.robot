*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem

*** Variables ***
${URL}               https://qa.erp.parmple.com/
${SCREENSHOT_DIR}     ../screenshots
${GENERATOR}    file:///C:/Dev/robotframework/assets/GENERATOR.html
${VALIDATOR}    file:///C:/Dev/robotframework/assets/VALIDATOR.html
${USER_1_ID}    chera-m1@twosun.com
${USER_1_PW}    asdf1234
${USER_2_ID}    chera@twosun.com
${USER_2_PW}    dummy_password123!

*** Keywords ***
Initialize Test Suite
    Log To Console    Initialzing Test Suite
    Log To Console    Opening Browser
    Open Browser    ${URL}    Chrome
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

