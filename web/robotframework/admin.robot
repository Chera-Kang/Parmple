*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    String
Library    RequestsLibrary
Library    BuiltIn
Library    Process
Library    DateTime
Resource   keywords.robot

Suite Setup    Initialize Admin Test Suite
Suite Teardown    Finalize Test Suite


*** Variables ***
*** Keywords ***
*** Test Cases ***
testcase
    Sleep    2
    Input Text    name=email    admin@twosun.com
    Input Text    name=password    password123!
    Sleep    1
    Click Button    xpath=//button[text()='로그인']    
    Sleep    2

    Click Element    xpath=//span[text()='매뉴얼 관리']
    Sleep    1

    FOR    ${i}    IN RANGE    2    100
        Click Element    xpath=//button[text()='추가하기']
        Sleep    1
        Click Element    xpath=//label[text()='CSO']
        Input Text    id=manual-title    CSO-${i}
        Input Text    id=manual-sort    ${i}
        Choose File     xpath=//*[@id="manual-file-uuid"]//input    ${TESTFILE_PATH}
        Sleep    1
        Click Element    xpath=//button[text()='저장하기']    
        Sleep    1
    END
