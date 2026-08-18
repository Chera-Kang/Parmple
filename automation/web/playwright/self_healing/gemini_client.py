import os
import json
import google.generativeai as genai
try:
    from .ai_agent_prompt import generate_healing_prompt
except ImportError:
    from ai_agent_prompt import generate_healing_prompt

# .env 파일에서 API 키를 자동으로 로드합니다.
def load_api_key():
    # 1. 환경 변수에 이미 있다면 우선 사용
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINO_API_KEY")
    if key:
        return key

    # 2. dotenv 라이브러리가 있다면 로드 시도
    env_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "auth", ".env"),
        os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"),
        os.path.join(os.getcwd(), "common", "auth", ".env"),
        os.path.join(os.getcwd(), ".env")
    ]
    try:
        from dotenv import load_dotenv
        for p in env_paths:
            if os.path.exists(p):
                load_dotenv(p)
                key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINO_API_KEY")
                if key:
                    return key
    except ImportError:
        pass

    # 3. 직접 .env 파일 파싱 fallback
    for p in env_paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY=") or line.startswith("GEMINO_API_KEY="):
                        return line.split("=", 1)[1].strip()
    return None

API_KEY = load_api_key()
if API_KEY:
    genai.configure(api_key=API_KEY)

async def call_gemini_for_selector(
    intent: str, 
    failed_selector: str, 
    dom_snippet: str,
    screenshot_path: str = None,
    error_message: str = ""
) -> dict:
    """
    제미나이 API를 호출하여 새로운 셀렉터를 추론받습니다.
    """
    if not API_KEY:
        print("[AI Client] 경고: GEMINI_API_KEY가 설정되지 않아 더미 데이터를 반환합니다.")
        # 키가 없을 때 테스트용으로 반환할 더미 데이터
        return {
            "reasoning": "API 키가 없어 임시로 반환된 더미 결과입니다.",
            "new_selector": "button"
        }
        
    try:
        # 프롬프트 생성
        prompt_data = generate_healing_prompt(
            intent=intent,
            failed_selector=failed_selector,
            dom_snippet=dom_snippet,
            error_message=error_message
        )
        
        # 최신 모델 선택 (Gemini 3.7 Flash)
        model = genai.GenerativeModel(
            model_name="gemini-3.7-flash",
            system_instruction=prompt_data["system_instruction"]
        )
        
        # 스크린샷 이미지와 프롬프트를 함께 준비
        contents = [prompt_data["user_message"]]
        
        if screenshot_path and os.path.exists(screenshot_path):
            import PIL.Image
            img = PIL.Image.open(screenshot_path)
            contents.append(img)
            
        print("[AI Client] 제미나이에게 셀렉터 추론을 요청 중입니다...")
        
        # 모델 호출 (JSON 형태로 응답을 강제하기 위한 설정 가능)
        response = model.generate_content(
            contents,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        
        # 응답 텍스트를 JSON으로 파싱
        result_json = json.loads(response.text)
        print(f"[AI Client] 추론 성공: {result_json}")
        return result_json
        
    except Exception as e:
        print(f"[AI Client] API 호출 실패: {e}")
        return None
