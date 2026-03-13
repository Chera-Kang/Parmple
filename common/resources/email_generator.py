import datetime
import sys

# =============================================================================
# [Email Generator] 테스트용 고유 이메일 주소 생성 도구
# =============================================================================

def generate_email(prefix="chera.workspace", domain="gmail.com"):
    """
    초 단위까지 포함하여 중복 가능성을 완전히 제거한 고유 이메일을 생성합니다.
    형식: chera.workspace+yymmdd.hhmmss@gmail.com
    예: chera.workspace+260312.152411@gmail.com
    """
    now = datetime.datetime.now()
    # YYMMDD.HHMMSS 형식 (예: 260312.152411)
    time_str = now.strftime("%y%m%d.%H%M%S")
    
    email_addr = f"{prefix}+{time_str}@{domain}"
    return email_addr

if __name__ == "__main__":
    # CLI 호출 시 커스텀 prefix/domain 지원
    p = sys.argv[1] if len(sys.argv) > 1 else "chera.workspace"
    d = sys.argv[2] if len(sys.argv) > 2 else "gmail.com"
    
    print(generate_email(p, d))
