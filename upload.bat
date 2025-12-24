@echo off
:: 한글 깨짐 방지
chcp 65001 > nul

echo ========================================
echo   Web 프로젝트(Parmple) 업데이트 시작
echo ========================================

:: 1. 변경사항 등록
git add .

:: 2. 커밋
set currenttime=%time:~0,5%
set datetime=%date% %currenttime%

git commit -m "update (%datetime%)"

:: 3. 서버로 업로드
echo.
echo [GitHub 서버로 업로드 중...]
git push origin main

echo.
echo ========================================
echo   업데이트가 완료되었습니다!
echo ========================================
pause