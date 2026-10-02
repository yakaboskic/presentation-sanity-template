<script setup lang="ts">
/**
 * Full-screen manim layout.
 *
 * Usage in slides.md:
 *
 *   ---
 *   layout: manim
 *   scene: intro          # required — matches a key in manifest.scenes
 *   format: webm          # optional, default webm
 *   autoplay: true        # optional — play on every slide entry (default true)
 *   controls: false       # optional — show video controls (default false)
 *   background: black     # optional — slide background (default black)
 *   replayKey: r          # optional — key to replay (default 'r')
 *   pauseKey: p           # optional — key to toggle pause/play (default 'p')
 *   ---
 *
 * Plays automatically every time you enter the slide. Click anywhere on
 * the video, or press the replayKey, to replay. Press the pauseKey to
 * freeze on the current frame and again to resume.
 *
 * Resolves the video to <BASE_URL>manim/<scene>.<format> — exactly where
 * `presentation-sanity build-manim` writes its output. Using
 * `import.meta.env.BASE_URL` so the path follows Vite's `base` setting
 * (necessary when the built site is served from a subdirectory; Vite's
 * base rewriting only applies to static imports, not runtime strings).
 */
import { onSlideEnter, onSlideLeave, useIsSlideActive } from '@slidev/client'
import { computed, onMounted, onUnmounted, ref } from 'vue'

const props = withDefaults(
  defineProps<{
    scene: string
    format?: string
    autoplay?: boolean
    controls?: boolean
    background?: string
    replayKey?: string
    pauseKey?: string
  }>(),
  {
    format: 'webm',
    autoplay: true,
    controls: false,
    background: 'black',
    replayKey: 'r',
    pauseKey: 'p',
  },
)

const src = computed(() => `${import.meta.env.BASE_URL}manim/${props.scene}.${props.format}`)
const video = ref<HTMLVideoElement>()
const isActive = useIsSlideActive()

function replay() {
  const v = video.value
  if (!v) return
  v.currentTime = 0
  void v.play()
}

function togglePause() {
  const v = video.value
  if (!v) return
  if (v.paused) void v.play()
  else v.pause()
}

function pauseAndReset() {
  const v = video.value
  if (!v) return
  v.pause()
  v.currentTime = 0
}

onSlideEnter(() => {
  if (props.autoplay) replay()
})
onSlideLeave(pauseAndReset)

function onKeydown(e: KeyboardEvent) {
  if (!isActive.value) return
  // Don't intercept while typing in inputs/textareas (Goto, Monaco, etc.)
  const t = e.target as HTMLElement | null
  if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return
  const k = e.key.toLowerCase()
  if (k === props.replayKey.toLowerCase()) {
    e.preventDefault()
    replay()
  }
  else if (k === props.pauseKey.toLowerCase()) {
    e.preventDefault()
    togglePause()
  }
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <div class="slidev-layout manim-layout" :style="{ background }">
    <!-- `muted` is required for browser autoplay policies; click/keys still play with sound off -->
    <video
      ref="video"
      class="manim-video"
      :controls="controls"
      preload="auto"
      muted
      playsinline
      @click="replay"
    >
      <source :src="src" :type="`video/${format}`" />
      <p class="manim-fallback">
        Video not found at <code>{{ src }}</code>.<br />
        Render with <code>presentation-sanity build-manim</code>.
      </p>
    </video>

    <!-- Key-hint affordances, top-right. Subtle by default; restyle in style.css. -->
    <div class="manim-hint">
      <kbd>{{ replayKey }}</kbd> replay
      <span class="manim-hint-sep">·</span>
      <kbd>{{ pauseKey }}</kbd> pause
    </div>

    <!-- Optional caption overlay from slide content -->
    <div class="manim-slot">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.manim-layout {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
  overflow: hidden;
}
.manim-video {
  width: 100%;
  height: 100%;
  object-fit: contain;
  cursor: pointer;
}
.manim-fallback {
  color: white;
  font-family: monospace;
  font-size: 1.1rem;
  text-align: center;
  padding: 2rem;
}
.manim-hint {
  position: absolute;
  top: 0.9rem;
  right: 0.9rem;
  color: rgba(255, 255, 255, 0.32);
  font-size: 0.68rem;
  font-weight: 300;
  pointer-events: none;
  user-select: none;
  letter-spacing: 0.03em;
}
.manim-hint kbd {
  display: inline-block;
  padding: 0 0.35em;
  margin-right: 0.2em;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 2px;
  font-family: ui-monospace, Menlo, monospace;
  font-size: 0.9em;
  font-weight: 400;
}
.manim-hint-sep {
  margin: 0 0.5em;
  opacity: 0.5;
}
.manim-slot {
  position: absolute;
  bottom: 1.5rem;
  left: 0;
  right: 0;
  text-align: center;
  color: rgba(255, 255, 255, 0.85);
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.6);
  pointer-events: none;
}
.manim-slot:empty {
  display: none;
}
</style>
