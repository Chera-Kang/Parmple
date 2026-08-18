import os
import time
from typing import Callable, Any
from functools import wraps
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

# 추출된 데이터를 저장할 기본 디렉토리
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "error_artifacts")

def create_output_dir_if_not_exists():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

async def extract_context_on_failure(page: Page, target_container_selector: str = "body"):
    """
    실패 시점의 스크린샷과 특정 DOM 영역의 스니펫을 추출하여 저장합니다.
    """
    create_output_dir_if_not_exists()
    timestamp = int(time.time())
    
    screenshot_path = os.path.join(OUTPUT_DIR, f"screenshot_{timestamp}.png")
    dom_path = os.path.join(OUTPUT_DIR, f"dom_snippet_{timestamp}.html")
    
    # 1. 스크린샷 캡처
    print(f"[Self-Healing] 스크린샷 캡처 중... -> {screenshot_path}")
    await page.screenshot(path=screenshot_path, full_page=True)
    
    # 2. DOM 스니펫 추출 (전체 body 또는 특정 Grid/Container 영역)
    print(f"[Self-Healing] DOM 데이터 추출 중... (Selector: {target_container_selector}) -> {dom_path}")
    try:
        # 특정 영역으로 좁혀서 추출 (AI 토큰 최적화를 위해 중요)
        container = page.locator(target_container_selector).first
        
        # Playwright의 evaluate를 통해 해당 요소의 innerHTML 또는 outerHTML을 가져옴
        dom_content = await container.evaluate("el => el.outerHTML")
        
        with open(dom_path, 'w', encoding='utf-8') as f:
            f.write(dom_content)
            
    except Exception as e:
        print(f"[Self-Healing] DOM 추출 실패: {e}")
        # 실패 시 fallback으로 전체 페이지 컨텐츠 저장
        content = await page.content()
        with open(dom_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    return screenshot_path, dom_path


def with_self_healing(target_container_selector: str = "body"):
    """
    Playwright 액션 함수에 적용할 수 있는 Self-healing 데코레이터입니다.
    TimeoutError 발생 시 예외를 포착하고 분석을 위한 데이터를 추출합니다.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(page: Page, *args, **kwargs):
            try:
                # 원래의 테스트 액션 실행 (예: 버튼 클릭, 텍스트 입력 등)
                return await func(page, *args, **kwargs)
            
            except PlaywrightTimeoutError as e:
                print(f"\n[Self-Healing Alert] TimeoutError 발생! 요소를 찾을 수 없습니다.")
                print(f"Error Details: {str(e)[:200]}...")
                
                # 에러 발생 시 데이터(스크린샷, DOM) 추출
                screenshot_path, dom_path = await extract_context_on_failure(
                    page, target_container_selector
                )
                
                print(f"[Self-Healing] AI 분석에 필요한 데이터가 수집되었습니다.")
                print(f"- Screenshot: {screenshot_path}")
                print(f"- DOM Snippet: {dom_path}")
                
                # Gemini API 호출 및 셀렉터 추론 로직 연동
                try:
                    from .gemini_client import call_gemini_for_selector
                except ImportError:
                    from gemini_client import call_gemini_for_selector
                
                # 방금 실패한 액션에 대한 인텐트를 여기서 하드코딩하거나 
                # decorator 인자로 받도록 구조화할 수 있습니다.
                intent = "요소와 상호작용 (예: 버튼 클릭)" 
                failed_selector = "Unknown Selector" # 원래 함수에서 추출할 수 있으면 가장 좋습니다
                
                inferred_data = await call_gemini_for_selector(
                    intent=intent,
                    failed_selector=failed_selector,
                    dom_snippet=open(dom_path, encoding='utf-8').read(),
                    screenshot_path=screenshot_path,
                    error_message=str(e)
                )
                
                if inferred_data and "new_selector" in inferred_data:
                    new_selector = inferred_data["new_selector"]
                    print(f"[Self-Healing] AI가 추천한 새로운 셀렉터로 재시도합니다: {new_selector}")
                    print(f"-> 이유: {inferred_data.get('reasoning', '')}")
                    
                    try:
                        # 재시도 (여기서는 단순히 클릭한다고 가정. 실제 프레임워크에서는 원래의 action type에 맞게 재시도해야 합니다)
                        return await page.locator(new_selector).click(timeout=3000)
                    except Exception as retry_e:
                        print(f"[Self-Healing] 재시도마저 실패했습니다: {retry_e}")
                        raise retry_e
                else:
                    # 자가 치유에 실패했다면 원래의 예외를 다시 던짐
                    raise e
        return wrapper
    return decorator


# --- 사용 예시 ---

@with_self_healing(target_container_selector="table#user-grid") # 그리드 영역으로 DOM 추출 한정
async def click_submit_button(page: Page):
    """
    테스트 로직 예시: 존재하지 않는 요소를 클릭하여 고의로 Timeout을 발생시킵니다.
    """
    print("제출 버튼 클릭 시도...")
    # Timeout 3초로 짧게 설정하여 빠른 테스트
    await page.locator("button#non-existent-submit").click(timeout=3000)

async def test_run():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 테스트용 더미 페이지 설정
        await page.set_content("""
        <html>
            <body>
                <h1>테스트 페이지</h1>
                <table id="user-grid">
                    <tr><td>사용자 1</td><td><button>수정</button></td></tr>
                    <tr><td>사용자 2</td><td><button>수정</button></td></tr>
                </table>
            </body>
        </html>
        """)
        
        try:
            await click_submit_button(page)
        except Exception as e:
            print(f"최종 실패: {type(e).__name__}")
            
        await browser.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_run())
