#!/bin/bash
# =====================================================================
# 將整個專案乾淨地推送（覆蓋）到 https://github.com/Miiduoa/nowrite
# 雙擊本檔，或於終端機執行： bash push-to-github.command
#
# 會以全新單一提交覆蓋遠端（--force），等同「清空後重新上傳」。
# 需求：已安裝 git，且你的電腦已登入 GitHub（或備妥 Personal Access Token）。
# =====================================================================
set -e
cd "$(dirname "$0")"
ROOT="$(pwd)"
REMOTE="https://github.com/Miiduoa/nowrite.git"
echo "專案：$ROOT"
echo "目標：$REMOTE"
echo ""

command -v git >/dev/null 2>&1 || { echo "✗ 找不到 git，請先安裝 Xcode Command Line Tools：xcode-select --install"; exit 1; }

# 1) 乾淨初始化（移除舊 .git 與沙箱遺留鎖檔，避免歷史殘留）
rm -rf .git
git init -q
git branch -M main
git config user.name  >/dev/null 2>&1 || git config user.name  "Miiduoa"
git config user.email >/dev/null 2>&1 || git config user.email "demohan513@gmail.com"

# 1.5) 移除上游作者殘留、會造成 Actions 紅叉且非本專案所需的 CI / 設定
#      （保留我的 build.yml 桌面打包，與 test_backend.yml 後端測試）
rm -f .github/workflows/backend.yml \
      .github/workflows/frontend.yml \
      .github/workflows/mysql.yml \
      .github/workflows/semantic_release.yml \
      .github/workflows/manual-workflow.yml \
      release.config.js
echo "已移除上游殘留 CI（docker push / semantic-release 等）。"

# 2) 加入檔案（.gitignore 已排除 node_modules / dist / 安裝檔等大型產物）
git add -A

# 3) 安全檢查：GitHub 單檔上限 100MB，先攔下任何 >95MB 的檔案
echo "檢查是否有過大的檔案…"
BIG="$(git ls-files -z | xargs -0 du -m 2>/dev/null | awk '$1>95 {print $1"MB\t"$2}')"
if [ -n "$BIG" ]; then
  echo "✗ 偵測到 >95MB 的檔案，已中止（請確認這些不該上傳，並補進 .gitignore）："
  echo "$BIG"
  exit 1
fi
echo "將提交的檔案數：$(git ls-files | wc -l | tr -d ' ')"

# 4) 建立提交
git commit -q -m "手寫生成：液態玻璃重設計 + 繁體中文 + 離線桌面版（Electron/PyInstaller）"

# 5) 設定遠端並強制覆蓋 nowrite
git remote add origin "$REMOTE"
echo ""
echo "→ 強制推送到 $REMOTE 的 main 分支（會覆蓋遠端現有內容）"
echo "  若被要求輸入帳密：帳號 = GitHub 使用者名稱，密碼 = Personal Access Token（不是登入密碼）"
echo ""
git push -u origin main --force

echo ""
echo "✅ 完成！請到 https://github.com/Miiduoa/nowrite 確認。"
echo "   推送後，GitHub Actions 會自動開始建置 macOS 與 Windows 安裝檔（Actions 分頁可下載）。"
echo "   若舊內容還在其他分支：到 repo 的 Settings → Branches 把預設分支設為 main，再刪除多餘分支即可。"
