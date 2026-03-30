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
6.0. 자료실 (신규 개원정보)
    Login_CSO

    Scroll Element Into View    xpath=//a[span[text()='신규 개원 정보']]
    Click Element    xpath=//a[span[text()='신규 개원 정보']]
    Wait Until Element Is Visible    xpath=//h2[text()='신규 개원 정보']    5

    # 지역
    Click Element    xpath=//button[normalize-space(.)='지역(전체)']
    Screenshot
    Click Element    xpath=//div[button[span[normalize-space(.)='광주']]]
    Screenshot
    Scroll Element Into View    xpath=//div[span[span[text()='01']]]
    Sleep    1
    Click Element    xpath=//button[normalize-space(.)='적용']
    Screenshot

    # 구분
    Click Element    xpath=//button[normalize-space(.)='구분(전체)']
    Screenshot
    Press Keys    NONE    ESC

    # 진료 과목
    Click Element    xpath=//button[normalize-space(.)='진료 과목(전체)']
    Click Element    xpath=//div[button[span[normalize-space(.)='결핵과']]]
    Scroll Element Into View    xpath=//div[span[span[text()='01']]]
    Click Element    xpath=//button[normalize-space(.)='적용']
    Screenshot

