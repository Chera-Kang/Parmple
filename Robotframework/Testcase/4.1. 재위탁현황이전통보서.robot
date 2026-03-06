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
4.4. 재위탁 현황


    Login_pharm_pharm1
    Sleep    1



    Click Element    xpath=//a[span[text()='재위탁 현황']]
    Sleep    1
    Screenshot

    # 검색 
    Click Element    xpath=//button[span[text()="상호/법인명"]]
    Wait Until Element Is Visible    xpath=//div[span[text()="사업자등록번호"]]    5
    Screenshot
    Press Keys    NONE    ESC
    Press Key    xpath=//input[@placeholder="검색어를 입력해 주세요"]    휴피스
    Screenshot
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot

    # 펼침 
    Click Element    xpath=//div[@style[contains(.,'cursor: pointer')]]/i
    Screenshot
    Sleep    0.5


4.5. 이전 통보서 관리
    Sleep    1

    Click Element    xpath=//a[span[text()='이전 통보서 관리']]
    Sleep    1
    Screenshot

