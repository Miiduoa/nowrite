<template>
  <div class="auth-wrap">
    <section class="auth-card glass">
      <div v-if="notification.show" class="alert"
        :class="notification.type === 'success' ? 'alert-success' : 'alert-danger'">
        {{ notification.message }}
      </div>
      <div class="auth-head">
        <span class="eyebrow">✦ {{ $t('message.register') }}</span>
        <h2 class="auth-title">{{ $t('message.register') }}</h2>
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
        <button type="submit" class="btn-ink auth-submit">{{ $t('message.register') }}</button>
      </form>
    </section>
  </div>
</template>


<script>
export default {
    data() {
        return {
            username: '',
            password: '',
            csrfToken: '',
            notification: {
                show: false,
                message: '',
                type: '',
            }
        }
    },
    methods: {
      submitForm() {
  // Get CSRF token from server
  // this.$http.get('/api/csrf-token')
  //   .then(csrfResponse => {
  //     if (csrfResponse.status === 200) {
  //       this.csrfToken = csrfResponse.data.token;
  //       console.log('CSRF token: ' + this.csrfToken);
  //     } else {
  //       // Handle error here
  //       console.error('Failed to get CSRF token');
  //       return;
  //     }
  //   });

  this.$http.post('/api/register', {
    username: this.username,
    password: this.password,
  }, {
    headers: {
      'X-CSRFToken': this.csrfToken,
      'Content-Type': 'application/json',
    }
  })
  .then(response => {
    if (response.data.status === 'success') {
      this.notification = {
        show: true,
        message: this.$t('message.registersuccess'),
        type: 'success',
      };
      // this.$router.push({name: 'Home'});
      this.$emit('update', false);
    }
  })
  .catch(error => {
    this.notification = {
      show: true,
      message: this.$t('message.registerfailed'),
      type: 'error',
    };
    console.error('register failed' + error);
  });
}

    },

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
.alert {
  margin-bottom: 16px;
}
</style>
