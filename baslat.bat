@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
if not exist ".venv\Scripts\activate.bat" (
  echo Once kurulum.bat dosyasini calistirin.
  pause & exit /b 1
)
call ".venv\Scripts\activate.bat"
echo Brand Post Agent baslatiliyor... Tarayici birkac saniye icinde acilacak.
echo Kapatmak icin bu pencereyi kapatin.
start "" cmd /c "timeout /t 5 >nul & start http://localhost:8501"
streamlit run app.py
pause
