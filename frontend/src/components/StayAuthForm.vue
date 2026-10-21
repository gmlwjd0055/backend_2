<script>
import { computed, reactive } from 'vue'

export default {
  props: {
    mode: { type: String, default: 'login', validator: value => ['login', 'signup'].includes(value) },
    busy: { type: Boolean, default: false },
    error: { type: String, default: '' },
    providers: { type: Array, default: () => ['naver', 'google', 'apple'] },
  },
  emits: ['submit', 'social-login', 'change-mode'],
  setup(props, { emit }) {
    const fields = reactive({ name: '', email: '', password: '' })
    const signup = computed(() => props.mode === 'signup')
    function submit() {
      emit('submit', { ...fields })
    }
    function providerLabel(provider) {
      return ({ naver: '네이버', google: 'Google', apple: 'Apple' })[provider] || provider
    }
    return { fields, signup, emit, submit, providerLabel }
  },
}
</script>

<template>
  <section class="stay-auth" :aria-labelledby="'stay-auth-title'">
    <div class="stay-auth__head"><span class="stay-auth__logo" aria-hidden="true">s</span><h1 id="stay-auth-title">{{ signup ? '회원가입' : '로그인' }}</h1></div>
    <p class="stay-auth__intro">{{ signup ? '새로운 여행을 함께 시작해요.' : '다시 만나 반가워요.' }}</p>
    <p v-if="error" class="stay-auth__error" role="alert">{{ error }}</p>
    <form class="stay-auth__form" @submit.prevent="submit">
      <label v-if="signup">이름<input v-model="fields.name" autocomplete="name" required></label>
      <label>이메일<input v-model="fields.email" type="email" autocomplete="email" required></label>
      <label>비밀번호<input v-model="fields.password" type="password" :autocomplete="signup ? 'new-password' : 'current-password'" minlength="8" required></label>
      <p v-if="signup" class="stay-auth__terms">계속 진행하면 서비스 이용약관과 개인정보 처리방침에 동의하는 것으로 간주됩니다.</p>
      <button class="stay-auth__submit" type="submit" :disabled="busy">{{ busy ? '잠시만 기다려 주세요…' : signup ? '가입하기' : '로그인' }}</button>
    </form>
    <div v-if="providers.length" class="stay-auth__providers" aria-label="다른 로그인 방법">
      <button v-for="provider in providers" :key="provider" class="stay-auth__social" type="button" @click="emit('social-login', provider)">{{ providerLabel(provider) }} 계정으로 계속하기</button>
    </div>
    <p class="stay-auth__switch">{{ signup ? '이미 계정이 있나요?' : '아직 계정이 없나요?' }} <button type="button" @click="emit('change-mode', signup ? 'login' : 'signup')">{{ signup ? '로그인' : '회원가입' }}</button></p>
  </section>
</template>

<style scoped>
.stay-auth{width:min(100%,430px);margin:auto;padding:30px;border:1px solid #ddd;border-radius:14px;background:#fff;color:#222}.stay-auth__head{display:flex;align-items:center;gap:12px;padding-bottom:18px;border-bottom:1px solid #eee}.stay-auth__head h1{margin:0;font-size:20px}.stay-auth__logo{display:grid;place-items:center;width:31px;height:31px;border-radius:50%;background:#FAED7D;font:italic 22px Georgia,serif}.stay-auth__intro{margin:20px 0;color:#444;font-size:15px;font-weight:650}.stay-auth__form{display:grid;gap:14px}.stay-auth__form label{display:grid;gap:7px;font-size:12px;font-weight:650}.stay-auth__form input{height:47px;padding:0 12px;border:1px solid #999;border-radius:7px;background:#fff;font:inherit;font-size:14px}.stay-auth__form input:focus{outline:2px solid #222;outline-offset:1px}.stay-auth__terms{margin:0;color:#717171;font-size:10px;line-height:1.6}.stay-auth__submit,.stay-auth__social{width:100%;min-height:48px;border-radius:8px;font-size:13px;font-weight:650;cursor:pointer}.stay-auth__submit{border:0;background:#FAED7D;color:#222}.stay-auth__submit:hover:not(:disabled){background:#f4e45b}.stay-auth__submit:disabled{opacity:.6;cursor:wait}.stay-auth__providers{display:grid;gap:9px;margin-top:12px}.stay-auth__social{border:1px solid #222;background:#fff;color:#222}.stay-auth__social:hover{background:#f7f7f7}.stay-auth__switch{margin:22px 0 0;text-align:center;font-size:12px}.stay-auth__switch button{padding:0;border:0;background:none;color:#222;font-size:12px;font-weight:700;text-decoration:underline;cursor:pointer}.stay-auth__error{padding:10px;border-radius:7px;background:#fff1f0;color:#b42318;font-size:12px}
@media(max-width:480px){.stay-auth{padding:22px 18px;border:0;border-radius:0}.stay-auth__head h1{font-size:18px}}
</style>
