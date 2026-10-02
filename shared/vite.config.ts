import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig, type Plugin } from 'vite'
import yaml from '@modyfi/vite-plugin-yaml'

// `import segments from 'virtual:psanity-manim'` → { <scene>: segments.json }
// for every stepped scene under public/manim/<scene>/. The manim-steps layout
// must know its segment count *synchronously* when it mounts: that's when it
// registers one Slidev click per segment, and the click-by-click export counts
// what is registered at mount. Files in public/ can't be imported directly, so
// this plugin reads them from disk (and re-reads them when they change).
function manimSegments(): Plugin {
  const id = 'virtual:psanity-manim'
  const resolved = '\0' + id
  const dir = fileURLToPath(new URL('../public/manim', import.meta.url))
  return {
    name: 'psanity-manim-segments',
    resolveId: source => (source === id ? resolved : undefined),
    load(loaded) {
      if (loaded !== resolved) return
      const index: Record<string, unknown> = {}
      for (const key of existsSync(dir) ? readdirSync(dir) : []) {
        const file = join(dir, key, 'segments.json')
        if (!existsSync(file)) continue
        this.addWatchFile(file)
        index[key] = JSON.parse(readFileSync(file, 'utf8'))
      }
      return `export default ${JSON.stringify(index)}`
    },
  }
}

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
  plugins: [yaml(), manimSegments()],

  slidev: {
    components: {
      // Slidev resolves same-named components first-wins (shared before deck);
      // flip that so presentations/<name>/components/X.vue overrides X.vue here.
      allowOverrides: true,
    },
  },
})
