<template>
  <div class="auth-wrap">
    <section class="auth-card glass">
      <div class="auth-head">
        <span class="eyebrow">✦ {{ $t('message.login') }}</span>
        <h2 class="auth-title">{{ $t('message.login') }}</h2>
      </div>
      <form @submit.prevent="submitForm" class="auth-form">
        <div class="auth-group">
          <label for="username">{{ $t('message.username') }}</label>
          <input id="username" v-model="username" type="text" class="form-control glass-field" placeholder="Username">
        </div>
        <div class="auth-group">
          <label for="password">{{ $t('message.password') }}</label>
          <input id="password" v-model="password" type="password" class="form-control glass-field" placeholder="Password">
        </div>
        <button type="submit" class="btn-ink auth-submit">{{ $t('message.login') }}</button>
      </form>
    </section>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    // ...mapMutations(['setUsername']),
    submitForm() {
      this.$http.post('/api/login', {
        username: this.username,
        password: this.password
      })
        .then(response => {
          if (response.data.status === 'success') {
            // 使用 mutation 設定全域的 username
            // this.setUsername(this.username);
            // this.$router.push({name: 'Home'});

            //使得模態框消失
            this.$emit('update', false);
            //使得未登入訊息消失
            this.$emit('login_delete', true)
          }
        })
        .catch(error => {
          console.log('login failed 應該顯示sweet的報錯資訊' + error);
          console.log(this.$t('message.loginfailed'));
          this.showAlert();
        });
    },
    showAlert() {
      Swal.fire({
        title: 'Error!',
        text: this.$t('message.loginfailed'),
        icon: 'error',
        confirmButtonText: 'OK',
        customClass: {
          popup: 'swal2-popup-custom'
        }
      })
    }

  }
}
</script>

<style scoped>
.auth-wrap {
  display: grid;
  place-items: center;
  min-height: 64vh;
}
.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 34px;
}
.auth-head {
  margin-bottom: 22px;
}
.auth-title {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 1.5rem;
  color: var(--ink);
  margin: 8px 0 0;
}
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.auth-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}
.auth-group label {
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--ink-soft);
}
.auth-submit {
  margin-top: 6px;
  width: 100%;
}
.swal2-popup-custom {
  z-index: 2000 !important;
}
</style>
