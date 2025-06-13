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
${bizRegNo}    None

*** Keywords ***
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
    ${files}=         List Files In Directory    ${unused_bizRegNo_DIR}    pattern=bizRegNo_*.txt
    ${random_index}=  Evaluate    random.randint(0, len(${files}) - 1)    modules=random
    ${file}=          Get From List    ${files}    ${random_index}
    ${path}=          Catenate    SEPARATOR=/    ${unused_bizRegNo_DIR}    ${file}
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


*** Test Cases ***
---- Testcase (로그인)



    Sleep    2
    Input Text    name=email    ${id_1}
    Press Key    name=password    ${password}
    Sleep    1
    Click Button    xpath=//button[text()='로그인']

    ${lastBizReNo}=    Get Last BizRegNo From File
    Set Suite Variable    ${lastBizReNo}
    Log To Console    ${lastBizReNo}

    Sleep    3

    # 업체 추가하기 
    Click Button    css=button[title="작성하기"]
    Sleep    2

    # 직전 회원가입한 사업자번호 입력
    Press Key    id=bizNumber    ${lastBizReNo}
    Sleep    2
    Click Button    xpath=//button[text()='확인하기']
    Sleep    2

    # 위탁업체 추가하기 
    Wait Until Element Is Visible    class=text-lg    5
    # 관리코드
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=managementCode    ${managementCode}
    # 담당자 이름
    Press Key    name=managerName    automation
    ## 담당자 휴대폰 번호 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Press Key    name=managerPhone    ${phone_number}
    # 담당자 이메일 
    Press Key    name=managerEmail    auto@mation.com
    Sleep    1 
    Click Button    xpath=//button[text()='추가하기']
    Sleep    1

    Press Keys    NONE    ESC
    
    Sleep    2


    ## 미사용 사업자 번호 위탁 업체 추가 
    # 업체 추가하기 
    Click Button    css=button[title="작성하기"]
    Sleep    2
    ${bizRegNo}=      Find Valid Biz Number
    Press Key    id=bizNumber    ${bizRegNo}
    Sleep    2
    Click Button    xpath=//button[text()='확인하기']
    Sleep    2
    Press Keys    NONE    ESC
    Sleep    2




    # 업체 상세 
    # Click Element    xpath=//a[translate(normalize-space(text()), "-", "") = "${lastBizReNo}"]







    Sleep    3

---- Testcase 2

    Log To Console    ${lastBizReNo}
    Log To Console    ${bizRegNo}




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

