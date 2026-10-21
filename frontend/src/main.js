import { createApp } from 'vue'
import App from './App.vue'
import './assets/style.css'

window.__KAKAO_JS_KEY__ = import.meta.env.VITE_KAKAO_JS_KEY || ''

if (window.Kakao && import.meta.env.VITE_KAKAO_JS_KEY && !window.Kakao.isInitialized()) {
  window.Kakao.init(import.meta.env.VITE_KAKAO_JS_KEY)
}

createApp(App).mount('#app')
