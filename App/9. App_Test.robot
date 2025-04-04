*** Settings ***
Library    AppiumLibrary
Library    OperatingSystem
Library    .venv/Lib/site-packages/robot/libraries/Process.py

*** Variables ***
${REMOTE_URL}    http://127.0.0.1:4723/wd/hub
${PLATFORM_NAME}    Android
${AUTOMATION_NAME}    UiAutomator2
${NO_RESET}    true
${USER_1_ID}    chera-m1@twosun.com
${USER_1_PW}    asdf1234
${SCREENSHOT_DIR}    C:/Dev/appium_screenshot

# LG V30
${DEVICE_NAME}    LGMV300S9da9bb03    # LG V30
# Nexus 5X
# ${DEVICE_NAME}    02664b87309f3009    

# Chrome
# ${APP_PACKAGE}    com.android.chrome
# ${APP_ACTIVITY}    com.google.android.apps.chrome.Main

# Calculator
# ${APP_PACKAGE}    com.google.android.calculator
# ${APP_ACTIVITY}    com.android.calculator2.Calculator

# Wikipedia
${APP_PACKAGE}    org.wikipedia
${APP_ACTIVITY}    org.wikipedia.main.MainActivity


*** Keywords ***
# Screenshot
#     ${SetTime}=    Evaluate    __import__('datetime').datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
#     Sleep    1
#     # 1. ADB를 이용해 디바이스에서 스크린샷 촬영
#     Run    adb shell screencap -p /sdcard/Pictures/screenshot.png
#     # 2. 파일이 정상적으로 생성될 때까지 기다림
#     Wait Until Keyword Succeeds    10x    0.5s    Run    adb shell ls /sdcard/Pictures/screenshot.png
#     # 2. 스크린샷을 PC의 지정된 폴더로 복사
#     Run    adb pull /sdcard/Pictures/screenshot.png ${SCREENSHOT_DIR}/screenshot_${SetTime}.png
#     # 3. 디바이스에서 스크린샷 파일 삭제 (필요하면)
#     Run    adb shell rm /sdcard/screenshot.png
#     Sleep    1


Open Chrome
    Run Keyword And Ignore Error    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    appPackage=${APP_PACKAGE}
    ...    appActivity=${APP_ACTIVITY}
    ...    automationName=${AUTOMATION_NAME}
    ...    noReset=${NO_RESET}

    # 크롬이 이미 실행 중이라면, 이를 활성화
    Run Keyword And Ignore Error    Activate Application    ${APP_PACKAGE}


Open Wikipedia
    Run Keyword And Ignore Error    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    appPackage=${APP_PACKAGE}
    ...    appActivity=${APP_ACTIVITY}
    ...    automationName=${AUTOMATION_NAME}
    ...    noReset=${NO_RESET}


*** Test Cases ***
---- 앱 실행
    Open Wikipedia

    # 앱 실행 대기 
    Sleep    1
    Wait Until Element Is Visible    class=android.widget.FrameLayout    10


---- 탐색
    ${count} =    Set Variable    0
    ${status} =    Set Variable    False

    WHILE    not ${status} and ${count} < 15
        ${status} =    Run Keyword And Return Status    Element Should Be Visible    xpath=//*[contains(@text, "가장 많이 읽은 글 더 보기")]
        Run Keyword If    ${status}    Exit For Loop
        Swipe    700    2300    700    700
        ${count} =    Evaluate    ${count} + 1
    END

    IF    not ${status}
        Fail    "스크롤을 10번 해도 '가장 많이 읽은 글'을 찾을 수 없습니다."
    END

    # 가장 많이 읽은 글 더보기 진입
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/footerActionButton")

    # 목록의 첫번째 항목 진입
    Click Element    android=new UiSelector().className("android.view.ViewGroup").instance(2)

    Wait Until Element Is Visible    android=new UiSelector().description("보호된 페이지에서 섹션 편집").instance(0)    10
    # 저장 버튼
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/page_save")
    Sleep    1

    # 위쪽 뒤로가기 버튼
    # Wait Until Element Is Visible    class=android.widget.TextView    10
    Click Element    class=android.widget.ImageButton
    
    # 위쪽 뒤로가기 버튼
    Sleep    0.5
    Click Element    class=android.widget.ImageButton
    Sleep    1


