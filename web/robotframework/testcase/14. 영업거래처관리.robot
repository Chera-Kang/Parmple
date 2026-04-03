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
1. 영업 거래처 관리
    Login_pharm_pharm1

    Scroll Element Into View    xpath=//a[span[text()='영업 거래처 관리']]
    Click Element    xpath=//a[span[text()='영업 거래처 관리']]
    Sleep    1
    Screenshot


2. 거래처 상세 모달
    Click Element    xpath=//span[span[contains(text(), 'Auto')]]
    Wait Until Element Is Visible    xpath=//h2[text()='영업 거래처']    5
    Screenshot


2.1. 영업 상태 변경
    Click Button    xpath=//button[span[text()='변경할 상태 선택']]
    Screenshot
    Click Element    xpath=(//div[span[text()='제품별 승인']])[last()]
    Screenshot


2.2. 상태 저장하기
    Click Button    xpath=//button[text()='저장하기']
    Screenshot


3. 검색 
    Click Element    xpath=//button[span[text()='영업 상태(전체)']]
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5
    Click Element    xpath=//input[@placeholder='마지막 수정일시']
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5
    Click Element    xpath=//button[span[text()='병의원 명']]
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5
    Press Key    xpath=//input[@placeholder='검색어를 입력해 주세요']    휴베이스
    Screenshot
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot

