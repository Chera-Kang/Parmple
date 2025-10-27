# 자동화 테스트
제약회사 영업 관리 서비스 **팜플(Parmple)**의 자동화 테스트 스크립트 저장소

## 구성
> 자동화 테스트 구성 요약
- 📂 [Testcase](./Testcase)
  - 서비스 주요 기능별 자동화 **테스트 케이스**
- 📂 [resources](./resources)
  - 자동화 테스트에 필요한 리소스 및 환경 설정
- 📂 [Legacy](./Legacy)
  - 과거 버전 자동화 테스트 레거시 코드 및 기록용 스크립트
- 🗒️ [run.py](./run.py)
  - 자동화 테스트 **실행 스크립트**

---

## 테스트 결과
### 🎥 테스트 동영상 (Youtube)
> 각 버전별 테스트 시연 영상  
> *(테스트 자동화 진행 시점과 적용 버전에 따라 내용이 다를 수 있습니다.)*

- 자동화 테스트 동영상 **(25.10.27)** | *Design Sysyem 적용* | [▶️ 바로보기](https://youtu.be/e3fbpIVPqks)
- 자동화 테스트 동영상 **(25.08.06)** | *Renewal 적용* | [▶️ 바로보기](https://youtu.be/KU7lC9yqJbI)
- 자동화 테스트 동영상 **(25.04.15)** | *기존 버전* | [▶️ 바로보기](https://youtu.be/5YyteNw1Jz4)

| 날짜 | 내용 | 링크 |
|:--|:--|:--:|
| **25.10.27** | *Design System 적용* | [▶️ 바로보기](https://youtu.be/e3fbpIVPqks) |
| **25.08.06** | *Renewal 적용* | [▶️ 바로보기](https://youtu.be/KU7lC9yqJbI) |
| **25.04.15** | *기존 버전* | [▶️ 바로보기](https://youtu.be/5YyteNw1Jz4) |


## 테스트 결과 다운로드 (샘플)
> 테스트 결과 샘플파일 다운로드 및 구성 요소 요약

#### **Google Drive**
- [🔗 Test Result (.zip)](https://drive.google.com/drive/folders/1DHx_hG_0kR07e8FNK_DZIVcNYrUpTyi0)

#### 📦 ZIP 파일 구성
- 📁 `screenshots/`  
  - 테스트 실행 중 촬영된 주요 화면 스크린샷 모음
- 📄 `output.xml`  
  - Robot Framework 실행 결과를 XML 형식으로 저장한 원본 로그 파일
- 📄 `log.html`  
  - 테스트 상세 실행 과정을 확인할 수 있는 HTML 로그 (각 단계별 상태 및 메시지를 포함)
- 📄 **`report.html`**  
  - **테스트 요약 리포트**로, **전체 테스트 결과**(성공/실패 케이스 등) 확인 가능