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
3.1 위탁계약
    Login_CSO
    Sleep    1
    Screenshot


3.1.1. 업체 추가하기 (가입 업체)
    ##### 가입된 업체 추가 
    # 업체 추가하기 
    Click Button    xpath=//button[normalize-space(.)='추가하기']
    Wait Until Element Is Visible    xpath=//h2[text()='위탁 업체 추가']    5
    Screenshot


3.1.2. 사업자번호 입력
    # 직전 회원가입한 사업자번호 입력
    ${lastBizNo}=    Get Last Biz Number
    Press Key    id=bizNumber    ${lastBizNo}
    Screenshot
    Click Button    xpath=//button[text()='확인하기']
    Wait Until Element Is Visible    xpath=//h2[text()='위탁 업체 추가']    5
    Screenshot


3.1.3. 관리코드
    # 위탁업체 추가하기 
    # 관리코드
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=managementCode    ${managementCode}


3.1.4. 담당자 정보    
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
    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='나중에']    5
    Screenshot

    # 확인버튼
    Click Button    xpath=//button[normalize-space(.)='나중에']
    Sleep    1
    Screenshot


3.1.5. 업체 추가하기 (미가입 업체)
    ##### 미가입사용자 추가 
    # 업체 추가하기 
    Click Button    xpath=//button[normalize-space(.)='추가하기']    #추가하기 버튼 
    Wait Until Element Is Visible    xpath=//h2[text()='위탁 업체 추가']    5
    Screenshot


3.1.6. 사업자번호 입력
    ${bizNo}=     Get Biz Number
    Set Suite Variable    ${bizNo}
    Press Key    id=bizNumber    ${bizNo}
    Screenshot

    Click Button    xpath=//button[text()='확인하기']
    Wait Until Element Is Visible    xpath=//h2[text()='위탁 업체 추가']    5
    Screenshot


3.1.7. 파일첨부
    ## 파일 첨부    
    Choose File     xpath=//*[@id="bizRegCertFileUuid"]//input    ${testfile_PATH}
    Sleep    0.5
    Choose File     xpath=//*[@id="salesCertFileUuid"]//input    ${testfile_PATH}
    Screenshot


3.1.8. 관리코드
    # 관리코드
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=managementCode    ${managementCode}.
    

3.1.9. 담당자 정보
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
    Wait Until Element Is Visible    xpath=//h2[text()='업체 등록 요청이 완료되었습니다']    5
    Screenshot

    # 확인버튼
    Click Element    xpath=//button[text()='확인']
    sleep    1

3.1.10. 상세
    Click Element    xpath=//a[text()="${bizNo}"]
    Wait Until Element Is Visible    xpath=//h2[text()='업체 상세 보기']    5
    Screenshot



3.1.11. 수료증
    sleep   1
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


    # CSO 신고증 목록 보기 
    ${datetime}=    Evaluate    datetime.datetime.now().strftime('%Y-%m-%d')    modules=datetime
    Click Element    xpath=//dd[p[text()='${datetime}']]    
    Sleep    1
    Screenshot

    ## 교육 수료증 보기 버튼


    Press Keys    NONE    ESC



    Go Back
    Sleep    1






3.2. 업체 상세
    ${lastBizNo}=    Get Last Biz Number
    Click Element    xpath=//a[translate(normalize-space(text()), "-", "") = "${lastBizNo}"]
    Wait Until Element Is Visible    xpath=//h2[text()='업체 상세 보기']    5
    Screenshot


3.2.1. 관리코드 
    # 관리코드 수정 버튼 
    Click Button    xpath=//button[@title='수정'][1]
    Wait Until Element Is Visible    xpath=//h2[text()='관리 코드 수정']    5
    Screenshot

    # 관리 코드
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}

    Click Element    name=managementCode
    Click Element    xpath=//input[@name="managementCode"]/following-sibling::div/button
    Sleep    0.5
    Press Key    name=managementCode    ${managementCode}F
    Screenshot
    Click Button    xpath=//button[normalize-space(.)='저장하기']
    Screenshot


3.2.2. 첨부파일
    Scroll Element Into View    xpath=//dt[text()='이메일']
    Sleep    1


3.2.2.1. 사업자등록증
    Click Button    xpath=//button[text()='보기'][1]
    Wait Until Element Is Visible    xpath=//h2[text()='사업자등록증']    5
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC


