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
6.0. 자료실
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='회원가입']    5
    Login_CSO
    Sleep    1


6.1. 제약사 제품 공지 
    Scroll Element Into View    xpath=//a[span[text()='영업 자료실']]
    Click Element    xpath=//a[span[text()='제약사 제품 공지']]
    Wait Until Element Is Visible    xpath=//h2[text()='제약사 제품 공지']    5
    Screenshot

    # 제품 상세 진입 
    Click Element    xpath=//a[@class='underline hover:text-blue-500']
    Wait Until Element Is Visible    xpath=//h2[text()='제품 상세 보기']    5
    Screenshot
    Scroll Element Into View    xpath=//div[text()='ATC코드']
    Screenshot

    # 동일 성분 의약품
    Scroll Element Into View    xpath=//button[text()='동일 성분 의약품']
    Click Button    xpath=//button[text()='동일 성분 의약품']
    Screenshot

    # 목록으로 이동 
    Go Back
    Wait Until Element Is Visible    xpath=//h2[text()='제약사 제품 공지']    5

    # 제약사별 목록
    Click Button    xpath=//button[text()='제약사']
    Wait Until Element Is Visible    xpath=//span[text()='건일바이오팜']    5
    Screenshot
    
    # 펼침
    Click Element    xpath=//i[@class='ri-arrow-drop-down-fill']
    Screenshot

    # 구분별 목록
    Click Button    xpath=//button[text()='구분']
    Wait Until Element Is Visible    xpath=//span[text()='품절']    5
    Screenshot

    # 펼침
    Click Element    xpath=//i[@class='ri-arrow-drop-down-fill']
    Screenshot
    
    # 제품별 목록
    Click Button    xpath=//button[text()='제품']
    Wait Until Element Is Visible    xpath=//a[@class='underline hover:text-blue-500']    5
    Screenshot

    # 검색 
    Input Text    xpath=//input[@placeholder='제품명으로 검색해 주세요']    캡슐
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


6.2. 신규 개원 정보
    Scroll Element Into View    xpath=//a[span[text()='영업 자료실']]
    Click Element    xpath=//a[span[text()='신규 개원 정보']]
    Sleep    1
    Screenshot
    
    # 검색 
    Click Element    xpath=//button[span[text()='구분 (전체)']]
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'radix-') and normalize-space(text())='의원']
    Screenshot
    Click Element    xpath=//button[span[text()='진료과목 (전체)']]
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'radix-') and normalize-space(text())='내과']
    Screenshot
    Click Element    xpath=//button[span[text()='지역 (전체)']]
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'radix-') and normalize-space(text())='세종']
    Screenshot
    Click Element    xpath=//button[span[text()='검색']]
    Wait Until Element Is Visible    xpath=//div[span[text()='의원']]    5
    Screenshot


6.3. CSO 제품 정보
    Scroll Element Into View    xpath=//a[span[text()='영업 자료실']]
    Click Element    xpath=//a[span[text()='CSO 제품 정보']]
    Sleep    1
    Screenshot
    
    # 제품 상세 진입 
    Click Element    xpath=//a[@class='underline hover:text-blue-500']
    Wait Until Element Is Visible    xpath=//h2[text()='제품 상세 보기']    5
    Screenshot

    Scroll Element Into View    xpath=//div[text()='ATC코드']
    Screenshot

    # 동일 성분 의약품
    Scroll Element Into View    xpath=//button[text()='동일 성분 의약품']
    Click Button    xpath=//button[text()='동일 성분 의약품']
    Screenshot

    # 목록으로 이동 
    Go Back
    Wait Until Element Is Visible    xpath=//h2[text()='CSO 제품 정보']    5

    # 제약사별
    Click Button    xpath=//button[text()='제약사']
    Wait Until Element Is Visible    xpath=//span[text()='건일바이오팜']    5
    Screenshot
    
    # 펼침
    Click Element    xpath=//i[@class='ri-arrow-drop-down-fill']
    Screenshot

    # 구분별
    Click Button    xpath=//button[text()='구분']
    Wait Until Element Is Visible    xpath=//span[text()='최면진정제']    5
    Screenshot

    # 펼침
    Click Element    xpath=//i[@class='ri-arrow-drop-down-fill']
    Screenshot
    
    # 제품별
    Click Button    xpath=//button[text()='제품']
    Wait Until Element Is Visible    xpath=//a[@class='underline hover:text-blue-500']    5

    # 검색 
    Input Text    xpath=//input[@placeholder='제품/성분명으로 검색해 주세요']    캡슐
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot

