*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Resource   ../keywords_legacy.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite
*** Variables ***
*** Keywords ***
*** Test Cases ***
---- 0. ETC Testcase
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    Input Text    id=login-email    ${USER_2_ID}
    Input Text    id=login-password    ${USER_2_PW}
    Sleep    0.5
    Click Button    class=btn
    
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10


---- 1. 공지사항 Testcase
    MainMenu Mouse Over


-------- 1.1. 제약사 공지사항
    Click Element    xpath=//div[@class='gnb_title' and text()='제약사 공지사항']
    Wait Until Element Is Visible    class=b-grid-cell    10
    Screenshot

    ### 제약사별 sort 
    Click Element    xpath=//label[normalize-space(text())='제약사별']
    Screenshot
    Click Element    class=b-group-state-icon
    Screenshot
    Click Element    class=b-group-state-icon
    Screenshot
    
    ### 구분별 sort 
    Click Element    xpath=//label[normalize-space(text())='구분별']
    Screenshot
    Click Element    class=b-group-state-icon
    Screenshot
    Click Element    class=b-group-state-icon
    Screenshot    

    ### 제품별 sort
    Click Element    xpath=//label[normalize-space(text())='제품별']
    Sleep    1

    ### 제품 선택 
    Click Element    xpath=//*[@id="b-grid-1-normalSubgrid"]/div[3]/div[4]
    Sleep    5
    Screenshot

    #동일성분의약품
    Click Element    xpath=//*[@id="main_content"]/div/div/div/div[1]/ul[2]/li[2]/a
    Wait Until Element Is Visible    class=b-grid-panel-body    5
    Screenshot

    Go Back

    ### 제품 검색 
    Sleep    1
    Input Text    name=sw    라이트
    Click Button    btn-search
    Screenshot
    Click Button    btn-init-search
    Sleep    1


-------- 1.2. 신규 개원 정보
    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='신규 개원 정보']
    Wait Until Element Is Visible    class=b-grid-cell    10
    Screenshot

    ### 구분 필터 선택 
    Click Element    id=hp_class
    Screenshot
    Select From List By Label    id=hp_class    병원
    Sleep    1
    Press Keys    None    ESC

    ### 지역 필터 선택 
    Click Element    id=hp_area
    Screenshot
    Select From List By Label    id=hp_area    제주
    Sleep    1
    Press Keys    None    ESC

    ### 진료과목 필터 선택 
    Click Element    id=hp_department
    Screenshot
    Select From List By Label    id=hp_department    내과
    Sleep    1
    Press Keys    None    ES
    Sleep    1

    ### 검색 버튼 선택 
    Click Button    id=btn-search
    Wait Until Element Is Visible    class=b-grid-row    5
    Screenshot

    ### 초기화 버튼 선택 
    Click Button    id=btn-init-search
    Sleep    1


---- 2. 자료실 Testcase
    MainMenu Mouse Over


-------- 2.1. CSO 제품 정보
    Click Element    xpath=//div[@class='gnb_title' and text()='CSO 제품 정보']
    Wait Until Element Is Visible    class=b-grid-row    5
    Screenshot

    ### 제약사별 sort 
    Click Element    xpath=//label[normalize-space(text())='제약사별']
    Screenshot
    Click Element    class=b-action-ct
    Screenshot
    Click Element    class=b-action-ct
    Screenshot
    
    ### 약효분류별 sort 
    Click Element    xpath=//label[normalize-space(text())='분류별']
    Screenshot
    Click Element    xpath=//*[@id="b-grid-4-normalSubgrid"]/div[3]/div[1]/div
    Screenshot
    Click Element    xpath=//*[@id="b-grid-4-normalSubgrid"]/div[3]/div[1]/div/button
    Screenshot

    ### 제품별 sort
    Click Element    xpath=//label[normalize-space(text())='제품별']
    Sleep    1
    
    ### 제품 선택 
    Click Element    class=text_abbreviation
    Wait Until Element Is Visible    class=tab-content    5
    Screenshot

    ### 페이지 맨 아래로 스크롤
    Execute JavaScript    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
    Sleep    1

    ### 페이지 맨 위로 스크롤
    Execute JavaScript    window.scrollTo({ top: 0, behavior: 'smooth' })
    Sleep    1

    #동일성분의약품
    Click Element    xpath=//*[@id="main_content"]/div/div/div/div[1]/ul[2]/li[2]/a
    Wait Until Element Is Visible    class=b-grid-panel-body    5
    Screenshot

    ### 페이지 맨 아래로 스크롤
    Execute JavaScript    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
    Sleep    1

    ### 페이지 맨 위로 스크롤
    Execute JavaScript    window.scrollTo({ top: 0, behavior: 'smooth' })
    Sleep    1

    Go Back

    ### 제품 검색 
    Sleep    1
    Input Text    name=sw    라이트
    Click Button    btn-search
    Screenshot
    Click Button    btn-init-search
    Sleep    1


-------- 2.2. 영업자료실
    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='영업자료실']
    Sleep    5
    Screenshot


---- 3. 프로필 Testcase
    Sleep    1

    Click Element    xpath=//*[@id="navbar-collapse"]/ul/li/a/div/div
    Screenshot


-------- 3.1. 내 정보
    ${SetTime5}=    Evaluate    __import__('datetime').datetime.now().strftime('%y.%m.%d %H:%M')
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}

    Click Element    class=dropdown-menu
    Screenshot

    ### 이름
    Click Element    id=user.username
    Execute JavaScript    document.activeElement.value = ""
    Press Keys    id=user.username    Auto_${SetTime5}

    ### 휴대폰 번호
    Click Element    id=user.phone
    Execute JavaScript    document.activeElement.value = ""
    Press Keys    id=user.phone    ${phone_number}
    Screenshot

    ### 수정하기
    Click Element    //*[@id="updateProfileInformation"]/div/div[2]/div[4]/button
    Screenshot


-------- 3.2. 비밀번호
    ### 비밀번호 변경
    Click Element    //*[@id="updateProfileInformation"]/div/div[1]/button\
    Screenshot
    Input Password    id=current_password    dummy_password123!
    Input Password    id=password    dummy_password123!
    Input Password    id=password_confirmation    dummy_password123!
    Screenshot
    Click Element    xpath=//*[@id="updatePassword"]/div[3]/button[2]
    Wait Until Element Is Visible    class=swal2-popup    5
    Screenshot
    Click Button    class=swal2-confirm
    Sleep     0.5


-------- 3.3. 로그아웃
    Input Text    id=login-email    ${USER_2_ID}
    Input Text    id=login-password    ${USER_2_PW}
    Sleep    0.5
    Click Button    class=btn
    Sleep    1

    Click Element    xpath=//*[@id="navbar-collapse"]/ul/li/a/div/div
    Sleep    0.5

    Click Element    xpath=//*[@id="navbar-collapse"]/ul/li/ul/li[5]/a/span
    Screenshot
