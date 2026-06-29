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
1. 상위 업체 조회 Page
    Login_CSO
    
    Click Element    xpath=//a[span[text()='상위 업체 조회']]
    Wait Until Element Is Visible    xpath=//h2[text()='상위 업체 조회']    5
    Screenshot


1.1. 검색
    Click Element    xpath=//button[span[span[text()="상호/법인명"]]]
    Screenshot

    Press Keys    NONE    ESC
    Press Key    xpath=//input[@placeholder="검색어를 입력해 주세요"]    투썬
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


2. 상위 업체 상세 (제약사)
    Click Element    xpath=//a[text()='842-88-83121']
    Wait Until Element Is Visible    xpath=//h2[text()='상세 보기']    5
    Screenshot


2.1. 사업자등록증
    Click Button    xpath=(//button[text()='보기'])[last()]
    Wait Until Element Is Visible    xpath=//h2[text()='사업자등록증']    5
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC


2.2. 계약관리 - 수수료율
    Scroll Element Into View    xpath=//button[@title='처음']
    Screenshot

    # 계약서탭으로 이동
    Click Button    xpath=//button[@title='수수료율']
    Wait Until Element Is Visible    xpath=//h2[text()='수수료율']    5
    Screenshot
    Press Keys    NONE    ESC


2.3. 계약서
    Click Button    xpath=//button[@title='계약서']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서']    5
    Sleep    1
    Screenshot
    Press Keys    NONE    ESC


3. 상위 업체 상세 (CSO)
    Go Back
    Wait Until Element Is Visible    xpath=//h2[text()='상위 업체 조회']    5
    Screenshot
    
    Click Element    xpath=//a[text()='129-86-37855']
    Wait Until Element Is Visible    xpath=//h2[text()='상세 보기']    5
    Screenshot


3.1. 사업자등록증
    Click Button    xpath=(//button[text()='보기'])[last()]
    Wait Until Element Is Visible    xpath=//h2[text()='사업자등록증']    5
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC


3.3. 계약관리 - 수수료율
    Scroll Element Into View    xpath=//button[@title='처음']
    Screenshot

    Click Button    xpath=//button[@title='수수료율']
    Wait Until Element Is Visible    xpath=//h2[text()='수수료율']    5
    Screenshot
    Press Keys    NONE    ESC


3.4. 계약관리 - 계약서
    Click Button    xpath=//button[@title='계약서']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서']    5
    Sleep    1
    Screenshot
    Press Keys    NONE    ESC

