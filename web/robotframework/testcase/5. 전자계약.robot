*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    String
Library    RequestsLibrary
Library    BuiltIn
Library    Process
Library    DateTime
Library    ../../../.venv/Lib/site-packages/robot/libraries/XML.py
Resource   ../keywords.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***
*** Keywords ***
*** Test Cases ***
5.1. 전자계약
    Login_CSO
    Sleep    1



    # 전자계약 메뉴 
    Click Element    xpath=//a[span[text()='계약서 관리']]
    Wait Until Element Is Visible    xpath=//h2[text()='계약서 관리']    5
    Sleep    1

    Click Element    xpath=//button[span[text()='템플릿 관리']]
    Wait Until Element Is Visible    xpath=//h2[text()='템플릿 관리']    5
    Screenshot

    Click Element    xpath=//div[span[button[@title='수정']]]
    Wait Until Element Is Visible    xpath=//h2[text()='계약서 템플릿 관리']    5
    Screenshot

    Scroll Element Into View    xpath=//div[button[@title='삭제하기']]
    Screenshot

    Click Element    xpath=//button[@title='삭제하기']
    Wait Until Element Is Visible    xpath=//h2[text()='삭제할까요?']    5
    Screenshot

    Click Element    xpath=(//button[@title='삭제하기'])[last()]
    Sleep    2

    Click Element    xpath=//button[span[text()='템플릿 관리']]
    Wait Until Element Is Visible    xpath=//h2[text()='템플릿 관리']    5
    Screenshot

    Click Element    xpath=//button[span[text()='템플릿 추가']]
    Wait Until Element Is Visible    xpath=//h2[text()='계약서 템플릿 추가']    5
    Screenshot

    ${datetime}=    Evaluate    datetime.datetime.now().strftime('%y%m%d-%H%M')    modules=datetime
    Input Text    name=templateTitle    자동화테스트_${datetime}
    Sleep    1

    # Quill 에디터 영역에 텍스트 입력 (contenteditable 대응)
    Wait Until Element Is Visible    css:.ql-editor    5
    Execute Javascript    document.querySelector('.ql-editor').innerHTML = '<p>자동화테스트2</p>'

    Sleep    2
    Screenshot
    
    Click Element    xpath=//button[@title='미리보기']
    Wait Until Element Is Visible    xpath=//h2[text()='미리보기']    5
    Screenshot

    Press Keys    NONE    ESC
    Sleep    1

    Click Element    xpath=//button[@title='저장하기']
    Sleep    2

    Click Element    xpath=//button[span[text()='템플릿 관리']]
    Wait Until Element Is Visible    xpath=//h2[text()='템플릿 관리']    5
    Screenshot

    Press Keys    NONE    ESC
    Sleep    1



    Click Element    xpath=//button[span[text()='계약서 작성']]
    Wait Until Element Is Visible    xpath=//h2[text()='계약서 작성하기']    5
    Screenshot

    # 제목
    Input Text    name=title    자동화테스트
    Sleep    1

    Click Element    id=date
    Sleep    1


    # 계약일
    # 현재 날짜의 '일(day)' 가져오기 (1~31)
    ${day}=    Evaluate    datetime.datetime.now().day    modules=datetime
    # 해당 날짜 클릭
    Click Element    xpath=//td[button[text()='${day}']]
    Sleep    0.5
    Screenshot

    # 계약 업체
    Click Element    xpath=//button[@title='업체 검색']
    Wait Until Element Is Visible    xpath=//h2[text()='업체 검색']    5
    Screenshot




    # 업체명 검색 입력 (로케이터 수정: placeholder 일치 및 input 태그 직접 지정)
    Wait Until Element Is Visible    xpath=//input[@placeholder='상호/법인명 검색']    5
    Input Text    xpath=//input[@placeholder='상호/법인명 검색']    투썬
    Sleep    1

    # 검색 버튼 클릭
    Click Element    xpath=//button[span[text()='검색']]
    Sleep    1

    Click Element    xpath=//div[span[text()='투썬인베스트 주식회사']]
    Sleep    1

    Click Element    xpath=//button[@title='추가하기']
    Sleep    1

    # 계약서

    # 템플릿
    Scroll Element Into View    xpath=//div[label[text()='서명란']]
    Sleep    1


    Click Element    xpath=//div[button[span[text()='직접 입력']]]
    Sleep    1

    Click Element    xpath=//div[span[starts-with(text(), '자동화테스트_')]]    # 자동화테스트_ 가 포함되면 선택 
    Sleep    1

    # 내용
    Sleep    1

    # 미리보기
    Scroll Element Into View    xpath=//button[@title='작성하기']
    Sleep    1


    Click Element    xpath=//button[@title='미리보기']
    Wait Until Element Is Visible    xpath=//h2[text()='미리보기']    5
    Sleep    1

    Press Keys    NONE    ESC
    Sleep    1





    # 추가파일 업로드
    Wait Until Element Is Visible    xpath=//input[@type='file']    5
    Choose File    xpath=//input[@type='file' and contains(@accept, 'xlsx')]    ${testfile_PATH}
    Sleep    1

    
    Click Element    xpath=//button[@title='작성하기']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서를 작성할까요?']    5
    Sleep    1

    Click Element    xpath=(//button[@title='작성하기'])[last()]
    Sleep    1




    Sleep   5










    Sleep    5