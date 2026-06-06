[繁體中文](README.md) | [English](README_en.md)

# 手寫生成 · nowrite

把文字渲染成自然的**手寫圖片與 PDF**。全新設計的介面（Apple 液態玻璃 × Tesla 白色極簡）、繁體中文優先（繁／简／EN 可切換）、並提供**可離線使用的桌面版**（macOS / Windows）。

專案位址：<https://github.com/Miiduoa/nowrite>

> 想先看介面風格：用瀏覽器打開根目錄的 `redesign-preview.html`，右上角可切換 自動／淺色／深色。

---

## ✨ 特色

- **文字轉手寫**：用現有字型生成擬手寫的圖片，支援多頁輸出。
- **自訂字型**：上傳 `.ttf` 產生專屬手寫風格。
- **背景**：上傳背景圖；沒有背景圖也沒關係，只要給定寬高，會自動生成帶橫線的稿紙。
- **細緻參數**：邊距（上下左右）、字級、行距、字距、筆畫橫／縱向擾動與旋轉、墨色深淺、塗改痕跡，皆可微調。
- **多格式匯入**：直接輸入文字，或上傳 `.txt / .pdf / .docx` 自動擷取內容。
- **即時預覽 ＋ 批次輸出**：滿意後一鍵生成整套圖片（打包成 zip）或匯出 PDF。
- **介面**：液態毛玻璃 ＋ 白色極簡、明暗自動跟隨系統、繁／简／EN 語言切換。
- **離線桌面版**：App 內含後端，無需網路即可生成。

---

## 🚀 取得桌面 App（離線，推薦）

最簡單：到本 repo 的 **Actions**（或 **Releases**）下載已建好的安裝檔：

- macOS：`手寫生成-x.y.z-arm64.dmg`
- Windows：`手寫生成-x.y.z-setup.exe`

或自行建置（詳見 [`DESKTOP_BUILD.md`](DESKTOP_BUILD.md)）：

- **macOS 一鍵**：`bash build-dmg.command`
- **雲端同時建 mac + win**：`bash push-to-github.command` 推上 GitHub 後，GitHub Actions 會自動建置，於 Actions 分頁下載安裝檔。

> App 未經程式碼簽章（個人用途）：macOS 首次開啟請對 App 按右鍵 →「開啟」；Windows 出現 SmartScreen 時點「其他資訊 → 仍要執行」。

---

## 🧑‍💻 本機開發（網頁版）

需求：Node.js 18+、Python 3.10–3.12。

**後端**

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
# requirements.txt 為 UTF-16，先轉成 UTF-8 再安裝
python -c "open('req.txt','w',encoding='utf-8').write(open('requirements.txt',encoding='utf-16').read())"
pip install -r req.txt
python run_server.py                                   # http://127.0.0.1:5005
```

**前端**

```bash
cd frontend
npm install
npm run serve                                          # http://localhost:8080（/api 代理到 5005）
```

---

## 🐳 自架（Docker，進階）

倉庫附有 `dockerfile.frontend` 與 `dockerfile.backend`，可自行建置映像後部署（後端預設埠 5005、前端 80）。
注意：根目錄的 `docker-compose.yml` 預設會拉取上游公開映像；若要部署「本專案」的程式碼，請改為由原始碼建置映像。

---

## 🏗️ 技術棧

- **前端**：Vue 3、Vue Router、Vuex、vue-i18n、Bootstrap 5、SweetAlert2、axios
- **後端**：FastAPI、Uvicorn、[handright]、Pillow、OpenCV、scikit-learn、PyMuPDF、python-docx、PyPDF2；任務狀態以 **SQLite** 儲存
- **桌面**：Electron + electron-builder；後端以 **PyInstaller** 打包為隨附 sidecar
- **CI**：GitHub Actions 自動建置 macOS / Windows 安裝檔

---

## 📁 專案結構

```
frontend/                     Vue 3 前端（重新設計的 UI、i18n 繁/简/EN）
backend/                      FastAPI 後端（手寫渲染、檔案擷取、SQLite 任務）
  run_server.py               離線桌面版後端入口
desktop/                      Electron 殼與打包設定（mac dmg / win nsis）
  main.cjs / preload.cjs      啟動後端 sidecar、注入本機 API 位址
  electron-builder.yml        打包設定
  backend/handwrite-backend.spec   PyInstaller 規格
ttf_files/                    內建字型
.github/workflows/build.yml   CI：自動建 macOS + Windows
build-dmg.command             macOS 一鍵打包
push-to-github.command        推送並覆蓋到 GitHub（nowrite）
DESKTOP_BUILD.md              桌面打包 / CI 詳細說明
```

---

## ⚙️ 後端運作流程

提交任務 → 寫入 SQLite → 立即回傳 `task_id` → 背景協程排隊渲染（以 Semaphore 控制並發）→ 前端透過 **WebSocket 或輪詢**取得進度與結果。離線桌面版中，前端的 `/api` 請求會自動指向 App 內建後端 `127.0.0.1:5005`。

---

## 📄 授權與致謝

本專案以 **MIT** 授權釋出（見 [`LICENSE`](LICENSE)）。

介面重新設計（Apple 液態玻璃 × Tesla 白色極簡）、繁體中文在地化與離線桌面打包為本專案完成；核心手寫渲染採用開源函式庫 **handright**，並衍生自開源專案 **handwriting-web**（MIT, © Liuweiqing）。

[handright]: https://github.com/Gsllchb/Handright
