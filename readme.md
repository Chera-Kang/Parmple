# Parmple E2E Test Automation Framework
> Cross-Platform E2E Test Automation Architecture for Web & Hybrid App

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.62-2EAD33?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Appium](https://img.shields.io/badge/Appium-v2.15-662D91?style=flat-square&logo=appium&logoColor=white)](https://appium.io/)
[![Pytest](https://img.shields.io/badge/Pytest-9.1-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Allure Report](https://img.shields.io/badge/Allure-Report-FF7800?style=flat-square&logo=qameta&logoColor=white)](https://allurereport.org/)

B2B 제약 영업대행(CSO) 및 위탁 계약 관리 플랫폼의 품질 안정성을 확보하기 위해 구축된 E2E 테스트 자동화 프레임워크입니다.  
Selenium 및 Robot Framework 기반의 레거시 환경을 Playwright & Appium 모던 스택으로 전환하여 실행 속도와 테스트 신뢰도를 개선하고, 기획 스펙 분석부터 3단계 리포팅까지의 통합 파이프라인을 구축했습니다.

---

## 1. 주요 시연 영상 (Execution Demos)
> 브라우저 및 모바일 환경에서의 실제 구동 및 검증 전 과정을 녹화한 아카이브입니다.

- **[Web] Playwright + Pytest 마이그레이션 전체 회귀 테스트 시연 (2026.09)**  
  [▶️ YouTube 바로보기](https://youtu.be/t7XDqr4cbYw)  
  *기존 Robot Framework 대비 실행 속도 개선 및 16개 핵심 비즈니스 도메인 회귀 테스트 일괄 구동*

- **[Web] LLM 기반 3-Phase TC 자동 설계 및 18개 E2E 테스트 검증 (2026.09)**  
  [▶️ YouTube 바로보기](https://youtu.be/mywifH10t74)  
  *기획/UI 스펙 기반 점진적 3단계(Smoke ➔ Validation ➔ E2E) 자동 생성 및 18개 테스트 즉시 Pass 검증*

- **[App] Android 하이브리드 앱 Appium E2E 스모크 테스트 시연 (2026.09)**  
  [▶️ YouTube 바로보기](https://youtu.be/AGG6c-pH-6g)  
  *서버 프로세스 자동 관리, 1회 로그인 세션 재사용 및 GNB 핵심 메뉴 네비게이션 검증*

- **과거 마일스톤 시연 아카이브**:  
  [Design System 버전 (25.10.27)](https://youtu.be/e3fbpIVPqks) | [Renewal 버전 (25.08.06)](https://youtu.be/KU7lC9yqJbI) | [초기 버전 (25.04.15)](https://youtu.be/5YyteNw1Jz4) | [결과 리포트 샘플 (.zip)](https://drive.google.com/drive/folders/1f9foK6b4ZrYw6ugmbNNy25gB79n0HGNt)

---

## 2. 아키텍처 및 설계 원칙 (Key Architecture)

### 1) Multi-Role Session Fixture 기반의 계정 격리
- CSO(영업대행), 제약사, 플랫폼 관리자 등 복합 권한이 얽힌 B2B 플랫폼 특성에 맞춰, Pytest Fixture(`conftest.py`)를 통해 역할별 세션 라이프사이클을 독립 분리했습니다.
- 테스트 간 로그인 상태 간섭을 원천 차단하여 각 테스트 함수의 완전한 독립성을 확보했습니다.

### 2) Zero False-Positive (가짜 통과 원천 금지)
- 단순 클릭이나 화면 진입 후 단언문 없이 성공 처리되는 무음 통과(Silent Pass)를 배제했습니다.
- 모든 사용자 인터랙션 뒤에는 실질적인 DOM 상태 변화(State Mutation), 고유 텍스트 노출, 또는 URL 변경을 `expect().to_be_visible()`로 1:1 강제 단언하도록 거버넌스 헌장(`.agents/rules/qa_automation.md`)을 정립했습니다.

### 3) LLM을 활용한 TC 설계 고도화 및 Self-Healing
- **점진적 3-Phase 전략**: 기획서(Figma) 분석 시 `Phase 1 (Core Smoke)` ➔ `Phase 2 (Atomic Validation)` ➔ `Phase 3 (Dynamic E2E & CRUD)` 순으로 범위를 확장하는 설계 규칙을 적용하여 높은 테스트 커버리지와 신뢰도를 확보했습니다.
- **Self-Healing 파이프라인**: UI 개편으로 인한 Selector 변경 발생 시 장애 시점의 DOM 스냅샷과 에러 로그를 분석하여 대체 로케이터를 추천하는 보정 파이프라인을 구성했습니다.

### 4) 환경 추상화 및 시크릿 격리
- `BASE_URL`, `ADMIN_URL`, `ADMIN_API_URL`을 환경변수 레이어로 추상화하여 QA 서버, 로컬 개발 환경, 스테이징 서버로 유연하게 타겟팅을 전환할 수 있습니다.
- 민감 정보는 `.gitignore`로 완전 차단하고 `.env.example` 및 `credentials.sample.json` 템플릿을 제공하여 보안 거버넌스와 프로젝트 온보딩 편의성을 동시에 확보했습니다.

### 5) Multi-Tier 3-in-1 리포팅 체계
커스텀 테스트 러너(`run.py`) 1회 실행으로 목적에 맞춘 3가지 표준 결과물을 타임스탬프 디렉토리에 동시 번들링합니다:
- **Pytest HTML Report**: 실패 시 전체 화면 스크린샷이 자동 임베딩되는 단일 독립형 요약 리포트
- **Allure Single-file Dashboard**: 성공률 파이 차트, 스위트별 통계 및 실패 원인을 시각화한 인터랙티브 대시보드
- **Playwright Trace Viewer**: 마우스 이동 궤적, 클릭 전/후 DOM 스냅샷, 네트워크 트래픽을 프레임 단위로 재생하는 디버깅 도구

---

## 3. 프로젝트 구조 (Directory Structure)

```
Parmple\
├── .agents/rules/               # QA 품질 거버넌스 헌장 (Zero False-Positive, 3-Phase TC 설계)
│   ├── qa_automation.md
│   └── qa_tc_creation.md
│
├── automation/                  # 메인 테스트 자동화 프레임워크
│   ├── app/                     # [Appium] Android 하이브리드 앱 테스트 (conftest.py, smoke_test.py, run.py)
│   └── web/                     # [Web] 웹 E2E 테스트
│       ├── playwright/          # [메인 E2E] Playwright 프레임워크
│       │   ├── testcase/        # 기준 회귀 테스트 스위트 (01~16번)
│       │   ├── testcase_ai/     # 기획 스펙 기반 확장 검증 스위트 (01~21번)
│       │   ├── self_healing/    # Locator 자가 치유 파이프라인
│       │   ├── conftest.py      # 멀티 롤 브라우저 Fixture 및 훅
│       │   ├── report_manager.py# Allure / Trace / HTML 리포트 관리 모듈
│       │   └── run.py           # 실행 Entry Point
│       │
│       └── robotframework/      # [Legacy] 로봇프레임워크 아카이브
│
├── common/                      # 공통 모듈 (Auth 템플릿, Admin API, Gmail OTP, GSheet 연동)
│   ├── auth/                    # .env.example, credentials.sample.json
│   └── resources/               # admin_api.py, email_reader.py, testfile/
│
├── TestResult/                  # 타임스탬프 기반 테스트 결과 및 리포트/Trace 아카이브
└── .gitignore                   # 인증 정보 및 테스트 부산물 전역 격리
```

---

## 4. 환경 설정 및 실행 방법 (Quick Start)

### 1) 환경 구성 및 의존성 설치
```bash
# 가상환경 생성 및 활성화
python -m venv .venv
./.venv/Scripts/Activate.ps1

# 패키지 및 브라우저 드라이버 설치
pip install -r requirements.txt
playwright install chromium
```

### 2) 환경 변수 설정
```bash
# 샘플 템플릿 복사 후 대상 서버 및 테스트 계정 정보 기입
cp common/auth/.env.example common/auth/.env
cp common/auth/credentials.sample.json common/auth/credentials.json
```

### 3) 테스트 실행
```bash
# [A] 웹 전체 회귀 테스트 실행 (Headed 모드 + 3-in-1 리포트 자동 생성)
python automation/web/playwright/run.py

# [B] 특정 도메인 단독 실행 (예: 프로필)
python automation/web/playwright/run.py automation/web/playwright/testcase_ai/test_02_profile_ai.py

# [C] 모바일 하이브리드 앱 스모크 테스트 실행
python automation/app/run.py
```

---

## 5. 도메인별 검증 범위 (Test Coverage)

| No. | 스위트 명 | 검증 범위 및 세부 비즈니스 시나리오 |
| :---: | :--- | :--- |
| **01** | **회원가입** | 사업자등록번호 유효성 검증 ➔ Gmail OTP 수신 ➔ 가입 신청 ➔ Admin API 자동 승인 |
| **02** | **프로필 관리** | 비밀번호 유효성/예외, 계정 정보 수정, 서브계정 라이프사이클(등록/모달/삭제), 도장 및 수료증 등록 |
| **03** | **회원업체 관리** | CSO 업체 검색, 사업자번호 수정, 목록 필터링 및 업체 상태 변경 검증 |
| **04** | **상위업체 조회** | 상위 제약사 목록 조회, 상세 거래 조건 및 매핑 상태 검증 |
| **05** | **계약서 관리** | 전자계약서 작성, 위탁 제품 다중 추가, 계약서 전송 및 우측 상세 Drawer 검증 |
| **06** | **받은 계약서** | 수신 계약서 뷰어 검토, 전자 서명 날인 및 반려/승인 처리 플로우 |
| **07** | **재위탁 통보서** | 병/의원 대상 재위탁 통보서 생성, 품목 매핑 및 거래처 전송 |
| **08** | **받은 재위탁 통보서** | 수신된 재위탁 통보서 상세 내역 확인, 검토 및 수락 처리 |
| **09** | **재위탁 현황** | 거래처별 재위탁 진행 상태 실시간 집계 및 모니터링 |
| **10** | **이전 통보서 관리** | 과거 통보서 이력 조회, PDF 다운로드 및 이력 추적 |
| **11** | **필터링 직접 조회** | 거래처/의약품 필터링 조건 입력 및 실시간 유효성 체크 |
| **12** | **필터링 조회 관리** | 필터링 이력 데이터 테이블 관리, 상태 필터링 및 엑셀 다운로드 |
| **13** | **필터링 요청** | 신규 거래처 필터링 요청 등록, 수정 및 요청 취소 라이프사이클 |
| **14** | **필터링 회신 관리** | 제약사 수신 상세 조회, 임시 승인 선택 및 필수 회신서 작성 |
| **15** | **영업 거래처 관리** | 관리코드 수정, 제품별 승인 상태 변경 및 비고 메모 동기화 |
| **16** | **자료실** | 신규 개원정보 지역/진료과 드롭다운 필터링 및 첨부파일 열람 |
| **18+** | **실적 / 정산 관리** | EDI 업로드 및 취합, 실적 입력 검증 및 정산 관리 라이프사이클 (`testcase_ai`) |