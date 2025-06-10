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
Resource    ../support/secrets.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite


*** Variables ***


*** Keywords ***


*** Test Cases ***
---- Testcase (로그인)

    Log To Console    -Succese-

    Log To Console    ${ADMIN_EMAIL}
    Log To Console    ${ADMIN_PASSWORD}

    Sleep    5




    # Sleep    1
    # Click Element    xpath=//button[text()='로그인']
    # Sleep    2
    # Input Text    name=email    ${USER_RN_CSO_1}
    # Input Text    name=password    ${USER_RN_PW}

    # Click Element    xpath=//a[span[text()='위탁 계약']]
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

