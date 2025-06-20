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
${EMAIL_PREFIX}    chera.workspace
${EMAIL_DOMAIN}    gmail.com

${PYTHON_EXE}    ${EXECDIR}/.venv/Scripts/python.exe

${EMAIL}    None
${bizRegNo}    None

*** Keywords ***
# 이메일 번호 생성 
Generate Unique Email
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d.%H%M')
    ${email}=    Set Variable    ${EMAIL_PREFIX}+${datetime}@${EMAIL_DOMAIN}
    [Return]    ${EMAIL}

# 사업자번호 하이픈 제거
Remove Hyphen From BizNo
    [Arguments]    ${rawBizNo}
    ${cleaned}=    Replace String    ${rawBizNo}    -    ${EMPTY}
    [Return]    ${cleaned}

# 사업자번호 찾기
Check Biz Joinable
    [Arguments]    ${bizRegNo}
    Create Session    parmple    ${API}
    ${endpoint}=       Catenate    SEPARATOR=    /api/v1/companies/    ${bizRegNo}    /status
    ${headers}=        Create Dictionary    accept=*/*
    ${response}=       Get Request    parmple    ${endpoint}    headers=${headers}
    ${code}=           Convert To Integer    ${response.status_code}
    Should Be Equal As Numbers    ${code}    200
    ${json}=           To JSON    ${response.text}
    ${status}=         Get From Dictionary    ${json['data']['detail']}    status
    [Return]           ${status}

# 숫자 섞기 
Shuffle List
    [Arguments]    ${list}
    ${copy}=       Copy List    ${list}
    ${length}=     Get Length    ${copy}
    FOR    ${i}    IN RANGE    ${length}
        ${rand}=     Evaluate    random.randint(0, ${length} - 1)    modules=random
        ${tmp}=      Set Variable    ${copy[${i}]}
        Set List Value    ${copy}    ${i}    ${copy[${rand}]}
        Set List Value    ${copy}    ${rand}    ${tmp}
    END
    [Return]    ${copy}

# 사업자번호 찾기 
Find Valid Biz Number
    ${files}=         List Files In Directory    ${bizRegNo_DIR}    pattern=bizRegNo_*.txt
    ${random_index}=  Evaluate    random.randint(0, len(${files}) - 1)    modules=random
    ${file}=          Get From List    ${files}    ${random_index}
    ${path}=          Catenate    SEPARATOR=/    ${bizRegNo_DIR}    ${file}
    ${content}=       Get File    ${path}
    ${lines}=         Split To Lines    ${content}
    ${shuffled}=      Shuffle List    ${lines}

    ${bizRegNo}=      Set Variable    ${EMPTY}
    ${retry}=         Set Variable    0

    FOR    ${raw}    IN    @{shuffled}
        Exit For Loop If    ${retry} >= ${MAX_RETRY}
        ${bizNo}=      Remove Hyphen From BizNo    ${raw}
        ${status}=     Check Biz Joinable    ${bizNo}
        Run Keyword If    '${status}' == 'UNREGISTERED'    Set Global Variable    ${bizRegNo}    ${bizNo}
        Run Keyword If    '${status}' == 'UNREGISTERED'    Exit For Loop
        ${retry}=      Set Variable    ${retry + 1}
    END

    Run Keyword Unless    ${bizRegNo}    Log    유효한 사업자번호를 찾을 수 없습니다.    WARN
    Run Keyword Unless    ${bizRegNo}    Fatal Error    테스트를 종료합니다: 유효한 사업자번호 없음

    Log To Console    \n선택된 파일 : ${file}
    Log To Console    선택된 사업자번호 : ${bizRegNo}

    [Return]    ${bizRegNo}

# 파일 경로
Get Absolute File Path
    [Arguments]    ${relative_path}
    ${abs}=    Normalize Path    ${EXECDIR}/${relative_path}
    [Return]    ${abs}

# 어드민 로그인 토큰
Get Admin Access Token
    Create Session    parmple_admin    ${API}
    ${payload}=    Create Dictionary
    ...    email=${ADMIN_EMAIL}
    ...    password=${ADMIN_PASSWORD}
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
---- 회원가입
    ## 스탠바이 및 회원가입 시작
    ${result}=    Run Process    python    -c    "import sys; print(sys.executable)"    stdout=PIPE
    
    Wait Until Element Is Visible    class=mb-4
    Click Element    xpath=//button[text()='회원가입']
    Sleep    2

    ## 사업자 번호 입력
    ${bizRegNo}=      Find Valid Biz Number
    Set Suite Variable    ${bizRegNo}
    Sleep    1

    Input Text    id=bizNumber    ${bizRegNo}    # 사업자 번호 입력
    Sleep    1
    Click Element    xpath=//button[text()='확인하기']    # 사업자 번호 입력 후 회원가입 Page 로 진입
    Sleep    1
    Click Element    xpath=//button[text()='확인']
    Sleep    1

    ## 파일 첨부    
    ${abs_path}=    Normalize Path    ${testfile_PATH}
    Choose File     xpath=//*[@id="bizRegCertFileUuid"]//input    ${abs_path}
    Sleep    1
    Choose File     xpath=//*[@id="salesCertFileUuid"]//input    ${abs_path}
    Sleep    1

    # 화면 스크롤
    Scroll Element Into View    xpath=//*[@id="name"]
    Sleep    1

    ## 이메일 입력 
    ${EMAIL}=    Generate Unique Email
    Input Text    id=email    ${EMAIL}    # 이메일 입력
    Set Suite Variable    ${EMAIL}
    Log To Console    \n${EMAIL}

    # 인증번호 발송
    Sleep    1
    Click Element    xpath=//button[text()='인증번호 발송']
    Sleep    1
    Click Element    xpath=//button[text()='확인']
    Sleep    5

    # 인증번호 추출 및 입력 
    ${result}=    Run Process    ${PYTHON_EXE}    support/gmail_reader.py    stdout=PIPE    stderr=PIPE
    ${code}=      Set Variable   ${result.stdout.strip()}
    Log To Console    \n인증번호: ${code}
    Should Not Be Equal    ${code}    NO_CODE

    Input Text    id=emailVerificationKey    ${code}
    Sleep    1
    Click Element    xpath=//button[text()='인증하기']
    Sleep    1

    # 화면 스크롤
    Scroll Element Into View    xpath=//button[text()='가입하기']
    Sleep    1

    ## 비밀번호 입력
    Input Password    id=password    ${password}
    Sleep    1
    Input Password    id=passwordCheck    ${password}
    Sleep    1

    ## 이름 입력
    Input Text    id=name    테스트
    Sleep    1

    ## 휴대폰 번호 입력 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Press Key    id=phone    ${phone_number}
    Sleep    1

    ## 약관 동의
    Click Button    id=termsAll
    Sleep    1

    ## 가입하기 버튼
    Click Button    xpath=//button[text()='가입하기']
    Record BizRegNo To File    ${bizRegNo}
    Sleep    2
    # Wait Until Element Is Visible    id=radix-:r15:    5
    Click Element    xpath=//button[text()='확인']
    Sleep    1
    # 로그인 Page 로 이동


    ## Admin API 승인 Process    
    ${access_token}=    Get Admin Access Token
    ${company_id}=    Get Pending Company Review Id    ${access_token}
    Approve Company Review    ${access_token}    ${company_id}

    Sleep    2

---- Testcase3

    Input Text    name=email    ${EMAIL}
    Press Key    name=password    ${password}
    Sleep    1
    Click Button    xpath=//button[text()='로그인']

    Sleep    5

    Log To Console    ${EMAIL}
    Log To Console    ${bizRegNo}
    ${lastBizReNo}=    Get Last BizRegNo From File
    Log To Console    ${lastBizReNo}



