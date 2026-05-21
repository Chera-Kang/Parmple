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



2. 병의원 상세 Page
    Click Element    xpath=//span[span[contains(text(), 'Auto')]]
    Wait Until Element Is Visible    xpath=//h2[text()='상세 보기']    5
    Screenshot


2.1. 관리코드 수정 
    Click Element    xpath=//td[contains(@class, 'lg:table-cell')]//button[text()='수정']
    Wait Until Element Is Visible    xpath=//h2[text()='관리코드 수정']    5
    Screenshot

    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%y%m%d%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Input Text    name=managementCode    ${managementCode}
    Screenshot

    Click Button    xpath=//button[text()='저장하기']
    Screenshot

    Scroll Element Into View    class=ag-body-horizontal-scroll-viewport
    Screenshot


2.2. 거래처 관리
    Click Button    xpath=//button[@title='관리']
    Wait Until Element Is Visible    xpath=//h2[text()='영업 거래처']    5
    Screenshot

    Click Button    xpath=//button[span[text()='변경할 상태 선택']]
    Screenshot
    Click Element    xpath=(//div[span[text()='제품별 승인']])[last()]
    Screenshot

    Click Button    xpath=//button[text()='저장하기']
    Screenshot


2.3. 거래처 비고
    Click Button    xpath=//button[@title='비고']
    Wait Until Element Is Visible    xpath=//h2[text()='비고']    5
    Screenshot

    Press Key    name=note    자동화테스트
    Screenshot

    Click Button    xpath=//button[text()='저장하기']
    Sleep    1

    Go Back
    Wait Until Page Contains    영업 거래처 관리    5
    Screenshot


3. 검색
    Click Element    xpath=//button[span[text()='영업 상태(전체)']]
    Screenshot

    Press Keys    NONE    ESC
    Sleep    0.5
    Click Element    xpath=//input[@placeholder='등록일시']
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

