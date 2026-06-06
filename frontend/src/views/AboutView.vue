<template>
  <div class="about-wrap">
    <section class="about-card glass">
      <span class="eyebrow">✦ About</span>
      <h1 class="about-title">手寫文字生成</h1>
      <p class="about-text">
        一個免費、開源的線上工具：用現有字型把文字渲染成自然的手寫效果，支援自定義字型、背景、版面參數，並可匯出圖片或 PDF。
      </p>
      <div class="about-actions">
        <router-link to="/" class="btn-ink">開始生成</router-link>
        <router-link to="/Introduce" class="btn-glass">功能介紹</router-link>
        <a href="https://github.com/Miiduoa/nowrite" target="_blank" class="btn-glass">GitHub</a>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
}
</script>

<style scoped>
.about-wrap {
  display: grid;
  place-items: center;
  min-height: 60vh;
}
.about-card {
  width: 100%;
  max-width: 560px;
  padding: 38px;
  text-align: center;
}
.about-card .eyebrow {
  justify-content: center;
}
.about-title {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 2rem;
  letter-spacing: 2px;
  color: var(--ink);
  margin: 12px 0 14px;
}
.about-text {
  color: var(--ink-soft);
  line-height: 1.8;
  margin: 0 0 24px;
}
.about-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
