import json

def generate_healing_prompt(
    intent: str, 
    failed_selector: str, 
    dom_snippet: str,
    error_message: str = ""
) -> dict:
    """
    스크린샷과 DOM 트리를 바탕으로 AI 모델(Gemini 1.5 Pro Vision 등)에게
    새로운 셀렉터 추론을 요청하기 위한 프롬프트를 생성합니다.
    """
    
    system_prompt = """
    You are an expert QA Automation Engineer and AI Agent specializing in web element location.
    Your task is to analyze the provided screenshot and HTML DOM snippet to find a stable Playwright selector for a target element.
    
    [Context]
    A Playwright E2E test has failed to locate an element due to a TimeoutError. 
    The web application uses a dynamic grid where standard ID or Class attributes are often random, missing, or unstable.
    
    [Your Goal]
    Identify the target element based on the 'User Intent' and the previous 'Failed Selector'.
    Provide a robust Playwright selector (CSS, XPath, or Playwright specific locator like text or chaining) that uniquely identifies the target element in the current DOM.
    
    [Guidelines for Selectors]
    1. Prefer text-based locators if the text is unique (e.g., `text="Submit"`).
    2. Prefer semantic relationships (e.g., finding a row by text, then a button inside it).
    3. Avoid highly absolute XPath or CSS paths (e.g., `div > div > span:nth-child(3)`).
    4. Focus on attributes like `aria-label`, `data-testid`, `placeholder`, or specific structural patterns if text is not available.
    
    [Output Format]
    You MUST respond with a valid JSON object containing exactly two keys:
    - "reasoning": A brief explanation of why the original selector failed and how you derived the new one.
    - "new_selector": The new, robust Playwright selector string.
    """

    user_prompt = f"""
    [Test Execution Context]
    - User Intent (Action): {intent}
    - Failed Selector: `{failed_selector}`
    - Error Message: {error_message}

    [DOM Snippet]
    Below is the HTML snippet of the container where the element was expected to be:
    ```html
    {dom_snippet}
    ```

    [Visual Context]
    (A screenshot of the current viewport is attached to this request)

    Please analyze the DOM and the screenshot, and provide the new selector in the required JSON format.
    """
    
    return {
        "system_instruction": system_prompt.strip(),
        "user_message": user_prompt.strip()
    }


# --- 사용 예시 ---
if __name__ == "__main__":
    # 실패 상황 가정
    intent_description = "사용자 그리드에서 '홍길동'이 있는 행의 '상세보기' 버튼 클릭"
    old_selector = "button#btn-detail-12345" # 동적 ID로 인해 실패
    
    # 추출된 DOM 스니펫 가상 데이터
    sample_dom = """
    <table class="ag-grid-container">
        <tbody>
            <tr role="row" class="ag-row">
                <td class="ag-cell">이몽룡</td>
                <td class="ag-cell"><button class="action-btn">상세보기</button></td>
            </tr>
            <tr role="row" class="ag-row">
                <td class="ag-cell">홍길동</td>
                <td class="ag-cell"><button class="action-btn">상세보기</button></td>
            </tr>
        </tbody>
    </table>
    """
    
    prompt_data = generate_healing_prompt(
        intent=intent_description,
        failed_selector=old_selector,
        dom_snippet=sample_dom,
        error_message="Timeout 30000ms exceeded."
    )
    
    print("=== System Prompt ===")
    print(prompt_data["system_instruction"])
    print("\n=== User Prompt ===")
    print(prompt_data["user_message"])
    
    print("\n\n[예상되는 AI 응답 예시 (JSON)]")
    dummy_ai_response = {
        "reasoning": "The old selector used a dynamic ID 'btn-detail-12345' which likely changed. Based on the DOM, the table contains rows with user names. We can locate the row containing '홍길동' and then find the '상세보기' button within that specific row.",
        "new_selector": "tr:has-text('홍길동') >> button:has-text('상세보기')" 
    }
    print(json.dumps(dummy_ai_response, indent=2, ensure_ascii=False))
