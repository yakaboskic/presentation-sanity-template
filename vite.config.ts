import { defineConfig } from 'vite'
import yaml from '@modyfi/vite-plugin-yaml'

// Slidev picks up this config automatically. The YAML plugin lets the
// DataValue component (and any slide) `import manifest from '../manifest.yaml'`
// and access variables directly — no Python intermediate step required.
//
// `base: './'` emits relative asset paths (e.g. `./assets/...`) so the
// built site works when served from a subdirectory (e.g.
// `https://host/preview/abc/`). Default `/` would 404 against
// `https://host/assets/...`.
export default defineConfig({
  base: './',
  plugins: [yaml()],
})
