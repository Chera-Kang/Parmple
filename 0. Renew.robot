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

Get Admin Access Token
    Create Session    parmple_admin    ${API}
    ${payload}=    Create Dictionary
    ...    email=${ADMIN_EMAIL}
    ...    password=${ADMIN_PASSWORD}
    ${headers}=    Create Dictionary    accept=*/*    Content-Type=application/json
    ${response}=    Post Request    parmple_admin    /api/v1/admins/auth/login    json=${payload}    headers=${headers}
    
    Log To Console    응답 코드: ${response.status_code}
    Log To Console    응답 내용: ${response.text}

    Should Be Equal As Numbers    ${response.status_code}    200
    
    ${json}=    To JSON    ${response.text}
    ${data}=    Get From Dictionary    ${json}    data
    ${detail}=    Get From Dictionary    ${data}    detail
    ${access_token}=    Get From Dictionary    ${detail}    accessToken
    [Return]    ${access_token}



Get Pending Company Review Id
    [Arguments]    ${access_token}
    Create Session    parmple_admin    ${API}

    ${filter_model}=    Create Dictionary
    ${sort_model}=      Create Dictionary    createdAt=desc

    ${payload}=    Create Dictionary
    ...    filterModel=${filter_model}
    ...    sortModel=${sort_model}
    ...    page=1
    ...    size=50

    ${headers}=    Create Dictionary
    ...    accept=*/*
    ...    Authorization=Bearer ${access_token}
    ...    Content-Type=application/json

    ${response}=    Post Request    parmple_admin    /api/v1/admins/company-reviews/search    json=${payload}    headers=${headers}

    Log To Console    응답 코드: ${response.status_code}
    Log To Console    응답 내용: ${response.text}

    Should Be Equal As Numbers    ${response.status_code}    200

    ${json}=    To JSON    ${response.text}

    ${data}=    Get From Dictionary    ${json}    data
    ${items}=   Get From Dictionary    ${data}    items

    ${company_id}=    Get From Dictionary    ${items}[0]    id

    [Return]    ${company_id}



Approve Company Review
    [Arguments]    ${access_token}    ${company_id}
    Create Session    parmple_admin    ${API}
    ${headers}=    Create Dictionary    accept=*/*    Authorization=Bearer ${access_token}    Content-Type=application/json
    ${payload}=    Create Dictionary    csoReportNo=테스트
    ${endpoint}=    Set Variable    /api/v1/admins/company-reviews/${company_id}/approve
    ${response}=    Post Request    parmple_admin    ${endpoint}    json=${payload}    headers=${headers}

    Log To Console    승인 응답 코드: ${response.status_code}
    Log To Console    승인 응답 내용: ${response.text}

    Should Be Equal As Numbers    ${response.status_code}    200


*** Test Cases ***
---- Testcase (로그인)

    Log To Console    -Succese-

    Log To Console    ${ADMIN_EMAIL}
    Log To Console    ${ADMIN_PASSWORD}

    Sleep    5

    ${access_token}=    Get Admin Access Token
    Log To Console    \n${access_token}
    Log To Console    ADMIN_EMAIL: ${ADMIN_EMAIL}
    Log To Console    ADMIN_PASSWORD: ${ADMIN_PASSWORD}
    Log To Console    API: ${API}


    ${company_id}=    Get Pending Company Review Id    ${access_token}
    Log To Console    승인할 회사 ID: ${company_id}
    Approve Company Review    ${access_token}    ${company_id}
    




    Sleep    3





    # Sleep    1
    # Click Element    xpath=//button[text()='로그인']
    # Sleep    2
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

