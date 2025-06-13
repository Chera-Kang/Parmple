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
${bizNo}    None


*** Keywords ***
Get Absolute File Path
    [Arguments]    ${relative_path}
    ${abs}=    Normalize Path    ${EXECDIR}/${relative_path}
    [Return]    ${abs}


*** Test Cases ***
---- Testcase

    Wait Until Element Is Visible    xpath=//img[contains(@src, 'logo_200.25f0e37e.png')]    5

    Input Text    name=email    ${id_1}
    Press Key    name=password    ${password}
    Sleep    1
    Click Button    xpath=//button[text()='로그인']
    Sleep    3


    ############################################################

    ${lastBizReNo}=    Get Last BizRegNo From File
    Log To Console    ${lastBizReNo}

    # 업체 상세 
    Click Element    xpath=//a[translate(normalize-space(text()), "-", "") = "${lastBizReNo}"]

    # 계약 추가
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}

    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='계약 추가']    5
    Click Button    xpath=//button[normalize-space(.)='계약 추가']
    Wait Until Element Is Visible    class=text-lg    5
    Press Key    name=contractTitle    자동화테스트 ${managementCode}
    Sleep    1

    ${abs_path}=    Normalize Path    ${testfile_PATH}
    Choose File     xpath=//*[@id="contractFile"]//input    ${abs_path}
    Sleep    1
    
    Click Element    id=direct
    Wait Until Element Is Visible    name=commissionText    5
    Press Key    name=commissionText    자동화테스트

    Click Button    xpath=//button[normalize-space(.)='추가하기']

    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='나중에']    5
    Click Button    xpath=//button[normalize-space(.)='나중에']
  
    Sleep    2

    Press Keys    NONE    ESC    
    Sleep    2

    # 관리코드 수정
    Click Button    xpath=(//button[normalize-space(.)='수정하기'])[1]
    Sleep    1

    Press Keys    NONE    ESC
    Sleep    1

    # 담당자 정보 수정 
    Click Button    xpath=(//button[normalize-space(.)='수정하기'])[2]
    Sleep    1
 
    Sleep    5



    # Sleep    1
    # Click Element    xpath=//button[text()='로그인']
    # Sleep    2
    # Click Element    xpath=//a[span[text()='위탁 계약']
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

