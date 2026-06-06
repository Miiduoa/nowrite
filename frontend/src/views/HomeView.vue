<template>
  <div class="home">
    <!-- 頂部簡介 -->
    <section class="hero">
      <span class="eyebrow">✦ 手寫文字生成</span>
      <h1 class="hero-title">把文字，寫成<span class="accent">手寫</span>。</h1>
      <p class="hero-sub">上傳字型與背景，調好版面，一鍵生成手寫圖片或 PDF。</p>
    </section>

    <!-- 全域提示（保留原行為） -->
    <div id="message" class="msg-area">
      <div v-if="message" class="alert alert-info" role="alert">{{ message }}</div>
      <div v-if="uploadMessage" class="alert alert-info" role="alert">{{ uploadMessage }}</div>
    </div>

    <div class="layout">
      <!-- 左側：控制面板 -->
      <div class="col-controls" id="form">

        <!-- 輸入內容 -->
        <section class="panel glass">
          <div class="panel-head">
            <span class="eyebrow">01 · 內容</span>
            <h2 class="panel-title">輸入內容</h2>
          </div>
          <TextInput @childEvent="(eventData) => { this.text = eventData }"></TextInput>
        </section>

        <!-- 字型與背景 -->
        <section class="panel glass">
          <div class="panel-head">
            <span class="eyebrow">02 · 素材</span>
            <h2 class="panel-title">字型與背景</h2>
          </div>

          <div class="field-row">
            <label class="field-label">{{ $t('message.fontFile') }}</label>
            <div class="picker">
              <button class="btn-glass btn-pick" @click="triggerFontFileInput">{{ $t('message.chooseFile') }}</button>
              <input type="file" ref="fontFileInput" @change="onFontChange" hidden />
              <select v-model="selectedOption" class="glass-field select-font">
                <option v-for="option in options" :value="option.value" :key="option.value">
                  {{ option.text }}
                </option>
              </select>
            </div>
          </div>

          <div class="field-row">
            <label class="field-label">{{ $t('message.backgroundImageFile') }}</label>
            <div class="picker bg-picker">
              <button class="btn-glass btn-pick" :class="{ 'is-disabled': isDimensionSpecified }"
                :title="isDimensionSpecified ? $t('message.widthAndHeightSpecified') : ''"
                @click="triggerImageFileInput">
                {{ $t('message.chooseFile') }}
                <span v-if="selectedImageFileName" class="clear-x" @click.stop="clearImage" aria-label="clear">×</span>
              </button>
              <span class="file-name" v-if="selectedImageFileName">{{ selectedImageFileName }}</span>
              <input type="file" ref="imageFileInput" @change="onBackgroundImageChange" hidden />
            </div>
            <div v-if="isLoading" class="inline-loader"><span class="spin"></span>{{ $t('message.loading') }}…</div>
          </div>
        </section>

        <!-- 版面尺寸 -->
        <section class="panel glass">
          <div class="panel-head">
            <span class="eyebrow">03 · 畫布</span>
            <h2 class="panel-title">版面尺寸</h2>
          </div>
          <div class="grid-2">
            <label class="ifield">
              <span class="ifield-label">{{ $t('message.width') }}</span>
              <input type="number" v-model="width" :disabled="isBackgroundImageSpecified"
                :title="isBackgroundImageSpecified ? $t('message.backgroundImageSpecified') : ''" class="glass-field" />
            </label>
            <label class="ifield">
              <span class="ifield-label">{{ $t('message.height') }}</span>
              <div class="with-clear">
                <input type="number" v-model="height" :disabled="isBackgroundImageSpecified"
                  :title="isBackgroundImageSpecified ? $t('message.backgroundImageSpecified') : ''" class="glass-field" />
                <button type="button" class="mini-x" aria-label="Close" @click="clearDimensions">×</button>
              </div>
            </label>
          </div>

          <div class="toggles">
            <label class="switch">
              <input type="checkbox" id="optionUnderline" v-model="isUnderlined" />
              <span class="switch-track"><span class="switch-thumb"></span></span>
              <span class="switch-text">增加下劃線</span>
            </label>
            <label class="switch">
              <input type="checkbox" id="optionEnglishSpacing" v-model="enableEnglishSpacing" />
              <span class="switch-track"><span class="switch-thumb"></span></span>
              <span class="switch-text">{{ $t('message.enableEnglishSpacing') }}</span>
            </label>
          </div>
        </section>

        <!-- 排版參數 -->
        <section class="panel glass">
          <div class="panel-head">
            <span class="eyebrow">04 · 排版</span>
            <h2 class="panel-title">排版參數</h2>
          </div>
          <div class="grid-2">
            <label class="ifield">
              <span class="ifield-label">{{ $t('message.fontSize') }}</span>
              <input type="number" v-model="fontSize" placeholder="recommend > 100" class="glass-field" />
            </label>
            <label class="ifield">
              <span class="ifield-label">{{ $t('message.lineSpacing') }}</span>
              <input type="number" v-model="lineSpacing" class="glass-field" />
            </label>
            <label class="ifield">
              <span class="ifield-label">{{ $t('message.topMargin') }}</span>
              <input type="number" v-model="marginTop" class="glass-field" />
            </label>
            <label class="ifield">
              <span class="ifield-label">{{ $t('message.bottomMargin') }}</span>
              <input type="number" v-model="marginBottom" class="glass-field" />
            </label>
            <label class="ifield">
              <span class="ifield-label">{{ $t('message.leftMargin') }}</span>
              <input type="number" v-model="marginLeft" class="glass-field" />
            </label>
            <label class="ifield">
              <span class="ifield-label">{{ $t('message.rightMargin') }}</span>
              <input type="number" v-model="marginRight" class="glass-field" />
            </label>
          </div>

          <button class="expand-btn" type="button" @click="toggleCollapse">
            <span>{{ $t('message.expand') }}</span>
            <svg :class="{ open: isExpanded }" class="chev" viewBox="0 0 24 24" width="16" height="16"
              fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m6 9 6 6 6-6" />
            </svg>
          </button>

          <transition name="collapse">
            <div v-if="isExpanded" id="collapseContent" class="advanced">
              <div class="grid-2">
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.lineSpacingSigma') }}</span>
                  <input type="number" v-model="lineSpacingSigma" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.fontSizeSigma') }}</span>
                  <input type="number" v-model="fontSizeSigma" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.wordSpacingSigma') }}</span>
                  <input type="number" v-model="wordSpacingSigma" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.perturbXSigma') }}</span>
                  <input type="number" v-model="perturbXSigma" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.perturbYSigma') }}</span>
                  <input type="number" v-model="perturbYSigma" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.perturbThetaSigma') }}</span>
                  <input type="number" v-model="perturbThetaSigma" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.wordSpacing') }}</span>
                  <input type="number" v-model="wordSpacing" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.strikethrough_length_sigma') }}</span>
                  <input type="text" v-model="strikethrough_length_sigma" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.strikethrough_angle_sigma') }}</span>
                  <input type="number" v-model="strikethrough_angle_sigma" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.strikethrough_width_sigma') }}</span>
                  <input type="number" v-model="strikethrough_width_sigma" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.strikethrough_probability') }}</span>
                  <input type="number" v-model="strikethrough_probability" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.strikethrough_width') }}</span>
                  <input type="number" v-model="strikethrough_width" class="glass-field" />
                </label>
                <label class="ifield">
                  <span class="ifield-label">{{ $t('message.ink_depth_sigma') }}</span>
                  <input type="number" v-model="ink_depth_sigma" class="glass-field" />
                </label>
              </div>
            </div>
          </transition>
        </section>

        <!-- 生成狀態 -->
        <div v-if="isGenerating || isInCooldownPeriod" class="generation-status">
          <div v-if="isGenerating" class="status-chip status-generating">🔄 正在生成中，請稍候…</div>
          <div v-else-if="isInCooldownPeriod" class="status-chip status-cooldown">⏳ 冷卻中，還需等待 {{ remainingCooldown }} 秒</div>
        </div>

        <!-- 動作 -->
        <section class="panel glass action-panel">
          <div class="actions-secondary">
            <button class="btn-glass" @click="loadPreset">{{ $t('message.loadSettings') }}</button>
            <button class="btn-glass" @click="savePreset">{{ $t('message.saveSettings') }}</button>
            <button class="btn-glass" @click="resetSettings">{{ $t('message.resetSettings') }}</button>
            <button v-if="isDevEnv" class="btn-glass" @click="toggleFullPreview" :disabled="shouldDisableButtons">
              本地全量預覽：{{ enableFullPreview ? '開' : '關' }}
            </button>
          </div>
          <div class="actions-primary">
            <button class="btn-ink" @click="generateHandwriting(preview = true)" :disabled="shouldDisableButtons">
              {{ buttonText || $t('message.preview') }}
            </button>
            <button class="btn-ink" @click="generateHandwriting(preview = false)" :disabled="shouldDisableButtons">
              {{ buttonText || $t('message.generateFullHandwritingImage') }}
            </button>
            <button class="btn-ink" @click="generateHandwriting(preview = false, pdf_save = true)" :disabled="shouldDisableButtons">
              {{ buttonText || $t('message.generatePdf') }}
            </button>
          </div>
          <router-link to="/Feedback" class="feedback-link">{{ $t('message.feedback') }} →</router-link>
        </section>

        <!-- 頁數提示 -->
        <div v-if="isProductionSite() && text && text.length > 0" class="page-info-alert">
          <div class="alert alert-warning">
            <strong>📄 頁數提示：</strong>
            預計生成 <strong>{{ estimatePageCount() }}</strong> 頁
            <span v-if="estimatePageCount() > 10" class="over-limit">
              （handwrite.14790897.xyz 限制一次最多 10 頁，超出部分將被截斷）
            </span>
          </div>
        </div>
      </div>

      <!-- 右側：預覽 -->
      <aside class="col-preview">
        <section class="panel glass preview">
          <div class="panel-head">
            <span class="eyebrow">預覽 · Preview</span>
            <h2 class="panel-title" v-if="!previewImages || previewImages.length === 0">{{ $t('message.preview') }}</h2>
          </div>

          <div class="preview-container">
            <div v-if="previewImages && previewImages.length > 1" class="pager">
              <button @click="prevPage" class="btn-glass pager-btn" :disabled="currentPreviewIndex === 0">← 上一頁</button>
              <span class="pager-info">第 {{ currentPreviewIndex + 1 }} 頁 / 共 {{ previewImages.length }} 頁</span>
              <button @click="nextPage" class="btn-glass pager-btn"
                :disabled="currentPreviewIndex === previewImages.length - 1">下一頁 →</button>
            </div>

            <div v-if="previewImages && previewImages.length > 0" class="preview-frame">
              <img :src="previewImages[currentPreviewIndex]"
                :alt="$t('message.previewImage') + ' ' + (currentPreviewIndex + 1)" />
            </div>
            <div v-else class="preview-frame">
              <img :src="previewImage" :alt="$t('message.previewImage')" />
            </div>
          </div>
        </section>
      </aside>
    </div>

    <!-- 頁尾 -->
    <footer class="site-footer">
      <div class="foot-row">
        <span class="muted">{{ $t('message.projectAddress') }}：</span>
        <a href="https://github.com/Miiduoa/nowrite" class="link-accent">GitHub</a>
      </div>
      <div class="freeprompt">{{ $t('message.freeprompt') }}</div>
    </footer>
  </div>
