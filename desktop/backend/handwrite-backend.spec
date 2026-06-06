# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller 規格：把 FastAPI 後端打包成單一可執行檔 handwrite-backend
# 於 macOS 上執行（從 backend/ 目錄呼叫）：
#   pyinstaller --clean -y \
#     --distpath ../desktop/dist-backend \
#     --workpath ../desktop/.pybuild \
#     ../desktop/backend/handwrite-backend.spec
#
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

# 後端原始碼目錄：以 spec 檔位置推算（desktop/backend → 專案根 → backend）
try:
    _SPEC_DIR = SPECPATH  # PyInstaller 會注入 spec 所在目錄
except NameError:
    _SPEC_DIR = os.path.abspath(os.path.dirname("."))
BACKEND = os.path.abspath(os.path.join(_SPEC_DIR, "..", "..", "backend"))

datas, binaries, hiddenimports = [], [], []

# 需要連同子模組／資料／二進位一起收集的套件
_PKGS = [
    "fastapi", "starlette", "anyio", "sniffio", "click", "h11",
    "uvicorn", "websockets", "watchfiles", "httptools",
    "slowapi", "handright", "PIL", "cv2", "sklearn", "scipy",
    "numpy", "fitz", "PyPDF2", "docx", "pypandoc", "dotenv",
    "multipart", "jinja2", "markupsafe", "werkzeug", "sentry_sdk",
    "psutil", "schedule",
]
for _pkg in _PKGS:
    try:
        d, b, h = collect_all(_pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception as exc:  # 套件名在某些平台可能不同，略過即可
        print("collect_all skip:", _pkg, exc)

# uvicorn 以字串動態載入協定/事件迴圈實作，務必全帶上
hiddenimports += collect_submodules("uvicorn")
hiddenimports += [
    "uvicorn.lifespan.on",
    "uvicorn.loops.auto",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.websockets.auto",
    "sentry_sdk.integrations.fastapi",
    "sentry_sdk.integrations.starlette",
]

# 本地相依模組（與 app.py 同目錄）
hiddenimports += ["app", "pdf", "identify", "task_store", "task_types", "schedule_clean"]

a = Analysis(
    [os.path.join(BACKEND, "run_server.py")],
    pathex=[BACKEND],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "PyQt5", "PySide2", "PySide6", "PyQt6"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="handwrite-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,          # 由 Electron 擷取 stdout/stderr，不會跳出視窗
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,      # 跟隨建置機器架構（Apple Silicon 產 arm64）
    codesign_identity=None,
    entitlements_file=None,
)
