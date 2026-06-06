// 預載腳本：把本機後端位址注入到前端 window（contextIsolation 下需用 contextBridge）
const { contextBridge } = require("electron");

const API_BASE = "http://127.0.0.1:5005";

try {
  contextBridge.exposeInMainWorld("__HW_API_BASE__", API_BASE);
  contextBridge.exposeInMainWorld("HW_DESKTOP", true);
} catch (e) {
  // 若停用了 contextIsolation，退而直接掛到 window
  // eslint-disable-next-line no-undef
  window.__HW_API_BASE__ = API_BASE;
}
