# presentation-sanity-template

A working **subject** driven by `manifest.yaml`: one set of variables, manim
scenes and figures, rendered into two printouts — a **Slidev deck**
(`slides.md`) and a **VitePress blog post** (`blog.md`). Use this repo as a
starting point: clone it (or "Use this template"), run `python init.py` to set
the name and authors, then write.

Declares [`presentation-sanity`](https://github.com/yakaboskic/presentation-sanity)
as a git dependency. By default the install **does not pull manim** —
pre-rendered videos live in `public/manim/` and travel with the repo, so
deploying doesn't require cairo/pango/native build tools. Add the `[manim]`
extra (see below) only when you want to render scenes locally.

## Why VitePress for the blog

Slidev and VitePress sit on the *same* substrate — Vite + Vue 3 + markdown-it +
Shiki. That's the whole reason for the pairing: your components, composables,
manifest and rendered assets are consumed unchanged by both. `<DataValue
var="n" />` in `blog.md` reads the same YAML as the same tag in `slides.md`;
a manim scene renders once and is embedded twice.

## Structure

```
your-subject/
├── init.py                 # one-time bootstrap: prompts for name, title, authors
├── pyproject.toml          # declares presentation-sanity dep (manim is optional)
├── package.json            # Slidev + VitePress + vite-plugin-yaml
├── manifest.yaml           # SINGLE SOURCE: outputs, variables, scenes, figures
│
├── blog.md                 # ← the blog   (VitePress; served at /)
├── slides.md               # ← the deck   (Slidev)
├── refs.bib                # ← bibliography source for \cite{}
│
├── components/             # SHARED by both renderers, auto-registered globally
│   ├── DataValue.vue       #   variable + provenance tooltip
│   ├── ProvenancePanel.vue #   the slide-in provenance graph (singleton)
│   ├── ManimFigure.vue     #   a manim scene as an inline blog figure
│   └── FigureImage.vue     #   an exported Excalidraw figure
├── composables/            # SHARED
├── layouts/manim.vue       # Slidev-only: full-screen manim slide
├── scenes/intro.py         # SHARED manim source
├── public/                 # SHARED static assets (served at / by both)
│   ├── manim/              #   rendered videos + last-frame posters
│   └── figures/            #   exported Excalidraw SVGs
│
├── style.css               # Slidev-only global styles (auto-loaded by Slidev)
├── blog.css                # VitePress-only styles (imported into the theme)
├── vite.config.ts          # SLIDEV ONLY — VitePress builds with configFile:false
│
├── .vitepress/             # GENERATED from manifest.yaml every build (gitignored)
├── .cache/                 # manim/figure/vitepress caches (gitignored)
└── site/                   # build output (gitignored)
    ├── index.html          #   landing page linking each printout
    ├── blog/
    └── slides/
```

## One-time setup

```bash
python init.py              # set name, title, authors (run once on a fresh clone)
uv sync                     # installs presentation-sanity (no manim by default)
npm install                 # installs Slidev + VitePress
```

To **render manim scenes locally**, install the manim extra and its native deps:

```bash
# Switch the dep in pyproject.toml to `presentation-sanity[manim]@…`, then:
uv sync

brew install ffmpeg cairo pango      # macOS — Linux: apt install libcairo2-dev libpango1.0-dev
# LaTeX is needed for MathTex (TeX Live, BasicTeX, etc.)
```

If you're just writing (and `public/manim/` already has rendered videos), skip
the manim install entirely — `build` auto-skips rendering with a log line.

## Daily workflow

```bash
uv run presentation-sanity outputs        # list what this subject declares
uv run presentation-sanity dev blog       # VitePress hot-reload  (localhost:5173)
uv run presentation-sanity dev slides     # Slidev hot-reload     (localhost:3030)
uv run presentation-sanity build          # every output → site/
uv run presentation-sanity build blog     # just one
uv run presentation-sanity preview blog   # serve site/blog at localhost:8000
uv run presentation-sanity build-manim    # re-render only stale scenes
uv run presentation-sanity export pdf
uv run presentation-sanity export-pptx    # PPTX with embedded, playable videos
```

`build` runs: parse manifest → export stale figures → render stale manim scenes
(both cached by content hash) → render each selected output. Shared artifacts
are produced **once** and consumed by every printout.

`preview` exists because **double-clicking `site/blog/index.html` won't work** —
browsers refuse to load ES modules from `file://` URLs. Any HTTP server is fine.

## Outputs

Each entry under `outputs:` is one printout of the subject. `engine` is inferred
for the well-known keys (`slides`/`deck` → slidev, `blog`/`post`/`article` →
vitepress); state it explicitly for anything else.

```yaml
outputs:
  blog:
    engine: vitepress
    entry: blog.md            # rewritten to `/` in the built site
    out: site/blog
    base: "/blog/"            # optional; VitePress needs an ABSOLUTE prefix
    nav: [{ text: "Home", link: "/" }]     # forwarded to themeConfig
    exclude: ["drafts/**"]                 # extra srcExclude globs
  slides:
    engine: slidev
    entry: slides.md
    out: site/slides
    theme: seriph
    base: "./"                # Slidev accepts a relative base
```

Delete an entry to stop building that format. A repo can be blog-only from day
one and grow a deck later by adding `outputs.slides`.

**One VitePress output per subject.** Extra markdown files next to `blog.md`
become extra *pages of the same site* — that's the model, rather than two sites.
Every other output's `entry` is added to `srcExclude` automatically, so
`slides.md` never becomes a blog page.

### `.vitepress/` is generated

`presentation-sanity` rewrites `.vitepress/config.mts` and
`.vitepress/theme/index.ts` from `manifest.yaml` before every `dev`/`build`, so
the directory is gitignored and never hand-edited. The generated theme:

- glob-registers every `components/*.vue` globally under its filename — the same
  convention Slidev uses, so `<DataValue>`, `<ManimFigure>` and `<FigureImage>`
  work in markdown with no imports;
- mounts `ProvenancePanel` once in the `layout-bottom` slot — the VitePress
  equivalent of Slidev's `global-bottom.vue` singleton;
- imports `blog.css` when present.

Run `presentation-sanity scaffold` to regenerate it without building (useful for
editor tooling). To customize beyond what `outputs.<key>:` exposes, edit
`blog.css`, or add components; to take full ownership, copy the generated
directory somewhere else and run VitePress yourself.

Both `markdown-it-mathjax3` (math) and `@modyfi/vite-plugin-yaml` (`<DataValue>`)
are detected at scaffold time — a subject without them still builds, with a note.

## Editing variables

Edit `manifest.yaml`. Both dev servers hot-reload on save.

```yaml
variables:
  num_samples:
    value: 12453
    format: ","                       # , .2e .3f .1%
    description: "Total samples after QC filtering"
    source: "data/results.csv"        # informational, surfaced in the panel
    command: "python scripts/fit.py"  # informational — not executed
    updated: "2026-04-29"
```

In either output, `<DataValue var="num_samples" />` renders `12,453`. **Click
the underlined value** and a side panel slides in from the right showing the
provenance as a vertical graph: `inputs → command → variable`. Press `Esc`,
click the backdrop, or click the `×` to dismiss.

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

Use `data:` (a list of file paths) for the multi-input case, or `source:` (a
single path) for the single-file fallback. If both are present, `data:` wins.

> **Writing tip.** Keep a component tag off the *start* of a line in markdown —
> markdown-it treats a line beginning with `<Tag` as an HTML *block* and closes
> the surrounding paragraph around it. Wrap so the tag lands mid-line.

## Math

The blog renders LaTeX to **static SVG at build time** (MathJax, full package
set) — no client-side math runtime, and it prints correctly. `$…$` and `$$…$$`
work as expected, and display environments can be written bare, with no `$$`
fence:

```markdown
\begin{align}
h^2 &= \frac{\sigma^2_A}{\sigma^2_P} \\
    &= \frac{\sigma^2_A}{\sigma^2_A + \sigma^2_E}
\end{align}
```

`align`, `equation`, `gather`, `multline`, `alignat`, `flalign`, `split`,
`aligned`, `eqnarray` and `CD` are recognised at block level, starred variants
included. Nested constructs (`cases`, `pmatrix`, …) still need `$$` fencing.
Anything not on the list stays literal, and an unterminated `\begin{…}` falls
back to a paragraph instead of swallowing the document.

Macros live in `manifest.yaml` so they mean the same thing everywhere:

```yaml
math:
  macros:
    Var: "\\operatorname{Var}"
    RR: "\\mathbb{R}"
    norm: ["\\left\\lVert #1 \\right\\rVert", 1]   # [expansion, arg count]
  tags: none            # none | ams | all
  environments: true    # or false, or an explicit list of env names
```

**Define macros here, not with an in-document `\newcommand`** — the renderer
keeps one TeX instance for the whole build, so an in-document definition leaks
into every later block and page, and whether it resolves depends on source
order.

`tags: ams` numbers display equations and enables `\label`/`\eqref`. The counter
is shared across the build and its starting point depends on page order, so it
is reliable for a single-page post; with several pages use an explicit `\tag{…}`
or reset with `\setcounter{equation}{0}`.

Dollar signs in prose are safe — `costs $5 and $10` stays literal, as does an
escaped `\$100`.

> The deck renders math with **KaTeX** (Slidev's built-in), not MathJax, so
> `math.macros` currently reaches the blog only.

## Citations

Cite the way you would in LaTeX. Name your `.bib` files in the manifest, use
`\cite{key}` in the document, and put `\bibliography` where the reference list
belongs.

```yaml
bibliography:
  sources: ["refs.bib"]     # a path, a list of paths, or a full mapping
  style: numeric            # numeric → [1]  |  author-year → (Smith et al., 2020)
  sort: appearance          # appearance | author | year
  title: "References"
```

| Command | numeric | author-year |
|---|---|---|
| `\cite{k}`, `\citep{k}` | `[1]` | `(Smith et al., 2020)` |
| `\citet{k}` | `Smith et al. [1]` | `Smith et al. (2020)` |
| `\cite{a,b}` | `[1, 2]` | `(Doe, 1996; Smith, 2020)` |
| `\cite[p. 12]{k}` | `[1, p. 12]` | `(Smith et al., 2020, p. 12)` |
| `\nocite{k}` | listed in the bibliography, no inline marker | |
| `\bibliography` | the reference list (`\printbibliography` also works) | |

Everything is parsed and formatted at build time, so the page ships plain
anchors and no citation runtime. Each citation links to its entry and shows the
full reference on hover. Switching `style` renumbers the in-text markers and
the list together — including `numeric` + `sort: author`, where `[1]` follows
alphabetical order rather than order of appearance.

Real-world BibTeX is handled: `@string` macros and `#` concatenation,
case-insensitive fields, brace-protected capitalisation (`{DNA}`), accents
(`M{\"u}ller` → Müller), `--`/`---`, `and others` → et al., and inline math in
titles. An unknown key renders a visible `[?key]` and logs a build warning
instead of vanishing. Citation commands inside code spans and math are left
alone.

> Editing a `.bib` needs a dev-server restart — the generated config is written
> when `dev` starts. Editing the document itself hot-reloads normally.
> Citations, like `math.macros`, currently reach the blog only.

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
3. **Use it.** In the blog, inline:
   ```markdown
   <ManimFigure scene="my_scene" caption="What this shows." />
   ```
   In the deck, full-screen:
   ```markdown
   ---
   layout: manim
   scene: my_scene
   ---
   ```
4. `uv run presentation-sanity build-manim` to render. Subsequent builds skip
   rendering until the source `.py` or the manifest entry changes.

Both consume `public/manim/<key>.webm` plus the last-frame poster that
`build-manim` extracts with ffmpeg — so the finished diagram shows wherever the
video can't play (initial paint, static PDF/PPTX export, print).

`<ManimFigure>` plays when scrolled into view and pauses when scrolled out, so a
long post with several scenes doesn't run them all at once. Frontmatter knobs:
`format`, `caption`, `autoplay`, `loop`, `controls`, `width`.

The Slidev `manim` layout (`layouts/manim.vue` — Slidev uses the filename
verbatim as the layout name, so keep it lowercase) handles autoplay,
click-to-replay on revisit, and aspect-ratio fit:

| Key | Default | Description |
|---|---|---|
| `scene` | required | Manifest scene key |
| `format` | `webm` | Video format / extension |
| `autoplay` | `true` | Replay automatically on every slide entry |
| `controls` | `false` | Show video controls |
| `background` | `black` | Slide background color |
| `replayKey` | `r` | Press this key (while the slide is active) to replay |
| `pauseKey` | `p` | Toggle pause/play — handy for stopping on a key frame |

## Theming the blog

There is no page file to edit — `.vitepress/` is generated from `manifest.yaml`
on every build. The levers, from lightest to heaviest:

**1. Manifest — structure and site options.** Everything under `outputs.blog:`
is forwarded into the generated config:

```yaml
outputs:
  blog:
    engine: vitepress
    entry: blog.md
    out: site/blog
    outline: [2, 3]                  # right-hand rail depth; false to remove
    nav: [{ text: "Home", link: "/" }]
    sidebar: false
    socialLinks: [{ icon: "github", link: "https://github.com/…" }]
    footer: { message: "…", copyright: "…" }
    head: [["link", { rel: "icon", href: "/favicon.svg" }]]
    themeConfig:                     # any OTHER default-theme option
      logo: "/logo.svg"
      aside: false                   # drop the outline rail entirely
      search: { provider: "local" }
      editLink: { pattern: "https://github.com/…/edit/main/:path" }
    vitepress:                       # any OTHER top-level VitePress option
      appearance: dark               # true | false | 'dark' | 'force-dark'
      lang: en-US
      titleTemplate: ":title · Notes"
```

`nav`, `sidebar`, `socialLinks`, `outline` and `footer` are lifted into
`themeConfig` for you; `themeConfig:` and `vitepress:` are the escape hatches
for anything this schema doesn't name.

**2. `blog.css` — appearance.** Imported *last* into the generated theme, so it
overrides both VitePress and the built-in citation styles. The default theme is
driven by CSS variables:

```css
:root {
  --vp-c-brand-1: #4a7c59;          /* links, accents */
  --vp-c-brand-2: #3d6749;
  --vp-c-bg: #fbfaf7;               /* page background */
  --vp-c-text-1: #1c1c1c;           /* body text */
  --vp-c-divider: #e4e1da;
  --vp-font-family-base: "Source Serif 4", Georgia, serif;
  --vp-font-family-mono: "JetBrains Mono", ui-monospace, monospace;
  --vp-layout-max-width: 1100px;    /* whole layout */
  --vp-sidebar-width: 240px;
  --vp-nav-height: 56px;
}
.dark {
  --vp-c-bg: #16161a;               /* dark-mode overrides go here */
}
/* Prose column width is a selector, not a variable: */
.VPDoc.has-aside .content-container { max-width: 760px; }
```

Full variable list: `node_modules/vitepress/dist/client/theme-default/styles/vars.css`.

**3. Frontmatter — per page.** `layout: doc` (default) / `page` (no doc
chrome) / `home` (hero + feature grid), plus `aside: false`, `sidebar: false`,
`navbar: false`, `outline: false`, `pageClass: my-essay` for page-scoped CSS.

**4. Components.** Anything in `components/` is registered globally under its
filename, so you can drop a `<Callout>` or a custom header straight into
`blog.md` — the same components the deck uses.

## Customizing styles

The two outputs have separate stylesheets on purpose:

- **`style.css`** — auto-loaded by Slidev. Written against `.slidev-layout` and
  hides Slidev's nav chrome; none of that means anything to the blog.
- **`blog.css`** — imported into the generated VitePress theme when present.
  Style `.vp-doc …` and override VitePress CSS variables here.

For per-slide CSS, use a scoped `<style>` block inside `slides.md`.

## Static deployment

```bash
uv run presentation-sanity build
aws s3 sync site/ s3://my-talks/on-traits/ --acl public-read
```

`site/index.html` is generated whenever a full build produces more than one
output under a common parent — a small landing page linking each printout.

The deck uses **hash routing** (`#/2`, `#/3`) and the blog uses
`cleanUrls: false` (so routes are real `.html` files), which means both work on
a dumb static host with no SPA-fallback or rewrite configuration.

### Subdirectory deploys

The two engines differ here, and it matters:

- **Slidev** accepts a relative base. `vite.config.ts` ships with `base: './'`,
  so `site/slides/` works unchanged at any URL prefix.
- **VitePress** does SSR and route matching, so it needs an **absolute**
  prefix — `base: '/blog/'`, not `'./'`. `presentation-sanity` coerces a
  relative value to `/` rather than emitting a site that 404s its own routes.

```bash
uv run presentation-sanity build slides --base ./
uv run presentation-sanity build blog   --base /on-traits/blog/
```

Or set `base:` per output in `manifest.yaml`. Both `<ManimFigure>` and the
`manim` layout read `import.meta.env.BASE_URL`, so asset URLs follow whichever
base is in force.
