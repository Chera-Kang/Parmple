
# Wikipedia(위키백과) - App 자동화 테스트  
## 기본 기능 검증을 위한 자동화 테스트  
- 사용 기술
  - **Robot Framework + Appium**
- 주요 테스트 대상:  
  - 탐색  
  - 위키 저장  
  - 검색  
  - 기타 
- 실행 시간 : 약 **5** 분 소요  

## 실행 방법
### 사전설정 (이후 Skip 가능)
1. 기본 설정
  - ADB 설정
  - Appium 설정
  - Wikipedia 다운로드 후 구동 확인
2. Device 설정
  - Android Device 개발자 옵션 활성화
  - 개발자 옵션 > USB 디버깅 활성화 
  - PC 와 Device USB 연결 
  - Device 에서 USB 디버깅 허용
3. 명령 프롬프트 실행 (CMD) > adb devices 입력하여 연결 확인
  - 모델 고유값 Device Name 노출
4. `App_Test.robot` 의 `Variables` 에 DeviceName 작성
  - 예시) ${DEVICE_NAME}    LGMV300S9da9bb03
### 테스트 설정
1. 명령프롬프트 실행 (CMD) > appium --base-path /wd/hub 입력하여 연결 확인
2. `App_test.robot` 실행

## 테스트 결과
- (작성 예정)
