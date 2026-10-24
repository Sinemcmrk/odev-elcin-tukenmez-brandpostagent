@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
echo ============================================
echo   Brand Post Agent - Kurulum
echo ============================================
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY (
  echo [HATA] Python bulunamadi. KURULUM_WINDOWS.md - Adim 1'e bakin.
  pause & exit /b 1
)
%PY% --version
echo.
echo [1/4] Sanal ortam olusturuluyor...
%PY% -m venv .venv || (echo [HATA] Sanal ortam olusturulamadi. & pause & exit /b 1)
call ".venv\Scripts\activate.bat"
echo [2/4] Paketler yukleniyor (birkac dakika surebilir)...
python -m pip install --upgrade pip
pip install -r requirements.txt || (echo [HATA] Paketler yuklenemedi. Internet baglantinizi kontrol edin. & pause & exit /b 1)
echo [3/4] Tarayici motoru (Chromium) yukleniyor...
python -m playwright install chromium || (echo [HATA] Chromium yuklenemedi. & pause & exit /b 1)
echo [4/4] Ayar dosyasi hazirlaniyor...
if not exist ".env" copy ".env.example" ".env" >nul
echo.
echo Kurulum tamamlandi.
echo Simdi acilacak .env dosyasinda GEMINI_API_KEY satirina anahtarinizi yapistirip KAYDEDIN.
pause
notepad ".env"