</template>


<script>
import { mapState } from 'vuex';
import TextInput from './TextInput.vue';
import Swal from 'sweetalert2';



export default {
  // props: {
  //   login_delete_message: {
  //     type: Boolean,
  //     default: false
  //   }
  // },
  components: {
    TextInput,

  },

  data() {
    return {
      text: "",
      fontFile: null,
      backgroundImage: null,
      fontSize: 124,
      lineSpacing: 200,
      fill: "(0, 0, 0, 255)",
      width: 2481,
      height: 3507,
      marginTop: 50,
      marginBottom: 50,
      marginLeft: 50,
      marginRight: 50,
      previewImage: "/default1.webp", // 新增一個新的資料屬性來儲存預覽圖片的 URL
      previewImages: [], // 用於儲存多頁預覽圖片的陣列
      currentPreviewIndex: 0, // 當前預覽的圖片索引
      preview: false,
      lineSpacingSigma: 0,
      fontSizeSigma: 2,
      wordSpacingSigma: 2,
      perturbXSigma: 3,
      perturbYSigma: 3,
      perturbThetaSigma: 0.05,
      wordSpacing: 1,
      endChars: '',
      errorMessage: '',  // 錯誤訊息
      message: '',  // 提示訊息
      uploadMessage: '',  // 上傳提示訊息
      selectedFontFileName: '',
      selectedImageFileName: '',
      //字型下拉選框
      selectedOption: '1',  // 當前選中的選項
      options: '',  // 下拉選項
      isLoading: false, //7.6
      strikethrough_length_sigma: 2,
      strikethrough_angle_sigma: 2,
      strikethrough_width_sigma: 2,
      strikethrough_probability: 0.005,
      strikethrough_width: 8,
      ink_depth_sigma: 30,
      isUnderlined: true,
      enableEnglishSpacing: false,
      isExpanded: false,
      // 生成狀態控制
      isGenerating: false,
      lastGenerateTime: 0,
      generateCooldown: 3000, // 3秒冷卻時間
      cooldownTimer: null,
      remainingCooldown: 0,
      isInCooldownPeriod: false,
      // 佇列滿倒計時
      queueFullCountdown: 0,        // 當前剩餘秒數，>0 時展示提示
      queueFullTotal: 0,            // 初始等待秒數，用於計算進度條
      queueFullTimer: null,         // setInterval 控制代碼
      enableFullPreview: false,
      localStorageItems: ['text', 'fontFile', 'fontSize', 'lineSpacing', 'fill', 'width', 'height', 'marginTop', 'marginBottom', 'marginLeft', 'marginRight', 'selectedFontFileName', 'selectedOption', 'lineSpacingSigma', 'fontSizeSigma', 'wordSpacingSigma', 'perturbXSigma', 'perturbYSigma', 'perturbThetaSigma', 'wordSpacing', 'strikethrough_length_sigma', 'strikethrough_angle_sigma', 'strikethrough_width_sigma', 'strikethrough_probability', 'strikethrough_width', 'ink_depth_sigma', 'isUnderlined', 'enableEnglishSpacing'],
    };
  },
  created() {

    // const localStorageItems = ['text', 'fontFile', 'fontSize', 'lineSpacing', 'fill', 'width', 'height', 'marginTop', 'marginBottom', 'marginLeft', 'marginRight', 'selectedFontFileName', 'selectedOption', 'lineSpacingSigma', 'fontSizeSigma', 'wordSpacingSigma', 'perturbXSigma', 'perturbYSigma', 'perturbThetaSigma', 'wordSpacing'];//, 'backgroundImage', 'selectedImageFileName'

    this.localStorageItems.forEach(item => {
      const value = localStorage.getItem(item);
      if (value !== null && value !== "undefined") {
        try {
          this[item] = JSON.parse(value);
          console.log('成功載入localStorage專案:', item, '值:', this[item]);
        } catch (error) {
          console.error('解析localStorage專案失敗:', item, '原始值:', value, '錯誤:', error);
        }
      } else {
        console.log('localstorage缺失item:' + item)
      }
    });

    this.$http.get('/api/fonts_info').then(response => {
      this.options = response.data.map((font, index) => {
        return { value: String(index + 1), text: font };
      });
    }).catch(error => {
      if (error.response && error.response.data) {
        this.errorMessage = error.response.data.error;
        this.message = '';
        this.uploadMessage = '';
      } else {
        this.errorMessage = error;
        this.message = '';
        this.uploadMessage = '';
      }
    });
    console.log('options' + this.options)
  },
  computed: {
    isDimensionSpecified() {
      // 當寬度或高度有值時，返回 true，這會停用背景圖片輸入框
      return !!(this.width || this.height);
    },
    isBackgroundImageSpecified() {
      // 當有背景圖片時，返回 true，這會停用寬度和高度輸入框
      return !!this.backgroundImage;
    },

    // 按鈕是否應該被停用
    shouldDisableButtons() {
      return this.isGenerating || this.isInCooldownPeriod || this.queueFullCountdown > 0;
    },

    // 佇列滿進度條（從100%倒減到0%）
    queueFullBarPercent() {
      if (this.queueFullTotal <= 0) return 0;
      return Math.max(0, (this.queueFullCountdown / this.queueFullTotal) * 100);
    },

    // 按鈕顯示文本
    buttonText() {
      if (this.isGenerating) {
        return '生成中...';
      } else if (this.isInCooldownPeriod) {
        return `請等待 ${this.remainingCooldown}s`;
      }
      return null; // 使用預設文本
    },
    isDevEnv() {
      return process.env.NODE_ENV === 'development';
    },

    //vuex中的login_delete_message，下面使用watch監控這個值  7.13
    ...mapState(['login_delete_message']),
  },
  watch: {
    login_delete_message(newVal) {
      if (newVal) {
        // this.message = '';
        // this.uploadMessage = '';
        console.log('已進入watch，錯誤訊息已經清空');
      }
    },
    errorMessage(newVal) {
      if (newVal) {
        this.$swal.fire({
          toast: true,
          position: 'top-end',
          icon: 'error',
          title: newVal,
          showConfirmButton: false,
          timer: 5000,
          timerProgressBar: true,
        });
      }
    },
    message(newVal) {
      if (newVal) {
        this.$swal.fire({
          toast: true,
          position: 'top-end',
          icon: 'success',
          title: newVal,
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true,
        });
      }
    },
    uploadMessage(newVal) {
      if (newVal) {
        this.$swal.fire({
          toast: true,
          position: 'top-end',
          icon: 'info',
          title: newVal,
          showConfirmButton: false,
          timer: false, // 上傳提示保持顯示
          showClass: { popup: 'swal2-show' },
          hideClass: { popup: 'swal2-hide' },
        });
      }
    },
    queueFullCountdown(newVal) {
      if (newVal > 0) {
        this.$swal.fire({
          toast: true,
          position: 'top-end',
          icon: 'warning',
          title: `伺服器繁忙，佇列已滿，預計 ${newVal} 秒後可重試`,
          showConfirmButton: false,
          timer: newVal * 1000,
          timerProgressBar: true,
          didOpen: (toast) => {
            const progressBar = toast.querySelector('.swal2-timer-progress-bar');
            if (progressBar && this.queueFullTotal > 0) {
              // 更新進度條
              const updateProgress = () => {
                if (this.queueFullCountdown > 0 && progressBar) {
                  const percent = (this.queueFullCountdown / this.queueFullTotal) * 100;
                  progressBar.style.width = percent + '%';
                  requestAnimationFrame(updateProgress);
                }
              };
              requestAnimationFrame(updateProgress);
            }
          },
        });
      }
    },
    text: {
      handler(newVal) {
        localStorage.setItem('text', JSON.stringify(newVal));
      },
      deep: true
    },
    fontFile: {
      handler(newVal) {
        localStorage.setItem('fontFile', JSON.stringify(newVal));
      },
      deep: true
    },
    // backgroundImage: {
    //   handler(newVal) {
    //     localStorage.setItem('backgroundImage', JSON.stringify(newVal));
    //   },
    //   deep: true
    // },
    fontSize: {
      handler(newVal) {
        localStorage.setItem('fontSize', JSON.stringify(newVal));
      },
      deep: true
    },
    lineSpacing: {
      handler(newVal) {
        localStorage.setItem('lineSpacing', JSON.stringify(newVal));
      },
      deep: true
    },
    fill: {
      handler(newVal) {
        localStorage.setItem('fill', JSON.stringify(newVal));
      },
      deep: true
    },
    width: {
      handler(newVal) {
        localStorage.setItem('width', JSON.stringify(newVal));
      },
      deep: true
    },
    height: {
      handler(newVal) {
        localStorage.setItem('height', JSON.stringify(newVal));
      },
      deep: true
    },
    marginTop: {
      handler(newVal) {
        localStorage.setItem('marginTop', JSON.stringify(newVal));
      },
      deep: true
    },
    marginBottom: {
      handler(newVal) {
        localStorage.setItem('marginBottom', JSON.stringify(newVal));
      },
      deep: true
    },
    marginLeft: {
      handler(newVal) {
        localStorage.setItem('marginLeft', JSON.stringify(newVal));
      },
      deep: true
    },
    marginRight: {
      handler(newVal) {
        localStorage.setItem('marginRight', JSON.stringify(newVal));
      },
      deep: true
    },
    selectedFontFileName: {
      handler(newVal) {
        localStorage.setItem('selectedFontFileName', JSON.stringify(newVal));
      },
      deep: true
    },
    selectedImageFileName: {
      handler(newVal) {
        localStorage.setItem('selectedImageFileName', JSON.stringify(newVal));
      },
      deep: true
    },
    selectedOption: {
      handler(newVal) {
        localStorage.setItem('selectedOption', JSON.stringify(newVal));
      },
      deep: true
    },
    lineSpacingSigma: {
      handler(newVal) {
        localStorage.setItem('lineSpacingSigma', JSON.stringify(newVal));
      },
      deep: true
    },
    fontSizeSigma: {
      handler(newVal) {
        localStorage.setItem('fontSizeSigma', JSON.stringify(newVal));
      },
      deep: true
    },
    wordSpacingSigma: {
      handler(newVal) {
        localStorage.setItem('wordSpacingSigma', JSON.stringify(newVal));
      },
      deep: true
    },
    perturbXSigma: {
      handler(newVal) {
        localStorage.setItem('perturbXSigma', JSON.stringify(newVal));
      },
      deep: true
    },
    perturbYSigma: {
      handler(newVal) {
        localStorage.setItem('perturbYSigma', JSON.stringify(newVal));
      },
      deep: true
    },
    perturbThetaSigma: {
      handler(newVal) {
        localStorage.setItem('perturbThetaSigma', JSON.stringify(newVal));
      },
      deep: true
    },
    wordSpacing: {
      handler(newVal) {
        localStorage.setItem('wordSpacing', JSON.stringify(newVal));
      },
      deep: true
    },
    strikethrough_length_sigma: {
      handler(newVal) {
        localStorage.setItem('strikethrough_length_sigma', JSON.stringify(newVal));
      },
      deep: true
    },
    strikethrough_angle_sigma: {
      handler(newVal) {
        localStorage.setItem('strikethrough_angle_sigma', JSON.stringify(newVal));
      },
      deep: true
    },
    strikethrough_width_sigma: {
      handler(newVal) {
        localStorage.setItem('strikethrough_width_sigma', JSON.stringify(newVal));
      },
      deep: true
    },
    strikethrough_probability: {
      handler(newVal) {
        localStorage.setItem('strikethrough_probability', JSON.stringify(newVal));
      },
      deep: true
    },
    strikethrough_width: {
      handler(newVal) {
        localStorage.setItem('strikethrough_width', JSON.stringify(newVal));
      },
      deep: true
    },
    ink_depth_sigma: {
      handler(newVal) {
        localStorage.setItem('ink_depth_sigma', JSON.stringify(newVal));
      },
      deep: true
    },
    isUnderlined: {
      handler(newVal) {
        localStorage.setItem('isUnderlined', JSON.stringify(newVal));
      },
      deep: true
    },
    enableEnglishSpacing: {
      handler(newVal) {
        localStorage.setItem('enableEnglishSpacing', JSON.stringify(newVal));
      },
      deep: true
    },
  },

  methods: {
    prevPage() {
      if (this.currentPreviewIndex > 0) {
        this.currentPreviewIndex--;
      }
    },
    nextPage() {
      if (this.currentPreviewIndex < this.previewImages.length - 1) {
        this.currentPreviewIndex++;
      }
    },
    toggleCollapse() {
      this.isExpanded = !this.isExpanded;
    },
    toggleFullPreview() {
      this.enableFullPreview = !this.enableFullPreview;
    },
    startQueueFullCountdown(seconds) {
      // 清掉舊計時器
      if (this.queueFullTimer) {
        clearInterval(this.queueFullTimer);
        this.queueFullTimer = null;
      }
      this.queueFullTotal = seconds;
      this.queueFullCountdown = seconds;
      this.queueFullTimer = setInterval(() => {
        this.queueFullCountdown -= 1;
        if (this.queueFullCountdown <= 0) {
          this.queueFullCountdown = 0;
          clearInterval(this.queueFullTimer);
          this.queueFullTimer = null;
        }
      }, 1000);
    },
    updateTaskUploadMessage(taskData, taskId) {
      const taskStatus = taskData?.task_status;
      const taskMessage = taskData?.task_message || '任務處理中';
      const taskProgress = taskData?.task_progress;
      const queuePendingCount = taskData?.queue_pending_count;
      const queueAheadCount = taskData?.queue_ahead_count;
      const processingCount = taskData?.processing_count;
      if (taskStatus === 'pending' && typeof queuePendingCount === 'number' && typeof queueAheadCount === 'number') {
        if (typeof processingCount === 'number') {
          this.uploadMessage = `${taskMessage}（前方排隊 ${queueAheadCount} 人，當前排隊 ${queuePendingCount} 人，處理中 ${processingCount} 人） Task ID: ${taskId}`;
        } else {
          this.uploadMessage = `${taskMessage}（前方排隊 ${queueAheadCount} 人，當前排隊 ${queuePendingCount} 人） Task ID: ${taskId}`;
        }
      } else if (typeof taskProgress === 'number') {
        this.uploadMessage = `${taskMessage}（${taskProgress}%） Task ID: ${taskId}`;
      } else {
        this.uploadMessage = `${taskMessage} Task ID: ${taskId}`;
      }
    },
    async waitForTaskViaWebSocket(taskId, timeoutMs = 5 * 60 * 1000) {
      return new Promise((resolve, reject) => {
        let isSettled = false;
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const wsUrl = `${protocol}://${window.location.host}/api/generate_handwriting/ws/${taskId}`;
        const socket = new WebSocket(wsUrl);

        const timeoutId = setTimeout(() => {
          if (isSettled) return;
          isSettled = true;
          try {
            socket.close();
          } catch (e) {
            // ignore close errors
          }
          reject(new Error('WebSocket任務等待超時'));
        }, timeoutMs);

        socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            if (data?.status === 'error') {
              if (isSettled) return;
              isSettled = true;
              clearTimeout(timeoutId);
              socket.close();
              reject(new Error(data?.message || '任務不存在'));
              return;
            }

            this.updateTaskUploadMessage(data, taskId);
            if (data?.task_status === 'completed') {
              if (isSettled) return;
              isSettled = true;
              clearTimeout(timeoutId);
              socket.close();
              resolve();
            } else if (data?.task_status === 'failed') {
              if (isSettled) return;
              isSettled = true;
              clearTimeout(timeoutId);
              socket.close();
              reject(new Error(data?.error_message || '任務執行失敗'));
            }
          } catch (e) {
            // ignore malformed payload
          }
        };

        socket.onerror = () => {
          if (isSettled) return;
          isSettled = true;
          clearTimeout(timeoutId);
          reject(new Error('WebSocket連線失敗'));
        };

        socket.onclose = () => {
          if (isSettled) return;
          isSettled = true;
          clearTimeout(timeoutId);
          reject(new Error('WebSocket連線已關閉'));
        };
      });
    },
    async pollGenerationTask(taskId, timeoutMs = 5 * 60 * 1000, intervalMs = 1500) {
      const start = Date.now();
      while (Date.now() - start < timeoutMs) {
        const statusResponse = await this.$http.get(`/api/generate_handwriting/task/${taskId}`);
        const taskStatus = statusResponse.data?.task_status;
        this.updateTaskUploadMessage(statusResponse.data, taskId);
        if (taskStatus === 'completed') {
          return;
        }
        if (taskStatus === 'failed') {
          throw new Error(statusResponse.data?.error_message || '任務執行失敗');
        }
        await new Promise(resolve => setTimeout(resolve, intervalMs));
      }
      throw new Error('任務處理超時，請重試');
    },
    handleGenerationResultResponse(response) {
      const contentType = response.headers['content-type'] || '';
      if (contentType.includes('application/json')) {
        // 處理多頁預覽影像 (JSON)
        if (response.data && response.data.status === 'success') {
          this.previewImages = response.data.images.map(img => 'data:image/png;base64,' + img);
          this.currentPreviewIndex = 0; // 重置為第一頁
          if (this.previewImages.length > 0) {
            this.previewImage = this.previewImages[0]; // 相容顯示第一頁
          }
          this.message = '預覽影像已載入。';
          this.uploadMessage = '';
          this.errorMessage = '';
        }
      } else if (contentType.includes('image/png')) {
        // 相容舊的單張圖片返回邏輯
        const blobUrl = URL.createObjectURL(response.data);
        // 將預覽影像的 URL 儲存到資料屬性中
        this.previewImage = blobUrl;
        this.previewImages = [blobUrl];
        // 設定提示資訊
        this.message = '預覽影像已載入。';//顯示message時，隱藏其他提示資訊
        this.uploadMessage = '';
        this.errorMessage = '';

      } else if (contentType.includes('application/zip')) {
        // 處理.zip檔案
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'images.zip'); // 或任何其他檔名
        document.body.appendChild(link);
        link.click();
        // 下載完成後，將連結刪除，7.5
        document.body.removeChild(link);
        // 設定提示資訊
        this.message = '檔案已下載。';
        this.uploadMessage = '';
        this.errorMessage = '';

      } else if (contentType.includes('application/pdf')) {
        // 處理.pdf檔案
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'images.pdf'); // 或任何其他檔名
        document.body.appendChild(link);
        link.click();
        // 下載完成後，將連結刪除
        document.body.removeChild(link);
        // 設定提示資訊
        this.message = '檔案已下載。';
        this.uploadMessage = '';
        this.errorMessage = '';
      } else {
        // console.log(text);
        console.error(`Unexpected response type: ${contentType}, ${response.data}`);
      }
    },
    async generateHandwriting(preview = false, pdf_save = false) {
      // console.log('pdf_save', pdf_save)

      // 檢查是否正在生成
      if (this.isGenerating) {
        this.$swal.fire({
          icon: 'warning',
          title: '正在生成中，請稍候...',
          showConfirmButton: false,
          timer: 2000,
        });
        return;
      }

      // 檢查冷卻時間
      const currentTime = Date.now();
      const timeSinceLastGenerate = currentTime - this.lastGenerateTime;
      if (timeSinceLastGenerate < this.generateCooldown) {
        const remainingTime = Math.ceil((this.generateCooldown - timeSinceLastGenerate) / 1000);
        this.$swal.fire({
          icon: 'warning',
          title: `請等待 ${remainingTime} 秒後再次生成`,
          showConfirmButton: false,
          timer: 2000,
        });
        return;
      }

      // 設定生成狀態
      this.isGenerating = true;
      this.lastGenerateTime = currentTime;

      // 啟動冷卻時間定時器
      this.startCooldownTimer();

      try {
        // 檢查是否為生產環境並進行頁數限制
        if (!preview && this.isProductionSite()) {
          const estimatedPages = this.estimatePageCount();
          if (estimatedPages > 15) {
            const confirmed = await this.showPageLimitDialog(estimatedPages);
            if (!confirmed) {
              return; // 使用者取消生成
            }
            // 使用者確認繼續，在前端截斷文本到前15頁
            this.truncateTextToPages(15);
          }
        }

      // 驗證輸入
      const Items = ['text', 'backgroundImage', 'fontSize', 'lineSpacing', 'marginTop', 'marginBottom', 'marginLeft', 'marginRight', 'lineSpacingSigma', 'fontSizeSigma', 'wordSpacingSigma', 'perturbXSigma', 'perturbYSigma', 'perturbThetaSigma', 'wordSpacing', 'strikethrough_length_sigma', 'strikethrough_angle_sigma', 'strikethrough_width_sigma', 'strikethrough_probability', 'strikethrough_width', 'ink_depth_sigma'];
      Items.forEach(item => {
        let value = this[item];
        // if (!value) {
        //   console.error(`Missing value for ${item}`);
        //   return;
        // }
        // 對不同的輸入進行不同的驗證
        switch (item) {
          case 'text':
            // 驗證 text 是否是字串
            if (typeof value !== 'string') {
              console.error(`Invalid value for ${item}`);
              this.errorMessage = '請輸入字串';
            }
            // return;
            break;
          case 'fontSize':
          case 'lineSpacing':
          case 'marginTop':
          case 'marginBottom':
          case 'marginLeft':
          case 'marginRight':
          case 'lineSpacingSigma':
          case 'fontSizeSigma':
          case 'wordSpacingSigma':
          case 'perturbXSigma':
          case 'perturbYSigma':
          case 'perturbThetaSigma':
          case 'wordSpacing':
          case 'strikethrough_length_sigma':
          case 'strikethrough_angle_sigma':
          case 'strikethrough_width_sigma':
          case 'strikethrough_probability':
          case 'strikethrough_width':
          case 'ink_depth_sigma':
            // 驗證這些值是否是數字
            if (isNaN(Number(value))) {
              console.error(`Invalid value for ${item}`);
              this.errorMessage = '請輸入數字';
            }
            // return
            break;
          case 'backgroundImage':
            // 驗證 backgroundImage 是否是有效的 URL 或者檔案路徑
            // 這可能需要更復雜的驗證
            break;
          default:
            console.error(`Unknown item: ${item}`);
        }
      });

      if (this.height < this.marginTop + this.lineSpacing + this.marginBottom && this.isDimensionSpecified) {
        this.errorMessage = '上邊距、下邊距和行間距之和不能大於高度';
        this.message = '';
        this.uploadMessage = '';
        return;
      }
      if (this.fontSize > this.lineSpacing) {
        this.errorMessage = '字型大小不能大於行間距';
        this.message = '';
        this.uploadMessage = '';
        return;
      }

      this.preview = preview;
      // this.pdf_save = pdf_save;
      // 設定提示資訊為“內容正在上傳…”
      this.uploadMessage = '內容正在上傳並處理…（如果長時間沒有響應說明伺服器崩潰）單次請求最多處理五分鐘，超過這個時間則失敗';//顯示上傳提示資訊時，隱藏其他提示資訊
      console.log('內容正在上傳並處理…');
      this.message = '';
      this.errorMessage = '';
      const formData = new FormData();
      formData.append("text", this.text);
      // 只有當用戶選擇的字型檔名與字型下拉選項中的字型檔名相同時，才上傳字型檔案7.5
      if (this.options[this.selectedOption - 1].text == this.selectedFontFileName) {
        formData.append("font_file", this.fontFile);
      }
      formData.append("background_image", this.backgroundImage);
      formData.append("font_size", this.fontSize);
      formData.append("line_spacing", this.lineSpacing);
      formData.append("fill", this.fill);
      if (this.width) {
        formData.append("width", this.width);
      }
      if (this.height) {
        formData.append("height", this.height);
      }
      formData.append("top_margin", this.marginTop);
      formData.append("bottom_margin", this.marginBottom);
      formData.append("left_margin", this.marginLeft);
      formData.append("right_margin", this.marginRight);
      formData.append("line_spacing_sigma", this.lineSpacingSigma);
      formData.append("font_size_sigma", this.fontSizeSigma);
      formData.append("word_spacing_sigma", this.wordSpacingSigma);
      formData.append("end_chars", this.endChars);
      formData.append("perturb_x_sigma", this.perturbXSigma);
      formData.append("perturb_y_sigma", this.perturbYSigma);
      formData.append("perturb_theta_sigma", this.perturbThetaSigma);
      formData.append("word_spacing", this.wordSpacing);
      formData.append("preview", this.preview.toString());
      formData.append("font_option", this.options[this.selectedOption - 1].text);
      formData.append("strikethrough_length_sigma", this.strikethrough_length_sigma);
      formData.append("strikethrough_angle_sigma", this.strikethrough_angle_sigma);
      formData.append("strikethrough_width_sigma", this.strikethrough_width_sigma);
      formData.append("strikethrough_probability", this.strikethrough_probability);
      formData.append("strikethrough_width", this.strikethrough_width);
      formData.append("ink_depth_sigma", this.ink_depth_sigma);
      formData.append("pdf_save", pdf_save.toString());
      formData.append("isUnderlined", this.isUnderlined.toString());
      formData.append("enableEnglishSpacing", this.enableEnglishSpacing.toString());
      
      // 根據環境與按鈕決定是否啟用多頁預覽
      const isDevEnv = process.env.NODE_ENV === 'development';
      const allowFullPreview = isDevEnv && this.enableFullPreview && preview;
      formData.append("full_preview", allowFullPreview.toString());

      for (let pair of formData.entries()) {
        console.log(pair[0] + ', ' + pair[1]);
      }

      const taskCreateResponse = await this.$http.post(
        '/api/generate_handwriting',
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          withCredentials: true, //在跨域的時候，需要新增這句話，才能傳送cookie 6.30
        }
      );

      const taskId = taskCreateResponse.data?.task_id;
      if (!taskId) {
        throw new Error('未獲取到任務ID');
      }

      this.uploadMessage = `任務已提交，正在生成中（Task ID: ${taskId}）…`;
      try {
        await this.waitForTaskViaWebSocket(taskId);
      } catch (wsError) {
        console.warn('WebSocket不可用，降級為輪詢模式', wsError);
        await this.pollGenerationTask(taskId);
      }

      const resultResponse = await this.$http.get(
        `/api/generate_handwriting/task/${taskId}/result`,
        {
          // 預覽模式下：開發環境使用json接收多頁圖片，生產環境使用blob接收單頁圖片
          responseType: preview ? (allowFullPreview ? 'json' : 'blob') : 'blob',
          withCredentials: true,
        }
      );
      this.handleGenerationResultResponse(resultResponse);
      } catch (error) {
        if (error.response) {
          // ── 佇列已滿：503 queue_full ────────────────────────────────
          const errData = error.response.data;
          if (
            error.response.status === 503 &&
            errData?.status === 'queue_full'
          ) {
            const waitSec = errData.estimated_wait_seconds || 30;
            this.startQueueFullCountdown(waitSec);
            this.message = '';
            this.uploadMessage = '';
            this.errorMessage = '';
            return; // 不走通用錯誤展示
          }
          // ────────────────────────────────────────────────────────────
          // console.log('已進入報錯處理程序')
          // 如果伺服器返回了一個JSON錯誤訊息
          if (error.response.data instanceof Blob) {
            let reader = new FileReader();
            reader.onload = (e) => {
              try {
                let errorData = JSON.parse(e.target.result);
                this.errorMessage = errorData.message;
              } catch (parseError) {
                // 如果解析失敗，直接顯示原始資訊
                this.errorMessage = e.target.result;
                console.log('非JSON格式的錯誤資料：', e.target.result);
              }
              this.message = '';
              this.uploadMessage = '';
              console.log('錯誤資訊：', this.errorMessage);
              console.log(error);
            };//注意，這裡只能使用箭頭函式，不然this指向全域物件window，6.30
            reader.readAsText(error.response.data);
          } else {
            this.errorMessage = error.response.data?.message || '生成失敗，請稍後重試';
            // this.errorMessage = error.response.data.message;
            this.message = '';
            this.uploadMessage = '';
          }
        } else {
          // 如果沒有從伺服器收到響應
          this.errorMessage = error.message || '網路錯誤，請稍後再試';
          this.message = '';
          this.uploadMessage = '';
        }
      } finally {
        // 重置生成狀態，但保持冷卻狀態
        this.isGenerating = false;
        // 冷卻定時器會自動處理冷卻狀態的重置
      }
    },
    savePreset() {
      try {
        let data = {};
        this.localStorageItems.forEach(item => {
          data[item] = this[item];
        });
        // 將物件轉換為 JSON 格式的字串
        let dataString = JSON.stringify(data);

        // 將字串儲存到 localStorage 中
        localStorage.setItem('myPreset', dataString);

        this.$swal.fire({
          icon: 'success',
          title: '預設設定儲存成功！',
          timer: 2000,
          showConfirmButton: false,
        });
      } catch (error) {
        console.error('儲存預設設定失敗:', error);
        this.$swal.fire({
          icon: 'error',
          title: '儲存預設設定失敗',
        });
      }
    },
    resetSettings() {
      // this.text = '';13213不能刪除，會導致文字為空，但是輸入框沒有清除
      this.fontFile = null;
      this.backgroundImage = null;
      this.fontSize = 124;
      this.lineSpacing = 200;
      this.fill = "(0, 0, 0, 255)";
      this.width = 2481;
      this.height = 3507;
      this.marginTop = 50;
      this.marginBottom = 50;
      this.marginLeft = 50;
      this.marginRight = 50;
      this.lineSpacingSigma = 0;
      this.fontSizeSigma = 2;
      this.wordSpacingSigma = 2;
      this.perturbXSigma = 3;
      this.perturbYSigma = 3;
      this.perturbThetaSigma = 0.05;
      this.wordSpacing = 1;
      this.strikethrough_length_sigma = 2;
      this.strikethrough_angle_sigma = 2;
      this.strikethrough_width_sigma = 2;
      this.strikethrough_probability = 0.005;
      this.strikethrough_width = 8;
      this.ink_depth_sigma = 30;
      this.isUnderlined = true;
      this.enableEnglishSpacing = false;
      this.errorMessage = '';
      this.message = '';
      this.uploadMessage = '';
      this.selectedFontFileName = '';
      this.selectedImageFileName = '';
      this.selectedOption = '1';
      this.previewImage = "/default1.webp";
    },
    loadPreset() {
      try {
        // 從 localStorage 中獲取字串
        let dataString = localStorage.getItem('myPreset');

        if (dataString === null || dataString === "undefined") {
          this.$swal.fire({
            icon: 'info',
            title: '沒有找到儲存的預設設定',
          });
          return;
        }

        // 將字串轉換回物件
        let data = JSON.parse(dataString);
        Object.keys(data).forEach(item => {
          this[item] = data[item];
        });

        this.$swal.fire({
          icon: 'success',
          title: '預設設定載入成功！',
          timer: 2000,
          showConfirmButton: false,
        });
      } catch (error) {
        console.error('載入預設設定失敗:', error);
        this.$swal.fire({
          icon: 'error',
          title: '載入預設設定失敗，請檢查儲存的資料是否有效',
        });
      }
    },
    onBackgroundImageChange(event) {
      // 當用戶選擇了一個新的背景圖片檔案時，更新 selectedImageFileName，由於這邊直接觸發函數了，所以localstorage可以在這裡修改，
      //之前因為文字不能觸發函式，所以要放在watch裡面
      this.selectedImageFileName = event.target.files[0].name;
      this.backgroundImage = event.target.files[0];
      // 由於檔案無法在瀏覽器儲存，所以下面的程式碼無效 7.15
      // localStorage.setItem('backgroundImage', JSON.stringify(this.backgroundImage));
      // if (localStorage.getItem('backgroundImage')) {
      //   console.log('Data successfully saved to localStorage.');
      // } else {
      //   console.log('Failed to save to localStorage.');
      // }

      this.previewImage = URL.createObjectURL(event.target.files[0]);
      Swal.fire({
        title: '你希望自動識別頁面的四周邊距嗎？（儘量不要上傳帶有alpha透明通道的圖片）',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: '確定',
        cancelButtonText: '取消'
      }).then((result) => {
        if (result.isConfirmed) {
          let formData = new FormData();
          formData.append('file', this.backgroundImage);  // 'file' 是你在伺服器端獲取檔案資料時的 key
          this.isLoading = true;
          this.$http.post(
            '/api/imagefileprocess',
            formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(response => {
              this.marginLeft = response.data.marginLeft;
              this.marginRight = response.data.marginRight;
              this.marginTop = response.data.marginTop - this.lineSpacing;
              this.marginBottom = response.data.marginBottom;
              this.lineSpacing = response.data.lineSpacing;
              this.message = '背景圖片已載入。';
              this.errorMessage = '';
              this.uploadMessage = '';
              this.isLoading = false;
            })
            .catch(error => {
              console.error(error);
              this.errorMessage = error.response.data.error;
              this.message = '';
              this.uploadMessage = '';
              this.isLoading = false;
            });
        }
      })
    },
    onFontChange(event) {
      // 當用戶選擇了一個新的字型檔案時，更新 selectedFontFileName
      this.selectedFontFileName = event.target.files[0].name;
      this.fontFile = event.target.files[0];
      // 建立一個新的 option 物件
      const newOption = {
        value: String(this.options.length + 1), // 使用 options 陣列的長度 + 1 作為新選項的 value
        text: this.selectedFontFileName // 使用字型檔名作為新選項的 text
      };

      // 將新選項新增到 options 陣列中
      this.options.push(newOption);

      // 將 selectedOption 設為新選項的 value，這樣下拉選單就會自動更新為新新增的字型
      this.selectedOption = newOption.value;

    },
    triggerImageFileInput() {
      if (!this.isDimensionSpecified) {
        this.$refs.imageFileInput.click();
      }
      else {
        Swal.fire({
          title: '需要先清空高度寬度才能選擇圖片',
          text: '選擇圖片後需要點選按鈕左下角的X刪除圖片才能再輸入寬度高度',
          icon: 'question',
          showCancelButton: true,
          confirmButtonText: '清空寬度高度',
          cancelButtonText: '取消'
        }).then((result) => {
          if (result.isConfirmed) {
            this.width = null
            this.height = null
            this.$refs.imageFileInput.click();
          }
        })
      }
    },
    triggerFontFileInput() {
      this.$refs.fontFileInput.click();
    },
    //清空影像按鈕對應的函式
    clearImage() {
      // 清空儲存影像資訊的變數
      this.selectedImageFileName = null;
      this.backgroundImage = null;
      // 清空檔案輸入框
      this.$refs.imageFileInput.value = null;
    },
    clearDimensions() {
      console.log('清空影像尺寸');
      this.width = null
      this.height = null
    },

    // 檢查是否為生產網站
    isProductionSite() { // localhost:8080 handwrite.14790897.xyz
      return window.location.hostname === 'handwrite.14790897.xyz';
    },

    // 估算頁數
    estimatePageCount() {
      if (!this.text || this.text.length === 0) {
        return 0;
      }

      // 獲取頁面參數
      const pageWidth = this.width || (this.backgroundImage ? 2481 : 2481); // 預設寬度
      const pageHeight = this.height || (this.backgroundImage ? 3507 : 3507); // 預設高度
      const fontSize = parseInt(this.fontSize) || 20;
      const lineSpacing = parseInt(this.lineSpacing) || 30;
      const marginTop = parseInt(this.marginTop) || 50;
      const marginBottom = parseInt(this.marginBottom) || 50;
      const marginLeft = parseInt(this.marginLeft) || 50;
      const marginRight = parseInt(this.marginRight) || 50;

      // 計算可用區域
      const usableWidth = pageWidth - marginLeft - marginRight;
      const usableHeight = pageHeight - marginTop - marginBottom;

      // 估算每行字元數（粗略估算，中文字元按字型大小計算）
      const avgCharWidth = fontSize * 0.8; // 中文字元寬度約為字型大小的0.8倍
      const charsPerLine = Math.floor(usableWidth / avgCharWidth);

      // 估算每頁行數
      const linesPerPage = Math.floor(usableHeight / lineSpacing);

      // 估算每頁字元數
      const charsPerPage = charsPerLine * linesPerPage;

      // 計算頁數
      const estimatedPages = Math.ceil(this.text.length / charsPerPage);

      console.log('頁數估算:', {
        textLength: this.text.length,
        charsPerLine,
        linesPerPage,
        charsPerPage,
        estimatedPages
      });

      return estimatedPages;
    },

    // 顯示頁數限制對話方塊
    async showPageLimitDialog(estimatedPages) {
      try {
        const result = await this.$swal.fire({
          title: '頁數限制提醒',
          html: `
            <div style="text-align: left; line-height: 1.6;">
              <p><strong>檢測到您的文本預計會生成 ${estimatedPages} 頁</strong></p>
              <p>由於伺服器資源限制，在 <strong>handwrite.14790897.xyz</strong> 網站上單次最多隻能生成 <strong>10頁</strong>。</p>
              <p>如果您選擇繼續：</p>
              <ul style="margin: 10px 0; padding-left: 20px;">
                <li>系統將只生成前 10 頁內容</li>
                <li>超出部分將被自動截斷</li>
                <li>建議您分批處理長文本</li>
              </ul>
              <p style="color: #666; font-size: 14px;">
                💡 提示：您可以將長文本分成多個部分，分別生成，或者自行搭建本專案來處理更長的文本
              </p>
              <p style="color: #888; font-size: 12px; margin-top: 10px;">
                注：此限制僅適用於 handwrite.14790897.xyz 網站
              </p>
            </div>
          `,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: '繼續生成（前10頁）',
          cancelButtonText: '取消',
          confirmButtonColor: '#f39c12',
          cancelButtonColor: '#d33',
          width: '500px'
        });

        return result.isConfirmed;
      } catch (error) {
        console.error('SweetAlert2 error:', error);
        // 降級到原生 confirm
        return confirm(`檢測到您的文本預計會生成 ${estimatedPages} 頁。\n\n由於伺服器資源限制，在 handwrite.14790897.xyz 網站上單次最多隻能生成 10頁。\n\n是否繼續生成前10頁？`);
      }
    },

    // 截斷文本到指定頁數
    truncateTextToPages(maxPages) {
      if (!this.text || this.text.length === 0) {
        return;
      }

      // 獲取頁面參數
      const pageWidth = this.width || (this.backgroundImage ?2481 : 2481); // 預設寬度
      const pageHeight = this.height || (this.backgroundImage ? 3507 : 3507); // 預設高度
      const fontSize = parseInt(this.fontSize) || 20;
      const lineSpacing = parseInt(this.lineSpacing) || 30;
      const marginTop = parseInt(this.marginTop) || 50;
      const marginBottom = parseInt(this.marginBottom) || 50;
      const marginLeft = parseInt(this.marginLeft) || 50;
      const marginRight = parseInt(this.marginRight) || 50;

      // 計算可用區域
      const usableWidth = pageWidth - marginLeft - marginRight;
      const usableHeight = pageHeight - marginTop - marginBottom;

      // 估算每行字元數
      const avgCharWidth = fontSize * 0.8;
      const charsPerLine = Math.floor(usableWidth / avgCharWidth);

      // 估算每頁行數
      const linesPerPage = Math.floor(usableHeight / lineSpacing);

      // 計算每頁字元數
      const charsPerPage = charsPerLine * linesPerPage;

      // 計算最大字元數
      const maxChars = charsPerPage * maxPages;

      // 截斷文本
      if (this.text.length > maxChars) {
        const originalLength = this.text.length;
        this.text = this.text.substring(0, maxChars);

        console.log('文本截斷:', {
          originalLength,
          truncatedLength: this.text.length,
          maxPages,
          charsPerPage,
          maxChars
        });

      }
    },

    // 啟動冷卻時間定時器
    startCooldownTimer() {
      // 清除現有定時器
      if (this.cooldownTimer) {
        clearInterval(this.cooldownTimer);
      }

      // 設定初始冷卻狀態
      this.isInCooldownPeriod = true;
      this.remainingCooldown = Math.ceil(this.generateCooldown / 1000);

      // 啟動新定時器，每1秒更新一次顯示
      this.cooldownTimer = setInterval(() => {
        const currentTime = Date.now();
        const timeSinceLastGenerate = currentTime - this.lastGenerateTime;
        const remaining = this.generateCooldown - timeSinceLastGenerate;

        if (remaining <= 0) {
          // 冷卻結束
          this.isInCooldownPeriod = false;
          this.remainingCooldown = 0;
          clearInterval(this.cooldownTimer);
          this.cooldownTimer = null;
        } else {
          // 更新剩餘時間
          this.remainingCooldown = Math.ceil(remaining / 1000);
        }
      }, 1000);
    },

  },

  // 元件銷燬時清理定時器
  beforeUnmount() {
    if (this.cooldownTimer) {
      clearInterval(this.cooldownTimer);
      this.cooldownTimer = null;
    }
  },

};
</script>


