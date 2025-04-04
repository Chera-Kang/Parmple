*** Settings ***
Library    AppiumLibrary
Library    OperatingSystem


*** Variables ***
${REMOTE_URL}    http://127.0.0.1:4723/wd/hub
${PLATFORM_NAME}    Android
${AUTOMATION_NAME}    UiAutomator2
${NO_RESET}    true

${SCREENSHOT_DIR}    C:/Dev/appium_screenshot

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