# 🏥 Parmple E2E Test Automation Framework
> **Web & Hybrid App Cross-Platform QA Automation Architecture**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.62-2EAD33?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Appium](https://img.shields.io/badge/Appium-v2.15-662D91?style=flat-square&logo=appium&logoColor=white)](https://appium.io/)
[![Pytest](https://img.shields.io/badge/Pytest-9.1-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Allure Report](https://img.shields.io/badge/Allure-Report-FF7800?style=flat-square&logo=qameta&logoColor=white)](https://allurereport.org/)
[![Google Gemini](https://img.shields.io/badge/Gemini-Self--Healing-8E75C2?style=flat-square&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)

제약 CSO 및 영업 관리 SaaS 플랫폼 **팜플(Parmple)**의 전사 비즈니스 로직을 검증하는 **풀스택 E2E 테스트 자동화 및 AI 자가 치유(Self-Healing) 시스템**입니다.  
과거 Selenium/Robot Framework 기반 레거시를 **Playwright & Appium** 기반 모던 아키텍처로 전면 마이그레이션하여 테스트 신뢰도와 실행 속도를 대폭 개선했습니다.

---

## 📌 Key Architectural Features

### 1. 🌐 Cross-Platform E2E Coverage (Web & Mobile)
- **Web E2E (Playwright)**:
  - 브라우저 컨텍스트 격리 및 자동 대기(Auto-waiting) 메커니즘을 적용한 16개 핵심 도메인 회귀 테스트
  - Headless CI 모드 및 실시간 육안 검증을 위한 Headed Slow-Mo(0.5s) 모드 지원
- **Mobile Hybrid App (Appium & UiAutomator2)**:
  - Android 하이브리드 앱 GNB 메뉴 및 핵심 사용자 플로우 자동화
  - 자동 권한 허용(`auto_grant_permissions`) 및 Appium 포트 헬스체크 프로세스 내장

### 2. ⚡ Full-Stack Data & Admin API Pipeline
- **실시간 유효 데이터 풀 (Google Sheets API)**:
  - 회원가입 및 거래처 등록에 필요한 사업자등록번호를 구글 시트에서 실시간 할당받고 중복 등록을 원천 차단
- **메일 인증 자동화 (Gmail OAuth API)**:
  - 가입 및 본인 인증 시 발송되는 이메일 본문의 OTP 인증 링크/토큰을 파이썬 백그라운드에서 실시간 파싱
- **백엔드 어드민 동기화 (Admin REST API)**:
  - 테스트 가입 완료 업체를 관리자 API(`qa.api.parmple.com`)를 통해 즉시 자동 승인하여 후속 E2E 시나리오 연속성 보장

### 3. 🤖 AI-Driven Self-Healing & Zero-Base QA
- **Gemini LLM 자가 치유 (Self-Healing)**:
  - UI 렌더링 변경으로 인한 Selector 실패 발생 시, 장애 시점의 DOM 트리와 에러 로그를 LLM이 실시간 분석하여 대체 선택자 추천 및 복구 파이프라인 제공
- **피그마(Figma) 기반 제로베이스 TC 설계**:
  - 신규 피그마 기획/디자인 시안을 바탕으로 정상 경로(Happy Path)뿐만 아니라 유효성 검사, 경계값, 예외 처리(Negative)를 망라한 구조화된 TC 매트릭스 도출 및 자동화 스크립트 작성

### 4. 📊 Multi-Tier 3-in-1 Reporting Engine
단 1회의 테스트 구동으로 목적에 맞는 3가지 표준 리포트를 타임스탬프 디렉토리에 동시 번들링:
- **Pytest HTML Report**: 단일 HTML 파일로 공유 가능한 경량 요약 리포트
- **Allure Single-file Dashboard**: 성공률 파이 차트, 스위트별 통계, 실패 스텝 로그를 시각화한 인터랙티브 대시보드
- **Playwright Trace Viewer**: 마우스 이동 궤적, 클릭 전/후 DOM 스냅샷, 네트워크 트래픽을 프레임 단위로 재생하는 디버깅 도구

---

## 📁 Directory Structure

```
c:\Dev\Parmple\
├── automation/                  # 🌟 자동화 메인 프레임워크
│   ├── app/                     # 📱 [Appium] 모바일 하이브리드 앱 테스트
│   │   ├── testcase/            # conftest.py, smoke_test.py
│   │   └── run.py               # 앱 테스트 실행 스크립트
│   │
│   └── web/                     # 🌐 [Web] 웹 E2E 테스트
│       ├── playwright/          # 🌟 [메인 E2E] Playwright 최신 프레임워크
│       │   ├── testcase/        # 기준 회귀 테스트 스위트 (01~16번)
│       │   ├── testcase_ai/     # 🤖 AI 제로베이스 & 신규 피그마 검증 스위트
│       │   ├── self_healing/    # Gemini LLM 기반 자가 치유 파이프라인
│       │   ├── conftest.py      # 브라우저 Fixture 및 공통 설정
│       │   ├── report_manager.py# Allure / Trace / HTML 리포트 관리자
│       │   └── run.py           # 실행 Entry Point (모듈식 리포트 On/Off)
│       │
│       └── robotframework/      # 📦 [Legacy] 로봇프레임워크 아카이브
│           ├── 1. Web (before Renewal)/
│           ├── 2. Web (before Design)/
│           ├── 3. Web (latest robot)/
│           ├── keywords.robot
│           ├── keywords_legacy.robot
│           └── run.py
│
├── common/                      # 🛠️ 공통 연동 모듈 (Auth/.env, GSheet, Admin API, Gmail)
├── TestResult/                  # 📈 테스트 결과 및 리포트/Trace 통합 아카이브
└── .gitignore                   # 인증 정보 및 테스트 부산물 격리
```

---

## 🧪 Test Suite & Domain Coverage

| No. | 스위트 명 | 검증 범위 및 세부 시나리오 |
| :---: | :--- | :--- |
| **01** | **회원가입** | 구글 시트 사업자번호 발급 ➡️ Gmail OTP 수신 ➡️ 가입 ➡️ Admin API 실시간 승인 |
| **02** | **프로필 관리** | 비밀번호 유효성/예외, 계정 정보 수정, 서브계정 관리, 도장/수료증 등록 라이프사이클 |
| **03** | **회원업체 관리** | CSO 업체 검색, 사업자번호 수정, 목록 다이나믹 필터링 및 상태 변경 |
| **04** | **상위업체 조회** | 상위 제약사 목록 조회, 상세 거래 조건 및 매핑 상태 검증 |
| **05** | **계약서 관리** | 전자계약 작성, 위탁 제품 다중 추가(피그마 신규), 전송 및 우측 상세 Drawer 검증 |
| **06** | **받은 계약서** | 수신 계약서 뷰어 검토, 전자 서명 날인 및 반려/승인 처리 플로우 |
| **07** | **재위탁 통보서** | 병/의원 대상 재위탁 통보서 생성, 품목 매핑 및 거래처 전송 |
| **08** | **받은 재위탁 통보서** | 수신된 재위탁 통보서 상세 내역 확인, 검토 및 수락 처리 |
| **09** | **재위탁 현황** | 거래처별 재위탁 진행 상태 실시간 집계 및 모니터링 |
| **10** | **이전 통보서 관리** | 과거 통보서 이력 조회, PDF 다운로드 및 이력 추적 |
| **11** | **필터링 직접 조회** | 거래처/의약품 필터링 조건 입력 및 실시간 유효성 체크 |
| **12** | **필터링 조회 관리** | 필터링 이력 데이터 테이블 관리, 상태 필터링 및 엑셀 다운로드 |
| **13** | **필터링 요청** | 신규 거래처 필터링 요청 등록, 수정 및 요청 취소 라이프사이클 |
| **14** | **필터링 회신 관리** | 제약사 수신 상세 조회, 임시 승인 라디오 선택 및 필수 회신서 작성 |
| **15** | **영업 거래처 관리** | 관리코드 수정, 제품별 승인 상태 변경 및 비고 메모 동기화 |
| **16** | **자료실** | 신규 개원정보 지역/진료과 실시간 드롭다운 필터링 및 첨부파일 열람 |

---

## 🚀 Execution & Report Inspection

### 1. Web E2E 테스트 실행
```powershell
# 기본 전체 회귀 테스트 실행
python automation/web/playwright/run.py

# AI 제로베이스 & 특정 테스트 케이스 단독 실행
python automation/web/playwright/run.py automation/web/playwright/testcase_ai/test_05_계약서관리_ai.py
```

### 2. Mobile App 테스트 실행
```powershell
python automation/app/run.py
```

### 3. 결과 리포트 열람 (더블클릭 실행)
테스트 완료 후 생성된 `TestResult/YY-MM-DD_HH-MM/` 디렉터리 내에서 바로 확인 가능합니다:
- 📄 `report.html` : Pytest HTML 요약 리포트 (더블클릭)
- 📊 `allure_report/index.html` : Allure 대시보드 리포트 (더블클릭)
- 🎬 `열기_PlaywrightTrace.bat` : 대화형 Playwright Trace Viewer 선택기 (더블클릭)

---

## 🎥 Video Demos & History Archive

- 🎬 **Design System 적용 E2E 시연 영상 (25.10.27)**: [▶️ Youtube 바로보기](https://youtu.be/e3fbpIVPqks)
- 🎬 **Renewal 버전 E2E 시연 영상 (25.08.06)**: [▶️ Youtube 바로보기](https://youtu.be/KU7lC9yqJbI)
- 🎬 **초기 버전 시연 영상 (25.04.15)**: [▶️ Youtube 바로보기](https://youtu.be/5YyteNw1Jz4)
- 🗂️ **테스트 결과 샘플 (.zip)**: [🔗 Google Drive 다운로드](https://drive.google.com/drive/folders/1f9foK6b4ZrYw6ugmbNNy25gB79n0HGNt)