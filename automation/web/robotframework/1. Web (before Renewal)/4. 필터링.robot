*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Resource   ../keywords_legacy.robot

Suite Setup    Initialize Test Suite
Suite Teardown    Finalize Test Suite

*** Variables ***
*** Keywords ***
*** Test Cases ***
---- 1. 필터링 Testcase
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    Input Text    id=login-email    ${USER_2_ID}
    Input Text    id=login-password    ${USER_2_PW}
    Sleep    0.5
    Click Button    class=btn
    
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10


-------- 1.1. 필터링 조회
    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='필터링 조회']
    Wait Until Element Is Visible    class=grid-contents-list-fit     10
    Screenshot

    # # 필터링 검색 1
    # Click Element    class=select2-selection__arrow
    # Press Key    class=select2-search__field    기아
    # Press Keys    None    ENTER
    # Wait Until Element Is Visible    class=mp-selectbox    2
    # Click Element    class=mp-selectbox
    # Press Key    id=check_biz_reg_no    1234567890
    # Screenshot
    # Click Element    id=btn-search
    # Screenshot

    # # 필터링 검색 2
    # Click Element    class=select2-selection__arrow
    # Press Key    class=select2-search__field    김승일마취통증의학과의원
    # Press Keys    None    ENTER
    # Wait Until Element Is Visible    class=mp-selectbox    2
    # Click Element    class=mp-selectbox
    # Press Key    id=check_biz_reg_no    2049137937
    # Screenshot
    # Click Element    id=btn-search
    # Screenshot

    # 필터링 검색 3 (qa 서버 db 관련 이슈로 검색되지 않는 것만 확인)
    Click Element    class=select2-selection__arrow
    Press Key    class=select2-search__field    메디
    Press Keys    None    ENTER
    Wait Until Element Is Visible    class=mp-selectbox__info    2
    Click Element    class=mp-selectbox__info
    Wait Until Element Is Visible    class=mp-selectbox__title    2
    Press Key    id=check_biz_reg_no    2049137937
    Screenshot
    Click Element    id=btn-search
    Screenshot
    Click Button    class=swal2-confirm
    
    # # 세로 스크롤이 있는지 확인하고 스크롤 동작 수행
    # Execute JavaScript    if (document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").scrollHeight > document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").clientHeight) { document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").scrollTo({ top: document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").scrollHeight, behavior: 'smooth' }); } else { console.log('세로 스크롤 없음'); }
    # Screenshot

    # # 세로 스크롤을 맨 위로 스크롤
    # Execute JavaScript    if (document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").scrollHeight > document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").clientHeight) { document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").scrollTo({ top: 0, behavior: 'smooth' }); } else { console.log('세로 스크롤 없음'); }
    # Screenshot


-------- 1.2. 필터링 조회 이력
    # 계정 변경  
    Click Element    xpath=//*[@id="navbar-collapse"]/ul/li/a/div/div
    Sleep    0.5

    Click Element    xpath=//*[@id="navbar-collapse"]/ul/li/ul/li[5]/a/span
    Screenshot

    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    Input Text    id=login-email    pharm_manager@example.com
    Input Text    id=login-password    dummy_password123!
    Screenshot
    Click Button    class=btn
    
    Wait Until Element Is Visible    //img[@src='https://qa.erp.parmple.com/assets/img/branding/logo_pp.png']    10

    MainMenu Mouse Over
    Click Element    xpath=//div[@class='gnb_title' and text()='필터링 조회 이력']
    Wait Until Element Is Visible    class=b-grid-cell    10
    Screenshot

    # 가로 스크롤이 있는지 확인하고 가로 스크롤 동작 수행
#   Execute JavaScript    if (document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-virtual-scrollers.b-show-yscroll-padding > div.b-virtual-scroller.b-widget-scroller.b-resize-monitored.b-horizontal-overflow").scrollWidth > document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-virtual-scrollers.b-show-yscroll-padding > div.b-virtual-scroller.b-widget-scroller.b-resize-monitored.b-horizontal-overflow").clientWidth) { document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-virtual-scrollers.b-show-yscroll-padding > div.b-virtual-scroller.b-widget-scroller.b-resize-monitored.b-horizontal-overflow").scrollTo({ left: document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-virtual-scrollers.b-show-yscroll-padding > div.b-virtual-scroller.b-widget-scroller.b-resize-monitored.b-horizontal-overflow").scrollWidth, behavior: 'smooth' }); } else { console.log('가로 스크롤 없음'); }
    Screenshot

    # 세로 스크롤이 있는지 확인하고 스크롤 동작 수행
    Execute JavaScript    if (document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").scrollHeight > document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").clientHeight) { document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").scrollTo({ top: document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").scrollHeight, behavior: 'smooth' }); } else { console.log('세로 스크롤 없음'); }
    Screenshot

    # 가로 스크롤을 맨 왼쪽으로 스크롤
#    Execute JavaScript    if (document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-virtual-scrollers.b-show-yscroll-padding > div.b-virtual-scroller.b-widget-scroller.b-resize-monitored.b-horizontal-overflow").scrollWidth > document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-virtual-scrollers.b-show-yscroll-padding > div.b-virtual-scroller.b-widget-scroller.b-resize-monitored.b-horizontal-overflow").clientWidth) { document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-virtual-scrollers.b-show-yscroll-padding > div.b-virtual-scroller.b-widget-scroller.b-resize-monitored.b-horizontal-overflow").scrollTo({ left: 0, behavior: 'smooth' }); } else { console.log('가로 스크롤 없음'); }
    Screenshot

    # 세로 스크롤을 맨 위로 스크롤
    Execute JavaScript    if (document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").scrollHeight > document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").clientHeight) { document.querySelector("#b-grid-1 > div.b-vbox.b-box-center.b-panel-body-wrap.b-grid-body-wrap > div.b-grid-panel-body > div.b-grid-body-container.b-widget-scroller.b-resize-monitored.b-vertical-overflow").scrollTo({ top: 0, behavior: 'smooth' }); } else { console.log('세로 스크롤 없음'); }
    Screenshot
