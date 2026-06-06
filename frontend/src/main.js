import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import "bootstrap";
// 液態毛玻璃設計系統（在 bootstrap 之後引入以覆蓋其預設樣式）
import "./assets/theme.css";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import i18n from "./i18n";
import axios from "axios";
import axiosRetry from "axios-retry";
import Clarity from "@microsoft/clarity";
// eslint-disable-next-line no-unused-vars
import Swal from "sweetalert2";
import { createHead } from "@vueuse/head";

import * as Sentry from "@sentry/vue";

// import Viewer from "v-viewer";H
// import "viewerjs/dist/viewer.css";

const app = createApp(App);
const head = createHead();

// 桌面（離線）版旗標：preload 會注入 window.__HW_API_BASE__
const __isDesktop = typeof window !== "undefined" && !!window.__HW_API_BASE__;

// 啟動期致命錯誤就地顯示（避免整頁空白，方便診斷）
function __hwShowFatal(msg) {
  try {
    const el = document.getElementById("app") || document.body;
    el.innerHTML =
      '<pre style="white-space:pre-wrap;padding:24px;margin:0;font:13px/1.6 -apple-system,Menlo,monospace;color:#c0392b">啟動發生錯誤 / Startup error:\n\n' +
      String(msg) +
      "</pre>";
  } catch (e) {
    /* ignore */
  }
}
window.addEventListener("error", (e) =>
  __hwShowFatal((e && e.error && e.error.stack) || (e && e.message) || e)
);
window.addEventListener("unhandledrejection", (e) =>
  __hwShowFatal((e && e.reason && e.reason.stack) || (e && e.reason) || e)
);

// 外部分析與 Sentry 只在網頁版啟用；離線桌面版略過（避免初始化失敗造成白屏）
if (!__isDesktop) {
// 非同步載入Google Analytics的JavaScript庫
const script = document.createElement("script");
script.async = true;
script.src = "https://www.googletagmanager.com/gtag/js?id=G-GB1XG89B6Z";
document.head.appendChild(script);

// 當指令碼載入完成後進行初始化
script.onload = () => {
  console.log("Clarity已經載入");
  const projectId = "ounxp8da5s";
  Clarity.init(projectId);
  // 初始化window.dataLayer陣列
  window.dataLayer = window.dataLayer || [];

  // 定義gtag函式
  function gtag() {
    window.dataLayer.push(arguments);
  }

  // 呼叫gtag函式進行配置
  gtag("js", new Date());
  gtag("config", "G-GB1XG89B6Z");

  (function (c, l, a, r, i, t, y) {
    c[a] =
      c[a] ||
      function () {
        (c[a].q = c[a].q || []).push(arguments);
      };
    t = l.createElement(r);
    t.async = 1;
    t.src = "https://www.clarity.ms/tag/" + i;
    y = l.getElementsByTagName(r)[0];
    y.parentNode.insertBefore(t, y);
  })(window, document, "clarity", "script", "ounxp8da5s");
};

const chatwootScript = document.createElement("script");
chatwootScript.async = true;
chatwootScript.defer = true;
chatwootScript.src = "https://chatwoot.14790897.xyz/packs/js/sdk.js";
chatwootScript.onload = () => {
  if (window.chatwootSDK) {
    window.chatwootSDK.run({
      websiteToken: "LqgSJHw9boXsan69qwxSs8eg",
      baseUrl: "https://chatwoot.14790897.xyz",
    });
  }
};
document.head.appendChild(chatwootScript);

Sentry.init({
  app,
  dsn: "https://507b601bbd374cf58b7c5468cb434578@o4505255803551744.ingest.sentry.io/4505485557891072",
  integrations: [
    new Sentry.BrowserTracing({
      // Set `tracePropagationTargets` to control for which URLs distributed tracing should be enabled
      tracePropagationTargets: ["localhost", /^https:\/\/yourserver\.io\/api/],
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
    }),
    new Sentry.Replay(),
  ],
  // Performance Monitoring
  tracesSampleRate: 1.0, // Capture 100% of the transactions, reduce in production!
  // Session Replay
  replaysSessionSampleRate: 0.1, // This sets the sample rate at 10%. You may want to change it to 100% while in development and then sample at a lower rate in production.
  replaysOnErrorSampleRate: 1.0, // If you're not already sampling the entire session, change the sample rate to 100% when sampling sessions where errors occur.
});
} // end if (!__isDesktop) — 離線桌面版略過外部分析與 Sentry

// const DEFAULT_TITLE = "handwrite";

// router.afterEach((to) => {
//   app.nextTick(() => {
//     document.title = to.meta.title || DEFAULT_TITLE;
//   });
// });

app.use(store);
app.use(router);
app.use(i18n);
app.use(head);

// 配置自動重試：網路錯誤 或 5xx 響應自動重試，最多 3 次，指數退避
axiosRetry(axios, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay, // 1s → 2s → 4s
  retryCondition: (error) => {
    // 503 queue_full 是業務狀態，不需要重試
    if (
      error.response?.status === 503 &&
      error.response?.data?.status === "queue_full"
    ) {
      return false;
    }
    // 網路錯誤 或 5xx 服務端錯誤時重試
    return (
      axiosRetry.isNetworkError(error) ||
      axiosRetry.isRetryableError(error)
    );
  },
  onRetry: (retryCount, error) => {
    console.warn(`請求重試第 ${retryCount} 次，原因：${error.message}`);
  },
});

// 桌面（離線）版：preload 會注入本機後端位址，讓所有 /api 請求指向內嵌後端
if (typeof window !== "undefined" && window.__HW_API_BASE__) {
  axios.defaults.baseURL = window.__HW_API_BASE__;
}

app.config.globalProperties.$http = axios;
app.config.globalProperties.$swal = Swal;
// const http = axios.create({
//   baseURL: "https://testhand.liuweiqing.top",
// });

// app.config.globalProperties.$http = http;

// app.use(Viewer);

try {
  app.mount("#app");
} catch (err) {
  __hwShowFatal((err && err.stack) || err);
}

// Service Worker 版本更新提示
if ("serviceWorker" in navigator) {
  window.addEventListener("load", async () => {
    try {
      // 登出舊版 /sw.js
      const registrations = await navigator.serviceWorker.getRegistrations();
      for (const reg of registrations) {
        if (reg.active?.scriptURL?.includes("sw.js")) {
          await reg.unregister();
        }
      }

      // 監聽新版本啟用，提示使用者重新整理
      navigator.serviceWorker.addEventListener("controllerchange", () => {
        if (confirm("網站已更新到新版本，點選確定重新整理頁面以載入最新內容。")) {
          window.location.reload();
        }
      });
    } catch (error) {
      console.error("[SW] 初始化失敗:", error);
    }
  });
}
