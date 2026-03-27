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

2.1 프로필
    Login_CSO

    Scroll Element Into View    xpath=//a[span[text()='필터링 직접 조회']]
    Click Element    xpath=//a[span[text()='필터링 직접 조회']]
    Sleep    1
    
    Click Element    xpath=//button[@role='combobox' and contains(., '제약사를 선택해 주세요')]
    Sleep    1

    # Click Element    xpath=//span[text()='투썬제약'][last()]
    Press Keys    None    ARROW_DOWN
    Press Keys    None    ARROW_DOWN
    Press Keys    None    ENTER
    Sleep    1

    Click Element    xpath=//button[text()='다음']
    Sleep    1

    Click Element    xpath=//button[text()='다음']
    Sleep    1


    # 병의원 검색
    Press Key    xpath=//input[@placeholder='병의원명을 입력해 주세요']    자동화테스트
    Sleep    1

    Press Keys    None    ENTER
    Sleep    1

    Press Key    xpath=//input[@placeholder='-없이 숫자만 가능']    6046400707
    Sleep    1
    
    Click Element    xpath=//button[text()='조회하기']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 조회 결과']    5
    Sleep    1
    
    Press Keys    None    ESC
    Sleep    1



    # 검색
    Click Element    xpath=//button[span[text()='조회 결과(전체)']]
    Sleep    1

    Click Element    xpath=(//div[span[text()="거래 불가"]])[last()]
    Sleep    1

    Click Element    id=date
    Sleep    1
    Press Keys    None    ESC
    Sleep    1

    Click Element    xpath=//button[span[text()='병의원 명']]
    Sleep    1
    Press Keys    None    ESC
    Sleep    1

    Press Key    xpath=//input[@placeholder="검색어를 입력해 주세요"]    테스트96
    Sleep    1

    Click Element    xpath=//button[span[text()='검색']]
    Sleep    1