<script setup lang="ts">
import { computed } from 'vue'
// @ts-expect-error — resolved at build time by @modyfi/vite-plugin-yaml
import manifest from '../manifest.yaml'
import { showProvenance } from '../composables/useProvenance'

const props = defineProps<{
  /** Variable key in manifest.yaml under `variables:` */
  var: string
  /** Override the format spec from the manifest. Python-style: `,`, `.2e`, `.3f`, `.1%` */
  format?: string
}>()

type Variable = {
  value: number | string
  format?: string
  description?: string
  source?: string
  command?: string
  updated?: string
}

const variables = (manifest?.variables ?? {}) as Record<string, Variable>
const entry = computed<Variable | undefined>(() => variables[props.var])

const hasProvenance = computed(() => {
  const e = entry.value
  return !!(e?.description || e?.source || e?.command || e?.updated)
})

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

const formatted = computed(() => {
  if (!entry.value) return `??${props.var}??`
  const spec = props.format ?? entry.value.format
  if (typeof entry.value.value === 'number' && spec) {
    return formatNumber(entry.value.value, spec)
  }
  return String(entry.value.value)
})

function onClick() {
  if (entry.value) showProvenance(props.var)
}
</script>

<template>
  <span
    class="data-value"
    :class="{
      'data-value--missing': !entry,
      'data-value--clickable': !!entry && hasProvenance,
    }"
    :role="entry && hasProvenance ? 'button' : undefined"
    :tabindex="entry && hasProvenance ? 0 : undefined"
    @click="onClick"
    @keydown.enter="onClick"
    @keydown.space.prevent="onClick"
  >{{ formatted }}</span>
</template>

<style scoped>
.data-value {
  border-bottom: 1px dashed currentColor;
}
.data-value--clickable {
  cursor: pointer;
  transition: background-color 0.15s;
  border-radius: 2px;
  padding: 0 0.15em;
}
.data-value--clickable:hover {
  background-color: rgba(94, 131, 146, 0.18);
}
.data-value--clickable:focus-visible {
  outline: 2px solid rgba(94, 131, 146, 0.5);
  outline-offset: 1px;
}
.data-value--missing {
  background: rgba(255, 80, 80, 0.2);
  color: #c00;
  cursor: not-allowed;
}
</style>
