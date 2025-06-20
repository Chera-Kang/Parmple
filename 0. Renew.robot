*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    String
Library    RequestsLibrary
Library    BuiltIn
Resource   ../support/keywords.robot
Library    Process
Library    DateTime
Resource    ../.secrets.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***
${lastBizReNo}    None
${bizNo}    None


*** Keywords ***
Get Absolute File Path
    [Arguments]    ${relative_path}
    ${abs}=    Normalize Path    ${EXECDIR}/${relative_path}
    [Return]    ${abs}


*** Test Cases ***
---- Testcase

    Wait Until Element Is Visible    xpath=//img[contains(@src, 'logo_200.25f0e37e.png')]    5

    Input Text    name=email    ${id_1}
    Press Key    name=password    ${password}
    Sleep    1
    Click Button    xpath=//button[text()='로그인']
    Sleep    3

    ${lastBizReNo}=    Get Last BizRegNo From File

    # 업체 상세 
    Click Element    xpath=//a[translate(normalize-space(text()), "-", "") = "${lastBizReNo}"]


    ############################################################


    Sleep    1

    Click Button    xpath=//button[@title='재위탁통보서']

    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='통보서 작성하기']    5
    Click Button    xpath=//button[normalize-space(.)='통보서 작성하기']
    Sleep    1

    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='작성하기']    5


    Sleep    1

    Input Text    name=reason    ${EMPTY}
    Sleep    0.5
    Press Key    name=reason    automation test

    Sleep    1

    Input Text    name=note    ${EMPTY}
    Sleep    0.5
    Press Key    name=note    automation test

    Click Element    id=created-date
    Sleep    1
    Press Keys    NONE    ESC
    Sleep    1

    # 화면 스크롤
    Scroll Element Into View   xpath=//button[normalize-space(.)='작성하기']
    Sleep    1


    Click Button    xpath=//button[normalize-space(.)='추가하기']

    Sleep    1

    Click Element    xpath=//*[normalize-space(.)='제약사 명 검색']
    Sleep    1
    Input Text    xpath=//input[@placeholder='제약사 명 검색']    투썬 
    Sleep    2
    Press Keys    xpath=//input[@placeholder='제약사 명 검색']    ENTER
    Sleep    3
    Click Button    xpath=(//button[normalize-space(.)='추가하기'])[2]
    Sleep    1
   


    Click Element    xpath=//button[normalize-space(.)='작성하기']
    Sleep    1
    Wait Until Element Is Visible    xpath=(//button[normalize-space(.)='작성하기'])[2]    5
    Click Button    xpath=(//button[normalize-space(.)='작성하기'])[2]





    Sleep    10


    Press Keys    NONE    ESC
    Sleep    1


    Sleep    5


    # Sleep    1
    # Click Element    xpath=//button[text()='로그인']
    # Sleep    2
    # Click Element    xpath=//a[span[text()='위탁 계약']
    # Sleep    2



# 1. 회원가입
    # 이메일은 이런 형태면 안겹칠듯 chera+auto.25-05-20_17-56-11@twosun.com
# 2. 로그인
# 3. 위탁 계약
# 4. 수탁 계약
# 5. 재위탁 통보서 작성
# 6. 필터링 조회
# 7. 제약사 제품 공지
# 8. 신규 개원 정보

