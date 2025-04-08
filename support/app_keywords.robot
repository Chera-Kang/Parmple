*** Settings ***
Library    AppiumLibrary
Library    OperatingSystem
Library    Process
Library    String
Library    DateTime

*** Variables ***
${REMOTE_URL}    http://127.0.0.1:4723/wd/hub
${PLATFORM_NAME}    Android
${AUTOMATION_NAME}    UiAutomator2
${NO_RESET}    true

# 스크린샷 저장 후 이동시키기
${RUN_TIMESTAMP}    dummy    #밑의 ${RESULT_DIR} 에 ${RUN_TIMESTAMP} 빨간줄 그어지는거 해소용
${RESULT_DIR}    C:/Dev/TestResult/${RUN_TIMESTAMP}_App
${SCREENSHOT_DIR}    ${RESULT_DIR}


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
Take App Screenshot
    ${raw_time}=      Get Time
    ${timestamp}=     Replace String    ${raw_time}    :    -
    ${timestamp}=     Replace String    ${timestamp}    ${SPACE}    _
    ${filename}=      Set Variable    ${timestamp}.png
    ${device_path}=   Set Variable    /sdcard/ETC/screenshots/${filename}

    ${result}=        Run Process    adb    shell    screencap    -p    ${device_path}    shell=True    stdout=TRUE    stderr=TRUE

Copy All Screenshots To Dated Folder2
    Log To Console    복사 시작: ${SCREENSHOT_DIR}
    Run Process    adb    pull    /sdcard/ETC/screenshots    ${SCREENSHOT_DIR}
    Log To Console    복사 완료: ${SCREENSHOT_DIR}


# Open Chrome
#     Run Keyword And Ignore Error    Open Application    ${REMOTE_URL}
#     ...    platformName=${PLATFORM_NAME}
#     ...    deviceName=${DEVICE_NAME}
#     ...    appPackage=${APP_PACKAGE}
#     ...    appActivity=${APP_ACTIVITY}
#     ...    automationName=${AUTOMATION_NAME}
#     ...    noReset=${NO_RESET}

#     # 크롬이 이미 실행 중이라면, 이를 활성화
#     Run Keyword And Ignore Error    Activate Application    ${APP_PACKAGE}





##################################################
################## 참고사항 #######################
##################################################
### adb shell
# $ pm list packages -f | grep "chrome"


### appium 시작전 
#  appium --base-path /wd/hub



# appium app 요소 찾는 도구
# appium inspector / uiautomatorviewer


# adb shell dumpsys package com.android.chrome | grep -A 1 "MAIN"