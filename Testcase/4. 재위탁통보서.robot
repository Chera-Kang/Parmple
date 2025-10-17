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
---- 재위탁통보서
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Login_CSO
    Click Element    xpath=//a[span[text()='재위탁 통보서 관리']]
    Sleep    1
    Screenshot
    

---- 재위탁통보서 작성
    # 통보서 작성 Page 진입
    Click Element    xpath=//button[@title='작성하기']
    Sleep    1
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서 작성하기']    5
    Screenshot

    #제약사 선택
    Click Element    xpath=//input[@placeholder='제약사 명 검색']
    Input Text    xpath=//input[@placeholder='제약사 명 검색']    투썬
    Screenshot
    Press Keys    xpath=//input[@placeholder='제약사 명 검색']    ENTER
    Screenshot

    # 재위탁 사유, 기타
    Input Text    name=reason    1
    Input Text    name=reason    ${EMPTY}
    Sleep    0.5
    Press Key    name=reason    automation test
    Sleep    0.5
    Input Text    name=note    1
    Input Text    name=note    ${EMPTY}
    Sleep    0.5
    Press Key    name=note    automation test
    Screenshot
    

    Scroll Element Into View    xpath=//button[@title='추가하기']

    # 통보서 기재일 
    Click Button    xpath=//button[@id='date']
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    
    Scroll Element Into View    xpath=//button[@title='작성하기']

    # 재위탁 업체 추가
    Click Element    xpath=//button[@title='추가하기']
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 업체 추가하기']    5
    Screenshot
    Click Element    xpath=(//div[contains(@class,'ag-selection-checkbox')])[1]
    Click Element    xpath=(//div[contains(@class,'ag-selection-checkbox')])[2]
    Click Element    xpath=(//div[contains(@class,'ag-selection-checkbox')])[3]
    Screenshot

    # 재위탁 업체 모달의 추가하기 버튼 
    Click Button    xpath=(//button[@title="추가하기"])[2]   
    Screenshot

    # 추가한 업체 삭제
    Click Element    xpath=//button[@title='삭제'][1]
    Screenshot

    # 통보서 작성 Page 의 작성하기 버튼
    Click Button    xpath=//button[@title="작성하기"]
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서를 작성할까요?']    5
    Screenshot

    # 모달의 컨펌 확인 
    Click Button    xpath=(//button[@title="작성하기"])[2]
    Sleep    0.5
    Screenshot



---- 재위탁통보서 삭제/수정
    Sleep    1
    # 목록 첨부파일 확인
    Click Element    xpath=(//button[@title='재위탁통보서'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='수탁자의 재위탁 통보서']    5
    Screenshot

    # 미전송 통보서 삭제하기
    Click Button    xpath=//button[text()='삭제하기']
    Wait Until Element Is Visible    xpath=//h2[text()='삭제할까요?']    5
    Screenshot
    Click Button    xpath=//button[@title='삭제하기']
    Sleep    1
    Screenshot

    # 미전송 통보서 정보 수정
    Click Element    xpath=(//button[@title='재위탁통보서'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='수탁자의 재위탁 통보서']    5
    Screenshot

    # 재위탁 사유/기타
    Input Text    name=reason    1
    Input Text    name=reason    ${EMPTY}
    Sleep    0.5
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=reason    자동화_${datetime}
    Screenshot

    Scroll Element Into View    xpath=//div[text()='(서명 또는 인)']

    Input Text    name=note    1
    Input Text    name=note    ${EMPTY}
    Sleep    0.5
    ${datetime}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    ${managementCode}=    Set Variable    ${datetime}
    Press Key    name=note    자동화_${datetime}
    Screenshot

    # 미전송 통보서 수정
    Click Button    xpath=//button[text()='수정하기']
    Wait Until Element Is Visible    xpath=//h2[text()='수정 완료']    5
    Screenshot

    # 모달의 컨펌 확인 
    Click Button    xpath=(//button[@title="확인"])[last()]
    Sleep    0.5
    Press Keys    NONE    ESC
    Sleep    0.5


    # 그리드에서 첨부자료 확인    
    Click Element    css=div.ag-body-horizontal-scroll
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_RIGHT
    Screenshot

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



---- 재위탁통보서 전송
    Sleep    1
    # 그리드 체크박스 선택
    Click Element    css=div.ag-body-horizontal-scroll
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_LEFT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_LEFT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_LEFT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_LEFT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_LEFT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_LEFT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_LEFT
    Press Keys       css=div.ag-body-horizontal-scroll    ARROW_LEFT
    Screenshot

    ## 재위탁 통보서 작성 의 check box 선택 
    Wait Until Element Is Visible    xpath=//div[contains(@class,'ag-selection-checkbox')]    5
    Click Element    xpath=(//div[contains(@class,'ag-selection-checkbox')])[2]
    Screenshot

    # 전송하기 버튼 
    Click Button    xpath=//button[@title="전송하기"]
    Wait Until Element Is Visible   xpath=//h2[text()='1건의 통보서를 전송할까요?']    5
    Screenshot

    # 모달의 버튼 선택
    Click Button    xpath=(//button[@title="전송하기"])[2]
    Screenshot


---- 재위탁통보서 관리
    # 계정 변경
    Logout
    Login_pharm_pharm1

    Click Element    xpath=//a[span[text()='받은 재위탁 통보서']]
    Sleep    1
    Screenshot

    Scroll Element Into View    xpath=//span[text()='Page']

    # 재위탁통보서
    Click Button    xpath=//button[@title='재위탁통보서']
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 수수료율 
    Click Button    xpath=//button[@title='수수료율']
    Wait Until Element Is Visible    xpath=//h2[text()='수수료율']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 계약서
    Click Button    xpath=//button[@title='계약서']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


---- 재위탁 현황
    Sleep    1

    Click Element    xpath=//a[span[text()='재위탁 현황']]
    Sleep    1
    Screenshot

    Scroll Element Into View    xpath=//span[text()='Page']

    # 검색 
    Click Element    xpath=//button[span[text()="상호/법인명"]]
    Wait Until Element Is Visible    xpath=//div[span[text()="사업자등록번호"]]    5
    Screenshot
    Press Keys    NONE    ESC
    Press Key    xpath=//input[@placeholder="검색어를 입력해주세요"]    휴피스
    Screenshot
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot

    # 펼침 
    Click Element    xpath=//div[@style[contains(.,'cursor: pointer')]]/i
    Screenshot
    Sleep    0.5

    # 재위탁통보서 
    Click Element    xpath=(//button[@title='재위탁통보서'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5



---- 이전 통보서 관리
    Sleep    1

    Click Element    xpath=//a[span[text()='이전 통보서 관리']]
    Sleep    1
    Screenshot







