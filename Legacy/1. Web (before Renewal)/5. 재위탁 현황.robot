*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Resource   ../keywords.robot

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
# Check and Handle Button 1
#     ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_1}
#     Run Keyword IF    ${button_exists}    Handle Button Exists 1
#     ...    ELSE    Sleep    1


# Handle Button Exists 1
#     Sleep    1
#     Click Element    ${div_xpath_1}
#     Sleep    1
#     Screenshot
#     Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
#     Sleep    1


# Check and Handle Button 2
#     ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_2}
#     Run Keyword IF    ${button_exists}    Handle Button Exists 2
#     ...    ELSE    Sleep    1


# Handle Button Exists 2
#     Sleep    1
#     Click Element    ${div_xpath_2}
#     Sleep    1
#     Screenshot
#     Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
#     Sleep    1


# Check and Handle Button 3
#     ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_3}
#     Run Keyword IF    ${button_exists}    Handle Button Exists 3
#     ...    ELSE    Sleep    1


# Handle Button Exists 3
#     Sleep    1
#     Click Element    ${div_xpath_3}
#     Sleep    1
#     Screenshot
#     Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    # 닫기 버튼
#     Sleep    1


# Check and Handle Button 4
#     ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_4}
#     Run Keyword IF    ${button_exists}    Handle Button Exists 4
#     ...    ELSE    Sleep    1


# Handle Button Exists 4
#     Sleep    1
#     Click Element    ${div_xpath_4}
#     Sleep    1
#     Screenshot
#     Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    # 닫기 버튼
#     Sleep    1


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


# Check and Handle Button 7
#     ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_7}
#     Run Keyword IF    ${button_exists}    Handle Button Exists 7
#     ...    ELSE    Sleep    1


# Handle Button Exists 7
#     Sleep    1
#     Click Element    ${div_xpath_7}
#     Sleep    1
#     Screenshot
#     Click Element    xpath=//div[contains(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
#     Sleep    1


# Check and Handle Button 8
#     ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_8}
#     Run Keyword IF    ${button_exists}    Handle Button Exists 8
#     ...    ELSE    Sleep    1


# Handle Button Exists 8
#     Sleep    1
#     Click Element    ${div_xpath_8}
#     Screenshot
#     Click Element    xpath=//div[contains(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
#     Sleep    1


# Check and Handle Button 9
#     ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_9}
#     Run Keyword IF    ${button_exists}    Handle Button Exists 9
#     ...    ELSE    Sleep    1


# Handle Button Exists 9
#     Sleep    1
#     Click Element    ${div_xpath_9}
#     Sleep    1
#     Screenshot
#     Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
#     Sleep    1


Sub Selectection 1
    Wait Until Page Contains Element    ${XPATH_WITH_TEXT}    timeout=10s
    Click Element    ${XPATH_WITH_TEXT}


Sub Selectection 2
    Wait Until Page Contains Element    ${XPATH_WITH_TEXT_2}    timeout=10s
    Click Element    ${XPATH_WITH_TEXT_2}


*** Test Cases ***
---- 1. 재위탁 현황 (제약사)
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    Input Text    id=login-email    ${USER_1_ID}
    Input Text    id=login-password    ${USER_1_PW}
    Sleep    0.5
    Click Button    class=btn
    
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10


-------- 1.1. 재위탁 구조도
    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='재위탁 구조도']
    Wait Until Element Is Visible    class=grid-contents-list-fit    10
    Screenshot


------------ 1.1.1. 하위 업체 선택
    Sub Selectection 1
    Screenshot

    
------------ 1.1.2. 구조도 view type 변경
    ### 좌우 선택
    Click Button    id=b-button-1
    Screenshot
    Click Button    id=b-button-1
    Screenshot

    ### 상하 선택 
    Click Button    id=b-button-2
    Screenshot
    Click Button    id=b-button-2
    Screenshot
    Click Button    id=b-button-2
    Sleep    1


------------ 1.1.3. 첨부자료 확인
    ### 하위 업체 선택 2
    Sub Selectection 2
    Screenshot

    ### 사업자등록증 
    Click Button    id=b-button-4
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
    Sleep    1

    ### 의약품 판촉영업 신고증 
    Click Button    id=b-button-5
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    #닫기 버튼
    Sleep    1


-------- 1.2. 재위탁 목록
    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='재위탁 목록']
    Wait Until Element Is Visible    class=b-grid-cell    10
    Screenshot

    ### 검색
    Input Text    name=sw    체라메디
    ### 검색하기 버튼
    Click Button    btn-search
    Screenshot
    ### 검색어 초기화 버튼
    Click Button    btn-init-search
    Sleep    0.5


------------ 1.2.1. 하위 업체 목록 확인
    ### 하위 업체 펼치기
    Click Element    class=b-tree-expander
    Screenshot
    Click Element    class=b-tree-expander
    Screenshot


------------ 1.2.2. 첨부파일 확인
    ### 사업자 등록증
    Check and Handle Button 5    

    ### 판촉영업신고증
    Check and Handle Button 6

    Sleep    1
