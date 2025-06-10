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

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite


*** Variables ***

${EMAIL_PREFIX}    chera.workspace
${EMAIL_DOMAIN}    gmail.com

${PYTHON_EXE}    ${EXECDIR}/.venv/Scripts/python.exe

${EMAIL}    None


*** Keywords ***

Generate Unique Email
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d.%H%M%S')
    ${email}=    Set Variable    ${EMAIL_PREFIX}+${datetime}@${EMAIL_DOMAIN}
    [Return]    ${EMAIL}


Remove Hyphen From BizNo
    [Arguments]    ${rawBizNo}
    ${cleaned}=    Replace String    ${rawBizNo}    -    ${EMPTY}
    [Return]    ${cleaned}

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


Get Absolute File Path
    [Arguments]    ${relative_path}
    ${abs}=    Normalize Path    ${EXECDIR}/${relative_path}
    [Return]    ${abs}



*** Test Cases ***
---- Testcase (로그인)

    ${result}=    Run Process    python    -c    "import sys; print(sys.executable)"    stdout=PIPE
    Log To Console    Robot Framework Run Process uses: ${result.stdout}

    Wait Until Element Is Visible    class=mb-4
    ${bizRegNo}=      Find Valid Biz Number
    Sleep    1
    Click Element    xpath=//button[text()='회원가입']
    Sleep    2
    Input Text    id=bizNumber    ${bizRegNo}    # 사업자 번호 입력
    Sleep    1
    Click Element    xpath=//button[text()='확인하기']    # 사업자 번호 입력 후 회원가입 Page 로 진입
    Sleep    1
    Click Element    xpath=//button[text()='확인']
    Sleep    1


    ${abs_path}=    Normalize Path    ${testfile_PATH}
    Choose File     xpath=//*[@id="bizRegCertFileUuid"]//input    ${abs_path}
    Sleep    1
    Choose File     xpath=//*[@id="salesCertFileUuid"]//input    ${abs_path}
    Sleep    1


    Scroll Element Into View    xpath=//*[@id="name"]
    Sleep    1

    ${EMAIL}=    Generate Unique Email
    Input Text    id=email    ${EMAIL}    # 이메일 입력
    Set Suite Variable    ${EMAIL}
    Log To Console    ${EMAIL}

    Sleep    1
    Click Element    xpath=//button[text()='인증번호 발송']
    Sleep    1
    Click Element    xpath=//button[text()='확인']
    Sleep    5

    ${result}=    Run Process    ${PYTHON_EXE}    support/gmail_reader.py    stdout=PIPE    stderr=PIPE

    ${code}=      Set Variable   ${result.stdout.strip()}
    Log To Console    \n인증번호: ${code}
    Should Not Be Equal    ${code}    NO_CODE

    Input Text    id=emailVerificationKey    ${code}

    Sleep    1
    Click Element    xpath=//button[text()='인증하기']
    Sleep    1

    Scroll Element Into View    xpath=//button[text()='가입하기']
    Sleep    1

    Input Password    id=password    ${password}
    Sleep    1
    Input Password    id=passwordCheck    ${password}
    Sleep    1

    Input Text    id=name    테스트
    Sleep    1

    Input Text    id=phone    01011111111
    Sleep    1

    Click Button    id=termsAll
    Sleep    1

    Click Button    xpath=//button[text()='가입하기']
    Sleep    1

    Wait Until Element Is Visible    id=radix-:r15:    5
    Click Element    xpath=//button[text()='확인']
    Sleep    1




    Sleep    10








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





---- Testcase3

    Log To Console    -Succese-
    Log To Console    ${EMAIL}

    Input Text    name=email    ${EMAIL}

    Sleep    5


    