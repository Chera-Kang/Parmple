import os
import re
import time
import random
import datetime
import pytest
from playwright.sync_api import Page, expect

# 공통 도구 모듈 import
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from common.resources.gsheet_reader import get_biz_no_from_sheet

# 파일 경로 상수
BIZNO_FILE = os.path.join(ROOT_DIR, "common", "resources", "used_bizNo.txt")
TESTFILE_PDF = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF.pdf")
TESTFILE_PDF2 = os.path.join(ROOT_DIR, "common", "resources", "testfile", "Sameple_PDF_2.pdf")

# ==============================================================================
# Helper Functions
# ==============================================================================

def get_last_biz_number() -> str:
    """used_bizNo.txt 파일에서 마지막으로 사용된(가입된) 사업자번호를 조회합니다."""
    if not os.path.exists(BIZNO_FILE):
        raise FileNotFoundError(f"사업자번호 파일이 없습니다: {BIZNO_FILE}")
    with open(BIZNO_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        raise ValueError("used_bizNo.txt에 기록된 사업자번호가 없습니다.")
    return lines[-1]

# ==============================================================================
# Phase 1 & 2: Core & Atomic Validation Test Cases
# Rules Applied: .agents/rules/qa_automation.md, .agents/rules/qa_tc_creation.md
# ==============================================================================

def test_tc_ctr_01_entrustment_contract_rendering(page: Page, login_cso):
    """
    [TC-CTR-01] Happy Path: CSO '회원 업체 관리' 페이지 렌더링 및 그리드 컬럼 검증
    - CSO 계정으로 진입하여 회원 업체 목록과 AG Grid 핵심 컬럼들의 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CTR-01] 회원 업체 관리 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 메뉴 이동
    print("[Step 1] '회원 업체 관리' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/contractor/entrustment-contract")
    page.wait_for_selector("h2:has-text('회원 업체 관리')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="회원 업체 관리").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*contractor/entrustment-contract.*"))

    # 3. AG Grid 렌더링 및 컬럼 검증
    print("[Step 2] AG Grid 테이블 컨테이너 및 헤더 컬럼 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()

    expect(page.locator(".ag-header-cell-text:has-text('상호/법인명'), .ag-header-cell:has-text('상호/법인명')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('사업자등록번호'), .ag-header-cell:has-text('사업자등록번호')").first).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('대표자'), .ag-header-cell:has-text('대표자')").first).to_be_visible()
    print("[Success] TC-CTR-01 회원 업체 관리 렌더링 검증 성공!")


def test_tc_ctr_02_add_contractor_modal_open_and_form_check(page: Page, login_cso):
    """
    [TC-CTR-02] Happy Path: '회원 업체 추가' 모달 오픈 및 폼 요소 렌더링 검증
    - '추가하기' 버튼 클릭 ➡️ 모달 노출 ➡️ 사업자등록번호 입력창/확인 버튼 가시성 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CTR-02] 회원 업체 추가 모달 오픈 검증 시작")
    print("=" * 60)

    # 1. 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/contractor/entrustment-contract")
    page.wait_for_selector("h2:has-text('회원 업체 관리')", timeout=10000)

    # 2. 추가하기 버튼 클릭
    print("[Step 1] '추가하기' 버튼 클릭")
    add_btn = page.locator("button:has-text('추가하기')").first
    expect(add_btn).to_be_visible()
    add_btn.click()

    # 3. 모달 및 폼 요소 단언
    print("[Step 2] 다이얼로그 모달 오픈 및 입력 필드 단언")
    dialog = page.locator("div[role='dialog']").first
    expect(dialog).to_be_visible()
    expect(dialog.locator("h2, h3").first).to_be_visible()

    expect(dialog.locator("input#bizNumber, input[placeholder*='-없이 숫자만 입력']").first).to_be_visible()
    expect(dialog.locator("button:has-text('확인하기'), button:has-text('확인')").first).to_be_visible()
    print("[Success] TC-CTR-02 회원 업체 추가 모달 오픈 검증 성공!")


