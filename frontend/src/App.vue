<template>
  <!-- 液態玻璃折射背景：固定在最底層，供上層玻璃面板折射 -->
  <div class="app-bg" aria-hidden="true">
    <span class="blob b1"></span>
    <span class="blob b2"></span>
    <span class="blob b3"></span>
    <span class="blob b4"></span>
    <span class="grain"></span>
  </div>

  <!-- 開場動畫 -->
  <transition name="splash-fade">
    <BookSplash v-if="showSplash" @complete="showSplash = false" />
  </transition>

  <!-- 全域玻璃導航欄 -->
  <AppHeader />

  <!-- 路由內容 -->
  <main class="app-main">
    <router-view />
  </main>

  <PWAInstallPrompt />
</template>

<script>
import PWAInstallPrompt from './components/PWAInstallPrompt.vue';
import BookSplash from './components/BookSplash.vue';
import AppHeader from './components/AppHeader.vue';
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useHead } from '@vueuse/head';

export default {
  name: 'App',
  components: {
    PWAInstallPrompt,
    BookSplash,
    AppHeader,
  },
  data() {
    return {
      showSplash: !localStorage.getItem('bookSplashShown'),
    };
  },
  setup() {
    const route = useRoute();
    const site = 'https://handwrite.sixiangjia.de';
    const defaultTitle = '手寫文字生成網站 - 線上生成手寫圖片與 PDF';
    const defaultDesc = '手寫文字生成網站，支援多種字型和背景，線上生成高質量手寫文字圖片與 PDF。適合作業、論文、信件等場景，支援自定義字型、背景與參數調節。';

    const title = computed(() => route.meta?.title || defaultTitle);
    const description = computed(() => route.meta?.description || defaultDesc);
    const robots = computed(() => route.meta?.robots || 'index, follow');
    const canonical = computed(() => site + route.fullPath);

    useHead(() => ({
      title: title.value,
      meta: [
        { name: 'description', content: description.value },
        { name: 'robots', content: robots.value },
        { property: 'og:type', content: 'website' },
        { property: 'og:url', content: canonical.value },
        { property: 'og:title', content: title.value },
        { property: 'og:description', content: description.value },
        { property: 'og:image', content: '/default1.webp' },
        { property: 'twitter:card', content: 'summary_large_image' },
        { property: 'twitter:url', content: canonical.value },
        { property: 'twitter:title', content: title.value },
        { property: 'twitter:description', content: description.value },
        { property: 'twitter:image', content: '/default1.webp' },
      ],
      link: [
        { rel: 'canonical', href: canonical.value },
      ],
    }));

    return {};
  },
};
</script>

<style>
/* App 級佈局（非 scoped，提供給全站） */
#app {
  min-height: 100vh;
}

.app-main {
  max-width: 1180px;
  margin: 0 auto;
  padding: 96px 22px 64px;
  box-sizing: border-box;
}

@media (max-width: 640px) {
  .app-main {
    padding: 84px 14px 48px;
  }
}

/* ── 折射背景 ── */
.app-bg {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  background: var(--bg-base);
  transition: background-color 0.6s ease;
}

.app-bg .blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.9;
  will-change: transform;
}
.app-bg .b1 {
  width: 46vw;
  height: 46vw;
  left: -8vw;
  top: -10vh;
  background: var(--blob-1);
  animation: drift1 26s ease-in-out infinite alternate;
}
.app-bg .b2 {
  width: 40vw;
  height: 40vw;
  right: -10vw;
  top: 4vh;
  background: var(--blob-2);
  animation: drift2 30s ease-in-out infinite alternate;
}
.app-bg .b3 {
  width: 44vw;
  height: 44vw;
  left: 14vw;
  bottom: -18vh;
  background: var(--blob-3);
  animation: drift3 34s ease-in-out infinite alternate;
}
.app-bg .b4 {
  width: 34vw;
  height: 34vw;
  right: 6vw;
  bottom: -12vh;
  background: var(--blob-4);
  animation: drift1 38s ease-in-out infinite alternate-reverse;
}

/* 紙張顆粒 */
.app-bg .grain {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: var(--grain);
  mix-blend-mode: soft-light;
  pointer-events: none;
}

@keyframes drift1 {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(6vw, 5vh) scale(1.12); }
}
@keyframes drift2 {
  0% { transform: translate(0, 0) scale(1.05); }
  100% { transform: translate(-7vw, 6vh) scale(0.95); }
}
@keyframes drift3 {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(5vw, -6vh) scale(1.1); }
}

/* 開場淡出 */
.splash-fade-leave-active {
  transition: opacity 0.5s ease;
}
.splash-fade-leave-to {
  opacity: 0;
}
</style>
