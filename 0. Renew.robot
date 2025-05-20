*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Resource   ../support/keywords.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***

*** Keywords ***

*** Test Cases ***
---- Testcase (로그인)
    Wait Until Element Is Visible    class=mb-4

    Input Text    name=email    ${USER_RN_CSO_1}
    Input Text    name=password    ${USER_RN_PW}

    Sleep    1
    Click Element    xpath=//button[text()='로그인']
    Sleep    2

    Click Element    xpath=//a[span[text()='위탁 계약']]
    Sleep    2

    Click Element    xpath=//a[span[text()='수탁 계약']]
    Sleep    2
    
    Click Element    xpath=//a[span[text()='재위탁 통보서 작성']]
    Sleep    2
    
    Click Element    xpath=//a[span[text()='필터링 조회']]
    Sleep    2
    
    Click Element    xpath=//a[span[text()='제약사 제품 공지']]
    Sleep    2

    Click Element    xpath=//a[span[text()='신규 개원 정보']]
    Sleep    2
    
    Click Element    xpath=//a[span[text()='CSO 제품 정보']]
    Sleep    2



---- Testcase

    Log To Console    -Succese-
    Sleep    5


    