# 手寫生成 · 離線桌面版（macOS .dmg / Windows .exe）

把這個網站打包成一個**可離線使用**的 Mac App，並產生 `.dmg` 安裝檔。App 內含：

- 你重新設計的前端（Tesla 白色極簡風、繁體中文）
- 內嵌的 Python 後端（FastAPI），以 sidecar 方式隨 App 啟動／關閉
- 內建字型，無需網路即可生成手寫圖片與 PDF

> ⚠️ Windows 的 `.exe` 與 macOS 的 `.dmg` 都必須在「該作業系統」上打包。
> 你用的是 Mac，要做 **Windows 版**最簡單的方式是用下方「方式 A」的 GitHub Actions 雲端自動建置（不需要 Windows 電腦）。

---

## 方式 A｜上傳 GitHub，自動建 Windows + macOS（推薦）

1. 把專案推送到 nowrite（會覆蓋遠端現有內容）：

   ```bash
   cd "/Users/miiduoa/Desktop/手寫字體/handwriting-web"
   bash push-to-github.command
   ```

   若被要求帳密：帳號＝GitHub 使用者名稱，密碼＝Personal Access Token（不是登入密碼）。

2. 推送後，GitHub 會自動執行 `.github/workflows/build.yml`，在雲端同時建出：
   - macOS（Apple Silicon）→ `手寫生成-1.3.0-arm64.dmg`
   - Windows → `手寫生成-1.3.0-setup.exe`

3. 到 repo 的 **Actions** 分頁 → 點最新一次執行 → 最下方 **Artifacts** 下載：
   - `handwrite-macos-dmg`
   - `handwrite-windows-setup`

   （也可在 Actions 分頁手動按「Run workflow」重新建置。）

**Windows 首次執行**：未簽章，SmartScreen 會提示 → 點「**其他資訊 → 仍要執行**」即可。

---

## 方式 B｜在 Mac 本機建 macOS .dmg（一鍵）

1. 安裝前置需求（只需一次）：
   - **Node.js 18+**：<https://nodejs.org>
   - **Python 3.10–3.12**：<https://www.python.org/downloads/>（或 `brew install python@3.12`）
     ⚠️ 後端相依只支援到 3.12；若你的 `python3` 是 3.13／3.14，腳本會自動尋找或用 Homebrew 安裝 3.12 來打包後端（不影響你系統預設的 Python）。
   - **Xcode Command Line Tools**：終端機執行 `xcode-select --install`

2. 打包：在 Finder 對著專案根目錄的 **`build-dmg.command`** 按右鍵 →「開啟」，
   或在終端機執行：

   ```bash
   cd "/Users/miiduoa/Desktop/手寫字體/handwriting-web"
   bash build-dmg.command
   ```

3. 完成後，`.dmg` 會在：

   ```
   desktop/release/手寫生成-1.3.0-<架構>.dmg
   ```

腳本會自動：建置前端 → 用 PyInstaller 打包後端 → 用 electron-builder 產生 `.dmg`。
首次執行會下載相依套件，視網速約需 5–15 分鐘。

---

## 首次開啟（Gatekeeper）

這個 App **沒有經過 Apple 簽章／公證**（個人離線使用）。第一次打開時 macOS 會擋：

- 對著 App 按**右鍵 →「開啟」→ 再按一次「開啟」**；或
- 系統設定 →「隱私權與安全性」→ 對提示按「仍要開啟」。

之後就能正常雙擊使用。

---

## 開發模式（不打包、直接跑桌面殼）

先啟動後端，再啟動 Electron：

```bash
# 1) 後端（任一終端機）
cd backend
python3 -m venv .venv && source .venv/bin/activate
python -c "open('/tmp/r.txt','w',encoding='utf-8').write(open('requirements.txt',encoding='utf-16').read())"
pip install -r /tmp/r.txt
python run_server.py            # 監聽 127.0.0.1:5005

# 2) 前端建置一次（桌面模式）
cd ../frontend && VUE_APP_TARGET=desktop npm run build

# 3) 桌面殼
cd ../desktop && npm install && npm start
```

---

## 架構說明

```
desktop/
  main.cjs              Electron 主程序：啟動後端 sidecar、等埠就緒、載入前端、結束清理
  preload.cjs           注入本機後端位址 window.__HW_API_BASE__ = http://127.0.0.1:5005
  electron-builder.yml  打包設定（mac dmg / win nsis；前端/字型/後端以 extraResources 內含）
  afterPack.js          mac 建置後對 App 與後端做 ad-hoc 簽章
  backend/
    handwrite-backend.spec   PyInstaller 規格（後端 → 單一執行檔）
    requirements-desktop.txt 後端相依（UTF-8 備援清單）
  build/icon.png        App 圖示
backend/run_server.py   後端入口：先建可寫目錄並 chdir，再啟動 uvicorn
build-dmg.command       一鍵打包腳本（macOS .dmg）
push-to-github.command  推送並覆蓋到 Miiduoa/nowrite
.github/workflows/build.yml  GitHub Actions：自動建 macOS(.dmg) + Windows(.exe)
```

> 在 Windows 電腦上本機打包：裝好 Node 18+ 與 Python 3.12 後，依序執行
> `cd frontend && set VUE_APP_TARGET=desktop && npm run build`、
> `pip install -r desktop/backend/requirements-desktop.txt && pyinstaller --clean -y --distpath desktop/dist-backend --workpath desktop/.pybuild desktop/backend/handwrite-backend.spec`、
> `cd desktop && npm install && npm run dist:win`。

執行時資料寫在：`~/Library/Application Support/手寫生成/`（SQLite、暫存、字型、log）。

---

## 注意事項

- **檔案較大**：因內含 Python＋OpenCV＋scikit-learn 等，App 約 300–600 MB 屬正常。
- **架構**：`.dmg` 會依你的 Mac 自動產生（Apple Silicon → arm64，Intel → x64）。
  要做通用版可改用 `cd desktop && npm run dist:universal`（需先備妥兩種架構的後端二進位，較進階）。
- **.doc/.rtf 上傳**：少數舊格式轉檔需要系統 `pandoc`；如需支援可 `brew install pandoc`。
  一般 `.txt / .pdf / .docx` 與直接輸入文字皆可離線運作。
- 若要做成可分發給他人的簽章版本，需要 Apple Developer 帳號做 codesign＋notarize（可另外協助設定）。
