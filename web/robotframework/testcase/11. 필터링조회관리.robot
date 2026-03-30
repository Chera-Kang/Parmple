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
    Login_pharm_pharm1

    Scroll Element Into View    xpath=//a[span[text()='필터링 조회 관리']]
    Click Element    xpath=//a[span[text()='필터링 조회 관리']]
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 조회 관리']    5
    Screenshot

    # 조건 관리
    Click Element    xpath=//button[@title='조건 관리']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 조건 관리']    5
    Screenshot

    Click Element    xpath=//button[@title='저장하기']
    Wait Until Element Is Visible    xpath=//h2[text()='저장할까요?']
    Screenshot
    Click Element    xpath=//button[@title='확인']
    Sleep    1

    # 실적 관리
    Click Element    xpath=//button[@title='실적 관리']
    Wait Until Element Is Visible    xpath=//h2[text()='실적 관리']    5
    Screenshot

    # 처방월 설정
    Click Element    xpath=//button[@title='처방월 설정']
    Wait Until Element Is Visible    xpath=//h2[text()='처방월 설정']    5
    Screenshot
    Press Keys    None    ESC
    Sleep    1

    # 일괄 추가
    Click Element    xpath=//button[@title='일괄추가']
    Wait Until Element Is Visible    xpath=//h2[text()='일괄추가']    5
    Screenshot
    Press Keys    None    ESC
    Sleep    1

    # 병의원 검색
    Press Key    xpath=//input[@placeholder="검색어를 입력해 주세요"]    테스트
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Sleep    1
    Screenshot

    Go Back
    Sleep    1

