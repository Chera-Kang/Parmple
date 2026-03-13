import email
import re
import time
import os
import sys
from email.header import decode_header
from imaplib import IMAP4_SSL
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# =============================================================================
# 1. 초기 설정 및 환경 변수 로드
# =============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, "common", "auth", ".env")
load_dotenv(ENV_PATH)

EMAIL_USER = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
SENDER_FILTER = "noreply@parmple.com"

# =============================================================================
# 2. 이메일 데이터 파싱 유틸리티
# =============================================================================

def decode_mime_words(s):
    """ MIME 인코딩된 문자열(제목, 보낸이 등)을 디코딩합니다. """
    decoded = decode_header(s)
    return ''.join(
        str(part[0], part[1] or 'utf-8') if isinstance(part[0], bytes) else part[0]
        for part in decoded
    )

# =============================================================================
# 3. 인증번호 추출 핵심 로직
# =============================================================================

def fetch_auth_code(max_retries=5, retry_delay=3):
    """
    Gmail IMAP을 통해 최신 인증 메일을 조회하고 숫자 코드를 추출합니다.
    추출 실패 시 재시도 로직을 포함합니다.
    """
    if not EMAIL_USER or not APP_PASSWORD:
        return "ERROR: EMAIL or APP_PASSWORD not set in .env"

    for attempt in range(1, max_retries + 1):
        try:
            with IMAP4_SSL("imap.gmail.com") as mail:
                mail.login(EMAIL_USER, APP_PASSWORD)
                mail.select("inbox")

                # 전체 메일 검색 (실제 환경에서는 최근 메일 위주로 필터링 권장)
                result, data = mail.search(None, "ALL")
                mail_ids = data[0].split()

                if mail_ids:
                    # 최신순으로 최근 10개 메일만 확인
                    for i in reversed(mail_ids[-10:]):
                        result, msg_data = mail.fetch(i, "(RFC822)")
                        raw_email = msg_data[0][1]
                        msg = email.message_from_bytes(raw_email)

                        sender = decode_mime_words(msg["From"])
                        if SENDER_FILTER in sender:
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/html":
                                        charset = part.get_content_charset() or "utf-8"
                                        body = part.get_payload(decode=True).decode(charset, errors="replace")
                                        break
                            else:
                                charset = msg.get_content_charset() or "utf-8"
                                body = msg.get_payload(decode=True).decode(charset, errors="replace")

                            # HTML에서 텍스트 추출 및 4~8자리 숫자(인증번호) 검색
                            soup = BeautifulSoup(body, "html.parser")
                            text = soup.get_text()
                            match = re.search(r"[0-9]{4,8}", text)
                            if match:
                                return match.group(0)
        except Exception:
            pass # 일시적인 네트워크 등 에러는 무시하고 재시도

        if attempt < max_retries:
            time.sleep(retry_delay)
            
    return "NO_CODE"

# =============================================================================
# 4. 메인 실행부 (CLI 호출 지원)
# =============================================================================

if __name__ == "__main__":
    # Robot Framework 등 외부에서 실행 시 인증번호만 출력
    print(fetch_auth_code())