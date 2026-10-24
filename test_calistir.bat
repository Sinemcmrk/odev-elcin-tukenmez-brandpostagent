@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
call ".venv\Scripts\activate.bat"
python -m tests.run_tests
echo.
python -m tests.app_smoke
echo.
python -m tests.cesitlilik_testi
pause
