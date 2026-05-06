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
${lastBizNo}    None
${unused_BizNo}    None

*** Keywords ***
*** Test Cases ***
1. 회원 업체 관리 Page 
    Login_CSO

    Wait Until Element Is Visible    xpath=//h2[text()='회원 업체 관리 ']    5
    Screenshot


1.1. 업체 추가하기 (가입 업체)
    ##### 가입된 업체 추가 
    # 업체 추가하기 
    Click Button    xpath=//button[normalize-space(.)='추가하기']
    Wait Until Element Is Visible    xpath=//h2[text()='회원 업체 추가']    5
    Screenshot


1.2. 사업자번호 입력
    # 직전 회원가입한 사업자번호 입력
    ${lastBizNo}=    Get Last Biz Number
    Input Text    id=bizNumber    ${lastBizNo}
    Screenshot
    Click Button    xpath=//button[text()='확인하기']
    Wait Until Element Is Visible    xpath=//h2[text()='회원 업체 추가']    5
    Screenshot


1.3. 관리코드
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Input Text    name=managementCode    ${managementCode}


1.4. 담당자 정보    
    # 담당자 이름
    Input Text    name=managerName    자동화
    
    ## 담당자 휴대폰 번호 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Input Text    name=managerPhone    ${phone_number}
    
    # 담당자 이메일 
    Input Text    name=managerEmail    auto@mation.com
    Screenshot

    # 추가하기
    Click Button    xpath=//button[text()='추가하기'][last()]
    Wait Until Element Is Visible    xpath=//h2[text()='계약서를 등록할까요?']    5
    Screenshot

    # 확인버튼
    Click Button    xpath=//button[normalize-space(.)='나중에']
    Sleep    1
    Screenshot


2.1. 업체 추가하기 (미가입 업체)
    ##### 미가입사용자 추가 
    # 업체 추가하기 
    Click Button    xpath=//button[normalize-space(.)='추가하기']    #추가하기 버튼 
    Wait Until Element Is Visible    xpath=//h2[text()='회원 업체 추가']    5
    Screenshot


2.2. 사업자번호 입력
    ${bizNo}=     Get Biz Number
    Set Suite Variable    ${bizNo}
    Input Text    id=bizNumber    ${bizNo}
    Screenshot

    Click Button    xpath=//button[text()='확인하기']
    Wait Until Element Is Visible    xpath=//h2[text()='회원 업체 추가']    5
    Screenshot


2.3. 파일첨부
    ## 파일 첨부    
    Choose File     xpath=//*[@id="bizRegCertFileUuid"]//input    ${testfile_PATH}
    Sleep    0.5
    Choose File     xpath=//*[@id="salesCertFileUuid"]//input    ${testfile_PATH2}
    Screenshot


2.4. 관리코드
    # 관리코드
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Input Text    name=managementCode    ${managementCode}.
    

2.5. 담당자 정보
    # 담당자 이름
    Input Text    name=managerName    자동화

    ## 담당자 휴대폰 번호 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Input Text    name=managerPhone    ${phone_number}
    
    # 담당자 이메일 
    Input Text    name=managerEmail    auto@mation.com
    Screenshot

    # 추가하기
    Click Button    xpath=//button[text()='추가하기'][last()]
    Wait Until Element Is Visible    xpath=//h2[text()='업체 등록 요청이 완료되었습니다']    5
    Screenshot

    # 확인버튼
    Click Button    xpath=//button[normalize-space(.)='확인']
    sleep    0.5


3. 상세 Page (미가입 업체)
    Click Element    xpath=//a[text()="${bizNo}"]
    Wait Until Element Is Visible    xpath=//h2[text()='상세 보기']    5


3.1. 업체 정보
    Screenshot


