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
Logout
    # 내 정보 선택
    Click Element    xpath=//button[@data-sidebar='menu-button']
    Wait Until Element Is Visible    xpath=//a[normalize-space(.)='내 정보']    5
    Sleep    1
    Click Element    xpath=//a[normalize-space(.)='내 정보']
    Wait Until Element Is Visible    xpath=//h2[normalize-space(.)='내 정보']
    Sleep    1

    # 화면 스크롤
    Scroll Element Into View    xpath=//*[normalize-space(.)='로그아웃']
    Sleep    0.5

    # 로그아웃
    Click Element    xpath=//button[@title='로그아웃']
    Wait Until Element Is Visible    name=email    5
    Sleep    0.5

Login CSO
    Input Text    name=email    ${id_1}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Sleep    3

Login pharm
    Input Text    name=email    ${id_2}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Sleep    3

Login samik
    Input Text    name=email    ${id_3}
    Press Key    name=password    ${password}
    Screenshot
    Click Button    xpath=//button[text()='로그인']
    Sleep    3


*** Test Cases ***
---- 필터링 조회 
    Wait Until Element Is Visible    xpath=//img[contains(@src, 'logo_200.25f0e37e.png')]    5

    Input Text    name=email    ${id_1}
    Press Key    name=password    ${password}
    Sleep    1
    Click Button    xpath=//button[text()='로그인']
    Sleep    3

    # 필터링 조회 
    Click Element    xpath=//a[span[text()='필터링 조회']]
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 조회']
    Sleep    1
    Screenshot

    # 병의원 검색 
    Press Key    xpath=//input[@placeholder='병의원명 검색 후 리스트 선택']    오토
    Screenshot
    Press Keys    xpath=//input[@placeholder='병의원명 검색 후 리스트 선택']    ENTER
    Screenshot
    Click Element    xpath=//div[text()='기아(주)오토랜드 광주제1의원']
    Screenshot
    Press Key    xpath=//input[@placeholder='사업자등록번호 (-없이 입력)']    1234567890
    Screenshot
    Click Element    xpath=//button[span[text()='조회하기']]
    Screenshot


---- 필터링 조회 이력 
    # 계정 변경
    Logout
    Sleep    1

    # 삼익제약 계약 로그인
    Login samik
    Sleep    1

    # 필터링 조회 이력 
    Click Element    xpath=//a[span[text()='필터링 조회 이력']]
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 조회 이력']
    Screenshot

    # 병의원 검색 
    Click Element    xpath=//button[span[text()='병의원명']]
    Screenshot
    Press Keys    NONE    ESC
    Sleep    0.5
    Press Key    xpath=//input[@placeholder='검색어를 입력해주세요']    오토
    Screenshot
    Click Element    xpath=//button[span[text()='검색']]
    Screenshot


---- 필터링 요청 
    # 로그아웃 
    Logout
    Sleep    1

    Login CSO
    Sleep    1

    # 필터링 요청 
    Click Element    xpath=//a[span[text()='필터링 요청']]
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 요청']
    Screenshot


---- 필터링 회신 관리 
    # 계정 변경 
    Logout
    Sleep    1

    # 제약사 계정 로그인
    Login pharm
    Sleep    1

    # 필터링 회신 관리
    Click Element    xpath=//a[span[text()='필터링 회신 관리']]
    Wait Until Element Is Visible    xpath=//h2[text()='필터링 회신 관리']
    Screenshot


---- 거래처 내역
    # 계정 변경 
    Logout
    Sleep    1

    # CSO 계정 로그인
    Login CSO
    Sleep    1

    # 거래처 내역
    Click Element    xpath=//a[span[text()='거래처 내역']]
    Wait Until Element Is Visible    xpath=//h2[text()='거래처 내역']
    Screenshot


---- 영업 거래처 관리
    # 계정 변경 
    Logout
    Sleep    1

    # 제약사 계정 로그인
    Login pharm
    Sleep    1

    # 영업 거래처 관리
    Click Element    xpath=//a[span[text()='영업 거래처 관리']]
    Wait Until Element Is Visible    xpath=//h2[text()='영업 거래처 관리']
    Screenshot