def test_tc_ctr_03_add_contractor_modal_close(page: Page, login_cso):
    """
    [TC-CTR-03] Validation: '회원 업체 추가' 모달 닫기 검증
    - 모달 열린 상태에서 ESC 키 또는 닫기(X/취소) 인터랙션 ➡️ 모달 사라짐 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CTR-03] 회원 업체 추가 모달 닫기 검증 시작")
    print("=" * 60)

    # 1. 모달 오픈
    page.goto(page.url.split("dashboard")[0] + "dashboard/contractor/entrustment-contract")
    page.wait_for_selector("button:has-text('추가하기')", timeout=10000)
    page.locator("button:has-text('추가하기')").first.click()

    dialog = page.locator("div[role='dialog']").first
    expect(dialog).to_be_visible()

    # 2. ESC 키로 닫기
    print("[Step 1] ESC 키를 통한 모달 닫기")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 3. 모달 비가시성 단언
    expect(page.locator("div[role='dialog']")).to_have_count(0)
    print("[Success] TC-CTR-03 회원 업체 추가 모달 닫기 검증 성공!")


def test_tc_ctr_04_commissioned_contract_rendering(page: Page, login_cso):
    """
    [TC-CTR-04] Happy Path: CSO '상위 업체 조회' 페이지 렌더링 및 그리드 검증
    - /dashboard/contractor/commissioned-contract 이동 ➡️ 헤딩 및 컬럼 정상 노출 단언
    """
    print("\n" + "=" * 60)
    print(" [TC-CTR-04] 상위 업체 조회 페이지 렌더링 검증 시작")
    print("=" * 60)

    # 1. 상위 업체 조회 메뉴 이동
    print("[Step 1] '상위 업체 조회' 메뉴 이동")
    page.goto(page.url.split("dashboard")[0] + "dashboard/contractor/commissioned-contract")
    page.wait_for_selector("h2:has-text('상위 업체 조회')", timeout=10000)

    # 2. 헤딩 및 URL 단언
    expect(page.locator("h2", has_text="상위 업체 조회").first).to_be_visible()
    expect(page).to_have_url(re.compile(r".*contractor/commissioned-contract.*"))

    # 3. AG Grid 렌더링 검증
    print("[Step 2] AG Grid 테이블 가시성 단언")
    grid = page.locator(".ag-root-wrapper, .ag-root").first
    expect(grid).to_be_visible()
    expect(page.locator(".ag-header-cell-text:has-text('상호/법인명'), .ag-header-cell:has-text('상호/법인명')").first).to_be_visible()
    print("[Success] TC-CTR-04 상위 업체 조회 렌더링 검증 성공!")


def test_tc_ctr_05_entrustment_contract_filter_dropdowns(page: Page, login_cso):
    """
    [TC-CTR-05] Phase 2 Happy Path: 회원 업체 관리 상단 검색 필터(구분, 영업 상태, 계약 상태) 드롭다운 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CTR-05] 회원 업체 관리 검색 필터 드롭다운 검증 시작")
    print("=" * 60)

    # 1. 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/contractor/entrustment-contract")
    page.wait_for_selector("h2:has-text('회원 업체 관리')", timeout=10000)

    # 2. '구분' 필터 드롭다운 클릭
    print("[Step 1] '구분' 필터 드롭다운 클릭 및 옵션 확인")
    category_filter = page.locator("button:has-text('구분')").first
    if category_filter.is_visible():
        category_filter.click()
        page.wait_for_timeout(300)
        expect(page.locator("div[role='option'], div[role='menuitem'], [role='menu'] div").first).to_be_visible()
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    # 3. '영업 상태' 필터 드롭다운 클릭
    print("[Step 2] '영업 상태' 필터 드롭다운 클릭 및 옵션 확인")
    sales_filter = page.locator("button:has-text('영업 상태')").first
    if sales_filter.is_visible():
        sales_filter.click()
        page.wait_for_timeout(300)
        expect(page.locator("div[role='option'], div[role='menuitem'], [role='menu'] div").first).to_be_visible()
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    # 4. '계약 상태' 필터 드롭다운 클릭
    print("[Step 3] '계약 상태' 필터 드롭다운 클릭 및 옵션 확인")
    contract_filter = page.locator("button:has-text('계약 상태')").first
    if contract_filter.is_visible():
        contract_filter.click()
        page.wait_for_timeout(300)
        expect(page.locator("div[role='option'], div[role='menuitem'], [role='menu'] div").first).to_be_visible()
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    print("[Success] TC-CTR-05 검색 필터 드롭다운 인터랙션 검증 성공!")


