import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: '/webclient/',
  server: {
    proxy: {
      '^/master/.*': {
        target: 'http://localhost:5000',
        rewrite: (path) =>  path.replace(/^\/master/, ''),
      },
    },
  }
})