<style scoped>
.home {
  width: 100%;
}

/* ── Hero ── */
.hero {
  text-align: center;
  margin: 4px auto 26px;
  max-width: 720px;
}
.hero .eyebrow {
  justify-content: center;
  margin-bottom: 10px;
}
.hero-title {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: clamp(1.9rem, 4.6vw, 3rem);
  line-height: 1.15;
  letter-spacing: 1px;
  color: var(--ink);
  margin: 0 0 10px;
}
.hero-title .accent {
  color: var(--accent);
}
.hero-sub {
  color: var(--ink-soft);
  font-size: 1.02rem;
  margin: 0;
}

/* ── 訊息區 ── */
.msg-area {
  max-width: 880px;
  margin: 0 auto 16px;
}
.msg-area .alert {
  margin-bottom: 10px;
}

/* ── 雙欄佈局 ── */
.layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: 22px;
  align-items: start;
}
.col-controls {
  display: flex;
  flex-direction: column;
  gap: 18px;
  min-width: 0;
}
.col-preview {
  position: sticky;
  top: 92px;
  min-width: 0;
}

/* ── 面板 ── */
.panel {
  padding: 22px;
}
.panel-head {
  margin-bottom: 16px;
}
.panel-title {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 1.22rem;
  letter-spacing: 1px;
  color: var(--ink);
  margin: 6px 0 0;
}

