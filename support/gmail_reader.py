import email
from email.header import decode_header
from imaplib import IMAP4_SSL
import re
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv() # .env 파일 환경변수로 불러오기

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
SENDER_FILTER = "noreply@parmple.com"

MAX_RETRIES = 5
RETRY_DELAY = 3  # 초

def decode_mime_words(s):
    decoded = decode_header(s)
    return ''.join(
        str(part[0], part[1] or 'utf-8') if isinstance(part[0], bytes) else part[0]
        for part in decoded
    )

def fetch_auth_code():
    with IMAP4_SSL("imap.gmail.com") as mail:
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("inbox")

        result, data = mail.search(None, "ALL")
        mail_ids = data[0].split()

        if not mail_ids:
            return None

        for i in reversed(mail_ids[-10:]):  # 최근 10개만 확인
            result, msg_data = mail.fetch(i, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            sender = msg["From"]
            subject = msg["Subject"]

            decoded_subject = decode_mime_words(subject)
            decoded_sender = decode_mime_words(sender)

            if SENDER_FILTER in decoded_sender:
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/html" and "attachment" not in content_disposition:
                            charset = part.get_content_charset() or "utf-8"
                            body = part.get_payload(decode=True).decode(charset, errors="replace")
                            break
                else:
                    charset = msg.get_content_charset() or "utf-8"
                    body = msg.get_payload(decode=True).decode(charset, errors="replace")

                soup = BeautifulSoup(body, "html.parser")
                text = soup.get_text(separator="\n")

                match = re.search(r"[0-9]{4,8}", text)
                if match:
                    return match.group(0)

    return None


if __name__ == "__main__":
    # 인증번호 추출 재시도
    for attempt in range(1, MAX_RETRIES + 1):
        # print(f"시도 {attempt}: EMAIL={EMAIL}, APP_PASSWORD={'SET' if APP_PASSWORD else 'NONE'}")
        code = fetch_auth_code()
        if code:
            print(code)
            break
        else:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    else:
        print("NO_CODE")



# # 인증번호 추출 재시도
# for attempt in range(1, MAX_RETRIES + 1):
#     print(f"시도 {attempt}: EMAIL={EMAIL}, APP_PASSWORD={'SET' if APP_PASSWORD else 'NONE'}") ################ 11
#     code = fetch_auth_code()
#     if code:
#         print(code)
#         break
#     else:
#         if attempt < MAX_RETRIES:
#             time.sleep(RETRY_DELAY)
# else:
#     print("NO_CODE")