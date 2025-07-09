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
${unused_BizNo}    None


*** Keywords ***
*** Test Cases ***
---- 위탁계약
    Wait Until Element Is Visible    xpath=//img[contains(@src, 'logo_200.25f0e37e.png')]    5

    Input Text    name=email    ${id_1}
    Press Key    name=password    ${password}
    Sleep    1
    Click Button    xpath=//button[text()='로그인']
    Sleep    3
    Screenshot

---- ---- 업체 추가하기 (가입 업체)
    ##### 가입된 업체 추가 
    # 업체 추가하기 
    Click Button    xpath=//button[normalize-space(.)='추가하기']    #추가하기 버튼 
    Wait Until Element Is Visible    xpath=//input[@placeholder='-없이 숫자만 입력']    5
    Screenshot

    # 직전 회원가입한 사업자번호 입력
    ${lastBizReNo}=    Get Last BizRegNo From File
    Press Key    id=bizNumber    ${lastBizReNo}
    Screenshot
    Click Button    xpath=//button[text()='확인하기']
    Screenshot

    # 위탁업체 추가하기 
    Wait Until Element Is Visible    class=text-lg    5
    # 관리코드
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=managementCode    ${managementCode}
    
    # 담당자 이름
    Press Key    name=managerName    자동화
    
    ## 담당자 휴대폰 번호 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Press Key    name=managerPhone    ${phone_number}
    
    # 담당자 이메일 
    Press Key    name=managerEmail    auto@mation.com
    Screenshot
    
    # 추가하기
    Click Button    xpath=//button[text()='추가하기']
    Screenshot

    # 확인버튼
    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='나중에']    5
    Click Button    xpath=//button[normalize-space(.)='나중에']
    Sleep    1
    Screenshot

---- ---- 업체 추가하기 (미가입 업체)
    ##### 미가입사용자 추가 
    # 업체 추가하기 
    Click Button    xpath=//button[normalize-space(.)='추가하기']    #추가하기 버튼 
    Wait Until Element Is Visible    xpath=//input[@placeholder='-없이 숫자만 입력']    5
    Screenshot

    # 미사용 번호 
    ${unused_BizNo}=    Get Biz Number    
    Press Key    id=bizNumber    ${unused_BizNo}
    Screenshot

    Click Button    xpath=//button[text()='확인하기']
    Screenshot

    # 모달 waiting
    Wait Until Element Is Visible    class=space-y-4    5

    # 파일 첨부    
    ${abs_path}=    Normalize Path    ${testfile_PATH}
    Choose File     xpath=//*[@id="bizRegCertFileUuid"]//input    ${abs_path}
    Sleep    1
    Choose File     xpath=//*[@id="salesCertFileUuid"]//input    ${abs_path}
    Sleep    1

    # 관리코드
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=managementCode    ${managementCode}.
    
    # 담당자 이름
    Press Key    name=managerName    자동화

    ## 담당자 휴대폰 번호 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Press Key    name=managerPhone    ${phone_number}
    
    # 담당자 이메일 
    Press Key    name=managerEmail    auto@mation.com
    Screenshot

    # 추가하기
    Click Button    xpath=//button[text()='추가하기']
    Wait Until Element Is Visible    xpath=//button[text()='확인']    5
    Screenshot

    # 확인버튼
    Click Button    xpath=//button[normalize-space(.)='확인']
    Sleep    2
    Screenshot

    Go Back    ## 등록시 상세로 이동되기에 이전 page 로 복귀 시킴 
    Sleep    1

---- ---- 업체 상세
    # 업체 상세 
    ${lastBizReNo}=    Get Last BizRegNo From File
    Click Element    xpath=//a[translate(normalize-space(text()), "-", "") = "${lastBizReNo}"]
    Screenshot