3.2. CSO 교육 수료증
    # CSO 교육 수료증 등록 버튼 선택
    ${REG_BUTTON}=    Set Variable    xpath=//tr[contains(@class, 'lg:table-row') and .//th[text()='CSO 교육 수료증']]//button[text()='등록']
    Wait Until Element Is Visible    ${REG_BUTTON}    10
    Click Button                     ${REG_BUTTON}

    Wait Until Element Is Visible    xpath=//h2[text()='CSO 교육 수료증 등록']    5
    Screenshot

    Choose File     xpath=//*[@id="fileUuid"]//input    ${testfile_PATH}
    Sleep    0.5
    Screenshot

    Click Element    xpath=//div[span[text()='수료증 기재일']]
    Screenshot

    # 현재 날짜의 '일(day)' 가져오기 (1~31)
    ${day}=    Evaluate    datetime.datetime.now().day    modules=datetime
    Log To Console    오늘 날짜: ${day}
    
    # 해당 날짜 클릭
    Click Element    xpath=//td[button[text()='${day}']]
    Sleep    0.5
    Screenshot

    ${datetime}=    Evaluate    datetime.datetime.now().strftime('%Y-%m%d-%H%M%S')    modules=datetime
    Press Key    xpath=//input[@placeholder='발급번호를 입력해 주세요']    ${datetime}
    Sleep    0.5
    Screenshot

    Click Button    xpath=//button[text()='등록하기']
    Wait Until Element Is Visible    xpath=//h2[text()='교육 수료증을 등록할까요?']    5
    Screenshot

    Click Button    xpath=//button[text()='확인']
    Screenshot


    #### 현재 모니터 화면에서의 UI 오류로 확인 불가, 추후 이슈 등록하여 확인 예정으로 그동안 주석처리

    # CSO 신고증 목록 보기 
    # CSO 교육 수료증 목록 보기 (날짜 span 클릭)
    # Click Element    xpath=//dl[dt[text()='CSO 교육 수료증']]//span[@role='button']
    # Wait Until Element Is Visible    xpath=//h2[text()='CSO 교육 수료 이력']    5
    # Sleep    1

    # Execute Javascript    document.body.style.zoom='90%'
    # Click Element    xpath=//button[@title='수료증']
    # Execute Javascript    document.body.style.zoom='100%'

    # # 이미지 또는 PDF 중 하나라도 로드될 때까지 대기
    # Wait Until Element Is Visible    xpath=//img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]    10
    # Screenshot
    # Press Keys    ${None}    ESC
    # Sleep    1

    #### 현재 모니터 화면에서의 UI 오류로 확인 불가, 추후 이슈 등록하여 확인 예정으로 그동안 주석처리


    Go Back
    Wait Until Element Is Visible    xpath=//h2[text()='회원 업체 관리 ']    5
    Sleep    3


4. 상세 Page (가입 업체)
    ${lastBizNo}=    Get Last Biz Number

    Click Element    xpath=//a[translate(normalize-space(.), "-", "") = "${lastBizNo}"]
    Wait Until Element Is Visible    xpath=//h2[text()='상세 보기']    5

4.1. 업체 정보
    Screenshot


4.2. 관리코드 
    # 관리코드 수정 버튼 
    Click Button    xpath=(//button[text()='수정'])[last()]
    Wait Until Element Is Visible    xpath=//h2[text()='관리 코드 수정']    5
    Screenshot

    # 관리 코드
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}

    Click Element    name=managementCode
    Click Element    xpath=//input[@name="managementCode"]/following-sibling::div/button
    Sleep    0.5
    Input Text    name=managementCode    ${managementCode}F
    Screenshot
    Click Button    xpath=//button[normalize-space(.)='저장하기']
    Screenshot


