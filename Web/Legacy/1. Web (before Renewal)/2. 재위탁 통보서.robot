*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Resource   ../resources/keywords.robot

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


# Check and Handle Button 5
#     ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_5}
#     Run Keyword IF    ${button_exists}    Handle Button Exists 5
#     ...    ELSE    Sleep    1


# Handle Button Exists 5
#     Sleep    1
#     Click Element    ${div_xpath_5}
#     Sleep    1
#     Screenshot
#     Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    # 닫기 버튼
#     Sleep    1


# Check and Handle Button 6
#     ${button_exists}=    Run Keyword And Return Status    Element Should Be Visible    ${div_xpath_6}
#     Run Keyword IF    ${button_exists}    Handle Button Exists 6
#     ...    ELSE    Sleep    1


# Handle Button Exists 6
#     Sleep    1
#     Click Element    ${div_xpath_6}
#     Sleep    1
#     Screenshot
#     Click Element    xpath=//*[starts-with(@id, 'modal_')]/div/div/div[3]/button[2]    # 닫기 버튼
#     Sleep    1


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


*** Test Cases ***
---- 1. 재위탁 통보서 Testcase (회원)
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    Input Text    id=login-email    ${USER_2_ID}
    Input Text    id=login-password    ${USER_2_PW}
    Sleep    0.5
    Click Button    class=btn
    
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='재위탁 통보서 목록']
    Wait Until Element Is Visible    class=b-grid-cell    10
    Screenshot


-------- 1.1. 재위탁통보서 작성
    ### 작성하기 진입
    Click Element    id=b-button-2
    Wait Until Element Is Visible    class=content-view-wrap    5
    Screenshot


------------ 1.1.1. 제약사 선택
    ### 제약사 선택 버튼 
    Click Button    id=btn-team-manufacturer
    Wait Until Element Is Visible    class=btn    5
    Screenshot
    ### 제약사 검색 및 선택
    Input Text    name=searchWord    메디제약
    Sleep    1
    Click Button    xpath=//*[@id="pharmacistSelectModal"]/div/div/div[2]/div[1]/form/div/button
    Sleep    0.5
    Click Element    class=b-field-inner
    Screenshot
    ### 적용 버튼 
    Click Button    //*[@id="pharmacistSelectModal"]/div/div/div[3]/button
    Screenshot


------------ 1.1.2. 수수료율표 첨부
    # ${SetTime2}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d %H.%M.%S')
    # Click Element    xpath=//label[normalize-space(text())='직접입력']
    # Screenshot
    # Click Element    name=rate_text
    # Sleep    0.5
    # Press Keys    name=rate_text    Commission AutomationTest ${SetTime2}
    # Screenshot

    ## 기존 첨부파일의 첨부형식
    ${File_Path}=    Set Variable    C:/Dev/robotframework/assets/Test_Sameple_PDF.pdf
    
    Click Element    xpath=//label[normalize-space(text())='파일첨부']
    Sleep    0.5
    Input Text    xpath=//*[@id="rate_file"]    ${File_Path}
    Screenshot


------------ 1.1.3. 재위탁사유 작성
    ${SetTime2}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d %H.%M.%S')
    
    Click Element    name=reconsignment_reason
    Execute JavaScript    document.activeElement.value = ""
    Press Keys    name=reconsignment_reason    Re AutomationTest ${SetTime2}
    Screenshot
    

------------ 1.1.4. 작성일자 선택
    Click Element    id=creation_date
    Screenshot
    Click Element    class=active.day
    Screenshot


------------ 1.1.5. 기타 작성
    ${SetTime2}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d %H.%M.%S')
    
    Click Element    name=reconsignment_etc
    Execute JavaScript    document.activeElement.value = ""
    Press Keys    name=reconsignment_etc    ETC AutomationTest ${SetTime2}
    Screenshot


------------ 1.1.6. 재수탁자 추가
    Click Button    id=btn-team-member
    Screenshot
    Click Element    xpath=//div[text()='파CSO']
    Screenshot
    Click Element    xpath=//*[@id="teamMemberSelectModal"]/div/div/div[3]/button
    Screenshot

    ### 페이지 맨 아래로 스크롤
    Execute JavaScript    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
    Sleep    1

    # ### 페이지 맨 위로 스크롤
    # Execute JavaScript    window.scrollTo({ top: 0, behavior: 'smooth' })
    # Sleep    1


------------ 1.1.7. 일괄작성 버튼 선택
    Click Element    xpath=//*[@id="main_content"]/div[1]/div/form/div[3]/button[2]
    Wait Until Element Is Visible    class=swal2-popup    5
    Screenshot
    Click Button    class=swal2-confirm

    Wait Until Element Is Visible    class=swal2-popup    5
    Sleep    0.5
    Click Button    class=swal2-confirm
    Sleep    1
    Screenshot


------------ 1.1.8. 재위탁통보서 확인
    Sleep    1
    # 재위탁 통보서 누르기
    Click Element    xpath=//*[@id="b-grid-1-normalSubgrid"]/div[3]/div[5]
    Screenshot

    # 재위탁통보서 > 수수료율표 누르기
    Check and Handle Button 7

    # 재위탁 통보서 닫기 버튼
    Click Element    xpath=//*[@id="sub-fiduciary-button-area"]/button[2]
    Screenshot

    # 수수료율표
    Check and Handle Button 8
    Sleep    1


-------- 1.2. 재위탁 통보서 전송
    Input Text    name=sw    파CSO
    Click Button    btn-search
    Screenshot

    ### 목록 선택
    Select Checkbox    id=b-checkbox-1-input
    Screenshot

    Click Button    id=b-button-1    # 전송하기
    Wait Until Element Is Visible    class=swal2-popup    5
    Screenshot
    Click Button    class=swal2-confirm
    Screenshot


------------ 1.2.1. 재위탁 통보서 검색하기
    ### 검색
    Input Text    name=sw    파CSO
    Click Button    btn-search    ### 검색하기 버튼
    Screenshot

    Click Button    btn-init-search    ### 검색어 초기화 버튼
    Sleep    0.5

    ### 로그아웃
    Click Element    xpath=//*[@id="navbar-collapse"]/ul/li/a/div/div
    Sleep    0.5

    Click Element    xpath=//*[@id="navbar-collapse"]/ul/li/ul/li[5]/a/span
    Screenshot


---- 2. 재위탁 통보서 Testcase (제약사)
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    Input Text    id=login-email    ${USER_1_ID}
    Input Text    id=login-password    ${USER_1_PW}
    Sleep    1
    Click Button    class=btn
    
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='재위탁 통보서 목록']
    Wait Until Element Is Visible    class=b-grid-cell    10
    Screenshot


-------- 2.1. 첨부자료 확인
    # 재위탁 통보서
    Click Element    xpath=//*[@id="b-grid-1-normalSubgrid"]/div[3]/div[4]
    Screenshot
    
    # 재위탁 통보서 > 수수료율표
    Check and Handle Button 9
 
    Click Button    xpath=//*[@id="sub-fiduciary-button-area"]/button    # 닫기 버튼
    Sleep    0.5

    ### 수수료율표
    Check and Handle Button 1

    ### 위탁 계약서
    Check and Handle Button 2

    ### 재위탁자 신고증
    Check and Handle Button 3

    ### 재수탁자 신고증
    Check and Handle Button 4


-------- 2.2. 재위탁 통보서 검색하기
    ### 검색
    Input Text    name=sw    파CSO
    Click Button    btn-search    ### 검색하기 버튼
    Screenshot

    ### 검색어 초기화 버튼
    Click Button    btn-init-search
    Sleep    0.5

