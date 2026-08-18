*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    String
Library    RequestsLibrary
Library    BuiltIn
Library    Process
Library    DateTime
Resource   ../keywords.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite


*** Variables ***
*** Keywords ***
*** Test Cases ***
1. 받은 재위탁 통보서
    Login_pharm_pharm1

    Click Element    xpath=//a[span[text()='받은 재위탁 통보서']]
    Sleep    1
    Screenshot


1.1. 재위탁 통보서
    Click Button    xpath=//button[@title='통보서']
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


1.2. 첨부파일
    Click Element    xpath=(//button[@title='파일'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='파일']    5


1.3. 계약서
    Sleep    2
    Screenshot


1.4. 수수료율
    Click Element    xpath=//button[normalize-space(.)='수수료율']
    Sleep    2
    Screenshot


1.5. 수료증
    Click Element    xpath=//button[normalize-space(.)='수료증']
    Sleep    2
    Screenshot


1.6. 수료증(재위탁)
    Click Element    xpath=//button[normalize-space(.)='수료증(재위탁)']
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5
