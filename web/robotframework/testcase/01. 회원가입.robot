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
# 어드민 승인 대상 ID 조회 및 승인 처리
Approve Pending Company Review Via Admin API
    # 리뷰 ID 조회
    ${result_id}=    Run Process    ${PYTHON_EXE}    ${ADMIN_API_PY}    get_review_id    stdout=PIPE    stderr=PIPE
    ${company_id}=   Set Variable   ${result_id.stdout.strip()}
    Run Keyword If    '${company_id}' == 'None' or '${company_id}' == ''    Fail    승인 대기 중인 업체를 찾을 수 없습니다.
    
    # 승인 처리
    ${result_app}=   Run Process    ${PYTHON_EXE}    ${ADMIN_API_PY}    approve    ${company_id}    stdout=PIPE    stderr=PIPE
    Should Be Equal  ${result_app.stdout.strip()}    SUCCESS    msg=어드민 승인 처리에 실패했습니다: ${result_app.stderr}
    
    # 결과 출력
    Log To Console    \n---------------------------------------
    Log To Console    company id : ${company_id}
    Log To Console    ---------------------------------------


# 테스트용 업체 데이터 준비 (등록 업체 조회 및 변수 설정)
Setup Registered Company Data
    ${item}=    Get Registered Company Info From Admin
    
    ${registeredBizName}=    Get From Dictionary    ${item}    bizName
    ${registeredBizNo}=      Get From Dictionary    ${item}    bizRegNo
    ${registeredCsoNo}=      Get From Dictionary    ${item}    csoReportNo

    Set Suite Variable    ${registeredBizNo}
    Set Suite Variable    ${registeredCsoNo}
    Set Suite Variable    ${registeredBizName}

    # 결과 출력
    Log To Console    \n---------------------------------------
    Log To Console    업체명 : ${registeredBizName}
    Log To Console    bizNo : ${registeredBizNo}
    Log To Console    csoNo : ${registeredCsoNo}
    Log To Console    ---------------------------------------


# 등록상태 업체 정보 조회 (isSignedUp=False)
Get Registered Company Info From Admin
    ${result}=    Run Process    ${PYTHON_EXE}    ${ADMIN_API_PY}    get_company    stdout=PIPE    stderr=PIPE
    ${json_str}=  Set Variable   ${result.stdout.strip()}
    ${json_match}=  Evaluate    re.search(r'\{.*\}', r'''${json_str}''', re.DOTALL).group(0) if re.search(r'\{.*\}', r'''${json_str}''', re.DOTALL) else None    modules=re
    Should Not Be Equal    ${json_match}    ${None}    msg=Admin API로부터 올바른 JSON 데이터를 가져오지 못했습니다: ${json_str}\nError: ${result.stderr}
    ${data}=      Evaluate       json.loads($json_match)    json
    RETURN    ${data}


# 이메일 생성
Generate Email
    ${result}=    Run Process    ${PYTHON_EXE}    ${EMAIL_GEN_PY}    chera.workspace    gmail.com    stdout=PIPE    stderr=PIPE
    ${email}=     Set Variable   ${result.stdout.strip()}
    RETURN    ${email}


# 이메일 인증번호 추출
Get Email Auth Code
    ${result}=    Run Process    ${PYTHON_EXE}    ${EMAIL_READER_PY}    stdout=PIPE    stderr=PIPE
    ${code}=      Set Variable   ${result.stdout.strip()}
    RETURN    ${code}


*** Test Cases ***
1. 회원가입 Flow
    ## 사전 준비
    ${result}=    Run Process    python    -c    "import sys; print(sys.executable)"    stdout=PIPE
    
    ## 로그인 Page 
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Screenshot

    # 회원가입 버튼
    Execute Javascript    document.body.style.zoom='90%'
    Click Element    xpath=//a[text()='회원가입']
    Execute Javascript    document.body.style.zoom='100%'


