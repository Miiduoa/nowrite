// electron-builder afterPack 鉤子：對 .app 與內嵌後端做 ad-hoc 簽章。
// 原因：Apple Silicon（arm64）要求可執行碼需有簽章才能啟動；個人離線版沒有
// Apple 憑證，這裡用「-」做 ad-hoc 簽章，讓本機建置的 App 與 sidecar 能正常執行。
const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

exports.default = async function afterPack(context) {
  if (context.electronPlatformName !== "darwin") return;

  const appName = context.packager.appInfo.productFilename; // 手寫生成
  const appPath = path.join(context.appOutDir, `${appName}.app`);
  const backendBin = path.join(
    appPath,
    "Contents",
    "Resources",
    "backend",
    "handwrite-backend"
  );

  const sign = (target, deep) => {
    const flag = deep ? "--deep " : "";
    execSync(`codesign --force ${flag}--sign - "${target}"`, { stdio: "inherit" });
  };

  try {
    if (fs.existsSync(backendBin)) {
      fs.chmodSync(backendBin, 0o755);
      sign(backendBin, false); // 先簽內嵌後端執行檔
      console.log("[afterPack] ad-hoc 簽章後端：", backendBin);
    } else {
      console.warn("[afterPack] 找不到後端執行檔（略過）：", backendBin);
    }
    sign(appPath, true); // 再對整個 App 深度 ad-hoc 簽章
    console.log("[afterPack] ad-hoc 簽章 App：", appPath);
  } catch (e) {
    console.warn("[afterPack] ad-hoc 簽章失敗（App 仍可能可用）：", e.message);
  }
};
