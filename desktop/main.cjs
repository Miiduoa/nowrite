// 手寫生成 桌面版（離線）— Electron 主程序
// 啟動內嵌的 Python 後端（sidecar），等待埠就緒後載入前端，結束時清理。
const { app, BrowserWindow, shell } = require("electron");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");
const net = require("net");

const API_HOST = "127.0.0.1";
const API_PORT = 5005;

let backendProc = null;
let mainWindow = null;

function dataDir() {
  // 可寫資料目錄：~/Library/Application Support/手寫生成/
  const d = app.getPath("userData");
  for (const sub of ["logs", "temp", "fonts"]) {
    fs.mkdirSync(path.join(d, sub), { recursive: true });
  }
  return d;
}

function resolveBackend() {
  if (app.isPackaged) {
    // 打包後：Resources/backend/handwrite-backend、內建字型 Resources/fonts
    return {
      useBinary: true,
      bin: path.join(
        process.resourcesPath,
        "backend",
        process.platform === "win32" ? "handwrite-backend.exe" : "handwrite-backend"
      ),
      fonts: path.join(process.resourcesPath, "fonts"),
    };
  }
  // 開發模式：直接用 python 跑 run_server.py
  return {
    useBinary: false,
    py: process.env.HW_PYTHON || (process.platform === "win32" ? "python" : "python3"),
    script: path.join(__dirname, "..", "backend", "run_server.py"),
    cwd: path.join(__dirname, "..", "backend"),
    fonts: path.join(__dirname, "..", "ttf_files"),
  };
}

function startBackend() {
  const data = dataDir();
  const bp = resolveBackend();
  const env = Object.assign({}, process.env, {
    HW_HOST: API_HOST,
    HW_PORT: String(API_PORT),
    HW_DATA_DIR: data,
    FONT_ASSETS_DIR: path.join(data, "fonts"),
    FONT_ASSETS_BUNDLED_DIR: bp.fonts,
    PYTHONUNBUFFERED: "1",
  });

  try {
    if (bp.useBinary) {
      backendProc = spawn(bp.bin, [], { cwd: data, env });
    } else {
      backendProc = spawn(bp.py, [bp.script], { cwd: bp.cwd, env });
    }
  } catch (e) {
    console.error("[backend] 無法啟動：", e);
    return;
  }

  backendProc.stdout && backendProc.stdout.on("data", (d) => console.log("[backend]", d.toString().trim()));
  backendProc.stderr && backendProc.stderr.on("data", (d) => console.log("[backend:err]", d.toString().trim()));
  backendProc.on("exit", (code) => console.log("[backend] 已結束，code =", code));
}

function waitForPort(host, port, timeoutMs = 90000) {
  const start = Date.now();
  return new Promise((resolve, reject) => {
    const tryConnect = () => {
      const socket = net.connect(port, host);
      socket.once("connect", () => {
        socket.destroy();
        resolve();
      });
      socket.once("error", () => {
        socket.destroy();
        if (Date.now() - start > timeoutMs) reject(new Error("後端啟動逾時"));
        else setTimeout(tryConnect, 400);
      });
    };
    tryConnect();
  });
}

async function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 860,
    minWidth: 880,
    minHeight: 600,
    title: "手寫生成",
    backgroundColor: "#f4f5f7",
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
      webSecurity: false, // 允許前端（file://）呼叫本機後端 127.0.0.1
    },
  });

  // 外部連結改用系統瀏覽器開啟
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });

  const indexFile = app.isPackaged
    ? path.join(process.resourcesPath, "app_dist", "index.html")
    : path.join(__dirname, "..", "frontend", "dist", "index.html");

  try {
    await waitForPort(API_HOST, API_PORT);
  } catch (e) {
    console.error(e); // 後端逾時仍載入前端，讓使用者看到畫面與錯誤
  }

  mainWindow.loadFile(indexFile);
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

function killBackend() {
  if (backendProc) {
    try {
      backendProc.kill();
    } catch (e) {
      /* ignore */
    }
    backendProc = null;
  }
}

app.whenReady().then(() => {
  startBackend();
  createWindow();
});

app.on("window-all-closed", () => {
  killBackend();
  app.quit();
});
app.on("before-quit", killBackend);
app.on("quit", killBackend);
