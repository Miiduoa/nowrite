"""
離線桌面版後端入口（由 Electron 以 sidecar 方式啟動）。

重點：
- app.py 於 import 時就會開啟 logs/app.log，並以相對路徑寫 temp/ 等，
  因此必須先確保「可寫的工作目錄」存在並 chdir 進去，再 import app。
- 資料（SQLite tasks.db、結果檔、字型、暫存）統一寫到 HW_DATA_DIR。
環境變數（由 Electron 傳入；命令列直接執行時亦有合理預設）：
  HW_DATA_DIR             可寫資料目錄（預設 = 當前工作目錄）
  HW_HOST / HW_PORT       監聽位址（預設 127.0.0.1:5005）
  FONT_ASSETS_DIR         可寫字型目錄（預設 = HW_DATA_DIR/fonts）
  FONT_ASSETS_BUNDLED_DIR 內建字型來源（啟動時會同步到 FONT_ASSETS_DIR）
"""
import os
import pathlib

# 1) 決定可寫資料目錄
_data_dir = os.environ.get("HW_DATA_DIR") or os.getcwd()
os.environ["HW_DATA_DIR"] = _data_dir

# 2) 預建必要子目錄（app.py 啟動時需要）
for _sub in ("logs", "temp", "fonts"):
    pathlib.Path(_data_dir, _sub).mkdir(parents=True, exist_ok=True)

# 3) 預設字型目錄指向可寫位置
os.environ.setdefault("FONT_ASSETS_DIR", str(pathlib.Path(_data_dir, "fonts")))

# 4) 切換到可寫工作目錄（app.py 以相對路徑開 logs/app.log、temp/ 等）
os.chdir(_data_dir)

# 5) 載入 FastAPI app（此時 import 副作用都會落在可寫目錄）
import uvicorn  # noqa: E402
from app import app  # noqa: E402


def main():
    host = os.environ.get("HW_HOST", "127.0.0.1")
    port = int(os.environ.get("HW_PORT", "5005"))
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
