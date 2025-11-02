import { defineConfig } from 'vite'
import path from 'path'

import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: true,
    allowedHosts: ['3000-i3m2n8eobvcrimmw48831-4930c309.manusvm.computer'],
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },
  preview: {
    host: true,
    allowedHosts: [
      '3000-i3m2n8eobvcrimmw48831-4930c309.manusvm.computer',
      'xbpneus-frontend-qd8u.onrender.com',
      'xbpneus-frontend.onrender.com',
      '.onrender.com'
    ]
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    chunkSizeWarningLimit: 1500,
  }
})
