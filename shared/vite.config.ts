import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import yaml from '@modyfi/vite-plugin-yaml'

// SLIDEV ONLY. This folder is a local Slidev *addon* (see ./package.json),
// enabled for every deck by the root package.json's `"slidev": {"addons"}`.
// Slidev merges this file into each deck's Vite config. The blogs don't read
// it — presentation-sanity generates a self-contained VitePress config with
// `configFile: false` (a second yaml() pass would hand components a string).
export default defineConfig({
  // Relative asset paths: a built deck works from any URL prefix
  // (e.g. https://host/talks/kickoff/slides/).
  base: './',

  // Every deck serves the PROJECT's public/ — logos, figures, rendered manim
  // videos. Must be absolute: a relative publicDir resolves against the deck's
  // own folder (presentations/<name>/), not this file.
  publicDir: fileURLToPath(new URL('../public', import.meta.url)),

  // Depth-independent imports for components: `@project/manifest.yaml`,
  // `@shared/composables/…`. A component copied into presentations/<name>/
  // to override the shared one keeps working unchanged. presentation-sanity
  // defines the same two aliases for the blogs.
  resolve: {
    alias: {
      '@project': fileURLToPath(new URL('..', import.meta.url)),
      '@shared': fileURLToPath(new URL('.', import.meta.url)),
    },
  },

  // Lets `import manifest from '@project/manifest.yaml'` in components work.
  // Register it here and nowhere else.
  plugins: [yaml()],

  slidev: {
    components: {
      // Slidev resolves same-named components first-wins (shared before deck);
      // flip that so presentations/<name>/components/X.vue overrides X.vue here.
      allowOverrides: true,
    },
  },
})
