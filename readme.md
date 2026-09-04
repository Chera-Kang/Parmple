# Parmple E2E Test Automation Framework
> Web & Hybrid App E2E Test Automation

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.62-2EAD33?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Appium](https://img.shields.io/badge/Appium-v2.15-662D91?style=flat-square&logo=appium&logoColor=white)](https://appium.io/)
[![Pytest](https://img.shields.io/badge/Pytest-9.1-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Allure Report](https://img.shields.io/badge/Allure-Report-FF7800?style=flat-square&logo=qameta&logoColor=white)](https://allurereport.org/)

B2B 제약 영업대행(CSO) 및 위탁 계약 관리 플랫폼의 품질 검증을 위해 구축한 E2E 테스트 자동화 프로젝트입니다.  
기존 Robot Framework와 Selenium으로 작성되었던 테스트 환경을 Playwright 및 Appium 환경으로 전환하여 실행 속도와 안정성을 개선하고, AI를 활용한 점진적 테스트 케이스 생성과 결과 리포팅 파이프라인을 구축했습니다.

---

## 1. 주요 시연 영상
> 실제 동작 과정을 녹화한 시연 영상입니다.

- **[Web] Playwright + Pytest 마이그레이션 회귀 테스트 시연 (2026.09)**  
  [▶️ YouTube 바로보기](https://youtu.be/t7XDqr4cbYw)  
  *Robot Framework에서 전환된 16개 핵심 업무 도메인 회귀 테스트 일괄 구동*

- **[Web] AI 활용 3단계 TC 자동 설계 및 18개 E2E 테스트 검증 (2026.09)**  
  [▶️ YouTube 바로보기](https://youtu.be/mywifH10t74)  
  *화면 기반 3단계(스모크 ➔ 유효성 ➔ 비즈니스 CRUD) 점진적 생성 및 18개 테스트 통과 검증*

- **[App] Android 하이브리드 앱 Appium 스모크 테스트 시연 (2026.09)**  
  [▶️ YouTube 바로보기](https://youtu.be/AGG6c-pH-6g)  
  *Appium 서버 자동 구동 및 앱 로그인 후 주요 GNB 메뉴 진입 확인*

- **과거 마일스톤 시연 영상**:  
  [Design System 적용 버전 (25.10.27)](https://youtu.be/e3fbpIVPqks) | [Renewal 버전 (25.08.06)](https://youtu.be/KU7lC9yqJbI) | [초기 버전 (25.04.15)](https://youtu.be/5YyteNw1Jz4) | [결과 리포트 샘플 (.zip)](https://drive.google.com/drive/folders/1f9foK6b4ZrYw6ugmbNNy25gB79n0HGNt)

---

## 2. 주요 설계 내용

### 1) 계정별 로그인 Fixture를 통한 세션 격리
- CSO(영업대행), 제약사, 관리자 등 여러 권한이 나뉘어 있는 B2B 플랫폼 구조에 맞춰, Pytest Fixture(`conftest.py`)로 역할별 로그인 세션을 분리했습니다.
- 각 테스트가 서로의 로그인 상태에 영향을 주지 않고 독립적으로 동작하도록 구성했습니다.

### 2) 상태 변화 단언 원칙 (Zero False-Positive)
- 단순 클릭이나 화면 이동 후 검증 없이 넘어가는 무음 통과(Silent Pass)를 방지했습니다.
- 모든 인터랙션 뒤에는 텍스트 노출, URL 변경, 요소 가시성 등 실제 화면에 일어난 상태 변화를 1:1로 검증하도록 테스트 규칙(`.agents/rules/qa_automation.md`)을 두었습니다.

### 3) AI를 활용한 점진적 3단계 TC 생성 전략
기획서가 충분하지 않은 상황에서도 안정적인 커버리지를 확보하기 위해 3단계 확장 방식을 적용했습니다:
- **Phase 1 (코어 스모크)**: 화면 진입, 기본 메뉴 및 주요 버튼 노출 등 필수 안전망 구축
- **Phase 2 (세부 유효성 검증)**: 각 입력 필드별 필수값 누락 방어, 경계값 및 비정상 입력 검증
- **Phase 3 (비즈니스 CRUD)**: 실제 데이터 등록, 확인 모달 처리, 목록 반영 및 삭제까지의 전체 흐름 검증
- **Self-Healing 보정**: UI 변경으로 셀렉터 실패 시, 에러 시점의 화면과 로그를 기반으로 대체 로케이터를 제안받아 유지보수할 수 있는 파이프라인 구성

### 4) 서버 주소 및 계정 정보 분리 (`.env`)
- `BASE_URL`, `ADMIN_URL` 등 접속 주소를 환경변수로 분리하여 대상 서버 변경이 용이하도록 구성했습니다.
- 실제 인증키나 계정 정보는 Git 추적에서 제외하고, `.env.example` 및 `credentials.sample.json` 샘플 파일을 제공하여 보안을 유지했습니다.

### 5) 3단계 결과 리포트 생성
테스트 실행(`run.py`) 1회로 다음 리포트들이 날짜별 폴더에 자동 생성됩니다:
- **Pytest HTML**: 실패 시 전체 화면 스크린샷이 첨부되는 단일 요약 파일
- **Allure Dashboard**: 테스트 성공률, 카테고리별 통계 및 실패 원인을 시각화한 대시보드
- **Playwright Trace Viewer**: 마우스 이동 궤적, 전/후 DOM 상태, 네트워크 요청을 확인하는 디버깅 도구

---

## 3. 폴더 구조

```
Parmple\
├── .agents/rules/               # AI 테스트 작성 규칙 (단언문 원칙, 3단계 생성 가이드)
├── automation/                  # 테스트 코드 메인 폴더
│   ├── app/                     # [Appium] Android 모바일 앱 테스트 (smoke_test.py, run.py)
│   └── web/                     # [Web] 웹 E2E 테스트
│       ├── playwright/          # [Playwright]
│       │   ├── testcase/        # 기존 회귀 테스트 (01~16번, Robot Framework ➔ Playwright 전환)
│       │   ├── testcase_ai/     # AI로 생성한 테스트 (01~21번, 3-Phase 점진적 생성)
│       │   ├── self_healing/    # 셀렉터 자가 치유 파이프라인
│       │   ├── conftest.py      # 공통 브라우저 설정 및 계정별 로그인 Fixture
│       │   ├── report_manager.py# Report 관리 모듈 (Allure / Trace / HTML)
│       │   └── run.py           # 테스트 실행 파일
│       │
│       └── robotframework/      # [Legacy] 기존 로봇프레임워크 아카이브
│
├── common/                      # 공통 모듈 (.env.example, Admin API, 메일 OTP 파싱 등)
├── TestResult/                  # 날짜별 테스트 결과 및 리포트 저장 폴더
└── .gitignore                   # 인증 정보 및 테스트 결과 파일 차단
```

---

## 4. 테스트 실행 방법
> ※ 사내 보안 및 QA 서버 접근 권한이 필요한 환경이므로, 실제 동작 과정은 상단의 **시연 영상 및 결과 리포트 샘플**을 통해 확인하실 수 있습니다.

```bash
# 1. 가상환경 활성화 및 패키지 설치
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
playwright install chromium

# 2. 환경 변수 설정 (.env.example 참고)
cp common/auth/.env.example common/auth/.env

# 3. 테스트 실행
# [웹 전체 회귀 테스트 실행]
python automation/web/playwright/run.py

# [특정 테스트 단독 실행 (예: 프로필)]
python automation/web/playwright/run.py automation/web/playwright/testcase_ai/test_02_profile_ai.py

# [모바일 앱 테스트 실행]
python automation/app/run.py
```

---

## 5. 도메인별 검증 범위

| No. | 테스트 영역 | 주요 검증 내용 |
| :---: | :--- | :--- |
| **01** | **회원가입** | 사업자번호 유효성 체크 ➔ 메일 OTP 수신 ➔ 가입 신청 ➔ Admin API 자동 승인 |
| **02** | **프로필 관리** | 비밀번호 변경/검증, 계정 정보 수정, 서브 계정 등록 및 삭제, 도장/수료증 등록 |
| **03** | **회원업체 관리** | CSO 업체 검색, 사업자번호 수정, 목록 필터링 및 업체 상태 변경 |
| **04** | **상위업체 조회** | 상위 제약사 목록 조회 및 거래 조건 매핑 상태 확인 |
| **05** | **계약서 관리** | 전자계약서 작성, 위탁 제품 추가, 계약서 전송 및 상세 정보 확인 |
| **06** | **받은 계약서** | 수신 계약서 내용 검토, 전자 서명 날인 및 승인/반려 처리 |
| **07** | **재위탁 통보서** | 병/의원 대상 재위탁 통보서 작성 및 거래처 전송 |
| **08** | **받은 재위탁 통보서** | 수신된 통보서 상세 확인 및 검토 처리 |
| **09** | **재위탁 현황** | 거래처별 재위탁 진행 상태 모니터링 |
| **10** | **이전 통보서 관리** | 과거 통보서 내역 조회 및 PDF 다운로드 확인 |
| **11** | **필터링 직접 조회** | 거래처/의약품 필터링 조건 입력 및 유효성 체크 |
| **12** | **필터링 조회 관리** | 필터링 이력 테이블 조회 및 엑셀 다운로드 |
| **13** | **필터링 요청** | 신규 거래처 필터링 요청 등록, 수정 및 취소 처리 |
| **14** | **필터링 회신 관리** | 제약사 수신 내역 확인 및 회신서 작성 |
| **15** | **영업 거래처 관리** | 관리코드 수정, 제품별 승인 상태 변경 및 메모 저장 |
| **16** | **자료실** | 신규 개원정보 지역/진료과 드롭다운 필터링 및 첨부파일 확인 |
| **18+** | **실적 및 정산 관리** | EDI 파일 업로드, 실적 입력 검증 및 정산 라이프사이클 (`testcase_ai`) |