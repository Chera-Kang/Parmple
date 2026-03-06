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

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***
*** Keywords ***
*** Test Cases ***
5.1. 필터링
    Login_CSO
    Sleep    1


5.3. 필터링 요청
    Logout
    Login_CSO

    Scroll Element Into View    xpath=//a[span[text()='필터링 요청']]
    Click Element    xpath=//a[span[text()='필터링 요청']]
    Screenshot


5.3.1. 필터링 요청 등록하기
    Click Button    xpath=//button[@title='필터링 요청 등록']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청 등록하기']    5
    Screenshot

    # 요청 업체 검색    
    Click Element    xpath=//input[@placeholder='업체를 검색해 주세요']
    Input Text    xpath=//input[@placeholder='업체를 검색해 주세요']    투썬
    Screenshot

    Click Element    xpath=//button[div[span[normalize-space(.)='제약사']]]
    Screenshot

    # 병의원 추가
    Click Element    xpath=//button[text()='신규 병의원 등록']
    Wait Until Element Is Visible    xpath=//h2[text()='신규 병의원 등록']    5
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%y%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    xpath=//input[@placeholder='병의원 명을 입력해 주세요.']    Auto ${datetime}
    Press Key    xpath=//input[@placeholder='병의원 주소를 입력해 주세요.']    자동화주소
    ${bizRegNo}=      Get Biz Number
    Press Key    xpath=//input[@placeholder='-없이 숫자만 입력해 주세요']    ${bizRegNo}
    Screenshot

    # 모달 등록하기 버튼
    Click Button    xpath=//button[text()='등록하기']
    Screenshot

    Scroll Element Into View    xpath=//button[@title='취소']

    # 문의 내용
    Input Text    name=inquiryContent    1
    Input Text    name=inquiryContent    ${EMPTY}
    Press Key    name=inquiryContent    자동화테스트
    Screenshot

    # 필터링 요청하기 
    Click Button    xpath=//button[@title='요청하기']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청']    5
    Screenshot

5.3.1.1. 한번 더 등록하기 (for delete test)
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
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%y%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    xpath=//input[@placeholder='병의원 명을 입력해 주세요.']    Auto ${datetime}
    Press Key    xpath=//input[@placeholder='병의원 주소를 입력해 주세요.']    자동화주소
    ${bizRegNo}=      Get Biz Number
    Press Key    xpath=//input[@placeholder='-없이 숫자만 입력해 주세요']    ${bizRegNo}
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
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청']    5
    Screenshot


5.3.2. 필터링 요청 상세
    # 요청 상세
    Click Element    xpath=//span[text()='자동화테스트']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청']    5
    Screenshot

    # 수정하기
    Click Element    xpath=//div[textarea[text()='자동화테스트']]
    Press Keys    None     _수정하기
    Screenshot
    Click Button    xpath=//button[text()='수정하기']
    Screenshot
 
    # 요청 취소
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

5.3.4. 필터링 > 검색
    # 병의원 검색 
    Click Element    xpath=//button[span[text()='상태 (전체)']]
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5
    Click Element    xpath=//button[span[text()='결과 (전체)']]
    Screenshot
    Click Element    xpath=//div[span[text()='반려']]
    Sleep    0.5
    Click Element    xpath=//button[span[text()='병의원명']]
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5
    Press Key    xpath=//input[@placeholder='검색어를 입력해 주세요']    인천
    Screenshot
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


5.4. 필터링 회신 관리
    Logout
    Login_pharm_pharm1

    # 필터링 회신 관리
    Scroll Element Into View    xpath=//a[span[text()='필터링 회신 관리']]
    Click Element    xpath=//a[span[text()='필터링 회신 관리']]
    Sleep    1
    Screenshot


5.4.1. 필터링 요청 상세
    # 요청 상세 모달
    Click Element    xpath=//span[text()='자동화테스트']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 회신']    5
    Screenshot
    Scroll Element Into View    xpath=//div[text()='필터링 결과/내용 회신 이후에는 수정이 불가합니다.']
    Screenshot

    # 필터링 결과 선택
    Click Button    xpath=//button[span[text()='필터링 결과']]
    Screenshot
    Click Element    xpath=(//div[span[text()='임시 승인']])[last()]
    
    # 회신내용
    Input Text    name=replyContent    1
    Input Text    name=replyContent    ${EMPTY}
    Press Key    name=replyContent    자동화테스트 회신
    Screenshot
    
5.4.2. 필터링 회신하기
    # 회신하기
    Click Button    xpath=//button[text()='회신하기']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 결과를 회신할까요?']    5
    Screenshot
    Click Button    xpath=(//button[text()='회신하기'])[last()]
    Screenshot

    # 회신한 필터링 확인
    Click Element    xpath=//span[text()='자동화테스트']
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 회신']    5
    Screenshot
    Scroll Element Into View    xpath=(//span[text()='회신 내용'])[last()]
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 병의원 검색 
    Click Element    xpath=//button[span[text()='상태 (전체)']]
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5
    Click Element    xpath=//button[span[text()='결과 (전체)']]
    Screenshot
    Click Element    xpath=//div[span[text()='반려']]
    Sleep    0.5
    Click Element    xpath=//button[span[text()='상호/법인명']]
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5
    Press Key    xpath=//input[@placeholder='검색어를 입력해 주세요']    휴피스
    Screenshot
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot

