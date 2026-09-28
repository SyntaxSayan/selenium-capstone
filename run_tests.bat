@echo off
echo ===============================================================================
echo   Selenium WebDriver with Python - E-Commerce Automation Capstone Project
echo ===============================================================================
echo.

REM Set Python UTF-8 encoding
set PYTHONIOENCODING=utf-8

REM Optional argument parsing (e.g., run_tests.bat --headless)
set HEADLESS_FLAG=--headless
if "%1"=="--headed" (
    set HEADLESS_FLAG=
)

echo [INFO] Running test suite via Pytest with HTML report generation...
python -m pytest %HEADLESS_FLAG%

echo.
echo ===============================================================================
echo   Execution finished! Report generated at: reports\report.html
echo ===============================================================================
echo.

REM Automatically open HTML report in default browser if report exists
if exist "reports\report.html" (
    echo [INFO] Opening HTML test report in default browser...
    start reports\report.html
)

pause
