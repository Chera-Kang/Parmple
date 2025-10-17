*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Resource   ../keywords.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite
*** Variables ***
${GENERATOR_Number}    dummy

*** Keywords ***
*** Test Cases ***
---- 0. 사전 준비 (사업자등록번호)
    Generaotr & Validator


---- 1. 업체 관리 Testcase
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10
    Screenshot

    # 아이디/비밀번호 입력
    Input Text    id=login-email    ${USER_2_ID}
    Input Text    id=login-password    ${USER_2_PW}
    Screenshot

    # 로그인 버튼
    Click Button    class=btn
    
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10
    Screenshot


-------- 1.1. 업체 등록하기
    ${SetTime2}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d %H.%M.%S')
    ${SetTime3}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d')
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}

    ### 등록하기 버튼
    Click Button    id=b-button-1
    Screenshot

    ### 사업자등록번호
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='business-biz_reg_no16']
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='business-biz_reg_no16']    ${GENERATOR_Number}
    Sleep    0.5

    ### 상호/법인명
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='business-biz_name17']
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='business-biz_name17']    Auto_${SetTime3}
    Sleep    0.5

    ### 대표자명
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='business-representative_name18']
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='business-representative_name18']    AutomationTest
    Sleep    0.5

    ### 담당자명
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='name19']
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='name19']    AutomationTest
    Sleep    0.5

    ### 담당자 휴대폰번호
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='phone20']
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='phone20']    ${phone_number}
    Sleep    0.5

    ### 담당자 이메일
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='email21']
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='email21']    Auto@test.com
    Sleep    0.5

    ### 비고
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='note22']
    Click Element    id=b-fieldtrigger-1
    Input Text    xpath=//textarea[@id='b-textareapickerfield-1-input']    Automation Test ! ${SetTime2}
    Click Element    id=b-fieldtrigger-1
    Screenshot

    ### 등록하기 버튼
    Click Button    id=btn-invite-members
    Wait Until Element Is Visible    class=swal2-popup    5
    Screenshot
    Click Button    class=swal2-confirm
    Screenshot


-------- 1.2. 업체 수정하기
    ${random_number}=    Evaluate    str(__import__('random').randint(10000000, 99999999))
    ${phone_number}=    Set Variable    010${random_number}
    
    Sleep    0.5

    ### 담당자명
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='name10']
    Sleep    0.5
    # Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='name10']    CTRL+A    # 전체 텍스트 선택
    # Sleep    1
    Execute JavaScript    document.activeElement.value = ""
    # Sleep    1
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='name10']    FIXED_Auto
    Sleep    0.5

    ### 담당자 휴대폰번호
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='phone11']
    Sleep    0.5
    Execute JavaScript    document.activeElement.value = ""
    # Sleep    1
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='phone11']    ${phone_number}
    Sleep    0.5

    ### 담당자 이메일
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='email12']
    Sleep    0.5
    Execute JavaScript    document.activeElement.value = ""
    # Sleep    1
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='email12']    FIXED@Auto.com
    Screenshot
    
    ### 저장하기
    Click Button    id=b-button-2
    Wait Until Element Is Visible    class=swal2-popup    5
    Screenshot
    Click Button    class=swal2-confirm
    Screenshot


-------- 1.3. 업체 검색
    ${SetTime4}=    Evaluate    __import__('datetime').datetime.now().strftime('%m.%d')
    
    Input Text    name=sw    ${SetTime4}
    Click Button    btn-search
    Screenshot
    Click Button    btn-init-search
    Sleep    0.5


---- 2. 계약 관리 Testcase
    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='계약 관리']
    Wait Until Element Is Visible    class=b-grid-cell    10
    Screenshot


-------- 2.1. 계약서 등록하기
    Click Element    class=modal-add
    Wait Until Element Is Visible    class=fa-solid    5
    Screenshot

    ### 날짜 선택
    Click Element    name=contractStartDate
    Wait Until Element Is Visible    class=datepicker    5
    Screenshot
    Click Element    class=today.active.day
    Screenshot

    ### 계약서 파일등록
    ${File_Path}=    Set Variable    C:/Dev/robotframework/assets/Test_Sameple_PDF.pdf
    Sleep    1
    Input Text    xpath=//*[@id="contractFile"]    ${File_Path}
    Screenshot
    
    ### 계약서 등록하기 버튼
    Click Button    xpath=//*[@id="contract-add"]/div/div[3]/button[2]
    Wait Until Element Is Visible    class=swal2-popup    5
    Screenshot
    Click Button    class=swal2-confirm
    Screenshot

-------- 2.2. 계약서 이력보기
    Click Element    class=modal-add
    Wait Until Element Is Visible    class=fa-solid    5
    Sleep    0.5

    ### 날짜 선택
    Click Element    name=contractStartDate
    Wait Until Element Is Visible    class=datepicker    5
    Sleep    0.5
    Click Element    class=today.active.day
    Sleep    0.5

    ### 계약서 파일등록
    ${File_Path}=    Set Variable    C:/Dev/robotframework/assets/Test_Sameple_PDF.pdf
    Sleep    1
    Input Text    xpath=//*[@id="contractFile"]    ${File_Path}
    Sleep    0.5
    
    ### 계약서 등록하기 버튼
    Click Button    xpath=//*[@id="contract-add"]/div/div[3]/button[2]
    Wait Until Element Is Visible    class=swal2-popup    5
    Sleep    0.5
    Click Button    class=swal2-confirm
    Sleep    0.5

    Click Element    class=modalHistory
    Sleep    1
    Screenshot
    Click Element    xpath=//*[@id="modalContractHistory"]/div/div/div/div[3]/button
    Sleep    0.5


-------- 2.3. 계약서 검색하기
    ${SetTime4}=    Evaluate    __import__('datetime').datetime.now().strftime('%m.%d')
    
    Input Text    name=sw    ${SetTime4}
    Click Button    btn-search
    Screenshot
    Click Button    btn-init-search
    Sleep    0.5
