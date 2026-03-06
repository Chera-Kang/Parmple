*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    String
Library    RequestsLibrary
Library    BuiltIn
Library    Process
Library    DateTime
Resource   ../resources/keywords.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***
*** Keywords ***
*** Test Cases ***

5.1. 필터링
    Login_CSO
    Sleep    1


5.1.1. 필터링 직접 조회
    Scroll Element Into View    xpath=//a[span[text()='필터링 직접 조회']]
    Click Element    xpath=//a[span[text()='필터링 직접 조회']]
    Sleep    1
    Screenshot


5.1.2. 병의원 검색
    Press Key    xpath=//input[@placeholder='병의원명 검색 후 리스트를 선택해 주세요']    오토
    Sleep    2
    Screenshot

    Press Keys    xpath=//input[@placeholder='병의원명 검색 후 리스트를 선택해 주세요']    ENTER
    Screenshot

    Press Key    xpath=//input[@placeholder='사업자 등록번호 (-없이 숫자만 가능)']    1234567890
    Screenshot

    Click Element    xpath=//button[span[text()='조회하기']]
    Screenshot


5.2. 필터링 조회 이력
    Logout
    Login_pharm_samik

    Scroll Element Into View    xpath=//a[span[text()='필터링 조회 이력']]
    Click Element    xpath=//a[span[text()='필터링 조회 이력']]
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 조회 이력']
    Screenshot

    # 병의원 검색 
    Click Element    xpath=//button[span[text()='병의원명']]
    Screenshot

    Press Keys    NONE    ESC
    Sleep    0.5
    Press Key    xpath=//input[@placeholder='검색어를 입력해 주세요']    강남
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Screenshot
