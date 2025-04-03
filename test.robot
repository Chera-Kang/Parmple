*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Resource   ../support/keywords.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite


*** Test Cases ***
---- Testcase (로그인)
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

---- Testcase
    Sleep    1



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
    Wait Until Element Is Visible    class=mp-selectbox    10
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













    Sleep    10


    