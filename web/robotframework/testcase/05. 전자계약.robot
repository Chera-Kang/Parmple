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

    Click Element    xpath=//a[span[text()='계약서 관리']]
    Wait Until Element Is Visible    xpath=//h2[text()='계약서 관리']    5
    Screenshot

템플릿
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
    Wait Until Element Is Visible    xpath=//h2[text()='계약서 관리']    5
    Sleep    1

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

    Sleep    1
    Screenshot
    
    Click Element    xpath=//button[@title='미리보기']
    Wait Until Element Is Visible    xpath=//h2[text()='미리보기']    5
    Screenshot

    Press Keys    NONE    ESC
    Sleep    1

    Click Element    xpath=//button[@title='저장하기']
    Sleep    1

    Click Element    xpath=//button[span[text()='템플릿 관리']]
    Wait Until Element Is Visible    xpath=//h2[text()='템플릿 관리']    5
    Screenshot

    Press Keys    NONE    ESC
    Sleep    1


계약서 작성
    Click Element    xpath=//button[span[text()='계약서 작성']]
    Wait Until Element Is Visible    xpath=//h2[text()='계약서 작성하기']    5
    Screenshot

    # 제목
    Input Text    name=title    자동화테스트
    Sleep    0.5

    Click Element    id=date
    Sleep    0.5
    # 계약일
    # 현재 날짜의 '일(day)' 가져오기 (1~31)
    ${day}=    Evaluate    datetime.datetime.now().day    modules=datetime
    # 해당 날짜 클릭
    Click Element    xpath=//td[button[text()='${day}']]
    Screenshot

    # 계약 업체
    Click Element    xpath=//button[@title='업체 검색']
    Wait Until Element Is Visible    xpath=//h2[text()='업체 검색']    5
    Screenshot

    # 업체명 검색 입력 (로케이터 수정: placeholder 일치 및 input 태그 직접 지정)
    Wait Until Element Is Visible    xpath=//input[@placeholder='상호/법인명 검색']    5
    Input Text    xpath=//input[@placeholder='상호/법인명 검색']    투썬
    Screenshot

    # 검색 버튼 클릭
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot

    Click Element    xpath=//div[span[text()='투썬인베스트 주식회사']]
    Screenshot

    Click Element    xpath=//button[@title='추가하기']
    Screenshot

    # 계약서
    # 템플릿
    Scroll Element Into View    xpath=//div[label[text()='서명란']]
    Screenshot

    Click Element    xpath=//div[button[span[text()='직접 입력']]]
    Screenshot

    # 자동화테스트_ 가 포함되면 선택
    Click Element    xpath=//div[span[starts-with(text(), '자동화테스트_')]]    
    Screenshot

    # 내용
    # 미리보기
    Sleep    0.5
    Scroll Element Into View    xpath=//button[@title='작성하기']
    Screenshot

    Click Element    xpath=//button[@title='미리보기']
    Wait Until Element Is Visible    xpath=//h2[text()='미리보기']    5
    Screenshot

    Press Keys    NONE    ESC
    Sleep    1

    # 추가파일 업로드
    Wait Until Element Is Visible    xpath=//input[@type='file']    5
    Choose File    xpath=//input[@type='file' and contains(@accept, 'xlsx')]    ${testfile_PATH}
    Screenshot
    
    Click Element    xpath=//button[@title='작성하기']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서를 작성할까요?']    5
    Screenshot

    Click Element    xpath=(//button[@title='작성하기'])[last()]
    Sleep    1


목록 계약서 확인
    # 목록 계약서 확인을 위한 검색 초기화 동작
    Sleep    2
    Click Element    xpath=//button[span[text()='검색 초기화']]
    Sleep    1
    Click Element    xpath=//button[span[text()='검색 초기화']]
    Sleep    1
    # 목록 계약서 확인을 위한 검색 초기화 동작

    Click Element    xpath=//button[@title='계약서']
    Sleep    2
    Screenshot
    
    Press Keys    None    ESC
    Sleep    1

계약서 수정하기
    Click Element    xpath=//button[@title='수정']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서 수정하기']    5
    Screenshot

    # 제목
    Input Text    name=title    _fix
    Screenshot

    Click Element    id=date
    Sleep    1
    Press Keys    None    ESC
    Sleep    1

    #내용
    # Quill 에디터 영역에 텍스트 입력 (contenteditable 대응)
    Wait Until Element Is Visible    css:.ql-editor    5
    Execute Javascript    document.querySelector('.ql-editor').innerHTML = '<p>자동화테스트 내용 수정하기</p>'
    Sleep    2
    Screenshot
    
    Click Element    xpath=//button[@title='수정하기']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서 관리']    5
    Sleep    1


전송하기
    Click Element    xpath=(//div[contains(@class,'ag-selection-checkbox')])[1]
    Screenshot

    Click Element    xpath=//button[@title='전송하기']
    Wait Until Element Is Visible    xpath=//h2[text()='계약서 전송하기']    5
    Screenshot

    Click Element    xpath=//button[div[span[text()='서명 가능 기한']]]
    Screenshot
    # 선택 가능한 첫 번째 날짜 클릭
    Click Element    xpath=(//button[@name='day' and not(@disabled)])[1]
    Screenshot

    Click Element    xpath=//button[i[contains(@class, 'ri-arrow-down-s-line')]]
    Screenshot

    Click Element    id=termsAll
    Screenshot

    # 전송하기 버튼 클릭 (가로막힘 문제를 방지하기 위해 JavaScript 클릭 활용)
    Execute Javascript    var btns = document.querySelectorAll("button[title='전송하기'][type='submit']"); if(btns.length > 0) btns[btns.length - 1].click();
    Sleep    1
    Screenshot


전송 완료
    # 목록 계약서 확인을 위한 검색 초기화 동작
    Sleep    2
    Click Element    xpath=//button[span[text()='검색 초기화']]
    Sleep    1
    Click Element    xpath=//button[span[text()='검색 초기화']]
    Sleep    1
    # 목록 계약서 확인을 위한 검색 초기화 동작

    Click Element    xpath=//button[@title='계약서']
    Sleep    2
    Screenshot
    Press Keys    None    ESC
    Sleep    1

전송 취소
    Click Element    xpath=(//div[contains(@class,'ag-selection-checkbox')])[1]
    Screenshot

    Click Element    xpath=//button[@title='전송취소']
    Wait Until Element Is Visible    xpath=//h2[text()='계약 전송을 취소할까요?']
    Screenshot

    Click Element    xpath=//button[@title='확인']
    Sleep    1


재전송
    # 전송하기
    Click Element    xpath=(//div[contains(@class,'ag-selection-checkbox')])[1]
    Sleep    1

    Click Element    xpath=//button[@title='전송하기']
    Sleep    1

    Click Element    xpath=//button[div[span[text()='서명 가능 기한']]]
    Sleep    1

    # 선택 가능한 첫 번째 날짜 클릭
    Click Element    xpath=(//button[@name='day' and not(@disabled)])[1]
    Sleep    1

    Click Element    xpath=//button[i[contains(@class, 'ri-arrow-down-s-line')]]
    Sleep    1

    Click Element    id=termsAll
    Sleep    1

    # 전송하기 버튼 클릭 (가로막힘 문제를 방지하기 위해 JavaScript 클릭 활용)
    Execute Javascript    var btns = document.querySelectorAll("button[title='전송하기'][type='submit']"); if(btns.length > 0) btns[btns.length - 1].click();
    Sleep    1

