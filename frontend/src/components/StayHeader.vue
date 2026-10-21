<script>
export default {
  props: {
    brand: { type: String, default: 'stay.' },
    user: { type: Object, default: null },
  },
  emits: ['home', 'login', 'signup', 'host', 'menu'],
  setup(props, { emit }) {
    return { emit }
  },
}
</script>

<template>
  <header class="stay-header">
    <button class="stay-header__brand" type="button" aria-label="홈으로" @click="emit('home')">
      <span class="stay-header__mark" aria-hidden="true">s</span>
      <span>{{ brand }}</span>
    </button>
    <nav class="stay-header__center" aria-label="주요 메뉴">
      <slot name="navigation">
        <button class="stay-header__nav-item stay-header__nav-item--active" type="button">숙소</button>
        <button class="stay-header__nav-item" type="button">체험</button>
        <button class="stay-header__nav-item" type="button">서비스</button>
      </slot>
    </nav>
    <div class="stay-header__actions">
      <button class="stay-header__host" type="button" @click="emit('host')">호스트 되기</button>
      <button v-if="!user" class="stay-header__login" type="button" @click="emit('login')">로그인</button>
      <span v-else class="stay-header__user">{{ user.name || user.email }}</span>
      <button class="stay-header__menu" type="button" aria-label="메뉴 열기" @click="emit('menu')">
        <span aria-hidden="true">☰</span><span class="stay-header__avatar" aria-hidden="true">●</span>
      </button>
    </div>
  </header>
</template>

<style scoped>
.stay-header{height:80px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:24px;padding:0 clamp(20px,5vw,76px);border-bottom:1px solid #ebebeb;background:#fff;color:#222}
.stay-header button{font:inherit;color:inherit;cursor:pointer}.stay-header__brand{display:flex;align-items:center;gap:9px;width:max-content;border:0;background:none;font-size:21px;font-weight:750;letter-spacing:-.06em}.stay-header__mark{display:grid;place-items:center;width:32px;height:32px;border-radius:50%;background:#FAED7D;color:#222;font-family:Georgia,serif;font-size:23px;font-style:italic;font-weight:400}
.stay-header__center,.stay-header__actions{display:flex;align-items:center;gap:22px}.stay-header__nav-item{position:relative;border:0;background:none;padding:12px 8px;color:#717171!important;font-size:14px!important}.stay-header__nav-item--active{color:#222!important;font-weight:650}.stay-header__nav-item--active:after{position:absolute;right:8px;bottom:-1px;left:8px;height:2px;background:#FAED7D;content:""}.stay-header__actions{justify-content:flex-end;gap:12px}.stay-header__host,.stay-header__login{border:0;background:none;padding:10px 12px;font-size:13px!important;font-weight:600!important}.stay-header__host:hover,.stay-header__login:hover{border-radius:22px;background:#f7f7f7}.stay-header__menu{display:flex;align-items:center;gap:11px;padding:6px 8px;border:1px solid #ddd;border-radius:24px;background:#fff}.stay-header__avatar{display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:#FAED7D;color:#222;font-size:10px}.stay-header__user{max-width:130px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:13px}
@media(max-width:720px){.stay-header{height:68px;grid-template-columns:1fr auto;padding:0 16px}.stay-header__center{display:none}.stay-header__host{display:none}.stay-header__actions{gap:4px}.stay-header__brand{font-size:19px}}
</style>