---- 저장됨
    # GNB 저장됨
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/nav_tab_reading_lists")

    # 진입
    Click Element    android=new UiSelector().className("android.view.ViewGroup").instance(5)

    # 저장된 항목 진입
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/page_list_item_container")

    Wait Until Element Is Visible    android=new UiSelector().description("보호된 페이지에서 섹션 편집").instance(0)    10
    # 저장버튼 선택해 해제
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/page_save")

    Wait Until Element Is Visible    android=new UiSelector().className("android.widget.FrameLayout").instance(1)    10
    # 저장됨에서 제거하기
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/content").instance(2)
    Sleep    1

    # 위쪽 뒤로가기 버튼
    Click Element    class=android.widget.ImageButton

    # 위쪽 뒤로가기 버튼
    Sleep    0.5
    Click Element    class=android.widget.ImageButton
    Sleep    1


---- 검색
    # GNB 검색 버튼
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/nav_tab_search")

    # 검색 하기
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/search_card")
    Sleep    0.5
    Input Text    android=new UiSelector().resourceId("org.wikipedia:id/search_src_text")    AI

    # 검색 결과 선택
    Wait Until Element Is Visible    android=new UiSelector().className("android.view.ViewGroup").instance(2)    10
    Click Element    android=new UiSelector().className("android.view.ViewGroup").instance(2)
    Wait Until Element Is Visible    android=new UiSelector().className("android.view.View").instance(1)    10

    # 언어 
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/page_language")
    Wait Until Element Is Visible    android=new UiSelector().className("android.widget.LinearLayout").instance(1)    10

    # 영어 선택
    Click Element    xpath=//*[contains(@text, "English")]
    Wait Until Element Is Visible    android=new UiSelector().text("Artificial intelligence").instance(0)    10

    # 문서에서 찾기
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/page_find_in_article")
    Wait Until Element Is Visible    android=new UiSelector().resourceId("org.wikipedia:id/search_src_text")    10
    Input Text    android=new UiSelector().resourceId("org.wikipedia:id/search_src_text")    openai
    Sleep    0.5
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/find_in_page_next")
    Sleep    0.5
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/find_in_page_next")
    Sleep    0.5
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/find_in_page_next")
    Sleep    0.5
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/action_mode_close_button")
    Sleep    0.5
    
    Swipe    700    1300    700    1600
    Wait Until Element Is Visible    android=new UiSelector().description("위로 이동")    10
    Click Element    android=new UiSelector().description("위로 이동")
    Sleep    0.5
    Click Element    android=new UiSelector().description("위로 이동")
    Sleep    0.5
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/search_close_btn")

    # 최근 검색 기록 삭제
    Click Element    id=org.wikipedia:id/recent_searches_delete_button
    Wait Until Element Is Visible    android=new UiSelector().resourceId("android:id/message")    10
    Click Element    id=android:id/button1
    Sleep    0.5
    Click Element    android=new UiSelector().description("위로 이동")
    Sleep    0.5

    # 검색 기록 삭제
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/history_delete")
    Wait Until Element Is Visible    android=new UiSelector().resourceId("org.wikipedia:id/title_template")    10
    Click Element    android=new UiSelector().resourceId("android:id/button1")


---- 편집
    # GNB 편집 버튼
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/nav_tab_edits")
    Sleep    1


---- 더보기
    # GNB 더보기 버튼
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/nav_tab_more")
    Wait Until Element Is Visible    android=new UiSelector().resourceId("org.wikipedia:id/main_drawer_account_container")    10

    # 설정
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/main_drawer_settings_container")
    Wait Until Element Is Visible    android=new UiSelector().resourceId("org.wikipedia:id/action_bar")    10
    Click Element    android=new UiSelector().description("위로 이동")

    # 기부
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/nav_tab_more")
    Wait Until Element Is Visible    android=new UiSelector().resourceId("org.wikipedia:id/main_drawer_account_container")    10
    Click Element    android=new UiSelector().resourceId("org.wikipedia:id/main_drawer_donate_container")
    Wait Until Element Is Visible    android=new UiSelector().resourceId("Thank_you_for_your_interest")    10
    Swipe    700    2000    700    700
    Swipe    700    700    700    2000
    Click Element    android=new UiSelector().resourceId("com.android.chrome:id/close_button")

    Sleep    5

    # 앱 종료 (필요하면)
    Terminate Application    ${APP_PACKAGE}





##################################################
##################################################
### adb shell
# $ pm list packages -f | grep "chrome"


### appium 시작전 
#  appium --base-path /wd/hub



# appium app 요소 찾는 도구
# appium inspector / uiautomatorviewer


# adb shell dumpsys package com.android.chrome | grep -A 1 "MAIN"

