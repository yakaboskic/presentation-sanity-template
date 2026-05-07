# presentation-sanity template

A working Slidev deck driven by `manifest.yaml`. Eventually extracted into
its own repo that declares `presentation-sanity` as a dependency. For now
it lives inside the tool's repo and uses a path-based dep
(`tool.uv.sources.presentation-sanity = { path = ".." }`).

## Structure

```
template/
├── pyproject.toml          # declares presentation-sanity[manim] dep
├── package.json            # Slidev + vite-plugin-yaml
├── vite.config.ts          # registers the YAML plugin
├── manifest.yaml           # single source of config (variables, scenes, theme)
├── slides.md               # the deck
├── style.css               # opinionated global styles (auto-loaded by Slidev)
├── components/
│   └── DataValue.vue       # reads manifest.yaml directly; provenance tooltip
├── layouts/
│   └── manim.vue           # custom layout — full-screen manim slides
├── scenes/
│   └── intro.py            # manim source
├── public/                 # static assets (absolute paths from /)
│   └── manim/              # rendered videos (gitignored)
├── .cache/                 # manim render cache (gitignored)
└── dist/                   # build output (gitignored)
```

## One-time setup

```bash
uv sync                     # installs presentation-sanity[manim] + Python deps
npm install                 # installs Slidev side (~700 packages)

# For manim:
brew install ffmpeg cairo pango      # macOS
# LaTeX is needed for MathTex (TeX Live, BasicTeX, etc.)
```

## Daily workflow

```bash
uv run presentation-sanity dev          # slidev hot-reload at localhost:3030
uv run presentation-sanity build        # full pipeline → dist/
uv run presentation-sanity preview      # serve dist/ at localhost:8000
uv run presentation-sanity build-manim  # re-render only stale scenes
uv run presentation-sanity export pdf
uv run presentation-sanity export pptx
```

`build` runs: parse manifest → render stale manim scenes (cached by content
hash) → `slidev build` → static bundle in `dist/`.

`preview` exists because **double-clicking `dist/index.html` won't work** —
modern browsers refuse to load ES modules from `file://` URLs. Any HTTP
server is fine; `preview` is just the convenient one-liner. Your eventual
S3/R2/GitHub-Pages deploy will work because those serve over HTTP.

## Editing variables

Edit `manifest.yaml`. Slidev hot-reloads on save.

```yaml
variables:
  num_samples:
    value: 12453
    format: ","                       # , .2e .3f .1%
    description: "Total samples after QC filtering"
    source: "data/results.csv"        # informational, surfaced in tooltip
    command: "python scripts/fit.py"  # informational — not executed
    updated: "2026-04-29"
```

In a slide: `<DataValue var="num_samples" />` renders `12,453`. **Click
the underlined value** and a side panel slides in from the right showing
the provenance as a vertical graph: `inputs → command → variable`. Press
`Esc`, click the backdrop, or click the `×` to dismiss.

```
┌─── INPUTS ───────────────────────┐
│ data/results.csv                 │   ← blue
│ data/cohort_metadata.tsv         │
└──────────────────────────────────┘
              ↓
┌─── COMMAND ──────────────────────┐
│ python scripts/effect_size.py    │   ← amber, monospace
└──────────────────────────────────┘
              ↓
┌─── VARIABLE ─────────────────────┐
│ effect_size:.3f    [0.342]       │   ← green, the output
└──────────────────────────────────┘
```

Use `data:` (a list of file paths) for the multi-input case, or
`source:` (a single path) for the single-file fallback. The panel
renders whichever is present; if both are present, `data:` wins.

The panel is a singleton mounted via `global-bottom.vue` (Slidev's
convention for app-level overlays), wired through a tiny shared ref in
`composables/useProvenance.ts`. To restyle, edit
`components/ProvenancePanel.vue`.

## Adding a manim scene

1. **Write the scene.** Add a class to `scenes/<name>.py` (subclass `manim.Scene`).
2. **Register it** in `manifest.yaml` under `scenes:`:
   ```yaml
   scenes:
     my_scene:
       source: "scenes/my_scene.py"
       class: "MyScene"
       quality: "h"          # l | m | h | p | k  (low → 4k)
       format: "webm"
   ```
3. **Use it** in `slides.md` as a full-screen layout:
   ```markdown
   ---
   layout: manim
   scene: my_scene
   ---

   (optional caption text — overlaid at bottom)
   ```
4. `uv run presentation-sanity build-manim` to render. Subsequent builds
   skip rendering until the source `.py` file or the manifest entry changes.

The `manim` layout (`layouts/manim.vue` — Slidev uses the filename verbatim
as the layout name, so keep it lowercase to match `layout: manim`) handles
autoplay, click-to-replay
on revisit, and aspect-ratio fit. Frontmatter knobs:

| Key | Default | Description |
|---|---|---|
| `scene` | required | Manifest scene key |
| `format` | `webm` | Video format / extension |
| `autoplay` | `true` | Replay automatically on every slide entry |
| `controls` | `false` | Show video controls |
| `background` | `black` | Slide background color |
| `replayKey` | `r` | Press this key (while the slide is active) to replay |
| `pauseKey` | `p` | Toggle pause/play — handy for stopping on a key frame |

Click anywhere on the video to replay too — clicking is bound to the same
handler as the replay key. Pause/reset happens on slide leave, so revisits
always start from frame 0.

## Customizing styles

`style.css` is auto-loaded by Slidev. The default file ships with:

- Overview button hidden (`title="Show slide overview"`)
- More-options gear hidden
- Light highlight on `<DataValue>` text

Uncomment / add lines to taste. Anything outside `.slidev-layout` applies
globally, including to the presenter UI — scope under `.slidev-layout` to
keep changes confined to the slides themselves.

For per-slide CSS, use a scoped `<style>` block inside `slides.md`:

```html
<style scoped>
  h1 { color: tomato; }
</style>
```

## Static deployment

```bash
uv run presentation-sanity build
# upload dist/ to your bucket
aws s3 sync dist/ s3://my-talks/2026-talk/ --acl public-read
```

The deck uses **hash routing** (`#/2`, `#/3`, etc.) so it works on any
static host without SPA fallback config.
