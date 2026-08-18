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
*** Keywords ***
Generate Email
    ${result}=    Run Process    ${PYTHON_EXE}    ${EMAIL_GEN_PY}    chera.workspace    gmail.com    stdout=PIPE    stderr=PIPE
    ${email}=     Set Variable   ${result.stdout.strip()}
    RETURN    ${email}


*** Test Cases ***
1 프로필
    Login_CSO
    Sleep    1


2. 내 정보 Page
    Click Element    xpath=//button[@title='내 정보']
    Wait Until Element Is Visible    xpath=//h2[text()='내 정보']    5
    

2.1. 계정 정보
    Screenshot


2.2. 비밀번호 변경
    Click Element    xpath=//button[span[text()='계정 관리']]
    Screenshot

    Click Element    xpath=//div[text()=' 비밀번호 변경']
    Wait Until Element Is Visible    xpath=//h2[text()='비밀번호 변경']    5
    Screenshot

    Press Key    id=password    ${password}
    Press Key    id=newPassword    ${password}
    Press Key    id=confirmNewPassword    ${password}
    Screenshot

    Click Element    xpath=//button[@title='변경하기']
    Wait Until Element Is Visible    xpath=//h2[text()='비밀번호가 변경되었습니다.']    5
    Screenshot
    Click Element    xpath=//button[@title='확인']
    Screenshot


2.3. 계정 정보 수정
    Click Element    xpath=//button[span[text()='계정 관리']]
    Screenshot

    Click Element    xpath=//div[text()=' 계정 정보 수정']
    Wait Until Element Is Visible    xpath=//h2[text()='계정 정보 수정']    5
    Screenshot

    ${datetime_monthday}=    Evaluate    __import__('datetime').datetime.now().strftime('%m%d-%H%M')
    Input Text    name=name    ${EMPTY}
    Input Text    name=name    테스트_${datetime_monthday}
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    Input Text    name=phone    010${random_number}
    Screenshot
    Click Element    xpath=//button[@title='수정하기']
    Screenshot


3. 사업자 정보
    Scroll Element Into View    xpath=//img[@alt='도장이미지']
    Screenshot


3.1. 사업자등록증
    Click Button    xpath=//button[text()='보기'][1]
    # 이미지 또는 PDF 중 하나라도 로드될 때까지 대기
    Wait Until Element Is Visible    xpath=//img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]    10
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