3.2.2.2. 의약품 판촉영업 신고증
    Click Button    xpath=(//button[text()='보기'])[last()]
    Wait Until Element Is Visible    xpath=//h2[text()='영업신고증']    5
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC


3.2.2.3. CSO 교육 수료증
    Click Element    xpath=//button[text()='등록']
    Wait Until Element Is Visible    xpath=//button[text()='확인']    5
    Screenshot
    Click Button    xpath=//button[text()='확인']
    Sleep    1



3.2.3. 담당자 정보
    Click Button    xpath=(//button[@title='수정'])[last()]
    Wait Until Element Is Visible    xpath=//h2[text()='담당자 정보 수정']    5
    Screenshot

    # 이름
    Click Element    name=name
    Click Element    xpath=//input[@name="name"]/following-sibling::div/button
    Sleep    0.5
    Press Key    name=name    자동화테스트

    # 연락처 
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    Click Element    name=phone
    Click Element    xpath=//input[@name="phone"]/following-sibling::div/button
    Sleep    0.5
    Press Key    name=phone    ${phone_number}

    # 이메일 
    Click Element    name=email
    Click Element    xpath=//input[@name="email"]/following-sibling::div/button
    Sleep    0.5
    Press Key    name=email    automation@test.com
    Screenshot

    Click Button    xpath=//button[normalize-space(.)='저장하기']
    Screenshot


3.4. 계약 관리
    Scroll Element Into View    xpath=//h2[text()='업체 상세 보기']


3.4.1. 계약 추가
    Click Button    xpath=//button[normalize-space(.)='계약 추가']
    Wait Until Element Is Visible    xpath=//h2[text()='계약 추가']    5
    Screenshot


3.4.2. 계약 제목
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=contractTitle    자동화테스트 ${managementCode}
    Sleep    0.5


3.4.3. 파일 첨부
    Choose File     xpath=//*[@id="contractFile"]//input    ${testfile_PATH}
    Sleep    0.5


3.4.4. 수수료율
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Click Element    id=direct
    Wait Until Element Is Visible    name=commissionText    5
    Press Key    name=commissionText    자동화테스트 ${managementCode}
    Screenshot

    # 계약 - 추가하기 버튼
    # Execute Javascript    document.body.style.zoom='80%'
    Click Button    xpath=//button[normalize-space(.)='추가하기']
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서를 작성할까요?']
    # Execute Javascript    document.body.style.zoom='100%'
    Screenshot
    Click Button    xpath=//button[normalize-space(.)='나중에']
    Sleep    1

    # 계약 1개 더 추가
    # 계약 추가
    Click Button    xpath=//button[normalize-space(.)='계약 추가']
    Wait Until Element Is Visible    xpath=//h2[text()='계약 추가']    5

    # 계약 제목 
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=contractTitle    자동화테스트 ${managementCode}

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


3.4.5. 수수료율 확인
    Click Button    xpath=//button[@title='수수료율']
    Wait Until Element Is Visible    xpath=//h2[text()='수수료율']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


3.4.6. 계약서 확인
    Click Button    xpath=//button[@title='계약서']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


3.4.7. 계약 삭제
    Click Element    css=div.ag-body-horizontal-scroll
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT

    Click Button    xpath=//button[@title='삭제'][1]
    Wait Until Element Is Visible    xpath=//h2[text()='삭제할까요?']    5
    Screenshot
    Click Button    xpath=//button[normalize-space(.)='삭제하기']
    Screenshot


3.5. 계약 - 재위탁통보서
    Click Button    xpath=//button[@title='재위탁 통보서'][1]
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서']    5
    Screenshot
    Click Button    xpath=//button[text()='통보서 작성하기']
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서 작성하기']    5
    Screenshot

    Scroll Element Into View    xpath=//h3[text()='제약사']


3.5.1. 재위탁 사유, 기타
    Click Element    name=reason
    Click Element    xpath=//input[@name="reason"]/following-sibling::div/button
    Sleep    0.5
    Press Key    name=reason    automation test
    Sleep    0.5
    Click Element    name=note
    # Click Element    xpath=//input[@name="note"]/following-sibling::div/button
    Sleep    0.5
    Press Key    name=note    automation test
    Screenshot


3.5.2. 통보서 기재일
    Click Element    id=created-date
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


3.5.3. 제약사 추가
    Scroll Element Into View   xpath=//button[normalize-space(.)='작성하기']
    Click Element    xpath=//button[text()='추가하기']

    Wait Until Element Is Visible    xpath=//h2[text()='제약사 추가']    5
    Screenshot


    # 제약사 검색
    Press Key    xpath=//input[@placeholder='제약사 명 검색']    팜플
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot
    Click Element    xpath=//div[text()='팜플제약']/ancestor::div[contains(@class,'ag-row')]//button
    Screenshot

    Click Element    xpath=//input[@placeholder='제약사 명 검색']
    Click Element    xpath=//input[@placeholder='제약사 명 검색']/following-sibling::div/button

    Press Key    xpath=//input[@placeholder='제약사 명 검색']    투썬
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


3.5.4. 통보서 작성하기
    Click Element    xpath=//button[text()='작성하기']
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서를 작성할까요?']    5
    Screenshot
    Click Element    xpath=(//button[text()='작성하기'])[last()]
    Sleep    0.5
    Screenshot

    # 위탁 계약 page로 복귀
    Click Element    xpath=//a[span[text()='위탁 계약']]
    Sleep    1


3.6. 검색
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
    Press Key    xpath=//input[@placeholder="검색어를 입력해 주세요"]    ${datetime_monthday}
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Screenshot

