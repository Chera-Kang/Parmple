*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    String
Library    RequestsLibrary
Library    BuiltIn
Resource   ../support/keywords.robot
Library    Process
Library    DateTime
Resource    ../.secrets.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***
*** Keywords ***
*** Test Cases ***
---- Testcase
    Wait Until Element Is Visible    xpath=//img[contains(@src, 'logo_200.25f0e37e.png')]    5

    Input Text    name=email    ${id_1}
    Press Key    name=password    ${password}
    Sleep    1
    Click Button    xpath=//button[text()='로그인']
    Sleep    3

    ## 제약사 제품 공지 page 진입 
    Click Element    xpath=//a[span[text()='제약사 제품 공지']]
    Wait Until Element Is Visible    xpath=//h2[text()='제약사 제품 공지']    5
    Screenshot
    
    # 제품 상세 진입 
    Click Element    xpath=(//a[@class="underline hover:text-primary"])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='제품 상세']    5
    Screenshot

    # 화면 스크롤
    Scroll Element Into View    xpath=//*[normalize-space(.)='ATC코드']
    Screenshot
    Scroll Element Into View    xpath=//h2[normalize-space(.)='제품 상세']
    Sleep    0.5

    # 동일성분의약품 
    Click Element    xpath=//button[text()='동일성분의약품']
    Screenshot

    # 목록으로 이동 
    Go Back
    Sleep    1
    
    # 제약사별 
    Click Element    xpath=//button[text()='제약사별']
    Wait Until Element Is Visible    xpath=//span[text()='건일바이오팜']    5
    Screenshot

    # 펼치기 
    Click Element    xpath=//*[starts-with(@id, 'cell-manufacturerName-')]/span/span[2]/span
    Wait Until Element Is Visible    xpath=//span[text()='보험코드']    5
    Screenshot

    # 구분별 
    Click Element    xpath=//button[text()='구분별']
    Wait Until Element Is Visible    xpath=//span[text()='품절']    5
    Screenshot

    # 펼치기 
    Click Element    xpath=//*[starts-with(@id, 'cell-noticeClass-')]/span/span[2]/span
    Wait Until Element Is Visible    xpath=//span[text()='보험코드']    5
    Screenshot
    
    # 제품별 
    Click Element    xpath=//button[text()='제품별']
    Screenshot

    # 검색 
    Input Text    xpath=//input[@placeholder='제품명 검색']    캡슐
    Screenshot
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


---- Testcase2
    # 신규 개원 정보 
    Click Element    xpath=//a[span[text()='신규 개원 정보']]
    Wait Until Element Is Visible    xpath=//h2[text()='신규 개원 정보']    5
    Screenshot

    # 검색 
    # 구분 
    Click Element    xpath=//button[span[text()='구분 (전체)']]
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'radix-') and normalize-space(text())='의원']
    Screenshot

    # 진료과목 
    Click Element    xpath=//button[span[text()='진료과목 (전체)']]
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'radix-') and normalize-space(text())='내과']
    Screenshot

    # 지역
    Click Element    xpath=//button[span[text()='지역 (전체)']]
    Screenshot
    Click Element    xpath=//*[starts-with(@id, 'radix-') and normalize-space(text())='세종']
    Screenshot

    # 검색 버튼
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


---- Testcase3
    # CSO 제품 정보 
    Click Element    xpath=//a[span[text()='CSO 제품 정보']]
    Wait Until Element Is Visible    xpath=//h2[text()='CSO 제품 정보']    5
    Screenshot

    # 제품 상세 
    Click Element    xpath=(//a[@class="underline hover:text-primary"])[1]
    Wait Until Element Is Visible    xpath=//h2[text()='제품 상세']    5
    Screenshot

    # 목록으로 이동 
    Go Back
    Sleep    1

    # 제약사별 
    Click Element    xpath=//button[text()='제약사별']
    Wait Until Element Is Visible    xpath=//span[text()='건일바이오팜']    5
    Screenshot

    # 펼침 
    Click Element    xpath=//*[starts-with(@id, 'cell-manufacturerName-')]/span/span[2]/span
    Wait Until Element Is Visible    xpath=//span[text()='보험코드']    5
    Screenshot

    # 분류별 
    Click Element    xpath=//button[text()='분류별']
    Wait Until Element Is Visible    xpath=//span[text()='최면진정제']    5
    Screenshot

    # 펼침 
    Click Element    xpath=//*[starts-with(@id, 'cell-drugClass-')]/span/span[2]/span
    Wait Until Element Is Visible    xpath=//span[text()='보험코드']    5
    Screenshot

    # 제품별 
    Click Element    xpath=//button[text()='제품별']
    Screenshot

    # 검색
    Input Text    xpath=//input[@placeholder='제품명/성분명 검색']    캡슐
    Screenshot

    # 검색 버튼 
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


