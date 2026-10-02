<script setup lang="ts">
/**
 * A manim scene stepped through on clicks: one segment per click.
 *
 *   ---
 *   layout: manim-steps
 *   scene: intro_steps      # a manifest scene with `steps: true`
 *   ---
 *
 * The scene subclasses manim_slides.Slide and ends each segment with
 * `self.next_slide()`; `presentation-sanity build-manim` cuts the render into
 * public/manim/<scene>/NN.webm, a last-frame poster per segment, and a
 * segments.json index (exposed here through `virtual:psanity-manim`).
 *
 * Entering the slide plays segment 0; each click plays the next segment; after
 * the last one the next click moves to the next slide. Going back shows the
 * previous checkpoint's final frame. A `loop` segment repeats until the next
 * click; an `auto_next` segment advances on its own when it ends. Exports and
 * previews show the checkpoint's poster instead of playing. Press `r` to
 * replay the current segment.
 */
import { computed, onMounted, onUnmounted, ref, watch, watchEffect } from 'vue'
import { useIsSlideActive, useNav, useSlideContext } from '@slidev/client'
// @ts-expect-error — provided by the psanity-manim-segments plugin in shared/vite.config.ts
import index from 'virtual:psanity-manim'

type Segment = { file: string; poster?: string; loop?: boolean; auto_next?: boolean; notes?: string }
type SceneIndex = { background?: string; segments: Segment[] }

const props = withDefaults(
  defineProps<{
    scene: string
    background?: string
    replayKey?: string
  }>(),
  { replayKey: 'r' },
)

const entry = (index as Record<string, SceneIndex>)[props.scene]
const segments: Segment[] = entry?.segments ?? []
const last = Math.max(segments.length - 1, 0)
const base = `${import.meta.env.BASE_URL}manim/${props.scene}/`
const bg = computed(() => props.background ?? entry?.background ?? 'black')

const { $clicksContext, $renderContext } = useSlideContext()
const { isPrintMode, next } = useNav()
const isActive = useIsSlideActive()
// Only the real slide view plays; exports, overview and the presenter's
// "next" preview show the checkpoint's poster.
const live = computed(() => !isPrintMode.value && ['slide', 'presenter'].includes($renderContext.value))

// N segments take N-1 clicks — Slidev's own VSwitch pattern. Registered in
// onMounted (before the slide finishes mounting) so the click-by-click export
// counts them; the step follows the slide's click position reactively.
const step = ref(0)
const clickId = `manim-steps-${props.scene}-${Math.random().toString(36).slice(2, 8)}`
onMounted(() => {
  if (segments.length < 2) return
  const info = $clicksContext.calculateSince('+1', segments.length - 1)
  if (!info) {
    step.value = last // clicks disabled (e.g. a final-state export)
    return
  }
  $clicksContext.register(clickId, info)
  watchEffect(() => {
    step.value = Math.min(Math.max(info.currentOffset.value + 1, 0), last)
  })
})
onUnmounted(() => $clicksContext.unregister(clickId))

const videos = ref<HTMLVideoElement[]>([])
const current = ref(0)
const playing = ref(false)

const poster = (k: number) => (k >= 0 && segments[k]?.poster ? base + segments[k].poster : undefined)
// What sits under the videos: the state the current segment starts from (the
// previous checkpoint's last frame), so a segment switch never flashes black.
const underlay = computed(() => {
  if (!live.value) return poster(step.value)
  return playing.value ? poster(current.value - 1) : poster(current.value)
})

function pauseAll(except = -1) {
  videos.value.forEach((v, i) => i !== except && v.pause())
}

function play(k: number) {
  current.value = k
  playing.value = true
  pauseAll(k)
  const v = videos.value[k]
  if (!v) return
  v.currentTime = 0
  void v.play().catch(() => {})
}

function still(k: number) {
  current.value = k
  playing.value = false
  pauseAll()
}

function onEnded(i: number) {
  // An ended <video> keeps showing its last frame, so nothing to swap.
  if (i === current.value && segments[i]?.auto_next && isActive.value && live.value) next()
}

let previous = -1
watch(
  [step, isActive, live, () => videos.value.length],
  ([k, active, isLive]) => {
    if (!isLive) return
    if (!active) {
      pauseAll()
      previous = -1
      return
    }
    if (videos.value.length < segments.length) return // not mounted yet
    // Forward by one (or entering at the start) plays; anything else — going
    // back, or arriving from the next slide on the last step — shows the
    // checkpoint's end state. Loops always play.
    const forward = previous === -1 ? k === 0 : k === previous + 1
    if (forward || segments[k]?.loop) play(k)
    else if (k !== previous) still(k)
    previous = k
  },
  { flush: 'post' },
)

function onKeydown(e: KeyboardEvent) {
  if (!isActive.value || !live.value) return
  const t = e.target as HTMLElement | null
  if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return
  if (e.key.toLowerCase() === props.replayKey.toLowerCase()) {
    e.preventDefault()
    play(current.value)
  }
}
onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <div class="slidev-layout manim-steps-layout" :style="{ background: bg }">
    <p v-if="!segments.length" class="manim-steps-missing">
      No segments for <code>{{ scene }}</code> — set <code>steps: true</code> on the scene and run
      <code>presentation-sanity build-manim</code>.
    </p>
    <img v-if="underlay" class="manim-steps-frame" :src="underlay" alt="" />
    <template v-if="live">
      <video
        v-for="(s, i) in segments"
        :key="s.file"
        :ref="(el) => { if (el) videos[i] = el as HTMLVideoElement }"
        class="manim-steps-frame"
        :class="{ 'is-visible': playing && current === i }"
        :src="base + s.file"
        :loop="s.loop"
        preload="auto"
        muted
        playsinline
        @ended="onEnded(i)"
      />
    </template>
    <div class="manim-steps-slot">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.manim-steps-layout {
  position: absolute;
  inset: 0;
  padding: 0;
  margin: 0;
  overflow: hidden;
}
.manim-steps-frame {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}
video.manim-steps-frame {
  opacity: 0;
}
video.manim-steps-frame.is-visible {
  opacity: 1;
}
.manim-steps-missing {
  position: absolute;
  inset: 0;
  display: grid;
  place-content: center;
  color: white;
  font-family: monospace;
  text-align: center;
  padding: 2rem;
}
.manim-steps-slot {
  position: absolute;
  bottom: 1.5rem;
  left: 0;
  right: 0;
  text-align: center;
  color: rgba(255, 255, 255, 0.85);
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.6);
  pointer-events: none;
}
.manim-steps-slot:empty {
  display: none;
}
</style>
