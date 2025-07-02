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
*** Keywords ***
*** Test Cases ***
---- 재위탁 통보서 작성 
    Wait Until Element Is Visible    xpath=//img[contains(@src, 'logo_200.25f0e37e.png')]    5

    Input Text    name=email    ${id_1}
    Press Key    name=password    ${password}
    Sleep    1
    Click Button    xpath=//button[text()='로그인']
    Sleep    3

    ## 재위탁 통보서 page 진입 
    Click Element    xpath=//a[span[text()='재위탁 통보서 작성']]
    Wait Until Element Is Visible    xpath=//div[contains(@class,'ag-selection-checkbox')]    5
    Screenshot

    # 목록 첨부파일 확인
    Click Element    xpath=(//button[@title='재위탁통보서'])[1]
    Screenshot

    # 재위탁사유 
    Input Text    name=reason    1
    Input Text    name=reason    ${EMPTY}
    Sleep    0.5
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=reason    자동화_${datetime}
    Sleep    0.5

    # 재위탁 내용 - 기타
    Input Text    name=note    1
    Input Text    name=note    ${EMPTY}
    Sleep    0.5
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=note    자동화_${datetime}
    Screenshot

    # 화면 스크롤
    Scroll Element Into View    xpath=//*[normalize-space(.)='귀하']
    Sleep    0.5

    # 재위탁통보서 - 수정하기 버튼 
    Click button    xpath=//button[normalize-space(.)='수정하기']
    Screenshot

    Press Keys    NONE    ESC
    Sleep    0.5
    Press Keys    NONE    ESC
    Sleep    0.5

    # 수수료율
    Click Element    xpath=(//button[@title='수수료율'])[1]
    Screenshot

    Press Keys    NONE    ESC
    Sleep    1

    # 계약서 
    Click Element    xpath=(//button[@title='계약서'])[1]
    Screenshot

    Press Keys    NONE    ESC
    Sleep    1

---- ---- 재위탁 통보서 작성하기 Page
    ## 재위탁 통보서 작성하기 page 
    Click button    xpath=//button[normalize-space(.)='작성하기']
    Wait Until Element Is Visible    xpath=//button[normalize-space(.)='작성하기']    5 
    Screenshot

    # 제약사 선택 
    Click Element    xpath=//*[normalize-space(.)='제약사 명 검색']
    Screenshot
    Input Text    xpath=//input[@placeholder='제약사 명 검색']    투썬 
    Screenshot
    Press Keys    xpath=//input[@placeholder='제약사 명 검색']    ENTER
    Screenshot

    # 재위탁 사유 
    Input Text    name=reason    1
    Input Text    name=reason    ${EMPTY}
    Sleep    0.5
    Press Key    name=reason    automation test
    Sleep    0.5

    # 기타 
    Input Text    name=note    1
    Input Text    name=note    ${EMPTY}
    Sleep    0.5
    Press Key    name=note    automation test
    Screenshot
    
    # 통보서 기재일 
    Click Button    xpath=//button[@id="writtenDate"]
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 화면 스크롤
    Scroll Element Into View    xpath=//button[text()='작성하기']
    Sleep    0.5

    # 재위탁업체 추가하기
    Click Button    xpath=//button[@title="추가하기"]
    Wait Until Element Is Visible    xpath=//input[@placeholder='상호/법인명 검색']    5
    Screenshot
    Click Element    xpath=(//div[contains(@class,'ag-selection-checkbox')])[1]
    Screenshot

    # 재위탁 업체 모달의 추가하기 버튼 
    Click Button    xpath=(//button[@title="추가하기"])[2]   
    Screenshot

    # Page 의 작성하기 버튼
    Click Button    xpath=//button[@title="작성하기"]
    Screenshot

    # 모달의 컨펌 확인 
    Click Button    xpath=(//button[@title="작성하기"])[2]
    Sleep    0.5

---- ---- 재위탁통보서 전송 
    ## 재위탁 통보서 작성 의 check box 선택 
    Wait Until Element Is Visible    xpath=//div[contains(@class,'ag-selection-checkbox')]    5
    Click Element    xpath=(//div[contains(@class,'ag-selection-checkbox')])[2]
    Screenshot

    # 전송하기 버튼 
    Click Button    xpath=//button[@title="전송하기"]
    Wait Until Element Is Visible   xpath=(//button[@title="전송하기"])[2]
    Screenshot

    # 모달의 버튼 선택
    Click Button    xpath=(//button[@title="전송하기"])[2]
    Screenshot

    # 검색 
    Click Element    xpath=//button[span[text()="전송상태 (전체)"]]
    Wait Until Element Is Visible    xpath=//div[span[text()="전송대기"]]    5
    Screenshot
    Press Keys    NONE    ESC

    Click Element    xpath=//input[@placeholder="통보서 기재일"]
    Wait Until Element Is Visible    name=previous-month    5
    Screenshot
    Press Keys    NONE    ESC

    Click Element    xpath=//button[span[text()="제약사"]]
    Wait Until Element Is Visible    xpath=//div[span[text()="관리코드"]]    5
    Screenshot
    Click Element    xpath=//div[span[text()="관리코드"]]
    Screenshot

    ${datetime_monthday}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d')
    Press Key    xpath=//input[@placeholder="검색어를 입력해주세요"]    ${datetime_monthday}
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


---- 재위탁 통보서 관리 
    ### 계정변경
    # 프로필
    Click Element    xpath=//button[@data-sidebar='menu-button']
    
    # 내 정보 선택
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='내 정보']    5
    Click Element    xpath=//a[normalize-space(.)='내 정보']
    Wait Until Element Is Visible    xpath=//h2[normalize-space(.)='내 정보']

    # 화면 스크롤
    Scroll Element Into View    xpath=//*[normalize-space(.)='로그아웃']
    Sleep    0.5

    # 로그아웃 버튼 선택 
    Click Element    xpath=//button[@title='로그아웃']
    Wait Until Element Is Visible    name=email    5

    # 제약사 로그인 
    Input Text    name=email    ${id_2}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Wait Until Element Is Visible    xpath=//a[span[text()='재위탁 통보서 관리']]    5

    #### 재위탁 통보서 관리 Page 
    Click Element    xpath=//a[span[text()='재위탁 통보서 관리']]
    Screenshot

    # 재위탁통보서 
    Click Element    xpath=(//button[@title='재위탁통보서'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 수수료율
    Click Element    xpath=(//button[@title='수수료율'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='수수료율']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 계약서 
    Click Element    xpath=(//button[@title='계약서'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='계약서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 검색 
    Click Element    xpath=//input[@placeholder="통보서 수신일"]
    Wait Until Element Is Visible    name=previous-month    5
    Screenshot
    Press Keys    NONE    ESC

    Click Element    xpath=//input[@placeholder="통보서 기재일"]
    Wait Until Element Is Visible    name=previous-month    5
    Screenshot
    Press Keys    NONE    ESC

    Click Element    xpath=//button[span[text()="수탁자 상호명"]]
    Wait Until Element Is Visible    xpath=//div[span[text()="재수탁자 상호명"]]    5
    Screenshot
    Click Element    xpath=//div[span[text()="재수탁자 상호명"]]
    Screenshot
    
    Press Key    xpath=//input[@placeholder="검색어를 입력해주세요"]    네이처
    Screenshot

    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


---- 재위탁 목록 
    ##### 재위탁 목록 Page 
    Click Element    xpath=//a[span[text()='재위탁 목록']]
    Sleep    1
    Screenshot

    # 펼침 
    Click Element    css=svg.lucide-chevron-right
    Screenshot
    Sleep    0.5

    # 재위탁통보서 
    Click Element    xpath=(//button[@title='재위탁통보서'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

