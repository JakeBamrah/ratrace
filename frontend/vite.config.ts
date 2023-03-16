import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { visualizer } from "rollup-plugin-visualizer";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 3000,
    host: true
  },
  build: {
      outDir: 'build'
  },
  plugins: [svelte(), visualizer()],
})
