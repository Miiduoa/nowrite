#!/bin/bash
# =====================================================================
# 手寫生成 · 離線桌面版 一鍵打包成 .dmg（請在 macOS 上執行）
# 雙擊本檔，或於終端機執行： bash build-dmg.command
#
# 需求：macOS、Node.js 18+、Xcode Command Line Tools
#       後端打包需要 Python 3.10–3.12（若系統 python3 過新，腳本會自動尋找／安裝 3.12）
# 產出：desktop/release/手寫生成-<版本>-<架構>.dmg
# =====================================================================
set -e
cd "$(dirname "$0")"
ROOT="$(pwd)"
echo "專案根目錄：$ROOT"
echo ""

# ---- 0) 檢查必要工具 ----
need() { command -v "$1" >/dev/null 2>&1 || { echo "✗ 找不到 $1，請先安裝後再試。"; exit 1; }; }
need node
need npm
echo "node: $(node -v)"

# ---- 找出可用的 Python 3.10–3.12（舊版相依只有這些版本有預編譯 wheel） ----
is_good_py() {
  "$1" -c 'import sys; v=sys.version_info[:2]; raise SystemExit(0 if (3,10)<=v<=(3,12) else 1)' >/dev/null 2>&1
}
find_python() {
  local c
  for c in python3.12 python3.11 python3.10 \
           /opt/homebrew/opt/python@3.12/bin/python3.12 \
           /usr/local/opt/python@3.12/bin/python3.12 \
           /opt/homebrew/opt/python@3.11/bin/python3.11 \
           /usr/local/opt/python@3.11/bin/python3.11 \
           /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 \
           /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 \
           python3; do
    if command -v "$c" >/dev/null 2>&1 && is_good_py "$c"; then
      command -v "$c"; return 0
    fi
  done
  return 1
}

PY="$(find_python || true)"
if [ -z "$PY" ]; then
  echo "！系統的 python3（$(python3 --version 2>&1)）版本不適用於後端相依（需 3.10–3.12）。"
  if command -v brew >/dev/null 2>&1; then
    echo "→ 偵測到 Homebrew，正在安裝 python@3.12 …（首次安裝較久）"
    brew install python@3.12 || true
    PY="$(find_python || true)"
  fi
fi
if [ -z "$PY" ]; then
  echo ""
  echo "✗ 找不到 Python 3.10–3.12。請擇一安裝後再執行本腳本："
  echo "    • Homebrew：  brew install python@3.12"
  echo "    • 官方安裝檔： https://www.python.org/downloads/release/python-3127/"
  exit 1
fi
echo "python（後端打包用）: $PY -> $("$PY" --version 2>&1)"
echo ""

# ---- 1) 建置前端（桌面模式：相對路徑 + hash 路由） ----
echo "===== 1/4 建置前端 ====="
cd "$ROOT/frontend"
npm install
VUE_APP_TARGET=desktop npm run build
echo "前端產物：$ROOT/frontend/dist"
echo ""

# ---- 2) 以 PyInstaller 打包後端為單一執行檔 ----
echo "===== 2/4 打包後端（PyInstaller，使用 Python 3.12） ====="
cd "$ROOT/backend"
rm -rf .venv-build
"$PY" -m venv .venv-build
# shellcheck disable=SC1091
source .venv-build/bin/activate
python -m pip install --upgrade pip wheel
# 使用放寬版本的相依清單（全程使用 wheel，不從原始碼編譯）
python -m pip install -r "$ROOT/desktop/backend/requirements-desktop.txt"

rm -rf "$ROOT/desktop/dist-backend" "$ROOT/desktop/.pybuild"
pyinstaller --clean -y \
  --distpath "$ROOT/desktop/dist-backend" \
  --workpath "$ROOT/desktop/.pybuild" \
  "$ROOT/desktop/backend/handwrite-backend.spec"
deactivate

if [ ! -f "$ROOT/desktop/dist-backend/handwrite-backend" ]; then
  echo "✗ 後端打包失敗：找不到 desktop/dist-backend/handwrite-backend"; exit 1
fi
chmod +x "$ROOT/desktop/dist-backend/handwrite-backend"
echo "後端執行檔：$ROOT/desktop/dist-backend/handwrite-backend"
echo ""

# ---- 3) 安裝 Electron 相依 ----
echo "===== 3/4 安裝 Electron 相依 ====="
cd "$ROOT/desktop"
npm install
echo ""

# ---- 4) 產生 DMG ----
echo "===== 4/4 產生 DMG ====="
npm run dist
echo ""
echo "✅ 完成！DMG 位於：$ROOT/desktop/release/"
open "$ROOT/desktop/release" 2>/dev/null || true
