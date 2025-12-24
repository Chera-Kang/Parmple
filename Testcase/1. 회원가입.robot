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
Resource    ../resources/.secrets.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite


*** Variables ***
${EMAIL_PREFIX}    chera.workspace
${EMAIL_DOMAIN}    gmail.com

${PYTHON_EXE}    ${EXECDIR}/.venv/Scripts/python.exe

${EMAIL}    None
${bizRegNo}    None


*** Keywords ***
# 이메일 번호 생성 
Generate Email
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d.%H%M')
    ${email}=    Set Variable    ${EMAIL_PREFIX}+${datetime}@${EMAIL_DOMAIN}
    [Return]    ${EMAIL}


# 어드민 로그인 토큰
Get Admin Access Token
    Create Session    parmple_admin    ${API}
    ${payload}=    Create Dictionary
    ...    email=${ADMIN_EMAIL}
    ...    password=${password}
    ${headers}=    Create Dictionary    accept=*/*    Content-Type=application/json
    ${response}=    Post Request    parmple_admin    /api/v1/admins/auth/login    json=${payload}    headers=${headers}
    
    Log To Console    응답 코드: ${response.status_code}
    # Log To Console    응답 내용: ${response.text}

    Should Be Equal As Numbers    ${response.status_code}    200
    
    ${json}=    To JSON    ${response.text}
    ${data}=    Get From Dictionary    ${json}    data
    ${detail}=    Get From Dictionary    ${data}    detail
    ${access_token}=    Get From Dictionary    ${detail}    accessToken
    [Return]    ${access_token}


# 어드민 승인요청관리 목록 
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
    # Log To Console    응답 내용: ${response.text}

    Should Be Equal As Numbers    ${response.status_code}    200

    ${json}=    To JSON    ${response.text}

    ${data}=    Get From Dictionary    ${json}    data
    ${items}=   Get From Dictionary    ${data}    items

    ${company_id}=    Get From Dictionary    ${items}[0]    id

    [Return]    ${company_id}


# 어드민 승인처리
Approve Company Review
    [Arguments]    ${access_token}    ${company_id}
    Create Session    parmple_admin    ${API}
    ${headers}=    Create Dictionary    accept=*/*    Authorization=Bearer ${access_token}    Content-Type=application/json
    ${payload}=    Create Dictionary    csoReportNo=자동화테스트
    ${endpoint}=    Set Variable    /api/v1/admins/company-reviews/${company_id}/approve
    ${response}=    Post Request    parmple_admin    ${endpoint}    json=${payload}    headers=${headers}

    Log To Console    승인 응답 코드: ${response.status_code}
    # Log To Console    승인 응답 내용: ${response.text}

    Should Be Equal As Numbers    ${response.status_code}    200


*** Test Cases ***
1.1. 로그인 Page
    ## 사전 준비
    ${result}=    Run Process    python    -c    "import sys; print(sys.executable)"    stdout=PIPE
    
    ## 로그인 Page 
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Screenshot

    # # 회원가입 버튼
    Execute Javascript    document.body.style.zoom='90%'
    Click Element    xpath=//a[text()='회원가입']
    Execute Javascript    document.body.style.zoom='100%'

1.1.1. 사업자 번호 입력
    Wait Until Element Is Visible    xpath=//input[@placeholder="-없이 숫자만 입력해 주세요"]    5
    Screenshot
    
    ## 사업자 번호 입력
    ${bizRegNo}=      Get Biz Number
    ${cleanBizNo}=    Remove Hyphen From BizNo    ${bizRegNo}
    Record BizRegNo To File    ${cleanBizNo}

    Input Text    id=bizNumber    ${cleanBizNo}
    Screenshot

    Click Element    xpath=//button[text()='확인']
    Wait Until Element Is Visible    xpath=//h2[text()='신규 가입 가능한 사업자번호 입니다']    5
    Screenshot
    
    Click Element    xpath=(//button[text()='확인'])[last()]
    Wait Until Element Is Visible    xpath=//h1[text()='회원가입']    5
    Screenshot

1.2.1. 파일 첨부
    ## 파일 첨부    
    Choose File     xpath=//*[@id="bizRegCertFileUuid"]//input    ${testfile_PATH}
    Sleep    0.5
    Choose File     xpath=//*[@id="salesCertFileUuid"]//input    ${testfile_PATH}
    Screenshot

    # 화면 스크롤
    Scroll Element Into View    xpath=//*[@id="name"]
    Sleep    0.5

1.2.2. 이메일 입력 및 인증
    ## 이메일 입력 
    ${EMAIL}=    Generate Email
    Set Suite Variable    ${EMAIL}
    Input Text    id=email    ${EMAIL}
    Log To Console    \n${EMAIL}
    Screenshot

    # 인증번호 발송
    Click Element    xpath=//button[text()='인증번호 발송']
    Wait Until Element Is Visible    xpath=//h2[text()='이메일로 인증번호를 발송했습니다.']    5
    Screenshot
    Click Element    xpath=//button[text()='확인']
    Sleep    5

    # 인증번호 추출 및 입력 
    ${result}=    Run Process    ${PYTHON_EXE}    resources/email_reader.py    stdout=PIPE    stderr=PIPE
    ${code}=      Set Variable   ${result.stdout.strip()}
    Log To Console    \n인증번호: ${code}
    Should Not Be Equal    ${code}    NO_CODE

    Input Text    id=emailVerificationKey    ${code}
    Screenshot
    Click Element    xpath=//button[text()='인증하기']
    Screenshot

    # 화면 스크롤
    Scroll Element Into View    xpath=//div[button[@id='termsAll']]
    Sleep    0.5

1.2.3. 비밀번호 입력
    ## 비밀번호 입력
    Input Password    id=password    ${password}
    Input Password    id=passwordCheck    ${password}

1.2.4. 회원정보 입력
    ## 이름 입력
    Input Text    id=name    테스트
    
    ## 휴대폰 번호 입력 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Press Key    id=phone    ${phone_number}
    Screenshot

1.2.5. 약관 동의
    ## 약관 동의
    Scroll Element Into View    xpath=//button[text()='가입하기']
    Click Button    id=termsAll
    Screenshot

1.2.6. 가입하기
    ## 가입하기 버튼
    Click Button    xpath=//button[text()='가입하기']
    Wait Until Element Is Visible    xpath=//button[text()='확인']    5
    Screenshot
    
    # 로그인 Page 로 이동
    Click Element    xpath=//button[text()='확인']
    Screenshot

1.3. Admin 승인 절차
    ## Admin API 승인 Process    
    ${access_token}=    Get Admin Access Token
    ${company_id}=    Get Pending Company Review Id    ${access_token}
    Approve Company Review    ${access_token}    ${company_id}
    Sleep    1

1.4. 로그인
    Input Text    name=email    ${EMAIL}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Wait Until Element Is Visible    xpath=//h2[text()='내 정보']    5
    Screenshot

    