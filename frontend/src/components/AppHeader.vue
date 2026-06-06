<template>
  <header class="hdr glass glass-strong">
    <!-- 品牌 -->
    <router-link to="/" class="brand" :aria-label="$t('message.home')">
      <span class="brand-mark">
        <img src="/favicon-96x96.png" alt="" />
      </span>
      <span class="brand-text">
        <span class="brand-cn">手寫生成</span>
        <span class="brand-en">Handwriting</span>
      </span>
    </router-link>

    <!-- 導覽 -->
    <nav class="nav">
      <router-link to="/" class="nav-link">{{ $t('message.home') }}</router-link>
      <router-link to="/Introduce" class="nav-link">{{ $t('message.introduce') }}</router-link>
      <router-link to="/Feedback" class="nav-link">{{ $t('message.feedback') }}</router-link>
    </nav>

    <!-- 控制：語言 + 明暗 -->
    <div class="controls">
      <div class="seg" role="group" aria-label="Language">
        <button class="seg-btn" :class="{ active: lang === 'tw' }" @click="setLang('tw')">繁</button>
        <button class="seg-btn" :class="{ active: lang === 'cn' }" @click="setLang('cn')">简</button>
        <button class="seg-btn" :class="{ active: lang === 'en' }" @click="setLang('en')">EN</button>
      </div>

      <button class="theme-btn" :title="themeLabel" :aria-label="themeLabel" @click="cycleTheme">
        <!-- auto -->
        <svg v-if="theme === 'auto'" viewBox="0 0 24 24" width="19" height="19">
          <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7" />
          <path d="M12 3a9 9 0 0 0 0 18Z" fill="currentColor" />
        </svg>
        <!-- light -->
        <svg v-else-if="theme === 'light'" viewBox="0 0 24 24" width="19" height="19" fill="none"
          stroke="currentColor" stroke-width="1.7" stroke-linecap="round">
          <circle cx="12" cy="12" r="4.2" />
          <path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5 5l1.6 1.6M17.4 17.4 19 19M19 5l-1.6 1.6M6.6 17.4 5 19" />
        </svg>
        <!-- dark -->
        <svg v-else viewBox="0 0 24 24" width="19" height="19">
          <path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a6.8 6.8 0 0 0 9.8 9.8Z" fill="currentColor" />
        </svg>
      </button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      theme: 'auto',
      lang: 'tw',
    };
  },
  computed: {
    themeLabel() {
      const map = { auto: '主題：自動', light: '主題：淺色', dark: '主題：深色' };
      return map[this.theme] || '主題';
    },
  },
  created() {
    // 主題：與 index.html 的初始化保持一致
    this.theme = document.documentElement.getAttribute('data-theme') || 'auto';
    // 語言：預設繁體中文
    const savedLang = localStorage.getItem('hw-lang');
    if (savedLang === 'tw' || savedLang === 'cn' || savedLang === 'en') {
      this.lang = savedLang;
    } else {
      this.lang = 'tw';
    }
    this.$i18n.locale = this.lang;
  },
  mounted() {
    // 當處於「自動」時，跟隨系統切換即時更新底色
    if (window.matchMedia) {
      this.mq = window.matchMedia('(prefers-color-scheme: dark)');
      this.onMq = () => {
        if (this.theme === 'auto') this.syncRootColor('auto');
      };
      this.mq.addEventListener
        ? this.mq.addEventListener('change', this.onMq)
        : this.mq.addListener(this.onMq);
    }
  },
  beforeUnmount() {
    if (this.mq && this.onMq) {
      this.mq.removeEventListener
        ? this.mq.removeEventListener('change', this.onMq)
        : this.mq.removeListener(this.onMq);
    }
  },
  methods: {
    setLang(l) {
      this.lang = l;
      this.$i18n.locale = l;
      try { localStorage.setItem('hw-lang', l); } catch (e) { /* ignore */ }
    },
    cycleTheme() {
      const order = ['auto', 'light', 'dark'];
      const next = order[(order.indexOf(this.theme) + 1) % order.length];
      this.theme = next;
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('hw-theme', next); } catch (e) { /* ignore */ }
      this.syncRootColor(next);
    },
    syncRootColor(pref) {
      const root = document.documentElement;
      const dark =
        pref === 'dark' ||
        (pref === 'auto' &&
          window.matchMedia &&
          window.matchMedia('(prefers-color-scheme: dark)').matches);
      root.style.background = dark ? '#16181d' : '#f4f5f7';
      root.style.colorScheme = dark ? 'dark' : 'light';
    },
  },
};
</script>

<style scoped>
.hdr {
  position: fixed;
  top: 14px;
  left: 50%;
  transform: translateX(-50%);
  width: min(1180px, calc(100% - 28px));
  z-index: 1200;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 9px 14px 9px 12px;
  border-radius: var(--r-pill);
}

/* 品牌 */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--ink);
  flex: 0 0 auto;
}
.brand-mark {
  width: 36px;
  height: 36px;
  border-radius: 11px;
  display: grid;
  place-items: center;
  background: var(--glass-bg-strong);
  border: 1px solid var(--glass-edge);
  box-shadow: inset 0 1px 0 var(--glass-hi);
  overflow: hidden;
}
.brand-mark img {
  width: 24px;
  height: 24px;
  object-fit: contain;
}
.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.05;
}
.brand-cn {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 1.06rem;
  letter-spacing: 2px;
  color: var(--ink);
}
.brand-en {
  font-size: 0.62rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--ink-faint);
}

/* 導覽 */
.nav {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0 auto;
}
.nav-link {
  position: relative;
  padding: 7px 14px;
  border-radius: var(--r-pill);
  color: var(--ink-soft);
  font-weight: 600;
  font-size: 0.92rem;
  transition: color 0.2s ease, background 0.2s ease;
}
.nav-link:hover {
  color: var(--ink);
  background: var(--accent-soft);
}
.nav-link.router-link-exact-active {
  color: var(--accent);
}
.nav-link.router-link-exact-active::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 2px;
  transform: translateX(-50%);
  width: 16px;
  height: 3px;
  border-radius: 3px;
  background: var(--accent);
}

/* 控制區 */
.controls {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 0 0 auto;
}

.seg {
  display: inline-flex;
  padding: 3px;
  border-radius: var(--r-pill);
  background: var(--field-bg);
  border: 1px solid var(--field-edge);
}
.seg-btn {
  border: none;
  background: transparent;
  color: var(--ink-soft);
  font-weight: 700;
  font-size: 0.8rem;
  padding: 5px 10px;
  border-radius: var(--r-pill);
  cursor: pointer;
  transition: all 0.2s ease;
}
.seg-btn.active {
  background: var(--btn-primary-bg);
  color: var(--btn-primary-fg);
  box-shadow: 0 2px 8px rgba(23, 26, 32, 0.22);
}

.theme-btn {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  border: 1px solid var(--field-edge);
  background: var(--field-bg);
  color: var(--ink);
  cursor: pointer;
  transition: transform 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}
.theme-btn:hover {
  transform: rotate(-12deg);
  color: var(--accent);
  border-color: var(--accent-ring);
}

/* 響應式 */
@media (max-width: 760px) {
  .hdr {
    flex-wrap: wrap;
    border-radius: var(--r-lg);
    row-gap: 6px;
  }
  .nav {
    order: 3;
    width: 100%;
    margin: 2px 0 0;
    justify-content: center;
  }
  .brand { margin-right: auto; }
}
@media (max-width: 400px) {
  .brand-en { display: none; }
  .nav-link { padding: 6px 10px; font-size: 0.86rem; }
}
</style>
