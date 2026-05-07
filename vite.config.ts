import { defineConfig } from 'vite'
import yaml from '@modyfi/vite-plugin-yaml'

// Slidev picks up this config automatically. The YAML plugin lets the
// DataValue component (and any slide) `import manifest from '../manifest.yaml'`
// and access variables directly — no Python intermediate step required.
export default defineConfig({
  plugins: [yaml()],
})
