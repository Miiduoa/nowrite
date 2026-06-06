@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
echo ============================================================
echo    OS Handwriting Generator  -  Build standalone EXE
echo    產生獨立 EXE（之後雙擊即可用，免裝 Python）
echo ============================================================
echo.

rem ---- 1) 確認 Python ----
python --version >nul 2>&1
if errorlevel 1 (
  echo [!] 偵測不到 Python，嘗試用 winget 自動安裝 Python 3.11 ...
  winget install -e --id Python.Python.3.11 --accept-source-agreements --accept-package-agreements
  echo.
  echo [!] 安裝完成後，請「關閉本視窗」再重新雙擊 build_exe.bat 一次。
  pause
  exit /b 1
)

echo [1/3] 安裝相依套件 (pillow numpy handright fonttools pyinstaller) ...
python -m pip install --upgrade pip
python -m pip install pillow numpy handright fonttools pyinstaller
if errorlevel 1 ( echo [x] 套件安裝失敗，請檢查網路。 & pause & exit /b 1 )

echo.
echo [2/3] 編譯 EXE （onefile，可能需要 1-3 分鐘）...
pyinstaller --onefile --windowed --noconfirm --clean --name "OS_Handwriting_Generator" --collect-all handright app.py
if errorlevel 1 ( echo [x] 編譯失敗。 & pause & exit /b 1 )

echo.
echo [3/3] 複製字體與文字檔到 dist 資料夾 ...
copy /Y "TekitouPoem.ttf" "dist\" >nul
copy /Y "OS_Cheat_Sheet_handwriting_source.txt" "dist\" >nul

echo.
echo ============================================================
echo  完成！獨立程式在： dist\OS_Handwriting_Generator.exe
echo  以後直接雙擊該 EXE 即可使用（免裝 Python）。
echo  注意：請讓該 EXE 與 TekitouPoem.ttf、.txt 放在同一個資料夾。
echo ============================================================
pause
