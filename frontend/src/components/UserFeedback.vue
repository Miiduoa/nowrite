<template>
  <div id="feedBack" class="fb-wrap">
    <section class="fb-card glass">
      <div class="fb-head">
        <span class="eyebrow">✦ {{ $t("message.feedback") }}</span>
        <h1 class="fb-title">{{ $t("message.feedback") }}</h1>
      </div>

      <form @submit.prevent="sendFeedback" class="fb-form">
        <div class="fb-group">
          <label for="email">{{ $t("message.email") }}</label>
          <input type="email" id="email" v-model="email" class="form-control glass-field" required />
        </div>
        <div class="fb-group">
          <label for="feedback">{{ $t("message.feedback") }}</label>
          <textarea id="feedback" v-model="feedback" class="form-control glass-field" rows="5" required></textarea>
        </div>
        <button type="submit" class="btn-ink fb-submit">Send</button>
      </form>

      <p class="fb-hint">
        {{ $t("message.suggest") }}
        <a href="https://github.com/Miiduoa/nowrite/issues" target="_blank" class="link-accent">GitHub issue</a>
      </p>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserFeedback",
  data() {
    return {
      email: "",
      feedback: "",
    };
  },
  methods: {
    async sendFeedback() {
      const emailToSend = this.email; // 儲存當前 `email` 值，防止在請求之前被清空導致資料丟失
      const feedbackToSend = this.feedback; // 儲存當前 `feedback` 值

      this.email = ""; // 提前清空
      this.feedback = ""; // 提前清空
      try {
        const res = await axios.post(
          "https://mail.14790897.xyz/api/sendEmail",
          {
            email: emailToSend,
            feedback: feedbackToSend,
          }
        );
        if (res.status === 200) {
          alert("Feedback sent successfully!");
        }
      } catch (error) {
        // 可在失敗時重新設定 email 和 feedback 恢復到傳送前狀態
        this.email = emailToSend;
        this.feedback = feedbackToSend;
        console.error("Error:", error);
        alert("Failed to send feedback.");
      }
    },
  },
};
</script>

<style scoped>
.fb-wrap {
  display: grid;
  place-items: center;
  min-height: 60vh;
}
.fb-card {
  width: 100%;
  max-width: 560px;
  padding: 32px;
}
.fb-head {
  margin-bottom: 22px;
}
.fb-title {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 1.5rem;
  color: var(--ink);
  margin: 8px 0 0;
}
.fb-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.fb-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}
.fb-group label {
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--ink-soft);
}
.fb-submit {
  align-self: flex-start;
  padding: 0.62em 1.6em;
}
.fb-hint {
  margin: 20px 0 0;
  color: var(--ink-soft);
  font-size: 0.9rem;
  line-height: 1.6;
}
</style>
