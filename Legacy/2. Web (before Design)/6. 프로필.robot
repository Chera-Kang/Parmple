*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    String
Library    RequestsLibrary
Library    BuiltIn
Resource   ../keywords.robot
Library    Process
Library    DateTime

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***
*** Keywords ***
*** Test Cases ***
---- 내 정보
    Wait Until Element Is Visible    xpath=//img[contains(@src, 'logo_200.25f0e37e.png')]    5

    Input Text    name=email    ${id_1}
    Press Key    name=password    ${password}
    Sleep    1
    Click Button    xpath=//button[text()='로그인']
    Sleep    3

    # 내 정보 선택
    Click Element    xpath=//button[@data-sidebar='menu-button']
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='내 정보']    5
    Screenshot
    Click Element    xpath=//a[normalize-space(.)='내 정보']
    Wait Until Element Is Visible    xpath=//h2[normalize-space(.)='내 정보']
    Screenshot

    # 화면 스크롤
    Scroll Element Into View    xpath=//*[normalize-space(.)='로그아웃']
    Sleep    0.5


---- ---- 계정 정보 수정
    # 계정 정보 수정 
    Click Element    xpath=//button[@title='계정 정보 수정']
    Wait Until Element Is Visible    xpath=//h2[text()='계정 정보 수정']    5
    Screenshot

    # 계정 정보 수정 > 이름 
    ${datetime_monthday}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    Input Text    name=name    1
    Input Text    name=name    ${EMPTY}
    Press Key    name=name    테스트_${datetime_monthday}
    Sleep    0.5

    # 계정 정보 수정 > 휴대폰 번호 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    Input Text    name=phone    1
    Input Text    name=phone    ${EMPTY}
    Press Key    name=phone    010${random_number}
    Screenshot

    # 계정 정보 수정 > 수정하기 버튼 
    Click Element    xpath=//div[button[@title='수정하기']]
    Sleep    0.5
    Screenshot


---- ---- 비밀번호 변경
    # 비밀번호 변경 
    Click Button    xpath=//button[@title='비밀번호 변경']
    Wait Until Element Is Visible    xpath=//h2[text()='비밀번호 변경']    5
    Screenshot

    Press Key    id=password    ${password}
    Press Key    id=newPassword    ${password}
    Press Key    id=confirmNewPassword    ${password}
    Screenshot

    # 비밀번호 변경하기 버튼 
    Click Element    xpath=(//div[button[@title='변경하기']])[2]
    Wait Until Element Is Visible    xpath=//h2[text()='비밀번호가 변경되었습니다.']    5
    Screenshot
    Click Element     xpath=//button[@title='확인']
    Sleep    0.5


---- ---- 도장 관리
    # 도장 관리 
    Click Element    xpath=//button[text()='변경하기']
    Wait Until Element Is Visible    xpath=//h2[text()='도장 관리']    5
    # Wait Until Element Is Visible    xpath=//div[button[text()='만들기']]    5
    Screenshot
    
    # 문구 입력 
    Press Key    id=stampName    테스트
    Screenshot

    # 도장 만들기 버튼
    Click Element    xpath=//button[text()='만들기']
    Wait Until Element Is Visible    xpath=//div[img[@alt='도장 미리보기']]    5
    Screenshot

    # 도장 저장하기 
    Click Element    xpath=//button[text()='저장하기']
    Sleep    0.5
    Screenshot


---- 약관 
    # 서비스 이용약관
    Click Element    xpath=//button[@data-sidebar='menu-button']
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='내 정보']    5
    Screenshot
    Click Element    xpath=//div[@title='서비스 이용약관']
    Wait Until Element Is Visible    xpath=//h2[text()='서비스 이용약관']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 개인정보 처리방침 
    Click Element    xpath=//button[@data-sidebar='menu-button']
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='내 정보']    5
    Screenshot
    Click Element    xpath=//div[@title='개인정보처리방침']
    Wait Until Element Is Visible    xpath=//h2[text()='개인정보처리방침']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


---- 고객센터
    # 고객센터
    Click Element    xpath=//button[@data-sidebar='menu-button']
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='내 정보']    5
    Screenshot
    Click Element    xpath=//a[@title='고객센터']
    Sleep    5
    Screenshot
    Switch To Tab    0
    Screenshot


---- 로그아웃
    # 로그아웃 버튼 선택 
    Click Element    xpath=//button[@title='로그아웃']
    Wait Until Element Is Visible    name=email    5
    Screenshot

