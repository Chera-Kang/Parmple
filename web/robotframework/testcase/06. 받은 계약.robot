*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    String
Library    RequestsLibrary
Library    BuiltIn
Library    Process
Library    DateTime
Library    ../../../.venv/Lib/site-packages/robot/libraries/XML.py
Resource   ../keywords.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***
*** Keywords ***
*** Test Cases ***
5.1. 받은 전자 계약
    Login_CSO3

    # 전자계약 메뉴 
    Click Element    xpath=//a[span[text()='받은 계약서']]
    Wait Until Element Is Visible    xpath=//h2[text()='받은 계약서']    5
    Sleep    1

계약서 보기
    Click Element    xpath=//button[@title='계약서']
    Sleep    2
    Screenshot
    Press Keys    None    ESC
    Sleep    1

서명하기
    Click Element    xpath=//button[@title='서명하기']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서']    5
    Sleep    1
    Screenshot

    Click Element    xpath=//button[text()='서명하기'][last()]
    Wait Until Element Is Visible    xpath=//h2[text()='서명하기']    5
    Screenshot

    Click Element    xpath=//button[i[contains(@class, 'ri-arrow-down-s-line')]]
    Screenshot

    Click Element    id=termsAll
    Screenshot

    # 서명하기 버튼 클릭 (가로막힘 및 중복 버튼 대응: 마지막 submit 버튼 클릭)
    Execute Javascript    var btns = document.querySelectorAll("button[title='서명하기'][type='submit']"); if(btns.length > 0) btns[btns.length - 1].click();
    Wait Until Element Is Visible    xpath=//h2[text()='계약서에 서명하였습니다']
    Screenshot

    Click Element    xpath=//button[text()='확인']
    Sleep    1

    Screenshot