---- ---- 계약 추가
    # 계약 추가
    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='계약 추가']    5
    Click Button    xpath=//button[normalize-space(.)='계약 추가']
    Wait Until Element Is Visible    class=text-lg    5
    Screenshot

    # 계약 제목 
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=contractTitle    자동화테스트 ${managementCode}
    Sleep    0.5

    # 파일 첨부 
    ${abs_path}=    Normalize Path    ${testfile_PATH}
    Choose File     xpath=//*[@id="contractFile"]//input    ${abs_path}
    Wait Until Element Is Visible    xpath=//button[.//span[text()='Remove file']]    5
    Sleep    0.5

    # 수수료율 입력 
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Click Element    id=direct
    Wait Until Element Is Visible    name=commissionText    5
    Press Key    name=commissionText    자동화테스트 ${managementCode}
    Screenshot

    # 계약 - 추가하기 버튼
    Click Button    xpath=//button[normalize-space(.)='추가하기']
    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='나중에']    5
    Screenshot

    # 계약 - 추가하기 - 컨펌 
    Click Button    xpath=//button[normalize-space(.)='나중에']
    Screenshot

    # 계약 - 수수료율 확인
    Click Button    xpath=//button[@title='수수료율']
    Wait Until Element Is Visible    xpath=//h2[text()='수수료율']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 계약 - 계약서 확인
    Click Button    xpath=//button[@title='계약서']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 관리코드 수정 버튼 
    Click Button    xpath=(//button[normalize-space(.)='수정하기'])[1]
    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='저장하기']    5
    Screenshot

    # 관리 코드
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}

    Click Button    xpath=//button[contains(@class, 'text-gray-400')]
    Sleep    0.5
    Press Key    name=managementCode    ${managementCode}F
    Screenshot
    Click Button    xpath=//button[normalize-space(.)='저장하기']
    Screenshot

    # 담당자 정보 수정 
    Scroll Element Into View    xpath=//span[span[text()='Page']]
    Click Button    xpath=(//button[normalize-space(.)='수정하기'])[2]
    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='저장하기']    5
    Screenshot

    # 이름 
    Click Button    xpath=(//button[contains(@class, 'text-gray-400')])[1]
    Sleep    0.5
    Press Key    name=name    자동화테스트

    # 연락처 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Click Button    xpath=(//button[contains(@class, 'text-gray-400')])[2]
    Sleep    0.5
    Press Key    name=phone    ${phone_number}

    # 이메일 
    Click Button    xpath=(//button[contains(@class, 'text-gray-400')])[3]
    Sleep    0.5
    Press Key    name=email    automation@test.com
    Screenshot

    Click Button    xpath=//button[normalize-space(.)='저장하기']
    Screenshot

---- ---- 위탁계약 > 재위탁 통보서 
    # 위탁계약 - 재위탁 통보서 
    Click Button    xpath=//button[@title='재위탁통보서']
    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='통보서 작성하기']    5
    Screenshot

    # 위탁 - 재위탁 통보서 작성하기 page 진입 
    Click Button    xpath=//button[normalize-space(.)='통보서 작성하기']
    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='작성하기']    5
    Screenshot

    # 재위탁 사유, 기타
    Input Text    name=reason    ${EMPTY}
    Sleep    0.5
    Press Key    name=reason    automation test
    Sleep    0.5
    Input Text    name=note    ${EMPTY}
    Sleep    0.5
    Press Key    name=note    automation test
    Screenshot

    # 통보서 기재일 
    Click Element    id=created-date
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 화면 스크롤
    Scroll Element Into View   xpath=//button[normalize-space(.)='작성하기']
    Sleep    0.5

    # 제약사 추가하기 버튼 
    Click Button    xpath=//button[normalize-space(.)='추가하기']
    Sleep    0.5
    Screenshot

    Click Element    xpath=//*[normalize-space(.)='제약사 명 검색']
    Screenshot
    Input Text    xpath=//input[@placeholder='제약사 명 검색']    투썬 
    Screenshot
    Press Keys    xpath=//input[@placeholder='제약사 명 검색']    ENTER
    Screenshot
    Click Button    xpath=(//button[normalize-space(.)='추가하기'])[2]
    Screenshot

    # 위탁 - 재위탁 통보서 작성하기 버튼 
    Click Element    xpath=//button[normalize-space(.)='작성하기']
    Wait Until Element Is Visible    xpath=(//button[normalize-space(.)='작성하기'])[2]    5
    Screenshot

    # 컨펌 작성하기 버튼 선택
    Click Button    xpath=(//button[normalize-space(.)='작성하기'])[2]
    Sleep    0.5
    Screenshot

    # 위탁 계약으로 복귀 
    Sleep    0.5
    Click Element    xpath=//a[span[text()='위탁 계약']]
    Sleep    0.5

    # 검색 
    Click Element    xpath=//button[span[text()="상태 (전체)"]]
    Wait Until Element Is Visible    xpath=//div[span[text()="등록"]]    5
    Screenshot
    Click Element    xpath=//div[span[text()="등록"]]
    Screenshot
    
    Click Element    xpath=//button[span[text()="사업자상태 (전체)"]]
    Sleep    0.5
    Screenshot
    Press Keys    NONE    ESC

    Click Element    xpath=//button[span[text()="상호/법인명"]]
    Wait Until Element Is Visible    xpath=//div[span[text()="관리코드"]]    5
    Screenshot
    Click Element    xpath=//div[span[text()="관리코드"]]
    Screenshot

    ${datetime_monthday}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d')
    Press Key    xpath=//input[@placeholder="검색어를 입력해주세요"]    ${datetime_monthday}
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


---- 수탁 계약

    Sleep    0.5
    Click Element    xpath=//a[span[text()='수탁 계약']]
    Sleep    0.5
    Screenshot

    # 검색 
    Click Element    xpath=//button[span[text()="상호/법인명"]]
    Sleep    0.5
    Screenshot
    Press Keys    NONE    ESC

    Press Key    xpath=//input[@placeholder="검색어를 입력해주세요"]    투썬
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Screenshot

---- ---- 업체 상세 
    # 업체 상세 
    Click Element    xpath=//a[text()='842-88-83121']
    Wait Until Element Is Visible    xpath=//h3[text()='계약 관리']
    Screenshot
    Sleep    1

