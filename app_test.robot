*** Settings ***
Library    AppiumLibrary
Library    OperatingSystem
Resource   ../support/app_keywords.robot
Library    ../.venv/Lib/site-packages/robot/libraries/Process.py
Library    String

*** Variables ***
# LG V30
${DEVICE_NAME}    LGMV300S9da9bb03    # LG V30
# Nexus 5X
# ${DEVICE_NAME}    02664b87309f3009    # Nexus 5X

*** Keywords ***
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

    Take App Screenshot

    Open Wikipedia
    
    # 앱 실행 대기 
    Sleep    1
    Wait Until Element Is Visible    class=android.widget.FrameLayout    10

    
    Take App Screenshot

    Sleep    2
    # Copy All Screenshots To Local

    Copy All Screenshots To Dated Folder
    

---- Test 종료 (앱 종료)
    # 앱 종료
    Terminate Application    ${APP_PACKAGE}
