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
2.1 프로필
    Login_CSO
    Sleep    1

    # 프로필 메뉴 
    Click Element    xpath=//button[@aria-haspopup='menu']
    Wait Until Element Is Visible    xpath=//div[@title='로그아웃']    5
    Screenshot


2.2. 내 정보
    # 프로필 진입 
    Click Element    xpath=//button[span[div[i[contains(@class, 'ri-user-line')]]]]
    Wait Until Element Is Visible    xpath=//h2[text()='내 정보']    5
    Screenshot

    Scroll Element Into View    xpath=//h3[text()='계정 정보']
    Screenshot

2.2.1. 첨부자료
    # 사업자등록증
    Click Button    xpath=//button[text()='보기'][1]
    Wait Until Element Is Visible    xpath=//h2[text()='사업자등록증']    5
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC

    # 의약품 판촉영업 신고증 
    Click Button    xpath=(//button[text()='보기'])[last()]
    Wait Until Element Is Visible    xpath=//h2[text()='영업신고증']    5
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC


2.2.2. CSO 교육 수료증
    Sleep    1
    Scroll Element Into View    xpath=//div[h3[text()='계정 정보']]
    Screenshot

    Click Element    xpath=//button[text()='등록']
    Wait Until Element Is Visible    xpath=//h2[text()='CSO 교육 수료증 등록']    5
    Screenshot

    Choose File     xpath=//*[@id="fileUuid"]//input    ${testfile_PATH}
    Sleep    0.5
    Screenshot

    Click Element    xpath=//div[span[text()='수료증 기재일']]
    Screenshot

    # 현재 날짜의 '일(day)' 가져오기 (1~31)
    ${day}=    Evaluate    datetime.datetime.now().day    modules=datetime
    
    # 해당 날짜 클릭
    Click Element    xpath=//td[button[text()='${day}']]
    Sleep    0.5
    Screenshot

    ${datetime}=    Evaluate    datetime.datetime.now().strftime('%Y-%m%d-%H%M%S')    modules=datetime
    Press Key    xpath=//input[@placeholder='발급번호를 입력해 주세요']    ${datetime}
    Sleep    0.5
    Screenshot

    Click Button    xpath=//button[text()='등록하기']
    Screenshot

    # CSO 신고증 목록 보기 
    ${datetime}=    Evaluate    datetime.datetime.now().strftime('%Y-%m-%d')    modules=datetime
    Click Element    xpath=//dd[p[text()='${datetime}']]    
    Sleep    1
    Screenshot

    # 교육 수료증 보기 버튼
    Click Element    xpath=//button[@title='수료증']
    Wait Until Element Is Visible    xpath=//h2[text()='교육 수료증']    5
    Screenshot



    Press Keys    NONE    ESC



2.3. 계정 정보
    Sleep    1

2.3.1. 비밀번호 변경
    Scroll Element Into View    xpath=//dt[text()='휴대폰번호']

    # 비밀번호 변경
    Click Element    xpath=//button[@title='비밀번호 변경']
    Wait Until Element Is Visible    xpath=//h2[text()='비밀번호 변경']    5
    Screenshot

    Press Key    id=password    ${password}
    Press Key    id=newPassword    ${password}
    Press Key    id=confirmNewPassword    ${password}
    Screenshot

    Click Element    xpath=//button[@title='변경하기']
    Wait Until Element Is Visible    xpath=//h2[text()='비밀번호가 변경되었습니다.']    5
    Screenshot
    Click Element    xpath=//button[@title='확인']

2.3.2. 계정 정보 수정
    # 계정 정보 수정 
    Click Element    xpath=//button[@title='계정 정보 수정']
    Wait Until Element Is Visible    xpath=//h2[text()='계정 정보 수정']    5
    Screenshot

    # 이름
    ${datetime_monthday}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    Input Text    name=name    ${EMPTY}
    Input Text    name=name    테스트_${datetime_monthday}
    Sleep    0.5

    # 휴대폰 번호 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    Input Text    name=phone    ${EMPTY}
    Input Text    name=phone    010${random_number}
    Screenshot

    # 수정하기 버튼 
    Click Element    xpath=//button[@title='수정하기']
    Sleep    0.5
    Screenshot

2.4. 도장 정보
    # 도장 정보 
    Click Element    xpath=//span[text()='도장 변경하기']
    Wait Until Element Is Visible    xpath=//h2[text()='도장 변경하기']    5
    Screenshot

    Press Key    id=stampName    테스트
    Screenshot

    Click Button    xpath=//button[text()='만들기']
    Wait Until Element Is Visible    xpath=//img[@alt='도장 미리보기']    5
    Screenshot

    Click Button    xpath=//button[@title='저장하기']
    Screenshot
    

2.5. 약관
    # 서비스 이용약관
    Click Element    xpath=//button[@aria-haspopup='menu']
    Wait Until Element Is Visible    xpath=//div[@title='서비스 이용약관']    5
    Click Element    xpath=//div[@title='서비스 이용약관']
    Wait Until Element Is Visible    xpath=//h2[text()='서비스 이용약관']    5
    Screenshot
    Press Keys    NONE    ESC

    # 개인정보처리방침
    Click Element    xpath=//button[@aria-haspopup='menu']
    Wait Until Element Is Visible    xpath=//div[@title='개인정보처리방침']    5
    Click Element    xpath=//div[@title='개인정보처리방침']
    Wait Until Element Is Visible    xpath=//h2[text()='개인정보처리방침']    5
    Screenshot
    Press Keys    NONE    ESC


2.6. 로그아웃
    Click Element    xpath=//button[@aria-haspopup='menu']
    Wait Until Element Is Visible    xpath=//div[@title='로그아웃']    5
    Click Element    xpath=//div[@title='로그아웃']
    Screenshot
    Sleep    1
