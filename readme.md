# Parmple 자동화 테스트
> **Web & App Automation Testing** | `Playwright` & `Appium` (with `Robot Framework` Legacy)

제약회사 영업 관리 서비스 **팜플(Parmple)** 의 Web & App E2E 자동화 테스트 스크립트

---

## 구성
> 자동화 테스트 구성 요약
- 📂 [Playwright (Web)](./automation/web/playwright)
  - Playwright 기반 웹 서비스 주요 기능별 자동화 **테스트 케이스** 및 실행 스크립트
- 📂 [Appium (App)](./automation/app)
  - Appium 기반 하이브리드 앱 GNB 및 주요 시나리오 자동화 **테스트 케이스**
- 📂 [common](./common)
  - 자동화 테스트에 필요한 공통 리소스 (계정 설정, Google 시트 연동, Admin API 등)
- 📂 [Robot Framework (Legacy)](./automation/web/robotframework)
  - 과거 버전 Robot Framework 자동화 테스트 레거시 코드 및 기록용 스크립트

---

## 테스트 결과
### 🎥 테스트 동영상 (Youtube)
> 각 버전별 테스트 시연 영상  
> *(테스트 자동화 진행 시점과 적용 버전에 따라 내용이 다를 수 있습니다.)*

- 자동화 테스트 동영상 **(25.10.27)** | *Design System 적용* | [▶️ 바로보기](https://youtu.be/e3fbpIVPqks)
- 자동화 테스트 동영상 **(25.08.06)** | *Renewal 적용* | [▶️ 바로보기](https://youtu.be/KU7lC9yqJbI)
- 자동화 테스트 동영상 **(25.04.15)** | *기존 버전* | [▶️ 바로보기](https://youtu.be/5YyteNw1Jz4)

## 테스트 결과 리포트 (Sample)
> 테스트 실행 후 생성되는 결과 리포트 요약

#### 🗂️ **Google Drive**
- [🔗 Test Result (.zip)](https://drive.google.com/drive/folders/1f9foK6b4ZrYw6ugmbNNy25gB79n0HGNt)

#### 📦 결과 파일 구성
- 📄 **`report.html`**  
  - Pytest 기반 **테스트 요약 리포트** (전체 성공/실패 케이스 및 실행 시간 확인)
- 📊 **`allure_report/`**  
  - Allure 기반 **인터랙티브 대시보드 리포트** (원형 차트 및 스텝별 상세 내역)
- 🎬 **`traces/`**  
  - Playwright Trace Viewer 파일 모음 (마우스 액션, DOM 스냅샷, 네트워크 타임라인 재생)
- 📁 **`screenshots/`**  
  - 테스트 실패 시 자동 캡처된 오류 화면 스크린샷

---

## Tech Stack
> 프로젝트에 사용된 주요 기술 및 도구
- **Language**: `Python`
- **Web Automation**: `Playwright` + `Pytest`
- **App Automation**: `Appium` (UiAutomator2)
- **Reporting**: `Allure Report` & `pytest-html`
- **Legacy Framework**: `Robot Framework` + `Selenium Library`

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![Appium](https://img.shields.io/badge/Appium-662D91?style=flat-square&logo=appium&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![Allure Report](https://img.shields.io/badge/Allure%20Report-FF7800?style=flat-square&logo=qameta&logoColor=white)
![Robot Framework](https://img.shields.io/badge/Robot%20Framework-000000?style=flat-square&logo=robotframework&logoColor=white)