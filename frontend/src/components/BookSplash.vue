<template>
  <transition name="splash-fade">
    <div v-if="visible" class="splash" @click="skipAnimation">
      <div class="splash-inner" :class="{ show: showBrand }">
        <div class="logo">
          <img src="/favicon-96x96.png" alt="logo" />
        </div>
        <div class="word">
          <span class="word-cn">手寫生成</span>
          <span class="word-en">Handwriting Studio</span>
        </div>
        <div class="line" :class="{ grow: bookOpen }"></div>
      </div>
      <div class="skip">點選任意處跳過</div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'BookSplash',
  data() {
    return {
      visible: true,
      bookOpen: false,
      showBrand: false,
    };
  },
  /**
   * 極簡品牌開場：標誌與字標淡入縮放、細線展開，
   * 結束後記錄 localStorage 並觸發 complete。
   */
  mounted() {
    setTimeout(() => { this.showBrand = true; }, 150);
    setTimeout(() => { this.bookOpen = true; }, 650);
    setTimeout(() => {
      localStorage.setItem('bookSplashShown', '1');
      this.visible = false;
      this.$emit('complete');
    }, 2400);
  },
  methods: {
    skipAnimation() {
      localStorage.setItem('bookSplashShown', '1');
      this.visible = false;
      this.$emit('complete');
    },
  },
};
</script>

<style scoped>
.splash {
  position: fixed;
  inset: 0;
  z-index: 9999;
  cursor: pointer;
  overflow: hidden;
  background: var(--bg-base);
  display: flex;
  align-items: center;
  justify-content: center;
}

.splash-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 22px;
  opacity: 0;
  transform: translateY(10px) scale(0.98);
  transition: opacity 0.7s ease, transform 0.7s cubic-bezier(0.22, 1, 0.36, 1);
}
.splash-inner.show {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.logo {
  width: 76px;
  height: 76px;
  border-radius: 20px;
  display: grid;
  place-items: center;
  background: var(--glass-bg-strong);
  border: 1px solid var(--glass-edge);
  box-shadow: var(--glass-shadow), inset 0 1px 0 var(--glass-hi);
  -webkit-backdrop-filter: blur(18px) saturate(150%);
  backdrop-filter: blur(18px) saturate(150%);
}
.logo img {
  width: 46px;
  height: 46px;
  object-fit: contain;
}

.word {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.word-cn {
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 30px;
  letter-spacing: 6px;
  color: var(--ink);
}
.word-en {
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.34em;
  text-transform: uppercase;
  color: var(--ink-faint);
}

.line {
  width: 0;
  height: 2px;
  border-radius: 2px;
  background: var(--accent);
  transition: width 0.9s cubic-bezier(0.22, 1, 0.36, 1);
}
.line.grow {
  width: 64px;
}

.skip {
  position: fixed;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  letter-spacing: 0.08em;
  color: var(--ink-faint);
  pointer-events: none;
}

.splash-fade-leave-active {
  transition: opacity 0.5s ease;
}
.splash-fade-leave-to {
  opacity: 0;
}
</style>