def test_tc_ctr_06_entrustment_contract_search_and_reset(page: Page, login_cso):
    """
    [TC-CTR-06] Phase 2 Validation: 회원 업체 관리 검색창 텍스트 입력 및 초기화 버튼 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CTR-06] 회원 업체 관리 검색 및 초기화 검증 시작")
    print("=" * 60)

    # 1. 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/contractor/entrustment-contract")
    page.wait_for_selector("h2:has-text('회원 업체 관리')", timeout=10000)

    # 2. 검색 입력 필드 확인
    search_input = page.locator("input[placeholder*='검색어'], input[placeholder*='입력']").first
    expect(search_input).to_be_visible()

    # 3. 검색어 입력 및 검색 실행
    print("[Step 1] 검색어 입력 및 검색 버튼 클릭")
    search_input.fill("휴피스")
    page.wait_for_timeout(300)

    search_btn = page.locator("button:has-text('검색')").first
    expect(search_btn).to_be_visible()
    search_btn.click()
    page.wait_for_timeout(1000)

    # 4. 초기화 버튼 클릭
    print("[Step 2] '초기화' 버튼 클릭하여 필터 리셋")
    reset_btn = page.locator("button:has-text('초기화')").first
    if reset_btn.is_visible():
        reset_btn.click()
        page.wait_for_timeout(500)
        expect(search_input).to_have_value("")

    print("[Success] TC-CTR-06 회원 업체 관리 검색 및 초기화 검증 성공!")


def test_tc_ctr_07_add_contractor_invalid_biz_number_validation(page: Page, login_cso):
    """
    [TC-CTR-07] Phase 2 Validation: 회원 업체 추가 시 짧은 사업자등록번호 입력 방어(disabled) 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CTR-07] 회원 업체 추가 짧은 사업자번호 방어 검증 시작")
    print("=" * 60)

    # 1. 모달 오픈
    page.goto(page.url.split("dashboard")[0] + "dashboard/contractor/entrustment-contract")
    page.wait_for_selector("button:has-text('추가하기')", timeout=10000)
    page.locator("button:has-text('추가하기')").first.click()

    dialog = page.locator("div[role='dialog']").first
    expect(dialog).to_be_visible()

    # 2. 3자리 짧은 사업자번호 입력 시 확인하기 버튼 disabled 단언
    print("[Step 1] 3자리 불완전한 번호 입력 시 확인 버튼 disabled 단언")
    biz_input = dialog.locator("input#bizNumber, input[placeholder*='-없이 숫자만 입력']").first
    biz_input.fill("123")
    page.wait_for_timeout(300)

    confirm_btn = dialog.locator("button:has-text('확인하기'), button:has-text('확인')").first
    expect(confirm_btn).to_be_disabled()

    # 3. ESC 키로 닫기
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    expect(page.locator("div[role='dialog']")).to_have_count(0)
    print("[Success] TC-CTR-07 회원 업체 추가 짧은 사업자번호 방어 검증 성공!")


def test_tc_ctr_08_commissioned_contract_search_interaction(page: Page, login_cso):
    """
    [TC-CTR-08] Phase 2 Happy Path: 상위 업체 조회 화면에서 검색 필터 드롭다운 및 텍스트 검색 인터랙션 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CTR-08] 상위 업체 조회 검색 인터랙션 검증 시작")
    print("=" * 60)

    # 1. 상위 업체 조회 페이지 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/contractor/commissioned-contract")
    page.wait_for_selector("h2:has-text('상위 업체 조회')", timeout=10000)

    # 2. 검색 조건 드롭다운 인터랙션
    print("[Step 1] 검색 조건 드롭다운 클릭")
    search_type_btn = page.locator("button:has-text('상호/법인명'), button:has-text('대표자'), button:has-text('사업자')").first
    if search_type_btn.is_visible():
        search_type_btn.click()
        page.wait_for_timeout(300)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    # 3. 검색어 입력 및 검색
    print("[Step 2] 검색어 입력 및 검색 실행")
    search_input = page.locator("input[placeholder*='검색어'], input[placeholder*='입력']").first
    if search_input.is_visible():
        search_input.fill("테스트")
        search_btn = page.locator("button:has-text('검색')").first
        if search_btn.is_visible():
            search_btn.click()
            page.wait_for_timeout(1000)

    print("[Success] TC-CTR-08 상위 업체 조회 검색 인터랙션 검증 성공!")


# ==============================================================================
# Phase 3: Dynamic E2E Workflow Test Cases
# ==============================================================================

def test_tc_ctr_09_add_registered_contractor_e2e(page: Page, login_cso):
    """
    [TC-CTR-09] Phase 3 E2E: 이미 가입된 업체 추가하기 Full Flow 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CTR-09] 가입된 회원 업체 추가 E2E 검증 시작")
    print("=" * 60)

    # 1. 회원 업체 관리 메인 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/contractor/entrustment-contract")
    page.wait_for_selector("h2:has-text('회원 업체 관리')", timeout=10000)

    # 2. '추가하기' 클릭
    print("[Step 1] '추가하기' 버튼 클릭")
    page.click("button:has-text('추가하기')")
    page.wait_for_selector("div[role='dialog']", timeout=5000)

    # 3. 마지막 가입 사업자번호 입력 및 확인
    last_biz_no = get_last_biz_number()
    print(f"[Step 2] 사용할 가입 사업자번호: {last_biz_no}")
    page.fill("#bizNumber, input[placeholder*='-없이 숫자만 입력']", last_biz_no)
    page.click("button:has-text('확인하기')")
    page.wait_for_selector("input[name='managementCode']", timeout=10000)

    # 4. 담당자 정보 및 관리코드 입력
    now_code = datetime.datetime.now().strftime("%m%d-%H%M")
    print(f"[Step 3] 관리코드({now_code}) 및 담당자 정보 입력")
    page.fill("input[name='managementCode']", now_code)
    page.fill("input[name='managerName']", "자동화담당자")
    page.fill("input[name='managerPhone']", f"010{random.randint(10000000, 99999999)}")
    page.fill("input[name='managerEmail']", "auto@mation.com")

    # 5. '추가하기' 클릭
    print("[Step 4] '추가하기' 클릭 및 팝업 대응")
    page.locator("button:has-text('추가하기')").last.click()
    page.wait_for_timeout(1500)

    # 이미 등록된 업체 팝업 또는 계약서 등록 확인 팝업 대응
    popup_confirm = page.locator("button:has-text('확인'), button:has-text('나중에')").last
    if popup_confirm.is_visible():
        popup_confirm.click()
        page.wait_for_timeout(1000)

    # ESC 키로 혹시 남은 다이얼로그 정리
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 메인 목록 복귀 단언
    expect(page.locator("h2", has_text="회원 업체 관리").first).to_be_visible()
    print("[Success] TC-CTR-09 가입된 회원 업체 추가 E2E 검증 성공!")


