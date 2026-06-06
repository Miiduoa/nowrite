# nowrite — 手寫小抄產生器 / Handwriting Cheat-Sheet Generator

把任意 UTF-8 文字檔，用指定的 TTF 字體轉成**擬手寫 PDF**。內建圖形介面，可調 19 項參數
（字體大小、行間距、各種筆畫擾動、墨汁深度、塗改…），支援空白／橫線／方格紙與黑／藍／灰墨色。

Turn any UTF-8 text file into a realistic **handwritten-style PDF** using a TTF font. Ships with a
GUI exposing 19 tunable parameters (size, spacing, stroke jitter, ink depth, cross-outs), three paper
styles (blank / lined / grid) and three ink colours (black / blue / dark-gray).

> 起源：把一份作業系統期末小抄（L5–L8）轉成手寫筆記。`OS_Cheat_Sheet_handwriting_source.txt` 是內建範例文字，換掉它就能手寫任何內容。

---

## ✨ Features
- **19 項參數**即時可調（見下表）
- 中英混排、CJK 友善；字體缺字時自動以**同字的日文寫法**替換（例：查→査、產→産），避免空白方塊（tofu）
- 紙張：`blank` 空白 / `lined` 橫線 / `grid` 方格；墨色：`black` 黑 / `blue` 藍筆 / `dark-gray` 深灰
- **一鍵編譯 Windows 獨立 EXE**（`build_exe.bat`，免裝 Python 即可分享）
- 純 Python：Pillow · NumPy · Handright · fontTools

## 🚀 Quick start

### Windows（最簡單，產生獨立 EXE）
1. 放一個 `.ttf` 字體到專案根目錄（見下方「字體」）。
2. 雙擊 `build_exe.bat` → 自動安裝相依套件並編譯出 `dist\OS_Handwriting_Generator.exe`。
3. 之後直接雙擊該 EXE 即可（免裝 Python）。

### 任何平台（用 Python）
```bash
pip install -r requirements.txt
python app.py          # 圖形介面
python render_core.py  # 無介面，用預設參數直接輸出 PDF
```

## 🖋 字體 / Font（重要）
本專案**不附帶字體**。原始使用的 `TekitouPoem.ttf`（適当ポエム, © Cockatrice Digital）為第三方字體，
內嵌授權序號、可能屬商用授權，故**未隨此 repo 散布**。請自行將你**擁有合法授權**的 `.ttf`
放到專案根目錄（任何 TTF 皆可，檔名建議 `TekitouPoem.ttf`，或在程式中用「瀏覽」選擇）。
`.gitignore` 已預設忽略 `*.ttf`。

This repo does **not** bundle any font. Drop your own licensed `.ttf` in the project root.

## ⚙️ Parameters

| 參數 (GUI 標籤) | key | 預設 | 說明 |
|---|---|---|---|
| 字體大小 | `font_size` | 73 | 字級 (px) |
| 行間距 | `line_spacing` | 74 | 行距 (px) |
| 上 / 下 / 左 / 右邊距 | `*_margin` | 42 / 43 / 50 / 50 | 頁邊距 (px) |
| 行間距擾動 | `line_spacing_sigma` | 3 | 行距隨機 |
| 字體大小擾動 | `font_size_sigma` | 3 | 字級隨機 |
| 字間距擾動 | `word_spacing_sigma` | 3 | 字距隨機 |
| 筆畫橫向偏移 | `perturb_x_sigma` | 4 | 筆畫 X 抖動 |
| 筆畫縱向偏移 | `perturb_y_sigma` | 4 | 筆畫 Y 抖動 |
| 筆畫旋轉偏移 | `perturb_theta_sigma` | 0.05 | 筆畫旋轉抖動 (rad) |
| 字間距 | `word_spacing` | 1 | 基礎字距 (px) |
| 塗改線長度 / 角度 / 寬度標準差 | `strike_*_sigma` | 2 / 2 / 1 | 塗改線隨機 |
| 塗改出現的幾率 | `strike_prob` | 0.005 | 每字出現塗改機率 |
| 塗改線寬度 | `strike_width` | 6 | 塗改線粗細 (px) |
| 墨汁深度標準差 | `ink_depth_sigma` | 28 | 墨色深淺變化 |
| 解析度 | `dpi` | 200 | A4 輸出 DPI |
| 亂數種子 | `seed` | 20260605 | 換數字＝不同字跡 |

## 📁 Files
```
app.py            圖形介面 (tkinter)
render_core.py    渲染核心（亦可當 CLI）
build_exe.bat     一鍵編譯 Windows EXE
run_app.bat       已裝 Python 者直接執行
requirements.txt  相依套件
OS_Cheat_Sheet_handwriting_source.txt  範例文字
README_使用說明.txt  詳細中文說明
```

## 📄 License
程式碼採 **MIT**（見 `LICENSE`）。**字體不在此授權範圍**，亦未隨本 repo 散布。
Engine: [Handright](https://github.com/Gsllchb/Handright) (handwriting simulation).
