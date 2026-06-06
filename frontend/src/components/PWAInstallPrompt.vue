<template>
  <div v-if="showInstallPrompt" class="pwa-install-prompt">
    <div class="prompt-content">
      <div class="prompt-icon">
        <img src="/icon.svg" alt="App Icon" width="48" height="48">
      </div>
      <div class="prompt-text">
        <h3>安裝手寫生成器</h3>
        <p>將此應用新增到主螢幕，獲得更好的使用體驗</p>
      </div>
      <div class="prompt-actions">
        <button @click="installApp" class="install-btn">安裝</button>
        <button @click="dismissPrompt" class="dismiss-btn">稍後</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PWAInstallPrompt',
  data() {
    return {
      showInstallPrompt: false,
      deferredPrompt: null
    };
  },
  mounted() {
    const dismissed = this.getCookie('pwa-install-dismissed') === '1';

    // 監聽 beforeinstallprompt 事件
    window.addEventListener('beforeinstallprompt', (e) => {
      console.log('PWA: beforeinstallprompt event fired');
      // 阻止預設的安裝提示
      e.preventDefault();

      // 使用者明確拒絕後，不再顯示
      if (dismissed || this.getCookie('pwa-install-dismissed') === '1') {
        return;
      }

      // 儲存事件，稍後使用
      this.deferredPrompt = e;
      // 顯示自定義安裝提示
      this.showInstallPrompt = true;
    });

    // 監聽應用安裝事件
    window.addEventListener('appinstalled', () => {
      console.log('PWA: App was installed');
      this.showInstallPrompt = false;
      this.deferredPrompt = null;
    });

    // 檢查是否已經安裝
    if (window.matchMedia('(display-mode: standalone)').matches) {
      console.log('PWA: App is running in standalone mode');
    }
  },
  methods: {
    async installApp() {
      if (!this.deferredPrompt) {
        return;
      }

      // 顯示安裝提示
      this.deferredPrompt.prompt();
      
      // 等待使用者響應 deferredPrompt是之前儲存的瀏覽器事件 測試 測試
      const { outcome } = await this.deferredPrompt.userChoice;
      console.log(`PWA: User response to the install prompt: ${outcome}`);

      // 使用者在原生提示中拒絕後，記憶選擇並不再彈出
      if (outcome === 'dismissed') {
        this.setCookie('pwa-install-dismissed', '1', 3650);
      }
      
      // 清理
      this.deferredPrompt = null;
      this.showInstallPrompt = false;
    },
    dismissPrompt() {
      this.showInstallPrompt = false;
      // 使用者選擇“稍後”視為拒絕，後續不再彈出
      this.setCookie('pwa-install-dismissed', '1', 3650);
    },
    setCookie(name, value, days) {
      const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
      document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
    },
    getCookie(name) {
      const target = `${name}=`;
      const cookies = document.cookie ? document.cookie.split('; ') : [];
      for (const item of cookies) {
        if (item.startsWith(target)) {
          return decodeURIComponent(item.substring(target.length));
        }
      }
      return null;
    }
  }
}
</script>

<style scoped>
.pwa-install-prompt {
  position: fixed;
  bottom: 20px;
  left: 20px;
  right: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.prompt-content {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 12px;
}

.prompt-icon img {
  border-radius: 8px;
}

.prompt-text {
  flex: 1;
}

.prompt-text h3 {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.prompt-text p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.prompt-actions {
  display: flex;
  gap: 8px;
}

.install-btn, .dismiss-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.install-btn {
  background: #2196f3;
  color: white;
}

.install-btn:hover {
  background: #1976d2;
}

.dismiss-btn {
  background: #f5f5f5;
  color: #666;
}

.dismiss-btn:hover {
  background: #e0e0e0;
}

@media (max-width: 480px) {
  .pwa-install-prompt {
    left: 10px;
    right: 10px;
    bottom: 10px;
  }
  
  .prompt-content {
    flex-direction: column;
    text-align: center;
  }
  
  .prompt-actions {
    width: 100%;
    justify-content: center;
  }
}
</style>
