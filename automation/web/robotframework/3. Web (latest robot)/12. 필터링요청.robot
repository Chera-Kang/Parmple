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
*** Test Cases ***
1. 필터링 요청
    Login_CSO

    Scroll Element Into View    xpath=//a[span[text()='필터링 요청하기']]
    Click Element    xpath=//a[span[text()='필터링 요청하기']]
    Screenshot


2. 필터링 요청 등록하기
    Click Button    xpath=//button[@title='필터링 요청 등록']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청 등록하기']    5
    Screenshot


2.1. 요청 업체 검색
    Click Element    xpath=//input[@placeholder='업체를 검색해 주세요']
    Input Text    xpath=//input[@placeholder='업체를 검색해 주세요']    투썬
    Sleep    1
    Screenshot

    Click Element    xpath=//button[div[span[normalize-space(.)='제약사']]]
    Screenshot


2.2. 병의원 추가
    Click Element    xpath=//button[text()='신규 병의원 등록']
    Wait Until Element Is Visible    xpath=//h2[text()='신규 병의원 등록']    5
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%y%m%d-%H%M%S')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    xpath=//input[@placeholder='병의원 명을 입력해 주세요.']    Auto ${datetime}
    Press Key    xpath=//input[@placeholder='병의원 주소를 입력해 주세요.']    자동화주소
    ${bizNo}=      Get Biz Number
    Press Key    xpath=//input[@placeholder='-없이 숫자만 입력해 주세요']    ${bizNo}
    Screenshot


2.3. 문의 내용
    # 모달 등록하기 버튼
    Click Button    xpath=//button[text()='등록하기']
    Screenshot

    Scroll Element Into View    xpath=//button[@title='취소']

    # 문의 내용
    Input Text    name=inquiryContent    1
    Input Text    name=inquiryContent    ${EMPTY}
    Press Key    name=inquiryContent    자동화테스트
    Screenshot


2.4. 문의하기
    # 필터링 요청하기 
    Click Button    xpath=//button[@title='요청하기']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청하기']    5
    Screenshot


2.5. 한번 더 등록하기 (for delete test)
    Click Button    xpath=//button[@title='필터링 요청 등록']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청 등록하기']    5
    Sleep    1

    # 요청 업체 검색    
    Click Element    xpath=//input[@placeholder='업체를 검색해 주세요']
    Input Text    xpath=//input[@placeholder='업체를 검색해 주세요']    투썬
    Sleep    1

    Click Element    xpath=//button[div[span[normalize-space(.)='제약사']]]
    Sleep    1

    # 병의원 추가
    Click Element    xpath=//button[text()='신규 병의원 등록']
    Wait Until Element Is Visible    xpath=//h2[text()='신규 병의원 등록']    5
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%y%m%d-%H%M%S')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    xpath=//input[@placeholder='병의원 명을 입력해 주세요.']    Auto ${datetime}
    Press Key    xpath=//input[@placeholder='병의원 주소를 입력해 주세요.']    자동화주소
    ${bizNo}=      Get Biz Number
    Press Key    xpath=//input[@placeholder='-없이 숫자만 입력해 주세요']    ${bizNo}
    Sleep    1

    # 모달 등록하기 버튼
    Click Button    xpath=//button[text()='등록하기']
    Sleep    1

    Scroll Element Into View    xpath=//button[@title='취소']

    # 문의 내용
    Input Text    name=inquiryContent    1
    Input Text    name=inquiryContent    ${EMPTY}
    Press Key    name=inquiryContent    자동화테스트
    Sleep    1

    # 필터링 요청하기 
    Click Button    xpath=//button[@title='요청하기']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청하기']    5
    Screenshot


3. 필터링 요청 상세
    # 요청 상세
    Click Element    xpath=//span[text()='자동화테스트']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청']    5
    Screenshot


3.1. 수정하기
    Click Element    xpath=//div[textarea[text()='자동화테스트']]
    Press Keys    None     _수정하기
    Screenshot
    Click Button    xpath=//button[text()='수정하기']
    Screenshot


3.2. 요청 취소
    Click Element    xpath=//span[text()='자동화테스트_수정하기']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청']    5
    Screenshot
    Click Button    xpath=//button[text()='요청 취소']
    Wait Until Element Is Visible    xpath=//button[text()='요청 취소하기']    5
    Screenshot
    Click Button    xpath=//button[text()='요청 취소하기']
    Screenshot

    # 취소 확인
    Click Element    xpath=//span[text()='자동화테스트_수정하기']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청']    5
    Screenshot
    Press Keys    NONE    ESC


4. 검색
    Click Element    xpath=//button[span[span[text()='상태 (전체)']]]
    Screenshot

    Press Keys    NONE    ESC
    Sleep    0.5
    Click Element    xpath=//button[span[span[text()='조회 결과(전체)']]]
    Screenshot

    Click Element    xpath=//div[span[text()='반려']]
    Sleep    0.5
    Click Element    xpath=//button[span[span[text()='병의원명']]]
    Screenshot

    Press Keys    NONE    ESC
    Sleep    0.5
    Press Key    xpath=//input[@placeholder='검색어를 입력해 주세요']    인천
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Screenshot

