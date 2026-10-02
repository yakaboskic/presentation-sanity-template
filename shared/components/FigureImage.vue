<script setup lang="ts">
/**
 * An Excalidraw figure exported by `presentation-sanity build-figures`,
 * resolved to `<BASE_URL>figures/<figure>.<format>` — the same file the deck
 * references, so a diagram is drawn once and printed twice.
 *
 *   <FigureImage figure="architecture" caption="The build pipeline." />
 *
 * Exports default to transparent SVG, which reads correctly on light and
 * dark backgrounds without a second export.
 */
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    /** Figure key under `figures:` in manifest.yaml */
    figure: string
    /** File extension the manifest exports (default svg) */
    format?: string
    caption?: string
    alt?: string
    width?: string
  }>(),
  { format: 'svg', width: '100%' },
)

const src = computed(
  () => `${import.meta.env.BASE_URL}figures/${props.figure}.${props.format}`,
)
</script>

<template>
  <figure class="ps-figure" :style="{ maxWidth: width }">
    <img class="ps-figure__img" :src="src" :alt="alt ?? caption ?? figure" />
    <figcaption v-if="caption || $slots.default" class="ps-figure__caption">
      <slot>{{ caption }}</slot>
    </figcaption>
  </figure>
</template>

<style scoped>
.ps-figure {
  margin: 2rem auto;
}
.ps-figure__img {
  display: block;
  width: 100%;
  height: auto;
}
.ps-figure__caption {
  margin-top: 0.6rem;
  font-size: 0.86em;
  line-height: 1.5;
  opacity: 0.7;
  text-align: center;
}
</style>
