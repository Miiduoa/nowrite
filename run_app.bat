@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
rem 直接用 Python 執行 GUI（不編譯 EXE）。適合已安裝 Python 的人快速試用。
python --version >nul 2>&1
if errorlevel 1 (
  echo [!] 偵測不到 Python。請改用 build_exe.bat（會自動安裝），或先安裝 Python。
  pause
  exit /b 1
)
echo 安裝/確認相依套件中 ...
python -m pip install pillow numpy handright fonttools >nul 2>&1
echo 開啟程式 ...
python app.py
