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
5.4. 필터링 회신 관리
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
    Click Element    xpath=//button[span[text()='조회 결과(전체)']]
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

