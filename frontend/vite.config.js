import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/board': 'http://127.0.0.1:8000',
      '/user': 'http://127.0.0.1:8000',
      '/courses': 'http://127.0.0.1:8000',
      '/payments': 'http://127.0.0.1:8000',
    },
  },
})