1.1. 사업자등록번호 입력
    Wait Until Element Is Visible    xpath=//input[@placeholder="-없이 숫자만 입력해 주세요"]    5
    Screenshot
    
    ${bizNo}=      Get Biz Number
    Record Biz Number    ${bizNo}
    Log To Console    ---------------------------------------
    Log To Console    bizNo : ${bizNo}
    Log To Console    ---------------------------------------
    Input Text    id=bizNumber    ${bizNo}
    Screenshot

    Click Element    xpath=//button[text()='확인']
    Wait Until Element Is Visible    xpath=//h2[text()='신규 가입 가능한 사업자번호 입니다']    5
    Screenshot
    
    Click Element    xpath=(//button[text()='확인'])[last()]


1.2. 회원가입 Page
    Wait Until Element Is Visible    xpath=//h1[text()='회원가입']    5
    Screenshot


1.3. 파일 첨부 (사업자등록증/CSO신고증)
    Choose File     xpath=//*[@id="bizRegCertFileUuid"]//input    ${testfile_PATH}
    Sleep    0.5
    Choose File     xpath=//*[@id="salesCertFileUuid"]//input    ${testfile_PATH2}
    Screenshot

    Scroll Element Into View    xpath=//*[@id="name"]
    Sleep    0.5


1.4. 이메일 입력
    ${EMAIL1}=    Generate Email
    Set Suite Variable    ${EMAIL1}

    Log To Console    \n---------------------------------------
    Log To Console    email : ${EMAIL1}
    Log To Console    ---------------------------------------
    
    Input Text    id=email    ${EMAIL1}
    Screenshot

    Click Element    xpath=//button[text()='인증번호 발송']
    Wait Until Element Is Visible    xpath=//h2[text()='이메일로 인증번호를 발송했습니다.']    5
    Screenshot
    Click Element    xpath=//button[text()='확인']
    Sleep    5


1.5. 인증번호 입력
    # 인증번호 추출 및 입력 
    ${code}=    Get Email Auth Code
    
    Log To Console    \n---------------------------------------
    Log To Console    인증번호 : ${code}
    Log To Console    ---------------------------------------

    Should Match Regexp    ${code}    ^[0-9]+$    msg=인증번호 형식이 올바르지 않습니다: ${code}

    Input Text    id=emailVerificationKey    ${code}
    Screenshot
    
    Scroll Element Into View    xpath=//button[text()='인증하기']
    Wait Until Element Is Visible    xpath=//button[text()='인증하기']    5
    Click Element    xpath=//button[text()='인증하기']
    Screenshot

    Scroll Element Into View    xpath=//div[button[@id='termsAll']]
    Sleep    0.5


1.6. 비밀번호 입력
    Input Password    id=password    ${password}
    Input Password    id=passwordCheck    ${password}


1.7. 회원정보 입력
    # 이름 
    Input Text    id=name    자동화테스트
    
    # 휴대폰 번호 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Press Key    id=phone    ${phone_number}
    Screenshot


1.8. 약관 동의
    Scroll Element Into View    xpath=//button[text()='가입하기']
    Click Button    id=termsAll
    Screenshot


1.9. 회원가입 완료
    Click Button    xpath=//button[text()='가입하기']
    Wait Until Element Is Visible    xpath=//button[text()='확인']    5
    Screenshot
    
    Click Element    xpath=//button[text()='확인']
    Screenshot


1.10. Admin 승인 절차
    # Admin API 승인 Process
    Approve Pending Company Review Via Admin API
    Sleep    1


1.11. 로그인
    Input Text    name=email    ${EMAIL1}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Wait Until Element Is Visible    xpath=//h2[text()='내 정보']    5
    Screenshot

    Scroll Element Into View    xpath=//button[text()=' 로그아웃']
    Screenshot
    Click Element    xpath=//button[text()=' 로그아웃']

    ## 로그인 Page 
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Screenshot


2. 등록 상태인 업체 회원가입 Flow
    # 회원가입 버튼
    Execute Javascript    document.body.style.zoom='90%'
    Click Element    xpath=//a[text()='회원가입']
    Execute Javascript    document.body.style.zoom='100%'


2.1. API 조회 (등록 상태 업체)
    Setup Registered Company Data


2.2. 사업자등록번호 입력
    Wait Until Element Is Visible    xpath=//input[@placeholder="-없이 숫자만 입력해 주세요"]    5
    Screenshot
    
    ## 사업자 번호 입력
    Input Text    id=bizNumber    ${registeredBizNo}
    Screenshot

    Click Element    xpath=//button[text()='확인']
    Wait Until Element Is Visible    xpath=//h2[text()='의약품 판촉영업 신고번호를 입력해주세요.']    5
    Screenshot
    

2.3. CSO 신고번호 입력
    Input Text    id=csoNumber    ${registeredCsoNo}
    Screenshot
    Click Element    xpath=(//button[text()='확인'])[last()]
    Sleep    1
    Screenshot
    Click Element    xpath=(//button[text()='확인'])[last()]


2.4. 회원가입 Page 및 업체 정보 확인
    Wait Until Element Is Visible    xpath=//h1[text()='회원가입']    5
    Screenshot

    Scroll Element Into View    xpath=//*[@id="name"]
    Sleep    0.5


2.5. 이메일 입력
    ## 이메일 입력 
    ${EMAIL2}=    Generate Email
    Set Suite Variable    ${EMAIL2}

    Log To Console    \n---------------------------------------
    Log To Console    email : ${EMAIL2}
    Log To Console    ---------------------------------------

    Input Text    id=email    ${EMAIL2}
    Screenshot

    # 인증번호 발송
    Click Element    xpath=//button[text()='인증번호 발송']
    Wait Until Element Is Visible    xpath=//h2[text()='이메일로 인증번호를 발송했습니다.']    5
    Screenshot
    Click Element    xpath=//button[text()='확인']
    Sleep    5


2.6. 인증번호 입력
    # 인증번호 추출 및 입력 
    ${code}=    Get Email Auth Code
    
    # 결과 출력
    Log To Console    \n---------------------------------------
    Log To Console    인증번호 : ${code}
    Log To Console    ---------------------------------------

    # 인증번호 검증 (숫자인지 확인)
    Should Match Regexp    ${code}    ^[0-9]+$    msg=인증번호 형식이 올바르지 않습니다: ${code}

    Input Text    id=emailVerificationKey    ${code}
    Screenshot
    
    # 클릭 전 스크롤 및 대기 
    Scroll Element Into View    xpath=//button[text()='인증하기']
    Wait Until Element Is Visible    xpath=//button[text()='인증하기']    5
    Click Element    xpath=//button[text()='인증하기']
    Screenshot

    # 화면 스크롤
    Scroll Element Into View    xpath=//div[button[@id='termsAll']]
    Sleep    0.5



2.7. 비밀번호 입력
    Input Password    id=password    ${password}
    Input Password    id=passwordCheck    ${password}
    Sleep    1


2.8. 회원정보 입력
    # 이름 
    Input Text    id=name    자동화테스트
    
    # 휴대폰 번호 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Press Key    id=phone    ${phone_number}
    Screenshot


2.9. 약관 동의
    Scroll Element Into View    xpath=//button[text()='가입하기']
    Click Button    id=termsAll
    Screenshot


2.10. 회원가입 완료
    # 가입하기 버튼
    Click Button    xpath=//button[text()='가입하기']
    Wait Until Element Is Visible    xpath=//button[text()='확인']    5
    Screenshot
    
    # 로그인 Page 로 이동
    Click Element    xpath=//button[text()='확인']
    Screenshot


2.11. 로그인
    Input Text    name=email    ${EMAIL2}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Wait Until Element Is Visible    xpath=//h2[text()='내 정보']    5
    Screenshot

    Scroll Element Into View    xpath=//button[text()=' 로그아웃']
    Screenshot
    Click Element    xpath=//button[text()=' 로그아웃']


3. 아이디 찾기
    ## 로그인 Page 
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Screenshot

    Execute Javascript    document.body.style.zoom='90%'
    Click Element    xpath=//a[text()='아이디 찾기']
    Execute Javascript    document.body.style.zoom='100%'


3.1. 아이디 찾기 Page
    Wait Until Element Is Visible    xpath=//h1[text()='가입정보 확인 후 아이디를 찾을 수 있습니다']    5
    Screenshot


3.2. 사업자번호/사용자정보 입력
    ${lastBizNo}=    Get Last Biz Number
    Press Key    id=businessNumber    ${lastBizNo}
    Input Text    id=name    자동화테스트
    Screenshot

    Click Element    xpath=//button[text()='아이디 찾기']
    Wait Until Element Is Visible    xpath=//h2[text()='가입하신 아이디 입니다']    5
    Screenshot

    Click Element    xpath=//button[text()='확인']
    

4. 비밀번호 재설정
    ## 로그인 Page 
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Screenshot

    Execute Javascript    document.body.style.zoom='90%'
    Click Element    xpath=//a[text()='비밀번호 재설정']
    Execute Javascript    document.body.style.zoom='100%'


4.1. 비밀번호 찾기 Page
    Wait Until Element Is Visible    xpath=//h1[text()='비밀번호를 잊으셨나요?']    5
    Screenshot


4.2. 이메일 입력
    Input Text    id=email    ${EMAIL1}
    Screenshot
    Click Element    xpath=//button[text()='인증번호 발송']
    Wait Until Element Is Visible    xpath=//h2[text()='이메일로 인증번호를 발송했습니다.']    5
    Screenshot
    Click Element    xpath=//button[text()='확인']
    Screenshot
    Sleep    5


4.3. 인증번호 입력
    # 인증번호 추출 및 입력 
    ${code}=    Get Email Auth Code
    
    # 결과 출력
    Log To Console    \n---------------------------------------
    Log To Console    인증번호 : ${code}
    Log To Console    ---------------------------------------

    # 인증번호 검증 (숫자인지 확인)
    Should Match Regexp    ${code}    ^[0-9]+$    msg=인증번호 형식이 올바르지 않습니다: ${code}

    Input Text    id=emailcode    ${code}
    Screenshot
    Wait Until Element Is Visible    xpath=//button[text()='인증하기']    5
    Click Element    xpath=//button[text()='인증하기']
    Screenshot

    Click Element    xpath=//button[text()='다음']
    Wait Until Element Is Visible    xpath=//h1[text()='비밀번호를 재설정 해주세요']    5
    Screenshot


4.4. 비밀번호 재설정
    Input Password    id=password    ${password}
    Input Password    id=confirmPassword    ${password}
    Screenshot

    Click Element    xpath=//button[text()='비밀번호 변경하기']
    Wait Until Element Is Visible    xpath=//h2[text()='비밀번호가 변경되었습니다']    5
    Screenshot

    Click Element    xpath=//button[text()='확인']
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Screenshot

