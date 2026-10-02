import { defineConfig } from 'vite'
import yaml from '@modyfi/vite-plugin-yaml'

// SLIDEV ONLY. Slidev merges this file into its Vite config; the blog does
// not — `presentation-sanity` generates a self-contained `.vitepress/config.mts`
// with `configFile: false` so this one is never applied twice. (It must not be:
// a second yaml() pass re-parses the emitted JS as YAML and hands components a
// string, and `base: './'` below is invalid for VitePress's router.)
//
// The YAML plugin lets the DataValue component (and any slide) `import manifest
// from '../manifest.yaml'` and access variables directly — no Python
// intermediate step required.
//
// `base: './'` emits relative asset paths (e.g. `./assets/...`) so the
// built deck works when served from a subdirectory (e.g.
// `https://host/preview/abc/`). Default `/` would 404 against
// `https://host/assets/...`.
export default defineConfig({
  base: './',
  plugins: [yaml()],
})
