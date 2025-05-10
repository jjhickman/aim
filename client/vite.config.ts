import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 4173,
    host: '0.0.0.0',
    origin: 'http://localhost:4173',
  },
  preview: {
    host: '0.0.0.0',
    port: 4173
  },
  resolve: {
    preserveSymlinks: true,
  }
})