3.2. 의약품 판촉영업 신고증 
    Click Button    xpath=(//button[text()='보기'])[last()]
    # 이미지 또는 PDF 중 하나라도 로드될 때까지 대기
    Wait Until Element Is Visible    xpath=//img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]    10
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


4. 업체 계정 관리
    Click Element    xpath=//button[span[text()='업체 관리']]
    Screenshot


4.1. 업체 계정 관리 Page
    Click Element    xpath=//div[text()=' 업체 계정 관리']
    Wait Until Element Is Visible    xpath=//h2[text()='업체 계정 관리']    5
    Screenshot

    # 마지막 삭제 버튼으로 스크롤 후 클릭 시도
    ${last_delete_btn}=    Set Variable    xpath=(//button[@title='삭제'])[last()]
    Set Suite Variable    ${last_delete_btn}
    Scroll Element Into View    ${last_delete_btn}
    Scroll Element Into View    ${last_delete_btn}
    Screenshot


4.2. 계정 삭제
    Click Element    ${last_delete_btn}
    Wait Until Element Is Visible    xpath=//h2[text()='삭제할까요?']
    Screenshot

    Click Element    xpath=//button[@title='확인']
    Sleep    0.5

    Scroll Element Into View    ${last_delete_btn}
    Scroll Element Into View    ${last_delete_btn}
    Screenshot
    

4.3. 계정 생성
    Click Element    xpath=//button[@title='계정 생성하기']
    Wait Until Element Is Visible    xpath=//h2[text()='계정 생성하기']
    Screenshot
    
    ${EMAIL}=    Generate Email
    Input Text    name=email    ${EMAIL}
    Input Text    name=name    xptmxm
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    Input Text    name=phone    ${EMPTY}
    Input Text    name=phone    010${random_number}
    Screenshot

    Click Element    xpath=//button[text()='생성하기']
    Sleep    0.5

    Scroll Element Into View    ${last_delete_btn}
    Scroll Element Into View    ${last_delete_btn}
    Screenshot

    Go Back
    Sleep    1


5. CSO 교육 수료증 등록
    Click Element    xpath=//button[span[text()='업체 관리']]
    Screenshot

    Click Element    xpath=//div[text()=' CSO 교육 수료증 등록']
    Wait Until Element Is Visible    xpath=//h2[text()='CSO 교육 수료증 등록하기']    5
    Screenshot


5.1. 수료증 첨부
    Choose File     xpath=//*[@id="fileUuid"]//input    ${testfile_PATH}
    Wait Until Element Is Visible    xpath=//button[@title='삭제']    5
    Screenshot


5.2. 수료일자
    Click Element    xpath=//div[span[text()='수료증 기재일']]
    Screenshot

    ${day}=    Evaluate    datetime.datetime.now().day    modules=datetime
    Click Element    xpath=//td[button[text()='${day}']]
    Screenshot


5.3. 발급번호
    ${datetime}=    Evaluate    datetime.datetime.now().strftime('%Y-%m%d-%H%M%S')    modules=datetime
    Press Key    xpath=//input[@placeholder='발급번호를 입력해 주세요']    ${datetime}
    Screenshot

    Click Button    xpath=//button[text()='등록하기']
    Sleep    0.5


5.4. 수료증 업데이트 확인
    Click Element    xpath=//dl[dt[text()='CSO 교육 수료증']]//button
    Wait Until Element Is Visible    xpath=//div[h2[text()='CSO 교육 수료 이력']]    5
    Execute Javascript    document.body.style.zoom='90%'
    Screenshot
    Click Element    xpath=//button[@title='수료증']
    Execute Javascript    document.body.style.zoom='100%'

    # 이미지 또는 PDF 중 하나라도 로드될 때까지 대기
    Wait Until Element Is Visible    xpath=//img[@alt='사업자등록증'] | //div[contains(@class, 'react-pdf__Document')]    10
    Screenshot
    Press Keys    ${None}    ESC
    Sleep    0.5


6. 도장 정보 관리
    Scroll Element Into View    xpath=//img[@alt='도장이미지']
    Screenshot

    Click Element    xpath=//button[span[text()='업체 관리']]
    Screenshot

    Click Element    xpath=//div[text()=' 도장 정보 관리']
    Wait Until Element Is Visible    xpath=//h2[text()='도장 정보 관리']    5
    Screenshot


6.1. 직접 만들기
    Press Key    id=stampName    테스트
    Screenshot
    
    Click Button    xpath=//button[text()='만들기']
    Wait Until Element Is Visible    xpath=//img[@alt='도장 미리보기']    5
    Screenshot

    Click Button    xpath=//button[@title='저장하기']
    Sleep    0.5
    
    Scroll Element Into View    xpath=//img[@alt='도장이미지']
    Screenshot


6.2. 파일 업로드
    Click Element    xpath=//button[span[text()='업체 관리']]
    Screenshot

    Click Element    xpath=//div[text()=' 도장 정보 관리']
    Wait Until Element Is Visible    xpath=//h2[text()='도장 정보 관리']    5
    Screenshot
    
    Click Element    xpath=//button[text()='파일 업로드']
    Wait Until Element Is Visible    xpath=//input[@accept='.png']
    Screenshot

    # 랜덤 파일 선택 및 업로드
    ${testfile_dir}=    Normalize Path    ${ROOT_DIR}/common/resources/testfile/img_number
    ${files}=    List Files In Directory    ${testfile_dir}
    ${random_file}=    Evaluate    random.choice(${files})    modules=random
    ${target_file_path}=    Join Path    ${testfile_dir}    ${random_file}
    
    # 실제 파일 선택창(input)에 파일 경로 전달
    Choose File    xpath=//input[@type='file']    ${target_file_path}
    Wait Until Element Is Visible    xpath=//button[@title='삭제']    5
    Screenshot

    Click Button    xpath=//button[@title='저장하기']
    Sleep    0.5

    Scroll Element Into View    xpath=//img[@alt='도장이미지']
    Screenshot


7. 추가 메뉴
    Click Element    xpath=//button[@aria-haspopup='menu']
    Wait Until Element Is Visible    xpath=//div[@title='서비스 이용약관']    5
    Screenshot


7.1. 서비스 이용 매뉴얼
    Click Element    xpath=//div[@title='서비스 이용 매뉴얼']
    Wait Until Element Is Visible    xpath=//h2[text()='서비스 이용 매뉴얼']    5
    Screenshot


7.2. 약관
    Click Element    xpath=//button[@aria-haspopup='menu']
    Wait Until Element Is Visible    xpath=//div[@title='서비스 이용약관']    5

    # 서비스 이용약관
    Click Element    xpath=//div[@title='서비스 이용약관']
    Wait Until Element Is Visible    xpath=//h2[text()='서비스 이용약관']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5

    # 개인정보처리방침
    Click Element    xpath=//button[@aria-haspopup='menu']
    Wait Until Element Is Visible    xpath=//div[@title='개인정보처리방침']    5
    Screenshot
    Click Element    xpath=//div[@title='개인정보처리방침']
    Wait Until Element Is Visible    xpath=//h2[text()='개인정보처리방침']    5
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5


8. 로그아웃
    Click Element    xpath=//button[@title='내 정보']
    Wait Until Element Is Visible    xpath=//h2[text()='내 정보']    5
    Screenshot

    Scroll Element Into View    xpath=//button[text()=' 로그아웃']
    Screenshot
    Click Element    xpath=//button[text()=' 로그아웃']
    Screenshot