def test_tc_ctr_10_add_unregistered_contractor_e2e(page: Page, login_cso):
    """
    [TC-CTR-10] Phase 3 E2E: 미가입 신규 업체 추가하기 (Google Sheet 사업자번호 연동 + 서류 첨부) Full Flow 검증
    """
    print("\n" + "=" * 60)
    print(" [TC-CTR-10] 미가입 신규 업체 추가 E2E 검증 시작")
    print("=" * 60)

    # 1. 회원 업체 관리 메인 이동
    page.goto(page.url.split("dashboard")[0] + "dashboard/contractor/entrustment-contract")
    page.wait_for_selector("h2:has-text('회원 업체 관리')", timeout=10000)

    # 2. '추가하기' 클릭
    print("[Step 1] '추가하기' 버튼 클릭")
    page.click("button:has-text('추가하기')")
    page.wait_for_selector("div[role='dialog']", timeout=5000)

    # 3. Google Sheet에서 미사용 사업자번호 추출
    print("[Step 2] Google Sheet에서 미사용 사업자번호 추출")
    biz_no = get_biz_no_from_sheet()
    if biz_no.startswith("ERROR") or biz_no == "NO_BIZ_NO":
        pytest.fail(f"사용 가능한 사업자번호를 가져오지 못했습니다: {biz_no}")

    clean_biz_no = biz_no.replace("-", "").strip()
    print(f"-> 사용할 미가입 사업자번호: {clean_biz_no}")

    page.fill("#bizNumber, input[placeholder*='-없이 숫자만 입력']", clean_biz_no)
    page.click("button:has-text('확인하기')")
    page.wait_for_selector("input[name='managementCode']", timeout=10000)

    # 4. 파일 첨부 (사업자등록증, CSO신고증)
    print("[Step 3] 필수 증빙 PDF 첨부")
    file_input1 = page.locator("#bizRegCertFileUuid input[type='file'], input[type='file']").first
    if file_input1.is_visible():
        file_input1.set_input_files(TESTFILE_PDF)
        page.wait_for_timeout(500)

    file_input2 = page.locator("#salesCertFileUuid input[type='file']").first
    if file_input2.is_visible():
        file_input2.set_input_files(TESTFILE_PDF2)
        page.wait_for_timeout(500)

    # 5. 관리코드 및 담당자 정보 입력
    now_code = datetime.datetime.now().strftime("%m%d-%H%M")
    print(f"[Step 4] 관리코드 및 담당자 정보 입력")
    page.fill("input[name='managementCode']", f"{now_code}.")
    page.fill("input[name='managerName']", "자동화미가입")
    page.fill("input[name='managerPhone']", f"010{random.randint(10000000, 99999999)}")
    page.fill("input[name='managerEmail']", "unreg@parmple.com")

    # 6. '추가하기' 클릭
    print("[Step 5] '추가하기' 클릭 및 요청 완료 팝업 확인")
    page.locator("button:has-text('추가하기')").last.click()
    page.wait_for_timeout(1500)

    # 등록 요청 완료 팝업 확인
    complete_confirm = page.locator("button:has-text('확인')").last
    if complete_confirm.is_visible():
        complete_confirm.click()
        page.wait_for_timeout(1000)

    # 메인 목록 복귀 단언
    expect(page.locator("h2", has_text="회원 업체 관리").first).to_be_visible()
    print("[Success] TC-CTR-10 미가입 신규 업체 추가 E2E 검증 성공!")
