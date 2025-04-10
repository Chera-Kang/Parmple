*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Resource   ../support/keywords.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***
${div_xpath_1}    id=b-button-9
${div_xpath_2}    id=b-button-10
${div_xpath_3}    //*[@id="b-grid-1-normalSubgrid"]/div[3]/div[10]/div
${div_xpath_4}    //*[@id="b-grid-1-normalSubgrid"]/div[3]/div[14]/div
${div_xpath_5}    id=b-button-1
${div_xpath_6}    id=b-button-2
${div_xpath_7}    //*[@id="sub-fiduciary-commis-view"]/a
${div_xpath_8}    //*[@id="b-grid-1-normalSubgrid"]/div[3]/div[6]/div
${div_xpath_9}    //*[@id="sub-fiduciary-commis-view"]/a
${XPATH_WITH_TEXT}    xpath=//div[@class='item-title' and @title='체라메디']
${XPATH_WITH_TEXT_2}    xpath=//div[@class='item-title' and @title='바CSO']


*** Keywords ***
Check and Handle Button 1
    ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_1}
    Run Keyword IF    ${button_exists}    Handle Button Exists 1
    ...    ELSE    Sleep    1


Handle Button Exists 1
    Sleep    1
    Click Element    ${div_xpath_1}
    Sleep    1
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
    Sleep    1


Check and Handle Button 2
    ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_2}
    Run Keyword IF    ${button_exists}    Handle Button Exists 2
    ...    ELSE    Sleep    1


Handle Button Exists 2
    Sleep    1
    Click Element    ${div_xpath_2}
    Sleep    1
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
    Sleep    1


Check and Handle Button 3
    ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_3}
    Run Keyword IF    ${button_exists}    Handle Button Exists 3
    ...    ELSE    Sleep    1


Handle Button Exists 3
    Sleep    1
    Click Element    ${div_xpath_3}
    Sleep    1
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    # 닫기 버튼
    Sleep    1


Check and Handle Button 4
    ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_4}
    Run Keyword IF    ${button_exists}    Handle Button Exists 4
    ...    ELSE    Sleep    1


Handle Button Exists 4
    Sleep    1
    Click Element    ${div_xpath_4}
    Sleep    1
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    # 닫기 버튼
    Sleep    1


Check and Handle Button 5
    ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_5}
    Run Keyword IF    ${button_exists}    Handle Button Exists 5
    ...    ELSE    Sleep    1


Handle Button Exists 5
    Sleep    1
    Click Element    ${div_xpath_5}
    Sleep    1
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    # 닫기 버튼
    Sleep    1


Check and Handle Button 6
    ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_6}
    Run Keyword IF    ${button_exists}    Handle Button Exists 6
    ...    ELSE    Sleep    1


Handle Button Exists 6
    Sleep    1
    Click Element    ${div_xpath_6}
    Sleep    1
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    # 닫기 버튼
    Sleep    1


Check and Handle Button 7
    ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_7}
    Run Keyword IF    ${button_exists}    Handle Button Exists 7
    ...    ELSE    Sleep    1


Handle Button Exists 7
    Sleep    1
    Click Element    ${div_xpath_7}
    Sleep    1
    Screenshot
    Click Element    xpath=//div[contains(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
    Sleep    1


Check and Handle Button 8
    ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_8}
    Run Keyword IF    ${button_exists}    Handle Button Exists 8
    ...    ELSE    Sleep    1


Handle Button Exists 8
    Sleep    1
    Click Element    ${div_xpath_8}
    Screenshot
    Click Element    xpath=//div[contains(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
    Sleep    1


Check and Handle Button 9
    ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_9}
    Run Keyword IF    ${button_exists}    Handle Button Exists 9
    ...    ELSE    Sleep    1


Handle Button Exists 9
    Sleep    1
    Click Element    ${div_xpath_9}
    Sleep    1
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
    Sleep    1


Sub Selectection 1
    Wait Until Page Contains Element    ${XPATH_WITH_TEXT}    timeout=10s
    Click Element    ${XPATH_WITH_TEXT}


Sub Selectection 2
    Wait Until Page Contains Element    ${XPATH_WITH_TEXT_2}    timeout=10s
    Click Element    ${XPATH_WITH_TEXT_2}



*** Test Cases ***
---- Testcase (로그인)
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    Input Text    id=login-email    ${USER_2_ID}
    Input Text    id=login-password    ${USER_2_PW}
    Sleep    0.5
    Click Button    class=btn
    
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='계약 관리']
    Wait Until Element Is Visible    class=b-grid-row    5
    Sleep    1

---- Testcase

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


    Log To Console    -Succese-
    Sleep    5


    