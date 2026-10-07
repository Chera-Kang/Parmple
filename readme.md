# Parmple E2E Test Automation Framework
> **B2B 제약 CSO ERP 서비스를 위한 E2E 테스트 자동화 & AI 자가치유 파이프라인**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.62-2EAD33?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-9.1-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Appium](https://img.shields.io/badge/Appium-v2.15-662D91?style=flat-square&logo=appium&logoColor=white)](https://appium.io/)
[![Allure Report](https://img.shields.io/badge/Allure-Report-FF7800?style=flat-square&logo=qameta&logoColor=white)](https://allurereport.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini_Self--Healing-8E75C2?style=flat-square&logo=googlegemini&logoColor=white)](https://ai.google.dev/)

---

## 🎬 시연 동영상
- 🎬 **[Web] Playwright + Pytest 16개 핵심 도메인 회귀 테스트 시연**: [▶️ YouTube 바로보기](https://youtu.be/t7XDqr4cbYw)
- 🎬 **[Web] AI 활용 3단계 점진적 TC 자동 설계 및 검증 (18개 E2E)**: [▶️ YouTube 바로보기](https://youtu.be/mywifH10t74)
- 🎬 **[App] Android 하이브리드 앱 Appium 스모크 테스트 시연**: [▶️ YouTube 바로보기](https://youtu.be/AGG6c-pH-6g)
- 📁 **테스트 결과 리포트 및 산출물 샘플**: [Google Drive 바로가기](https://drive.google.com/drive/folders/1DHx_hG_0kR07e8FNK_DZIVcNYrUpTyi0)

---

## 1. 프로젝트 배경 및 문제 정의

본 프로젝트는 B2B 제약 영업대행(CSO) 및 위탁 계약 관리 플랫폼의 무중단 품질 검증을 위해 구축된 엔터프라이즈 E2E 테스트 자동화 프레임워크입니다.

### 기존 레거시의 한계
- **실행 속도 및 리소스 낭비**: 기존 Robot Framework + Selenium 기반 스위트는 직렬 실행 구조와 묵시적 대기(Implicit Wait) 남발로 인해 전체 회귀 테스트 실행에 많은 시간이 소요되었습니다.
- **복합 권한 세션 오염**: CSO(영업사원), 제약사, 최고 관리자로 이어지는 다중 권한 워크플로우에서 테스트 간 세션 쿠키 간섭 및 데이터 충돌로 간헐적 실패(Flaky Test)가 발생했습니다.
- **수동 개입 병목**: 이메일 본인 인증번호(OTP) 수기 입력과 계약 승인 상태 수동 변경 등 휴먼 인터랙션이 테스트 무인화를 가로막았습니다.

### 엔지니어링 목표
1. **차세대 테스트 스택 마이그레이션**: Python 3.13 + Playwright + Pytest 기반 전면 개편을 통한 실행 속도 개선 및 안정성 확보.
2. **다중 역할 세션 격리**: 역할별 독립 브라우저 컨텍스트 격리 체계 구축.
3. **완전 무인화 자동화**: OTP 실시간 백그라운드 파싱 및 Admin REST API 연동 사전/사후 조건 자동화.
4. **AI 활용 자가치유 및 기획 연계**: UI 변경에 능동 대응하는 AI 자가치유 및 Figma 명세 기반 자동 TC 생성 파이프라인 수립.

---

## 2. 핵심 아키텍처 및 기술 솔루션

```mermaid
graph TD
    subgraph Spec["기획 연계 및 AI 파이프라인"]
        A["Figma REST API"] -->|"기획 워크플로우 분석"| B["Figma-to-Code 생성기"]
        B -->|"독립 서브플로우 TC 생성"| C["Playwright 테스트 스위트"]
        D["Gemini AI 클라이언트"] -->|"DOM 및 에러 화면 분석"| E["자가치유 엔진"]
    end

    subgraph Engine["테스트 실행 엔진"]
        C --> F["Pytest 러너"]
        G["다중 역할 Fixture"] -->|"세션 물리 격리"| F
        H["Admin REST API / OTP 파서"] -->|"사전/사후 조건 무인화"| F
        F --> I{"Playwright 실행"}
        I -->|"셀렉터 실패 감지"| E
        E -->|"대체 로케이터 제안"| I
    end

    subgraph Report["결과 분석 및 관측성"]
        I --> J["Allure 리포트"]
        I --> K["Playwright Trace Viewer"]
        J --> L["품질 지표 관리"]
    end
```

### ① Pytest Fixture 기반 다중 역할 세션 격리
- `conftest.py` 내 커스텀 Fixture 설계를 통해 CSO (`login_cso`, `login_cso2`, `login_cso3`), 제약사 (`login_pharm1`, `login_pharm2`), 최고 관리자 (`login_admin`)의 브라우저 컨텍스트를 완전 물리 격리.
- 테스트 간 상태 오염과 캐시 충돌을 차단하여 테스트 실행 시에도 일관된 멱등성 보장.

### ② 완전 무인화 자동화 파이프라인
- **실시간 OTP 파싱 (`tools/resources/email_reader.py`)**: 회원가입 및 본인인증 단계에서 IMAP 프로토콜 백그라운드 워커가 인증 메일을 수신, 정규표현식으로 실시간 6자리 OTP 코드를 추출하여 인풋에 즉각 주입.
- **Admin REST API Setup/Teardown (`tools/resources/admin_api.py`)**: UI를 통한 수동 데이터 생성 대신 관리자 토큰 인증을 통해 계정 활성화, 사업자 승인, 계약서 상태를 API 레벨에서 처리하여 테스트 사전 준비 시간 대폭 단축.
- **공공데이터포털 연동 사업자번호 검증기 (`tools/business-validator/CheckNumber.py`)**: 국세청 사업자등록정보 진위확인 API를 연동하여 유효한 사업자등록번호 풀을 자동 검증 및 공급.

### ③ 신속한 디버깅 및 분석 체계
- **Allure Report (`report_manager.py`)**: 비즈니스 시나리오 단위 스텝 맵핑, 스크린샷, 심각도 기반 직관적 시각화 리포트 생성.
- **Playwright Trace Viewer**: 실패 발생 시점의 Action 타임라인, 네트워크 호출 로그, DOM 스냅샷, 비디오 레코딩을 자동 덤프하여 재현 불가 결함 원인 분석 시간을 획기적으로 단축.

### ④ 듀얼 트랙 TC 생성 & AI 자가치유 (Self-Healing)
- **Figma 명세 기반 자동화 (Top-Down)**: Figma REST API를 통해 기획 명세 프레임을 파싱하고, 자동 완전 탐색 알고리즘으로 하위 모달/서브페이지까지 단일 Playwright 테스트(`testcase_figma/`)로 자동 변환.
- **점진적 3단계 생성 & 자가치유 (Bottom-Up)**: Smoke ➔ 입력값 검증 ➔ 비즈니스 CRUD 단계적 확장. UI 변경으로 셀렉터 실패 시 에러 시점의 DOM 스니펫과 스크린샷(`error_artifacts/`)을 Google Gemini API에 전달하여 최적의 대체 로케이터를 제안받는 자가 치유(`self_healing/`) 파이프라인 구축.

---

## 3. 디렉토리 구조

```
c:\Dev\Parmple/
├── automation/
│   ├── app/                              # Android 하이브리드 앱 Appium 자동화
│   │   ├── testcase/                     # 모바일 스모크 및 주요 메뉴 진입 테스트
│   │   └── run.py                        # Appium 테스트 러너
│   └── web/
│       ├── playwright/                   # [메인] Playwright E2E 프레임워크
│       │   ├── conftest.py               # 다중 세션 격리 & 브라우저 픽스처
│       │   ├── report_manager.py         # Allure & Trace Viewer 연계 리포트 매니저
│       │   ├── run.py                    # 웹 테스트 실행 및 리포트 일괄 오케스트레이터
│       │   ├── testcase/                 # 핵심 회귀 테스트 스위트 (16개 도메인)
│       │   ├── testcase_ai/              # AI 기반 3단계 점진적 생성 테스트
│       │   ├── testcase_figma/           # Figma REST API 기반 파싱 생성 테스트
│       │   └── self_healing/             # Gemini AI 기반 로케이터 자가치유 엔진
│       │       ├── gemini_client.py      # LLM 프롬프트 & DOM 로그 분석 클라이언트
│       │       ├── locator_examples.py   # 로케이터 추천 예시 모음
│       │       └── self_healing_pipeline.py
│       └── robotframework/               # [레거시] 마이그레이션 대조용 스위트
├── tools/
│   ├── auth/                             # 서비스 계정 인증 및 환경 변수 템플릿
│   ├── business-validator/               # 공공데이터포털 연계 사업자번호 검증기
│   └── resources/                        # 테스트 헬퍼 (OTP 수신, Admin API, Figma Client)
├── requirements.txt                      # 의존성 명세 (Python 3.13)
└── upload.bat                            # 자동 배포 스크립트
```

---

## 4. 환경 구성 및 실행 방법

### 사전 요구사항
- **Python**: 3.13 이상
- **Node.js**: LTS (Playwright 브라우저 바이너리 지원용)
- **Java**: 11+ (Allure Report 생성을 위한 옵션)

### 1) 의존성 설치
```bash
# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/Scripts/activate    # Windows: .venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# Playwright 전용 브라우저 바이너리 설치
playwright install chromium
```

### 2) 환경 변수 설정
`tools/auth/.env.example`을 복사하여 `tools/auth/.env`를 생성하고 실제 접속 정보와 API 키를 입력합니다.
```bash
cp tools/auth/.env.example tools/auth/.env
```
```env
# 엔드포인트
BASE_URL=https://qa.erp.parmple.com/
ADMIN_URL=https://qa.admin.parmple.com/
ADMIN_API_URL=https://qa.api.parmple.com

# Gmail IMAP (OTP 실시간 파싱)
EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password

# 테스트 계정 (Fixture & API)
ADMIN_EMAIL=admin@example.com
ID_CSO=cso1@example.com
PASSWORD=your_test_password123!

# 공공데이터포털 & Google Sheet
ODCLOUD_SERVICE_KEY=your_service_key_here
GSHEET_KEY=your_google_sheet_key_here

# AI 자가 치유 & Figma API
GEMINI_API_KEY=your_gemini_api_key_here
FIGMA_ACCESS_TOKEN=your_figma_personal_access_token_here
```

### 3) 테스트 실행

#### [Web] Playwright 전체 회귀 테스트 실행 및 리포트 생성
```bash
# 통합 실행 스크립트 (테스트 구동 + Allure 리포트 생성)
python automation/web/playwright/run.py

# 또는 Pytest 직접 실행
pytest automation/web/playwright/testcase/ --alluredir=allure-results
allure serve allure-results
```

#### [Web] Figma-to-Code 파이프라인 테스트 실행
```bash
pytest automation/web/playwright/testcase_figma/ -v
```

#### [App] Android 하이브리드 앱 스모크 테스트 실행
```bash
python automation/app/run.py
```

---

## 5. 자동화 프레임워크 전환 효과

| 구분 | 기존 레거시 (Robot Framework) | 신규 프레임워크 (Python + Playwright) | 개선 효과 |
|---|---|---|---|
| **테스트 실행 구조** | 단일 스레드 직렬 실행 | 다중 세션 격리 기반 최적화 실행 | 테스트 수행 속도 및 환경 안정성 대폭 개선 |
| **테스트 불안정성 (Flaky)** | 대기 시간 초과 및 세션 간섭 빈번 | DOM 상태 기반 대기 및 세션 물리 격리 | 간헐적 실패율 최소화 및 결과 신뢰성 확보 |
| **사전/사후 처리 무인화** | 인증번호 및 승인 상태 수동 개입 필요 | 실시간 OTP 파싱 및 Admin API 연동 | 사람의 개입이 필요 없는 완전 무인화 파이프라인 달성 |
| **실패 원인 디버깅** | 텍스트 로그 및 부분 스크린샷 의존 | Playwright Trace Viewer (비디오/DOM 타임라인) | 실패 재현 및 원인 분석 시간 단축 |
| **테스트케이스 설계** | 기획서 수동 분석 후 스크립트 작성 | Figma REST API 파싱 기반 자동 생성 | 신규 화면에 대한 테스트 작성 리소스 절감 |
| **UI 변경 유지보수** | 셀렉터 깨짐 시 수동 코드 수정 | Gemini AI 대체 로케이터 자동 제안 (자가치유) | UI 변경에 따른 테스트 중단 방지 및 유지보수성 향상 |