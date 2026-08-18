import asyncio
from playwright.async_api import async_playwright, Page

async def interact_with_dynamic_grid(page: Page):
    """
    동적 그리드(Dynamic Grid)에서 Playwright의 계층적 Locator를 활용하는 예시입니다.
    고정된 ID나 Class Name에 의존하지 않고, 텍스트나 DOM 구조적 관계를 통해 요소를 찾습니다.
    """
    
    # 예시 1: 특정 텍스트를 포함하는 행(Row)을 찾고, 그 행 내부의 버튼 클릭
    # 시나리오: "사용자 관리" 그리드에서 "홍길동"이라는 텍스트가 있는 행을 찾고, 해당 행의 "수정" 버튼을 클릭
    print("1. 특정 텍스트 기반 행(Row) 탐색 및 하위 요소 클릭")
    
    # 1. 그리드의 모든 행(tr) 요소를 잡습니다. (특정 그리드 컨테이너 내부로 한정하는 것이 좋습니다)
    grid_rows = page.locator('table#user-grid tbody tr') 
    
    # 2. '홍길동' 텍스트를 포함하는(filter) 행으로 범위를 좁힙니다.
    target_row = grid_rows.filter(has_text="홍길동")
    
    # 3. 해당 행 내부에서 '수정' 텍스트를 가진 버튼을 찾아 클릭합니다.
    edit_button = target_row.locator('button', has_text="수정")
    
    # 요소가 화면에 보일 때까지 대기 후 클릭 (Playwright는 auto-wait 기능을 지원함)
    # await edit_button.click()
    print(f"Locator 생성 완료: {edit_button}")


    # 예시 2: 특정 자식 요소를 가진(has) 부모 찾기
    # 시나리오: 체크박스가 선택된(checked) 상태인 행을 찾아서, 그 행의 특정 데이터를 가져오기
    print("\n2. 특정 자식 요소를 상태를 기반으로 부모 행(Row) 탐색")
    
    # 체크된 체크박스를 가지고 있는 tr 요소를 찾습니다.
    checked_rows = page.locator('tr').filter(has=page.locator('input[type="checkbox"]:checked'))
    
    # 찾은 행들 중에서 첫 번째 행의 세 번째 열(td)의 텍스트를 가져온다고 가정
    first_checked_row_data = checked_rows.first.locator('td').nth(2)
    # text_content = await first_checked_row_data.text_content()
    print(f"Locator 생성 완료: {first_checked_row_data}")


    # 예시 3: 형제 요소(Sibling) 참조
    # 시나리오: "상태" 라벨 옆에 있는 드롭다운(select) 선택하기
    print("\n3. 인접 형제 요소(Sibling) 기반 탐색")
    
    # 텍스트가 "상태:"인 label을 찾고, 그 바로 뒤에 오는(또는 인접한) select 태그 찾기
    status_label = page.locator('label', has_text="상태:")
    
    # Playwright에서는 XPath나 CSS의 형제 결합자를 사용하거나, locator chaining을 할 수 있습니다.
    # CSS 인접 형제 결합자 (+) 사용 예시:
    # status_dropdown = page.locator('label:has-text("상태:") + select')
    
    # 또는 XPath를 사용하여 부모로 올라갔다가 다른 자식을 찾는 방식도 유용합니다.
    # text="상태:" 요소를 기준으로 가장 가까운 부모 div를 찾고, 그 안의 select 요소를 찾음
    status_dropdown = status_label.locator("xpath=ancestor::div[1]//select")
    
    # await status_dropdown.select_option(value="ACTIVE")
    print(f"Locator 생성 완료: {status_dropdown}")

async def main():
    # 실행 테스트용 뼈대
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # await page.goto("https://example.com") # 실제 테스트 대상 URL로 변경 필요
        # await interact_with_dynamic_grid(page)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
