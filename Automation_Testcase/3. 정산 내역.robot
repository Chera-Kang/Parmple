*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Resource   ../support/keywords.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***
*** Keywords ***
*** Test Cases ***
---- 1. 정산내역관리 Testcase
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    Input Text    id=login-email    ${USER_1_ID}
    Input Text    id=login-password    ${USER_1_PW}
    Sleep    1
    Click Button    class=btn
    
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='정산 내역 관리']
    Wait Until Element Is Visible    class=b-grid-cell    10
    Screenshot


-------- 1.1. 정산내역 등록
    ${SetTime2}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d %H.%M.%S')
    ${SetTime3}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d')

    Click Button    id=b-button-2
    Screenshot

    Press Keys    id=biz_name    자동화_${SetTime3}
    Press Keys    id=biz_reg_no    1234567890
    Press Keys    id=prescription_date    123456
    Click Element    class=select2-selection__arrow
    Press Key    class=select2-search__field    오토
    Press Keys    None    ENTER
    Wait Until Element Is Visible    class=mp-selectbox    2
    Click Element    class=mp-selectbox
    Press Keys    id=manufacturer_name    자동화테스트_제약사이름
    Press Keys    id=product_name    자동화테스트_제품이름
    Press Keys    id=sales_cost    100
    Press Keys    id=sales_quantity    200
    Press Keys    id=sales_amount    300
    Press Keys    id=settlement_amount    400
    Press Keys    id=commission_rate    12
    Press Keys    id=addition_commission_rate    0.34
    Press Keys    name=note    Automation Test ! ${SetTime2}
    Screenshot

    Click Button    class=btn-primary
    Screenshot


-------- 1.2. 정산내역 수정
    # 페이지 오른쪽으로 스크롤 (그리드 가로 스크롤)
    Execute JavaScript    document.querySelector('[data-region="normal"]').scrollTo({ left: document.querySelector('[data-region="normal"]').scrollWidth, behavior: 'smooth' })
    Sleep    0.5
    
    ### 약가
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='sales_cost8']
    Execute JavaScript    document.activeElement.value = ""
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='sales_cost8']    1234

    ### 수량
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='sales_quantity9']
    Execute JavaScript    document.activeElement.value = ""
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='sales_quantity9']    2345

    ### 처방금액 
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='sales_amount10']
    Execute JavaScript    document.activeElement.value = ""
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='sales_amount10']    3456.7

    ### 처방금액 
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='settlement_amount11']
    Execute JavaScript    document.activeElement.value = ""
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='settlement_amount11']    4567.89

    ### 기본 수수료율 
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='commission_rate12']
    Execute JavaScript    document.activeElement.value = ""
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='commission_rate12']    0.05

    ### 추가 수수료율 
    Double Click Element    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='addition_commission_rate13']
    Execute JavaScript    document.activeElement.value = ""
    Press Keys    xpath=//div[contains(@class, 'b-grid-cell') and @data-column-id='addition_commission_rate13']    67.80
    Screenshot

    Click Button    id=b-button-1
    Screenshot

    Click Button    class=swal2-confirm
    Screenshot


