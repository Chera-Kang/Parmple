# Parmple QA Test Automation & E2E Engineering Rules

이 규칙은 팜플(Parmple) 프로젝트의 모든 E2E 자동화 테스트 케이스(Playwright, Appium) 작성 및 유지보수 시 AI와 엔지니어가 반드시 준수해야 하는 최상위 품질 거버넌스 헌장입니다.

---

## 1. Zero False-Positive (가짜 통과 원천 금지) 원칙
1. **상태 변화 단언(State Mutation Assertion) 필수**:
   - 모든 사용자 인터랙션(버튼 클릭, 탭 전환, 모달 열기, 폼 제출 등) 뒤에는 반드시 화면에 일어난 **실질적인 UI/DOM 변화(헤더 변경, 텍스트 노출, URL 변경 등)**를 `expect().to_be_visible()` 또는 `assert`로 1:1 강제 검증해야 한다.
   - 단순 클릭 후 단언문 없이 다음 단계로 넘어가거나 `print()`만 찍는 코드는 절대 금지한다.
2. **무음 통과(Silent Pass) 배제**:
   - `if element.count() > 0:`로 감싸서 화면에 요소가 없는데도 조용히 통과시키는 방어적 코드를 작성하지 않는다.
   - 요소가 반드시 있어야 하는 경우: `expect().to_be_visible()`로 없으면 즉시 **FAIL**을 낸다.
   - 계정의 사전 데이터가 부족하여 검증이 불가능한 경우: `pytest.skip("데이터 부족 사유")`로 **SKIP** 처리하여 리포트에 정직하게 남긴다.

---

## 2. Parmple UI 컴포넌트 셀렉터 표준 가이드
1. **그리드 (AG Grid / 가상화 테이블)**:
   - 일반 HTML `<table>` 태그가 아니므로 `//table` 대신 AG Grid 가시성 셀렉터를 사용한다.
   - 헤더 전체선택 체크박스: `dialog.locator("input[type='checkbox']:visible").first`
   - 행 체크박스: `dialog.locator(".ag-row:visible input[type='checkbox']")`
   - 페이지네이션 이동: `dialog.locator("button[@title='다음' or @aria-label='다음']")`
2. **탭 (Tabs)**:
   - `button:has-text('전송 완료')`와 같이 정확한 버튼을 타겟팅하고, 탭 전환 후 나타나는 고유 헤더/컨텐츠를 단언한다.
3. **모달 / 다이얼로그 (Radix UI)**:
   - `page.locator("div[role='dialog']")` 내부에서만 요소를 검색하여 백그라운드 요소 오클릭을 방지한다.

---

## 3. 통합 사용자 여정 (User Journey) 및 Trace Grouping
- 복잡한 다단계 E2E 시나리오(예: 가입 ➡️ 계약서 작성 ➡️ 통보서 수신 ➡️ 정산) 작성 시:
  - `context.tracing.group("스텝명")`과 `context.tracing.group_end()`를 활용하여 Playwright Trace Viewer에서 각 단계별 스냅샷을 접고 펼칠 수 있는 그룹 트리 구조로 구성한다.

---

## 4. 리포트 및 산출물 표준
- 모든 테스트는 3-in-1 리포트(`report.html`, `allure_report/index.html`, `열기_PlaywrightTrace.bat`)와 완벽히 호환되어야 하며, 배치 메뉴에는 순수 `def` 함수명이 노출되어야 한다.

---

## 5. Self-Healing 파이프라인 연계
- 런타임에 UI 변경으로 인한 셀렉터 실패나 타임아웃 발생 시, `automation/web/playwright/self_healing` 모듈이 작동하여 `error_artifacts`에 스크린샷과 DOM 스니펫을 수집하고 대체 Locator를 제안/치유할 수 있는 구조를 유지한다.
- TC 설계 문서인 [qa_tc_creation.md](file:///c:/Dev/Parmple/.agents/rules/qa_tc_creation.md)에 명시된 구체적인 UI 텍스트와 단언 기준을 기반으로 복구 가능성을 극대화한다.

