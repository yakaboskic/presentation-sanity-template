<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'
// @ts-expect-error — resolved at build time by @modyfi/vite-plugin-yaml
import manifest from '../manifest.yaml'
import { hideProvenance, provenanceKey } from '../composables/useProvenance'

type Variable = {
  value: number | string
  format?: string
  description?: string
  source?: string
  /** List of input files. If present, renders the "inputs" node and source is hidden. */
  data?: string[]
  command?: string
  updated?: string
}

const variables = (manifest?.variables ?? {}) as Record<string, Variable>

const entry = computed<Variable | undefined>(() =>
  provenanceKey.value ? variables[provenanceKey.value] : undefined,
)

function formatNumber(n: number, spec: string): string {
  if (spec === ',') return n.toLocaleString()
  const m = spec.match(/^\.(\d+)([eEfg%])?$/)
  if (!m) return String(n)
  const digits = parseInt(m[1], 10)
  const kind = m[2] ?? 'f'
  if (kind === 'e' || kind === 'E') return n.toExponential(digits)
  if (kind === '%') return (n * 100).toFixed(digits) + '%'
  return n.toFixed(digits)
}

const formattedValue = computed(() => {
  const e = entry.value
  if (!e) return ''
  if (typeof e.value === 'number' && e.format) return formatNumber(e.value, e.format)
  return String(e.value)
})

const labelWithFmt = computed(() => {
  const k = provenanceKey.value
  const e = entry.value
  if (!k) return ''
  return e?.format ? `${k}:${e.format}` : k
})

const inputs = computed<string[]>(() => {
  const e = entry.value
  if (!e) return []
  if (Array.isArray(e.data) && e.data.length) return e.data
  if (e.source) return [e.source]
  return []
})

/** Distinguish 'inputs' (data list) from 'source' (single fallback) for the label. */
const inputsLabel = computed(() => {
  const e = entry.value
  return Array.isArray(e?.data) && (e.data?.length ?? 0) > 0 ? 'inputs' : 'source'
})

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && provenanceKey.value !== null) {
    e.preventDefault()
    hideProvenance()
  }
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <Transition name="provenance-fade">
    <div v-if="provenanceKey" class="provenance-backdrop" @click="hideProvenance" />
  </Transition>

  <Transition name="provenance-slide">
    <aside v-if="provenanceKey && entry" class="provenance-panel" role="dialog" aria-label="Variable provenance">
      <header class="prov-head">
        <h3 class="prov-title">Provenance</h3>
        <button type="button" class="prov-close" aria-label="Close (Esc)" title="Close (Esc)" @click="hideProvenance">×</button>
      </header>

      <p v-if="entry.description" class="prov-description">{{ entry.description }}</p>

      <div class="prov-graph">
        <template v-if="inputs.length">
          <div class="prov-node inputs">
            <span class="prov-label">{{ inputsLabel }}</span>
            <ul>
              <li v-for="path in inputs" :key="path">{{ path }}</li>
            </ul>
          </div>
          <div class="prov-arrow" aria-hidden="true">↓</div>
        </template>

        <template v-if="entry.command">
          <div class="prov-node command">
            <span class="prov-label">command</span>
            <div class="prov-command-text">{{ entry.command }}</div>
          </div>
          <div class="prov-arrow" aria-hidden="true">↓</div>
        </template>

        <div class="prov-node output">
          <span class="prov-label">variable</span>
          <span class="prov-output-name">{{ labelWithFmt }}</span>
          <span class="prov-output-value">{{ formattedValue }}</span>
        </div>
      </div>

      <p v-if="entry.updated" class="prov-updated">updated {{ entry.updated }}</p>
    </aside>
  </Transition>
</template>

<style scoped>
/* ─── colors (light) ─────────────────────────────────────── */
.provenance-panel {
  --p-border: rgba(0, 0, 0, 0.10);
  --p-border-strong: rgba(0, 0, 0, 0.16);
  --p-muted: rgba(0, 0, 0, 0.55);
  --p-fg: #0f172a;
  --p-bg: #ffffff;
  --p-card-bg: #ffffff;
  --p-chip-bg: rgba(0, 0, 0, 0.05);

  --p-blue: 96, 165, 250;       /* inputs */
  --p-amber: 245, 158, 11;      /* command */
  --p-green: 22, 163, 74;       /* output */
}

.provenance-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.18);
  z-index: 999;
  cursor: pointer;
}

.provenance-panel {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: min(420px, 90vw);
  background: var(--p-bg);
  color: var(--p-fg);
  z-index: 1000;
  padding: 1.6rem 1.6rem 1.4rem;
  box-shadow:
    -8px 0 32px rgba(0, 0, 0, 0.08),
    -1px 0 0 rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  font-size: 0.9rem;
  line-height: 1.5;
}