-------- 1.2. 정산내역 삭제
    ${SetTime2}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d %H.%M.%S')
    ${SetTime3}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d')
    ${SetTime4}=    Evaluate    __import__('datetime').datetime.now().strftime('%y%m%d%H%M')
    ${SetTime5}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y%m')
    ${SetTime6}=    Evaluate    __import__('datetime').datetime.now().strftime('%H.%M.%S')

    # 정산내역공유에서 미전송 Case 대응용 
    Click Button    id=b-button-2
    Sleep    1

    Press Keys    id=biz_name    전송테스트_${SetTime2}
    Press Keys    id=biz_reg_no    ${SetTime4}
    Press Keys    id=prescription_date    ${SetTime5}
    Click Element    class=select2-selection__arrow
    Press Key    class=select2-search__field    오토
    Press Keys    None    ENTER
    Wait Until Element Is Visible    class=mp-selectbox    2
    Click Element    class=mp-selectbox
    Press Keys    id=manufacturer_name    자동화테스트_${SetTime3}
    Press Keys    id=product_name    자동화테스트_${SetTime3}
    Press Keys    id=sales_cost    100
    Press Keys    id=sales_quantity    200
    Press Keys    id=sales_amount    300
    Press Keys    id=settlement_amount    400
    Press Keys    id=commission_rate    12
    Press Keys    id=addition_commission_rate    0.34
    Press Keys    name=note    Automation Test ! ${SetTime2}

    Sleep    0.5
    Click Button    class=btn-primary
    Sleep    1

    # 받은 정산 내역 Case 확인용  
    Click Button    id=b-button-2
    Sleep    1

    Press Keys    id=biz_name    전송테스트_${SetTime2}
    Press Keys    id=biz_reg_no    2744708777
    Press Keys    id=prescription_date    ${SetTime5}
    Click Element    class=select2-selection__arrow
    Press Key    class=select2-search__field    오토
    Press Keys    None    ENTER
    Wait Until Element Is Visible    class=mp-selectbox    2
    Click Element    class=mp-selectbox
    Press Keys    id=manufacturer_name    자동화테스트_${SetTime6}
    Press Keys    id=product_name    자동화테스트_${SetTime2}
    Press Keys    id=sales_cost    100
    Press Keys    id=sales_quantity    200
    Press Keys    id=sales_amount    300
    Press Keys    id=settlement_amount    400
    Press Keys    id=commission_rate    12
    Press Keys    id=addition_commission_rate    0.34
    Press Keys    name=note    Automation Test ! ${SetTime2}

    Sleep    0.5
    Click Button    class=btn-primary
    Sleep    1

    # 삭제용 정산내역  
    Click Button    id=b-button-2
    Sleep    0.5
    Press Keys    id=biz_name    Delete_Test
    Press Keys    id=biz_reg_no    1234567890
    Screenshot

    Click Button    class=btn-primary
    Screenshot

    # 페이지 오른쪽으로 스크롤 (그리드 가로 스크롤)
    Execute JavaScript    document.querySelector('[data-region="normal"]').scrollTo({ left: document.querySelector('[data-region="normal"]').scrollWidth, behavior: 'smooth' })
    Sleep    0.5

    Click Element    id=b-button-9
    Screenshot

    Click Button    class=swal2-confirm
    Screenshot

    # 페이지 왼쪽으로 스크롤 (그리드 가로 스크롤)
    Execute JavaScript    document.querySelector('[data-region="normal"]').scrollTo({ left: 0, behavior: 'smooth' })
    Sleep    0.5


-------- 1.3. 정산내역 검색 & 정산월 변경
    Click Element    id=st
    Screenshot
    Select From List By Label    id=st    제품명
    Sleep    1
    Input Text    name=sw    자동화
    Sleep    0.5
    Click Button    btn-search
    Screenshot

    Click Button    id=btn-init-search
    Click Button    btn-search
    Sleep    0.5

    Click Element    id=apply_year_month
    Screenshot

    Click Element    xpath=//span[@class='month' and text()='2월']
    Screenshot


---- 2. 정산내역공유 Testcase
    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='정산 내역 공유']
    Wait Until Element Is Visible    class=b-grid-cell    10
    Screenshot


-------- 2.1. 정산내역 상세보기
    Click Element    xpath=//a[@data-name='체라메디' and text()='보기']
    Wait Until Element Is Visible    class=modal-body    10
    Screenshot

    Click Button    class=btn-close


-------- 2.2. 정산내역 공유하기
    # 목록 전체 선택
    Click Button    id=b-checkbox-1-input
    Sleep    0.5

    # 공유하기 버튼
    Click Button    id=b-button-1
    Wait Until Element Is Visible    class=swal2-container
    Screenshot

    # 공유하기 동작 
    Click Button    class=swal2-confirm
    Screenshot


---- 3. 받은 정산 내역 Testcase
    # 계정 변경  
    Click Element    xpath=//*[@id="navbar-collapse"]/ul/li/a/div/div
    Sleep    0.5

    Click Element    xpath=//*[@id="navbar-collapse"]/ul/li/ul/li[5]/a/span
    Screenshot

    Input Text    id=login-email    ${USER_2_ID}
    Input Text    id=login-password    ${USER_2_PW}
    Sleep    0.5
    Click Button    class=btn
    Sleep    1

    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='받은 정산 내역']
    Wait Until Element Is Visible    class=b-grid-cell    10
    Screenshot

    Click Element    id=st
    Sleep    0.5
    Select From List By Label    id=st    제품명   
    Sleep    1

    Input Text    name=sw    자동화
    Sleep    0.5
    Click Button    btn-search
    Screenshot
