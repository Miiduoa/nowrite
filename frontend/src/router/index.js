import { createRouter, createWebHistory, createWebHashHistory } from "vue-router";
import Home from "../views/HomeView.vue";
import Login from "../views/UserLogin.vue";
import Register from "../views/UserRegister.vue";
import UserFeedback from "@/components/UserFeedback";
import IntroduceComponent from "@/components/Introduce";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      title: "手寫文字生成網站 - 線上生成手寫圖片與 PDF",
      description:
        "手寫文字生成網站，支援多種字型和背景，線上生成高質量手寫文字圖片與 PDF。適合作業、論文、信件等場景，支援自定義字型、背景與參數調節。",
      robots: "index, follow",
    },
  },
  {
    path: "/About",
    name: "About",
    component: () => import("../views/AboutView.vue"),
    meta: {
      title: "關於 - 手寫文字生成網站",
      description: "關於本網站與功能介紹、使用方法及隱私說明。",
      robots: "index, follow",
    },
  },
  {
    path: "/Login",
    name: "Login",
    component: Login,
    meta: {
      title: "登入 - 手寫文字生成網站",
      description: "登入您的賬戶以使用更多功能。",
      robots: "noindex, nofollow",
    },
  },
  {
    path: "/Register",
    name: "Register",
    component: Register,
    meta: {
      title: "註冊 - 手寫文字生成網站",
      description: "註冊賬戶，開始生成個性化手寫圖片與 PDF。",
      robots: "noindex, nofollow",
    },
  },
  {
    path: "/Feedback",
    name: "Feedback",
    component: UserFeedback,
    meta: {
      title: "使用者反饋 - 手寫文字生成網站",
      description: "提交您的意見與建議，幫助我們改進產品。",
      robots: "index, follow",
    },
  },
  {
    path: "/Introduce",
    name: "Introduce",
    component: IntroduceComponent,
    meta: {
      title: "功能介紹 - 手寫文字生成網站",
      description: "瞭解網站核心功能、參數配置與使用技巧。",
      robots: "index, follow",
    },
  },
];

const router = createRouter({
  // 桌面（Electron file://）用 hash 路由；網頁版維持 history 路由
  history:
    process.env.VUE_APP_TARGET === "desktop"
      ? createWebHashHistory()
      : createWebHistory(process.env.BASE_URL),
  routes,
});

router.afterEach(() => {
  const routerViewElement = document.querySelector("router-view");
  if (routerViewElement) {
    routerViewElement.scrollIntoView({ behavior: "smooth", block: "start" });
  }
});

export default router;