4.3. 사업자등록증/CSO신고증
    Scroll Element Into View    xpath=//dt[text()='이메일']
    Sleep    1

    Click Button    xpath=(//button[text()='보기'])[last()-1]
    Wait Until Element Is Visible    xpath=//h2[text()='사업자등록증']    5
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC

    Click Button    xpath=(//button[text()='보기'])[last()]
    Wait Until Element Is Visible    xpath=//h2[text()='영업신고증']    5
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC


4.4. 담당자 정보
    Click Button    xpath=//button[@title='수정']
    Wait Until Element Is Visible    xpath=//h2[text()='담당자 정보 수정']    5
    Screenshot

    # 이름
    Click Element    name=name
    Click Element    xpath=//input[@name="name"]/following-sibling::div/button
    Sleep    0.5
    Input Text    name=name    자동화테스트

    # 연락처 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Click Element    name=phone
    Click Element    xpath=//input[@name="phone"]/following-sibling::div/button
    Sleep    0.5
    Input Text    name=phone    ${phone_number}

    # 이메일 
    Click Element    name=email
    Click Element    xpath=//input[@name="email"]/following-sibling::div/button
    Sleep    0.5
    Input Text    name=email    automation@test.com
    Screenshot

    Click Button    xpath=//button[normalize-space(.)='저장하기']
    Screenshot


5. 계약 관리
    Scroll Element Into View    xpath=//h3[text()='계약관리']


5.1. 계약 추가
    Click Button    xpath=//button[normalize-space(.)='계약 추가']
    Wait Until Element Is Visible    xpath=//h2[text()='계약 추가']    5
    Screenshot


5.2. 계약 제목
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Input Text    name=contractTitle    자동화테스트 ${managementCode}
    Screenshot


5.3. 파일 첨부
    Choose File     xpath=//*[@id="contractFile"]//input    ${testfile_PATH}
    Screenshot


5.4. 수수료율
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Click Element    id=direct
    Wait Until Element Is Visible    name=commissionText    5
    Input Text    name=commissionText    자동화테스트 ${managementCode}
    Screenshot

    # 계약 - 추가하기 버튼
    Click Button    xpath=//button[normalize-space(.)='추가하기']
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서를 작성할까요?']
    Screenshot
    Click Button    xpath=//button[normalize-space(.)='나중에']
    Sleep    1

    Scroll Element Into View    xpath=//button[@title='처음']
    Screenshot

    #### 계약 1개 더 추가
    # 계약 추가
    Click Button    xpath=//button[normalize-space(.)='계약 추가']
    Wait Until Element Is Visible    xpath=//h2[text()='계약 추가']    5

    # 계약 제목 
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Input Text    name=contractTitle    자동화테스트 ${managementCode}

    # 파일 첨부 
    Choose File     xpath=//*[@id="contractFile"]//input    ${testfile_PATH}
    Sleep    1

    # 계약 - 추가하기 버튼
    # Execute Javascript    document.body.style.zoom='80%'
    # Sleep    0.5
    Click Button    xpath=//button[normalize-space(.)='추가하기']
    Sleep    0.5
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서를 작성할까요?']
    # Execute Javascript    document.body.style.zoom='100%'
    Click Button    xpath=//button[normalize-space(.)='나중에']
    Sleep    1


5.5. 수수료율 확인
    Click Button    xpath=//button[@title='수수료율']
    Wait Until Element Is Visible    xpath=//h2[text()='수수료율']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


5.6. 계약서 확인
    Click Button    xpath=//button[@title='계약서']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


5.7. 계약 삭제
    Click Button    xpath=//button[@title='삭제'][1]
    Wait Until Element Is Visible    xpath=//h2[text()='삭제할까요?']    5
    Screenshot
    Click Button    xpath=//button[normalize-space(.)='삭제하기']
    Screenshot


6. 계약 - 재위탁통보서
    Click Button    xpath=//button[@title='재위탁 통보서'][1]
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서']    5
    Screenshot
    Click Button    xpath=//button[text()='통보서 작성하기']
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서 작성하기']    5
    Screenshot

    Scroll Element Into View    xpath=//h3[text()='제약사']


6.1. 재위탁 사유, 기타
    Click Element    name=reason
    Click Element    xpath=//input[@name="reason"]/following-sibling::div/button
    Sleep    0.5
    Input Text    name=reason    automation test
    Sleep    0.5
    Click Element    name=note
    # Click Element    xpath=//input[@name="note"]/following-sibling::div/button
    Sleep    0.5
    Input Text    name=note    automation test
    Screenshot


6.2. 통보서 기재일
    Click Element    id=created-date
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


6.3. 제약사 추가
    Scroll Element Into View   xpath=//button[normalize-space(.)='작성하기']
    Screenshot
    Click Element    xpath=//button[text()='추가하기']
    Wait Until Element Is Visible    xpath=//h2[text()='제약사 추가']    5
    Screenshot


    # 제약사 검색
    Input Text    xpath=//input[@placeholder='제약사 명 검색']    팜플
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot
    Click Element    xpath=//div[text()='팜플제약']/ancestor::div[contains(@class,'ag-row')]//button
    Screenshot

    Click Element    xpath=//input[@placeholder='제약사 명 검색']
    Click Element    xpath=//input[@placeholder='제약사 명 검색']/following-sibling::div/button

    Input Text    xpath=//input[@placeholder='제약사 명 검색']    투썬
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot
    Click Element    xpath=//div[text()='투썬제약']/ancestor::div[contains(@class,'ag-row')]//button
    Screenshot

    # 제약사 추가하기
    Click Element    xpath=(//button[text()='추가하기'])[last()]
    Screenshot

    # 추가한 제약사 삭제
    Click Element    xpath=//button[@title='삭제'][1]
    Screenshot


6.4. 통보서 작성하기
    Click Element    xpath=//button[text()='작성하기']
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서를 작성할까요?']    5
    Screenshot
    Click Element    xpath=(//button[text()='작성하기'])[last()]
    Sleep    0.5
    Screenshot

    # 위탁 계약 page로 복귀
    Click Element    xpath=//a[span[text()='회원 업체 관리 ']]
    Wait Until Element Is Visible    xpath=//h2[text()='회원 업체 관리 ']    5


7. 검색
    Click Element    xpath=//button[span[text()="상태 (전체)"]]
    Wait Until Element Is Visible    xpath=//div[span[text()="등록"]]    5
    Screenshot

    Click Element    xpath=//div[span[text()="등록"]]
    Screenshot

    Click Element    xpath=//button[span[text()="사업자상태 (전체)"]]
    Screenshot

    Press Keys    NONE    ESC
    Click Element    xpath=//button[span[text()="상호/법인명"]]
    Wait Until Element Is Visible    xpath=//div[span[text()="관리코드"]]    5
    Screenshot

    Click Element    xpath=(//div[span[text()="관리코드"]])[last()]
    Screenshot

    ${datetime_monthday}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d')
    Input Text    xpath=//input[@placeholder="검색어를 입력해 주세요"]    ${datetime_monthday}
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Sleep    1
    Screenshot

