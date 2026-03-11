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
3.7. 수탁 계약 

    Login_CSO
    Sleep    1
    Screenshot

    
    Click Element    xpath=//a[span[text()='수탁 계약']]
    Sleep    1
    Screenshot

    # 검색 
    Click Element    xpath=//button[span[text()="상호/법인명"]]
    Screenshot

    Press Keys    NONE    ESC
    Press Key    xpath=//input[@placeholder="검색어를 입력해 주세요"]    투썬
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


3.7.1. 수탁 업체 상세
    Click Element    xpath=//a[text()='842-88-83121']
    Wait Until Element Is Visible    xpath=//h2[text()='업체 상세 보기']    5
    Screenshot


3.7.2. 첨부자료
    Sleep    1


3.7.2.1. 사업자등록증
    Click Button    xpath=//button[text()='보기']
    Wait Until Element Is Visible    xpath=//h2[text()='사업자등록증']    5
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC


3.7.2.2. 계약관리 - 수수료율
    Click Button    xpath=//button[@title='수수료율']
    Wait Until Element Is Visible    xpath=//h2[text()='수수료율']    5
    Screenshot
    Press Keys    NONE    ESC


3.7.2.3. 계약관리 - 계약서
    Click Button    xpath=//button[@title='계약서']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서']    5
    Sleep    1
    Screenshot
    Press Keys    NONE    ESC