/* ── 欄位（行式） ── */
.field-row {
  margin-bottom: 14px;
}
.field-row:last-child {
  margin-bottom: 0;
}
.field-label {
  display: block;
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--ink-soft);
  margin-bottom: 7px;
}
.picker {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}
.btn-pick {
  flex: 0 0 auto;
  padding: 0.55em 1em;
  font-size: 0.88rem;
}
.btn-pick.is-disabled {
  opacity: 0.55;
}
.clear-x {
  display: inline-grid;
  place-items: center;
  width: 16px;
  height: 16px;
  margin-left: 6px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-size: 13px;
  line-height: 1;
}
.select-font {
  flex: 1 1 140px;
  min-width: 0;
}
.file-name {
  flex: 1 1 100%;
  font-size: 0.82rem;
  color: var(--ink-faint);
  word-break: break-all;
}

/* ── 欄位（網格） ── */
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px 14px;
}
.ifield {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}
.ifield-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--ink-soft);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.with-clear {
  display: flex;
  gap: 6px;
  align-items: center;
}
.with-clear .glass-field {
  flex: 1 1 auto;
}
.mini-x {
  flex: 0 0 auto;
  width: 34px;
  height: 34px;
  border-radius: var(--r-sm);
  border: 1px solid var(--field-edge);
  background: var(--field-bg);
  color: var(--ink-soft);
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  transition: all 0.2s ease;
}
.mini-x:hover {
  color: var(--accent);
  border-color: var(--accent-ring);
}

/* ── 開關 ── */
.toggles {
  display: flex;
  flex-wrap: wrap;
  gap: 14px 22px;
  margin-top: 16px;
}
.switch {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}
.switch input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}
.switch-track {
  position: relative;
  width: 44px;
  height: 26px;
  border-radius: 999px;
  background: var(--field-bg);
  border: 1px solid var(--field-edge);
  transition: background 0.25s ease, border-color 0.25s ease;
  flex: 0 0 auto;
}
.switch-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.switch input:checked + .switch-track {
  background: var(--accent);
  border-color: var(--accent);
}
.switch input:checked + .switch-track .switch-thumb {
  transform: translateX(18px);
}
.switch input:focus-visible + .switch-track {
  box-shadow: 0 0 0 4px var(--accent-soft);
}
.switch-text {
  font-size: 0.9rem;
  color: var(--ink);
  font-weight: 500;
}

/* ── 展開按鈕 + 進階區 ── */
.expand-btn {
  margin-top: 16px;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 14px;
  border-radius: var(--r-pill);
  background: var(--field-bg);
  border: 1px solid var(--field-edge);
  color: var(--ink-soft);
  font-weight: 600;
  font-size: 0.88rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.expand-btn:hover {
  color: var(--accent);
  border-color: var(--accent-ring);
}
.expand-btn .chev {
  transition: transform 0.3s ease;
}
.expand-btn .chev.open {
  transform: rotate(180deg);
}
.advanced {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed var(--field-edge);
  overflow: hidden;
}
.collapse-enter-active,
.collapse-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.collapse-enter-from,
.collapse-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ── 生成狀態 ── */
.generation-status {
  display: flex;
  justify-content: center;
}
.status-chip {
  padding: 10px 18px;
  border-radius: var(--r-pill);
  font-weight: 700;
  font-size: 0.92rem;
  border: 1px solid var(--glass-edge);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  animation: pulse 2s infinite;
}
.status-generating {
  background: var(--accent-soft);
  color: var(--accent);
}
.status-cooldown {
  background: var(--accent-soft);
  color: var(--accent-2);
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.62; }
}

