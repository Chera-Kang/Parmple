@echo off
title Business Number Checker
cd /d "%~dp0"

echo.
echo ======================================================
echo   Starting Business Number Check...
echo ======================================================
echo.

python CheckNumber.py

echo.
echo ======================================================
echo   Task Completed.
echo ======================================================
pause
