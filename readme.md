
# 자동화 테스트
Web 및 App 환경에서 수행 중인 자동화 테스트 스크립트를 정리한 저장소입니다.

## 구성
- 📂 [Web](./Web)  
  - Selenium 기반, Web 서비스 테스트 스크립트 (제약영업관리 서비스 "팜플")  
- 📂 [App](./App)  
  - Appium 기반, *Sample* App 테스트 스크립트 (Wikipedia)

> 각 폴더에는 테스트 코드 및 실행 방법이 포함되어 있습니다.

---

## 테스트 결과
### 테스트 동영상
- **Youtube**
  - [Web 자동화 테스트 시연] (https://www.youtube.com/watch?v=5YyteNw1Jz4)
  - [App 자동화 테스트 시연] (https://www.youtube.com/watch?v=L-_c_SkEAjs)

### 샘플 다운로드
- **Google Drive**
  - [전체 실행 결과 및 스크린샷 다운로드 (ZIP)] (https://drive.google.com/drive/folders/1DHx_hG_0kR07e8FNK_DZIVcNYrUpTyi0)
#### 📦 ZIP 파일 구성
- 📁 `screenshots/`  
  - 테스트 실행 중 촬영된 주요 화면 스크린샷 모음입니다.
- 📄 `output.xml`  
  - Robot Framework 실행 결과를 XML 형식으로 저장한 원본 로그 파일입니다.
- 📄 `log.html`  
  - 테스트 상세 실행 과정을 확인할 수 있는 HTML 로그입니다. 각 단계별 상태 및 메시지를 포함합니다.
- 📄 **`report.html`**  
  - **테스트 요약 리포트**로, **전체 테스트 결과**(성공/실패 케이스 등)를 한눈에 파악할 수 있습니다.