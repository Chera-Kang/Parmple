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
1. 필터링 직접 조회
    Login_CSO

    Scroll Element Into View    xpath=//a[span[text()='필터링 직접 조회']]
    Click Element    xpath=//a[span[text()='필터링 직접 조회']]
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 직접 조회']    5
    Screenshot


1.1. 업체 선택
    Click Element    xpath=//button[@role='combobox' and contains(., '제약사를 선택해 주세요')]
    Wait Until Element Is Visible    xpath=(//div[span[contains(text(), '투썬')]])[last()]    5
    Screenshot

    Click Element    xpath=(//div[span[contains(text(), '투썬')]])[last()]
    Screenshot


1.2. 공지사항
    Click Element    xpath=//button[text()='다음']
    Screenshot


1.3. 병의원 검색
    Click Element    xpath=//button[text()='다음']
    Screenshot

    Press Key    xpath=//input[@placeholder='병의원명을 입력해 주세요']    자동화테스트
    Wait Until Element Is Visible    xpath=//div[span[span[text()='자동화테스트']]]    5
    Click Element    xpath=//div[span[span[text()='자동화테스트']]]
    Screenshot

    Input Text    xpath=//input[@placeholder='-없이 숫자만 가능']    6046400707
    Screenshot
    

1.4. 조회 결과
    Click Element    xpath=//button[text()='조회하기']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 조회 결과']    5
    Screenshot
    
    Press Keys    None    ESC
    Sleep    0.5


2. 검색
    Click Element    xpath=//button[span[text()='조회 결과(전체)']]
    Screenshot
    Click Element    xpath=(//div[span[text()="거래 불가"]])[last()]
    Screenshot

    Click Element    id=date
    Screenshot
    Press Keys    None    ESC
    Sleep    0.5

    Click Element    xpath=//button[span[text()='병의원 명']]
    Screenshot
    Press Keys    None    ESC
    Sleep    0.5

    Press Key    xpath=//input[@placeholder="검색어를 입력해 주세요"]    테스트96
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Screenshot

