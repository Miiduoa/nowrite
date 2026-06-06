<template>
  <div class="intro">
    <section class="intro-hero">
      <span class="eyebrow">✦ 關於本站</span>
      <h1 class="intro-title">手寫文字生成網站</h1>
      <p class="intro-lead">
        歡迎來到我的手寫文字生成網站！這個平臺允許你使用現有的字型來建立模擬手寫文字的圖片。
      </p>
      <a class="intro-url link-accent" href="https://handwrite.sixiangjia.de">handwrite.sixiangjia.de</a>
    </section>

    <h2 class="section-title">功能</h2>
    <div class="feature-grid">
      <article class="feature glass">
        <div class="feature-ico">🖋️</div>
        <h3>自定義字型</h3>
        <p>你可以上傳自己的字型來生成符合你需求的獨特手寫風格。</p>
      </article>
      <article class="feature glass">
        <div class="feature-ico">🖼️</div>
        <h3>背景圖片</h3>
        <p>上傳你想要的背景圖片為手寫文字添加個人風格。沒有背景圖？只需指定寬度和高度，網站會自動生成帶橫線的背景。</p>
      </article>
      <article class="feature glass">
        <div class="feature-ico">🎚️</div>
        <h3>可調參數</h3>
        <p>完全控制邊距（上下左右）、字元隨機擾動、筆畫旋轉偏移、墨水深度變化與塗改痕跡，精細微調手寫外觀。</p>
      </article>
      <article class="feature glass">
        <div class="feature-ico">📄</div>
        <h3>多格式文本提取</h3>
        <p>可從 PDF、Word 等多種檔案型別中提取文本內容，讓你方便地上傳文字。</p>
      </article>
      <article class="feature glass">
        <div class="feature-ico">👁️</div>
        <h3>即時預覽</h3>
        <p>右側的預覽功能讓你在最終確定之前，方便地檢視手寫文字圖片的效果。</p>
      </article>
      <article class="feature glass">
        <div class="feature-ico">🗂️</div>
        <h3>完整圖片生成</h3>
        <p>對預覽滿意後即可生成整套圖片，並自動打包成 zip 檔案，便於下載。</p>
      </article>
      <article class="feature glass">
        <div class="feature-ico">📑</div>
        <h3>PDF 匯出</h3>
        <p>一鍵生成 PDF，不用再手動貼上圖片。</p>
      </article>
    </div>

    <section class="panel glass selfhost">
      <h2 class="section-title">自己搭建的方法</h2>
      <p>克隆專案，在專案目錄中執行 <code>docker-compose up -d</code>，預設埠為 <code>2345</code>。</p>
      <p>若要新增字型，將字型檔案放在專案根目錄下的 <code>ttf_files</code> 中即可。</p>
    </section>

    <section class="intro-outro">
      <p>希望你喜歡用它來建立屬於你的個性化手寫文字圖片！</p>
    </section>
  </div>
</template>

<script>
export default {
  name: 'IntroduceComponent',
}
</script>

<style scoped>
.intro {
  max-width: 920px;
  margin: 0 auto;
}

.intro-hero {
  text-align: center;
  margin-bottom: 34px;
}
.intro-hero .eyebrow {
  justify-content: center;
  margin-bottom: 12px;
}
.intro-title {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  letter-spacing: 1px;
  color: var(--ink);
  margin: 0 0 12px;
}
.intro-lead {
  color: var(--ink-soft);
  font-size: 1.05rem;
  line-height: 1.7;
  max-width: 640px;
  margin: 0 auto 12px;
}
.intro-url {
  font-weight: 600;
}

.section-title {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 1.4rem;
  letter-spacing: 1px;
  color: var(--ink);
  margin: 28px 0 16px;
  text-align: center;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}
.feature {
  padding: 22px;
}
.feature-ico {
  font-size: 26px;
  margin-bottom: 10px;
}
.feature h3 {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 8px;
}
.feature p {
  color: var(--ink-soft);
  font-size: 0.92rem;
  line-height: 1.65;
  margin: 0;
}

.selfhost {
  margin-top: 28px;
  padding: 26px;
  text-align: center;
}
.selfhost p {
  color: var(--ink-soft);
  line-height: 1.8;
  margin: 6px 0;
}
.selfhost code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  background: var(--accent-soft);
  color: var(--accent);
  padding: 2px 8px;
  border-radius: 7px;
  font-size: 0.9em;
}

.intro-outro {
  text-align: center;
  color: var(--ink-soft);
  margin: 30px 0 6px;
  font-size: 1.02rem;
}
</style>