.prov-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.7rem;
  border-bottom: 1px solid var(--p-border);
}
.prov-title {
  margin: 0;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--p-muted);
  font-weight: 600;
}
.prov-close {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.4rem;
  line-height: 1;
  color: var(--p-muted);
  padding: 0.05rem 0.45rem;
  border-radius: 4px;
  transition: color 0.15s, background 0.15s;
}
.prov-close:hover {
  color: var(--p-fg);
  background: var(--p-chip-bg);
}

.prov-description {
  font-size: 0.88rem;
  color: var(--p-muted);
  margin: 0 0 1.1rem;
}

/* ─── the graph ────────────────────────────────────────── */
.prov-graph {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 0.2rem;
  margin: 0;
}
.prov-node {
  border: 1px solid var(--p-border);
  border-radius: 0.5rem;
  padding: 0.6rem 0.75rem;
  background: var(--p-card-bg);
  transition: border-color 0.15s, box-shadow 0.15s;
}
.prov-node .prov-label {
  display: block;
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--p-muted);
  font-weight: 600;
  margin-bottom: 0.3rem;
}
.prov-node ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.prov-node li {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.78rem;
  padding: 0.1rem 0;
  word-break: break-word;
}
.prov-node li + li {
  border-top: 1px dashed var(--p-border);
  margin-top: 0.25rem;
  padding-top: 0.3rem;
}

.prov-node.inputs {
  background: rgba(var(--p-blue), 0.08);
  border-color: rgba(var(--p-blue), 0.32);
}
.prov-node.command {
  background: rgba(var(--p-amber), 0.08);
  border-color: rgba(var(--p-amber), 0.32);
}
.prov-node.output {
  background: rgba(var(--p-green), 0.08);
  border-color: rgba(var(--p-green), 0.40);
}

.prov-command-text {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.78rem;
  word-break: break-word;
  color: var(--p-fg);
}

.prov-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--p-muted);
  font-size: 1.1rem;
  line-height: 1;
  height: 1.1rem;
}

.prov-output-name {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--p-fg);
}
.prov-output-value {
  display: inline-block;
  margin-left: 0.55rem;
  padding: 0.05rem 0.45rem;
  background: var(--p-chip-bg);
  border-radius: 0.25rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-variant-numeric: tabular-nums;
  font-size: 0.85rem;
}

.prov-updated {
  font-size: 0.72rem;
  color: var(--p-muted);
  text-align: right;
  margin: 1rem 0 0;
  font-variant-numeric: tabular-nums;
}

/* ─── transitions ────────────────────────────────────── */
.provenance-slide-enter-active,
.provenance-slide-leave-active {
  transition: transform 0.24s cubic-bezier(0.32, 0.72, 0.24, 1), opacity 0.24s ease-out;
}
.provenance-slide-enter-from,
.provenance-slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
.provenance-fade-enter-active,
.provenance-fade-leave-active {
  transition: opacity 0.2s ease-out;
}
.provenance-fade-enter-from,
.provenance-fade-leave-to {
  opacity: 0;
}

/* ─── dark mode ──────────────────────────────────────── */
@media (prefers-color-scheme: dark) {
  .provenance-panel {
    --p-border: rgba(255, 255, 255, 0.10);
    --p-border-strong: rgba(255, 255, 255, 0.18);
    --p-muted: rgba(255, 255, 255, 0.55);
    --p-fg: rgba(255, 255, 255, 0.92);
    --p-bg: #11161c;
    --p-card-bg: #181f27;
    --p-chip-bg: rgba(255, 255, 255, 0.06);
    box-shadow:
      -8px 0 32px rgba(0, 0, 0, 0.5),
      -1px 0 0 rgba(255, 255, 255, 0.06);
  }
  .prov-node.inputs   { background: rgba(var(--p-blue), 0.12);  }
  .prov-node.command  { background: rgba(var(--p-amber), 0.12); }
  .prov-node.output   { background: rgba(var(--p-green), 0.14); }
}
:global(html.dark) .provenance-panel {
  --p-border: rgba(255, 255, 255, 0.10);
  --p-border-strong: rgba(255, 255, 255, 0.18);
  --p-muted: rgba(255, 255, 255, 0.55);
  --p-fg: rgba(255, 255, 255, 0.92);
  --p-bg: #11161c;
  --p-card-bg: #181f27;
  --p-chip-bg: rgba(255, 255, 255, 0.06);
  box-shadow:
    -8px 0 32px rgba(0, 0, 0, 0.5),
    -1px 0 0 rgba(255, 255, 255, 0.06);
}
:global(html.dark) .prov-node.inputs   { background: rgba(var(--p-blue), 0.12); }
:global(html.dark) .prov-node.command  { background: rgba(var(--p-amber), 0.12); }
:global(html.dark) .prov-node.output   { background: rgba(var(--p-green), 0.14); }
</style>
