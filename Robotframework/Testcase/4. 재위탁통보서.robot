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
4.1. 재위탁통보서
    Login_CSO
    Click Element    xpath=//a[span[text()='재위탁 통보서 관리']]
    Sleep    1
    Screenshot
    

4.1.1 재위탁통보서 작성하기
    Click Element    xpath=//button[@title='작성하기']
    Sleep    1
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서 작성하기']    5
    Screenshot


4.1.2. 제약사 선택
    Click Element    xpath=//input[@placeholder='제약사 명 검색']
    Input Text    xpath=//input[@placeholder='제약사 명 검색']    투썬
    Screenshot

    Press Keys    xpath=//input[@placeholder='제약사 명 검색']    ENTER
    Screenshot


4.1.3. 재위탁 사유, 기타
    # 재위탁 사유
    Input Text    name=reason    1
    Input Text    name=reason    ${EMPTY}
    Sleep    0.5
    Press Key    name=reason    automation test
    Sleep    0.5

    # 기타
    Input Text    name=note    ${EMPTY}
    Sleep    0.5
    Press Key    name=note    automation test
    Screenshot
    

4.1.4. 통보서 기재일
    Scroll Element Into View    xpath=//button[@title='추가하기']

    Click Button    xpath=//button[@id='date']
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


4.1.5. 재위탁 업체 추가
    Scroll Element Into View    xpath=//button[@title='작성하기']
    
    # 재위탁 업체 추가버튼
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


4.1.6. 재위탁통보서 작성하기
    # 통보서 작성 Page 의 작성하기 버튼
    Click Button    xpath=//button[@title="작성하기"]
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서를 작성할까요?']    5
    Screenshot

    # 모달의 컨펌 확인 
    Click Button    xpath=(//button[@title="작성하기"])[2]
    Sleep    0.5
    Screenshot


4.1.7. 재위탁통보서 삭제/수정
    Click Element    xpath=(//button[@title='재위탁통보서'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서']    5
    Screenshot

    # 미전송 통보서 삭제하기
    Click Button    xpath=//button[text()='삭제하기']
    Wait Until Element Is Visible    xpath=//h2[text()='삭제할까요?']    5
    Screenshot
    Click Button    xpath=//button[@title='삭제하기']
    Sleep    0.5
    Screenshot

    # 미전송 통보서 정보 수정
    Click Element    xpath=(//button[@title='재위탁통보서'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서']    5
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


4.1.8. 첨부파일
    Click Element    xpath=(//button[@title='파일'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='파일']    5


4.1.8.1. 계약서
    Sleep    2
    Screenshot


4.1.8.2. 수수료율
    Click Element    xpath=//button[normalize-space(.)='수수료율']
    Sleep    2
    Screenshot


4.1.8.3. 수료증
    Click Element    xpath=//button[normalize-space(.)='수료증']
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


4.2. 재위탁 통보서 전송
    ## 재위탁 통보서 작성 의 check box 선택 
    Wait Until Element Is Visible    xpath=//div[contains(@class,'ag-selection-checkbox')]    5
    Click Element    xpath=(//div[contains(@class,'ag-selection-checkbox')])[2]
    Screenshot


4.2.1. 재위탁 통보 전송하기
    # 전송하기 버튼 
    Click Button    xpath=//button[@title="전송하기"]
    Wait Until Element Is Visible   xpath=//h2[text()='1건의 통보서를 전송할까요?']    5
    Screenshot

    # 모달의 버튼 선택
    Click Button    xpath=(//button[@title="전송하기"])[2]
    Screenshot


4.3. 받은 재위탁 통보서
    # 계정 변경
    Logout
    Login_pharm_pharm1

    Click Element    xpath=//a[span[text()='받은 재위탁 통보서']]
    Sleep    1
    Screenshot


4.3.1. 재위탁 통보서
    Click Button    xpath=//button[@title='통보서']
    Wait Until Element Is Visible    xpath=//h2[text()='재위탁 통보서']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


4.3.2. 첨부파일
    Click Element    xpath=(//button[@title='파일'])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='파일']    5


4.3.2.1. 계약서
    Sleep    2
    Screenshot


4.3.2.2. 수수료율
    Click Element    xpath=//button[normalize-space(.)='수수료율']
    Sleep    2
    Screenshot


4.3.2.3. 수료증
    Click Element    xpath=//button[normalize-space(.)='수료증']
    Sleep    2
    Screenshot


4.3.2.4. 수료증(재위탁)
    Click Element    xpath=//button[normalize-space(.)='수료증(재위탁)']
    Sleep    2
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

