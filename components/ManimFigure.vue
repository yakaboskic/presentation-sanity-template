<script setup lang="ts">
/**
 * A manim scene as an inline *figure* — the blog counterpart to the deck's
 * `layout: manim` full-screen slide. Same rendered artifact, different
 * printout: both resolve `<BASE_URL>manim/<scene>.<format>`, exactly where
 * `presentation-sanity build-manim` writes.
 *
 * Usage in blog.md (globally registered, no import needed):
 *
 *   <ManimFigure scene="intro" caption="How a trait becomes a phenotype." />
 *
 * Plays when scrolled into view and pauses when scrolled out, so a page with
 * several scenes doesn't run them all at once. Click to replay.
 *
 * `import.meta.env.BASE_URL` keeps the src correct under a subdirectory
 * deploy — Vite only rewrites static imports, not runtime strings.
 */
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const props = withDefaults(
  defineProps<{
    /** Scene key under `scenes:` in manifest.yaml */
    scene: string
    /** Video container extension (default webm) */
    format?: string
    /** Caption rendered under the video; the default slot wins if provided */
    caption?: string
    /** Play/pause automatically as the figure enters/leaves the viewport */
    autoplay?: boolean
    /** Loop playback */
    loop?: boolean
    /** Show native video controls */
    controls?: boolean
    /** Max width of the figure (any CSS length) */
    width?: string
  }>(),
  {
    format: 'webm',
    autoplay: true,
    loop: false,
    controls: true,
    width: '100%',
  },
)

const base = import.meta.env.BASE_URL
const src = computed(() => `${base}manim/${props.scene}.${props.format}`)
// `build-manim` extracts the LAST frame — usually the finished diagram — so
// the figure reads correctly before playback and in print/PDF.
const poster = computed(() => `${base}manim/${props.scene}.poster.png`)

const video = ref<HTMLVideoElement>()
let observer: IntersectionObserver | undefined

function replay() {
  const v = video.value
  if (!v) return
  v.currentTime = 0
  void v.play()
}

onMounted(() => {
  if (!props.autoplay || typeof IntersectionObserver === 'undefined') return
  const v = video.value
  if (!v) return
  observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) void v.play()
      else v.pause()
    },
    { threshold: 0.35 },
  )
  observer.observe(v)
})

onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <figure class="manim-figure" :style="{ maxWidth: width }">
    <!-- `muted` is required by browser autoplay policies -->
    <video
      ref="video"
      class="manim-figure__video"
      :controls="controls"
      :loop="loop"
      :poster="poster"
      preload="metadata"
      muted
      playsinline
      @click="replay"
    >
      <source :src="src" :type="`video/${format}`" />
      <p>
        Video not found at <code>{{ src }}</code>. Render it with
        <code>presentation-sanity build-manim</code>.
      </p>
    </video>
    <figcaption v-if="caption || $slots.default" class="manim-figure__caption">
      <slot>{{ caption }}</slot>
    </figcaption>
  </figure>
</template>

<style scoped>
.manim-figure {
  margin: 2rem auto;
}
.manim-figure__video {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 6px;
  background: #000;
  cursor: pointer;
}
.manim-figure__caption {
  margin-top: 0.6rem;
  font-size: 0.86em;
  line-height: 1.5;
  opacity: 0.7;
  text-align: center;
}
</style>
