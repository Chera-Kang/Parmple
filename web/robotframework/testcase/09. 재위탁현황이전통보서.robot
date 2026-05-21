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
1. 재위탁 현황
    Login_pharm_pharm1

    Click Element    xpath=//a[span[text()='재위탁 현황']]
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 현황']    5
    Sleep    2
    Screenshot


1.1. 검색
    # 검색 
    Click Element    xpath=//button[span[text()="상호/법인명"]]
    Wait Until Element Is Visible    xpath=//div[span[text()="사업자등록번호"]]    5
    Screenshot
    Press Keys    NONE    ESC
    Input Text    xpath=//input[@placeholder="검색어를 입력해 주세요"]    휴피
    Screenshot
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


# 1.2. 하위목록 펼침
#     # 펼침 
#     Click Element    xpath=//div[@style[contains(.,'cursor: pointer')]]/i
#     Screenshot
#     Sleep    0.5


2. 이전 통보서 관리
    Click Element    xpath=//a[span[text()='이전 통보서 관리']]
    Sleep    1
    Screenshot


2.1. 업체 정보
    Click Element    xpath=//button[normalize-space(.)='업체 정보']
    Sleep    1
    Click Element    xpath=(//div[@role='gridcell' and @col-id='bizName'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='업체 정보 수정']    5
    Screenshot