/* ── 動作面板 ── */
.action-panel {
  display: flex;
  flex-direction: column;
  gap: 14px;
  align-items: stretch;
}
.actions-secondary,
.actions-primary {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.actions-secondary .btn-glass {
  flex: 1 1 auto;
  font-size: 0.86rem;
  padding: 0.5em 0.9em;
}
.actions-primary .btn-ink {
  flex: 1 1 auto;
}
.feedback-link {
  align-self: center;
  font-weight: 600;
  color: var(--ink-soft);
  font-size: 0.9rem;
  padding: 4px 8px;
}
.feedback-link:hover {
  color: var(--accent);
}

/* ── 頁數提示 ── */
.page-info-alert .alert {
  margin: 0;
  font-size: 0.88rem;
}
.over-limit {
  color: var(--accent);
  font-weight: 600;
}

/* ── 預覽 ── */
.preview {
  padding: 22px;
}
.preview-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.pager {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}
.pager-btn {
  font-size: 0.85rem;
  padding: 0.45em 0.9em;
}
.pager-info {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--ink-soft);
}
.preview-frame {
  display: flex;
  justify-content: center;
  padding: 14px;
  border-radius: var(--r-md);
  background: var(--field-bg);
  border: 1px solid var(--field-edge);
}
.preview-frame img {
  max-width: 100%;
  width: 560px;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(40, 33, 24, 0.18);
  background: #fff;
}

/* ── 頁尾 ── */
.site-footer {
  margin-top: 30px;
  text-align: center;
  padding: 18px;
}
.foot-row {
  font-size: 0.92rem;
}
.freeprompt {
  font-size: 0.8rem;
  color: var(--accent);
  margin-top: 8px;
  opacity: 0.85;
}

/* ── 響應式 ── */
@media (max-width: 920px) {
  .layout {
    grid-template-columns: 1fr;
  }
  .col-preview {
    position: static;
    order: -1;
  }
}
@media (max-width: 460px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }
  .panel {
    padding: 18px;
  }
}
</style>
