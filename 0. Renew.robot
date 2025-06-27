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
*** Keywords ***
*** Test Cases ***
---- Testcase

    Wait Until Element Is Visible    xpath=//img[contains(@src, 'logo_200.25f0e37e.png')]    5

    Input Text    name=email    ${id_1}
    Press Key    name=password    ${password}
    Sleep    1
    Click Button    xpath=//button[text()='로그인']
    Sleep    3


    #################################################

    Sleep    1
    # Click Element    xpath=//button[span[text()="사업자상태 (전체)"]]
    Click Element    xpath=//button[normalize-space(.)='상태 (전체)']

    Sleep    1



    #################################################


    Press Keys    NONE    ESC
    Sleep    10


    # Go Back

    # Sleep    1
    # Click Element    xpath=//button[text()='로그인']
    # Sleep    2
    # Click Element    xpath=//a[span[text()='위탁 계약']]
    # Sleep    2

    # Click Button    xpath=//button[normalize-space(.)='저장하기']
    # Click Button    xpath=//button[@title='재위탁통보서']
    # xpath=//input[@placeholder='제약사 명 검색']
    # xpath=//button[text()='작성하기']
    # xpath=//h3[text()='계약 관리']

    # # 화면 스크롤
    # Scroll Element Into View    xpath=//*[normalize-space(.)='로그아웃']
    # Sleep    0.5


# 1. 회원가입
    # 이메일은 이런 형태면 안겹칠듯 chera+auto.25-05-20_17-56-11@twosun.com
# 2. 로그인
# 3. 위탁 계약
# 4. 수탁 계약
# 5. 재위탁 통보서 작성
# 6. 필터링 조회
# 7. 제약사 제품 공지
# 8. 신규 개원 정보

