*** Settings ***
Library    AppiumLibrary
Library    OperatingSystem
Library    Process
Library    string
Library    DateTime

*** Variables ***
${REMOTE_URL}    http://127.0.0.1:4723/wd/hub
${PLATFORM_NAME}    Android
${AUTOMATION_NAME}    UiAutomator2
${NO_RESET}    true

${DEVICE_PATH}      /sdcard/ETC/image
${TIMESTAMP}        Get Current Date    result_format=%y-%m-%d_%H-%M-%S
${FILENAME}         screenshot-${TIMESTAMP}.png


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
App Screenshot
    ${device_filepath}=    Set Variable    ${DEVICE_PATH}/${FILENAME}
    ${local_filepath}=     Set Variable    ${SCREENSHOT_DIR}/${FILENAME}

    Run Process    adb    shell    screencap    -p    ${device_filepath}
    Run Process    adb    pull    ${device_filepath}    ${local_filepath}
    # Run Process    adb    shell    rm    ${device_filepath}


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