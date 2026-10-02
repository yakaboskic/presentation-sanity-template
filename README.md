# presentation-sanity-template

A working **project** driven by `manifest.yaml`: one set of variables, manim
scenes, figures and logos shared by every **presentation** you give about it.
Each presentation is a folder under `presentations/` with a **Slidev deck**
(`slides.md`), a **VitePress blog post** (`blog.md`), or both — and versions of
a talk are just folders next to each other. Use this repo as a starting point:
clone it (or "Use this template"), run `python init.py` to name the project and
its first presentation, then write.

Declares [`presentation-sanity`](https://github.com/yakaboskic/presentation-sanity)
as a git dependency **pinned to a release** (`@v0.3.0`), so every project made
from this template builds with the same tool until you choose to upgrade (see
[Upgrading presentation-sanity](#upgrading-presentation-sanity)). It includes
the **`[manim]` extra**, so `uv sync` installs manim and `build` renders your
scenes — the machine needs ffmpeg, cairo, pango and LaTeX (see
[One-time setup](#one-time-setup)).

## Why one repo per project

A new talk on the same subject usually reuses most of the last one: the logos,
the figures, the numbers, the manim scenes, a custom component or two. Keeping
every presentation of a project in one repo means each of those exists once.
A new version is a folder, not a branch or a copied repo — you can still branch
while you work on it and merge it back like any other change.

Slidev and VitePress sit on the *same* substrate — Vite + Vue 3 + markdown-it +
Shiki — so the shared components, manifest and rendered assets are consumed
unchanged by both. `<DataValue var="n" />` in a `blog.md` reads the same YAML
as the same tag in a `slides.md`; a manim scene renders once and is embedded
everywhere.

## Structure

```
your-project/
├── init.py                 # one-time bootstrap: project name, authors, first presentation
├── pyproject.toml          # declares presentation-sanity[manim], pinned to a release
├── package.json            # Slidev + VitePress; links shared/ as a Slidev addon
├── manifest.yaml           # SHARED: variables, scenes, figures, bibliography, math,
│                           #   and defaults for every presentation's outputs
├── refs.bib                # bibliography source for \cite{}
├── scenes/intro.py         # manim sources
├── public/                 # static assets served at / by every deck and blog
│   ├── manim/              #   rendered videos + last-frame posters
│   └── figures/            #   exported Excalidraw SVGs, logos, images
│
├── shared/                 # the shared Vue layer — a local Slidev addon
│   ├── package.json        #   (required: makes it an addon)
│   ├── vite.config.ts      #   publicDir, yaml plugin, @project/@shared aliases
│   ├── components/         #   DataValue, ProvenancePanel, ManimFigure, FigureImage
│   ├── composables/
│   ├── layouts/manim.vue   #   full-screen manim slide
│   ├── global-bottom.vue   #   mounts the provenance panel in every deck
│   ├── style.css           #   deck styles (every deck)
│   └── blog.css            #   blog styles (every blog)
│
├── presentations/
│   └── example/            # one presentation (rename it with init.py)
│       ├── slides.md       #   the deck   (Slidev)
│       ├── blog.md         #   the post   (VitePress)
│       └── manifest.yaml   #   optional: date, venue, title, output overrides
│
├── .cache/                 # manim/figure caches + generated VitePress configs (gitignored)
└── site/                   # build output (gitignored)
    ├── index.html          #   landing page listing every presentation
    └── example/{slides,blog}/
```

## One-time setup

```bash
python init.py              # project name, authors, first presentation (run once)
uv sync                     # installs presentation-sanity, with manim
npm install                 # installs Slidev + VitePress and links shared/
```

Rendering manim scenes needs these native tools on the machine:

```bash
brew install ffmpeg cairo pango      # macOS — Linux: apt install ffmpeg libcairo2-dev libpango1.0-dev
# LaTeX is needed for MathTex (TeX Live, BasicTeX, etc.)
```

Rendered videos are build output: `public/manim/` is gitignored, the first
`build` renders every scene, and later builds re-render only the scenes that
changed.

On a machine without those tools (a deploy runner, a co-author who only edits
text), drop `[manim]` from the dependency line or pass `--skip-manim`: `build`
then skips rendering and uses whatever is already in `public/manim/`. If you
deploy that way, commit the rendered videos — remove the `public/manim/` lines
from `.gitignore`.

## Upgrading presentation-sanity

The tool is pinned to a release tag in `pyproject.toml`, and `uv.lock` records
the exact commit behind it:

```toml
dependencies = [
    "presentation-sanity[manim] @ git+https://github.com/yakaboskic/presentation-sanity.git@v0.3.0",
]
```

To move to a newer release, read its notes on the
[releases page](https://github.com/yakaboskic/presentation-sanity/releases),
change the tag on that line (`@v0.3.0` → `@v0.4.0`), and re-lock:

```bash
uv lock      # resolves the new tag and records its commit in uv.lock
uv sync      # installs it
```

Edit the line rather than using `uv add`: `uv add` moves a git source into
`[tool.uv.sources]`, which works with uv but not with pip.

Avoid `@main`: it moves with every commit, so two clones of the same project
can end up building with different tools.

## Daily workflow

```bash
uv run presentation-sanity list                    # presentations + what's built
uv run presentation-sanity dev example             # Slidev hot-reload  (localhost:3030)
uv run presentation-sanity dev example:blog        # VitePress hot-reload (localhost:5173)
uv run presentation-sanity build                   # everything → site/
uv run presentation-sanity build example           # just one presentation
uv run presentation-sanity preview                 # serve site/ at localhost:8000
uv run presentation-sanity build-manim             # re-render only stale scenes
uv run presentation-sanity export pdf example      # → presentations/example/exports/
uv run presentation-sanity export-pptx example     # PPTX with embedded, playable videos
```

Commands take a **target**: a presentation id (its path under `presentations/`),
optionally with an output — `example:blog`. Run a command from inside a
presentation's folder and that presentation is the default. A grouping folder
selects everything in it, so `build kickoff` builds every version of `kickoff`.

`build` runs: parse manifest → export stale figures → render stale manim scenes
(both cached by content hash) → build each selected output → refresh
`site/index.html`. Shared artifacts are produced **once** and consumed by every
presentation.

`preview` exists because **double-clicking `site/index.html` won't work** —
browsers refuse to load ES modules from `file://` URLs. Any HTTP server is fine.

## Presentations & versions

Any folder under `presentations/` that has a `slides.md` and/or a `blog.md` is a
presentation; its path is its id. Folders without one just group presentations,
which is how versions stay together:

```
presentations/
├── kickoff/
│   ├── v1/slides.md            # id: kickoff/v1
│   └── nih-review/slides.md    # id: kickoff/nih-review
└── ashg-2026/slides.md         # id: ashg-2026
```

Start a presentation from scratch, or fork an existing one into a new version:

```bash
uv run presentation-sanity new ashg-2026 --title "Genetics as an anchor"
uv run presentation-sanity new kickoff/nih-review --from kickoff/v1 --title "Kickoff (NIH)"
```

`--from` copies the folder (skipping exports and Slidev's scratch state), sets
the new title in the deck's headmatter, and records `from: kickoff/v1` in the
copy's `manifest.yaml` — the landing page shows that lineage. Everything inside
a presentation's folder belongs to it; presentations don't nest inside other
presentations.

Each presentation builds to `site/<id>/<output>/`, and `site/index.html` lists
them grouped by folder with their title, date, venue and lineage.

### A presentation's own `manifest.yaml`

Optional, and deliberately small — it describes the presentation and tunes its
outputs. Shared inputs (variables, scenes, figures, bibliography, math) can only
be declared in the project manifest, so they never fork.

```yaml
metadata:
  title: "Kickoff (NIH)"      # default: the deck's headmatter `title`
  date: "2026-11-04"
  venue: "NIH program review"
  authors:                    # default: the project's authors
    - name: "Your Name"
      email: "you@institute.org"
outputs:
  blog: false                 # skip this presentation's blog.md
  slides:
    base: "./"                # merged over the project's `outputs.slides`
```

### Numbers that change between versions

Variables are project-wide on purpose: a number has one definition and one
provenance trail. When a fact changes, add a new key rather than editing the
old one — `n_samples_2026q3` next to `n_samples` — and point the new version at
it. Older versions keep showing the number they presented.

## Sharing and overriding

`shared/` is a local **Slidev addon** — the root `package.json` lists it as a
`file:` dependency and enables it for every deck under `"slidev": {"addons"}`.
That matters because Slidev takes its components, layouts and styles from the
deck's own folder; without the addon, a deck in `presentations/<id>/` wouldn't
see anything at the project root. VitePress gets the same components through
the config presentation-sanity generates.

A presentation can override any of it by adding the same file to its folder:

| Put this in `presentations/<id>/` | Effect |
|---|---|
| `components/X.vue` | replaces `shared/components/X.vue` for this presentation (deck and blog) |
| `layouts/X.vue` | replaces the shared layout of that name |
| `style.css` | loads after `shared/style.css` — add or override deck styles |
| `blog.css` | loads after `shared/blog.css` |

Import project files through the aliases rather than relative paths, so a
component works no matter which folder it sits in — copy a shared component
into a presentation and it keeps working unchanged:

```ts
import manifest from '@project/manifest.yaml'
import { showProvenance } from '@shared/composables/useProvenance'
```

Static assets are shared too: every deck and blog serves the project's
`public/`, so `/figures/logo.svg` means the same file everywhere.

> Adding or removing a file like `shared/global-bottom.vue` while `dev` is
> running needs a restart — press `r` in the Slidev terminal.

## Outputs

`outputs:` in the project manifest holds **defaults** for every presentation. A
presentation gets `slides` when it has a `slides.md` and `blog` when it has a
`blog.md`; settings here apply to all of them.

```yaml
outputs:
  blog:
    nav: [{ text: "Home", link: "/" }]     # forwarded to themeConfig
    exclude: ["drafts/**"]                 # extra srcExclude globs, relative to a presentation
  slides: {}                               # a deck's look lives in its headmatter
```

`out:` can't be set here — every presentation builds to its own
`site/<id>/<output>/` (a presentation's manifest may move just its own).

**One VitePress site per presentation.** Extra markdown files next to `blog.md`
become extra *pages of the same site*; the deck's `slides.md` never becomes a
page.

### The generated VitePress config

`presentation-sanity` writes each blog's config to
`.cache/vitepress/<id>/.vitepress/` from `manifest.yaml` before every
`dev`/`build`, so it is gitignored and never hand-edited. The generated theme:

- glob-registers every `shared/components/*.vue`, then the presentation's own
  `components/*.vue`, globally under its filename — the same convention Slidev
  uses, so `<DataValue>`, `<ManimFigure>` and `<FigureImage>` work in markdown
  with no imports;
- mounts `ProvenancePanel` once in the `layout-bottom` slot — the VitePress
  equivalent of Slidev's `global-bottom.vue` singleton;
- imports `shared/blog.css`, then the presentation's `blog.css`, when present.

Run `presentation-sanity scaffold <id>` to regenerate it without building
(useful for editor tooling).

Both `markdown-it-mathjax3` (math) and `@modyfi/vite-plugin-yaml` (`<DataValue>`)
are detected at scaffold time — a project without them still builds, with a note.

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

In any deck or post, `<DataValue var="num_samples" />` renders `12,453`.
**Click the underlined value** and a side panel slides in from the right showing
the provenance as a vertical graph: `inputs → command → variable`. Press `Esc`,
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

> The decks render math with **KaTeX** (Slidev's built-in), not MathJax, so
> `math.macros` currently reaches the blogs only.

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
alphabetical order rather than order of appearance. Each post lists only the
entries it cites, so one shared `.bib` serves the whole project.

Real-world BibTeX is handled: `@string` macros and `#` concatenation,
case-insensitive fields, brace-protected capitalisation (`{DNA}`), accents
(`M{\"u}ller` → Müller), `--`/`---`, `and others` → et al., and inline math in
titles. An unknown key renders a visible `[?key]` and logs a build warning
instead of vanishing. Citation commands inside code spans and math are left
alone.

> Editing a `.bib` needs a dev-server restart — the generated config is written
> when `dev` starts. Editing the document itself hot-reloads normally.
> Citations, like `math.macros`, currently reach the blogs only.

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
3. **Use it** — from any presentation. In a blog, inline:
   ```markdown
   <ManimFigure scene="my_scene" caption="What this shows." />
   ```
   In a deck, full-screen:
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
long post with several scenes doesn't run them all at once. Props:
`format`, `caption`, `autoplay`, `loop`, `controls`, `width`.

The Slidev `manim` layout (`shared/layouts/manim.vue` — Slidev uses the filename
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

## Theming the blogs

There is no config file to edit — each blog's VitePress config is generated from
`manifest.yaml` on every build. The levers, from lightest to heaviest:

**1. Manifest — structure and site options.** Everything under `outputs.blog:`
(in the project manifest for every blog, or a presentation's manifest for one)
is forwarded into the generated config:

```yaml
outputs:
  blog:
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

**2. `blog.css` — appearance.** `shared/blog.css` applies to every blog and a
presentation's own `blog.css` loads after it. Both are imported *last* into the
generated theme, so they override VitePress and the built-in citation styles.
The default theme is driven by CSS variables:

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

**4. Components.** Anything in `shared/components/` (or a presentation's own
`components/`) is registered globally under its filename, so you can drop a
`<Callout>` or a custom header straight into a `blog.md` — the same components
the decks use.

## Customizing styles

Decks and blogs have separate stylesheets on purpose:

- **`shared/style.css`** — loaded into every deck. Written against
  `.slidev-layout` and hides Slidev's nav chrome; none of that means anything to
  a blog. A presentation's own `style.css` loads after it.
- **`shared/blog.css`** — imported into every generated VitePress theme. Style
  `.vp-doc …` and override VitePress CSS variables here.

For per-slide CSS, use a scoped `<style>` block inside a `slides.md`.

## Static deployment

```bash
uv run presentation-sanity build
aws s3 sync site/ s3://my-talks/pigean/ --acl public-read
```

`site/index.html` lists every built presentation — grouped by folder, with
links to each output — and is refreshed on every build.

Decks use **hash routing** (`#/2`, `#/3`) and blogs use `cleanUrls: false` (so
routes are real `.html` files), which means everything works on a dumb static
host with no SPA-fallback or rewrite configuration.

### Subdirectory deploys

Pass the URL prefix the whole `site/` will be served from:

```bash
uv run presentation-sanity build --base /pigean/
```

Decks always build with a relative base (`./`), so they work under any prefix.
Blogs need an **absolute** base, so each one gets the prefix plus its own path
(`/pigean/kickoff/v1/blog/`). Both `<ManimFigure>` and the `manim` layout read
`import.meta.env.BASE_URL`, so asset URLs follow whichever base is in force.

## Moving a single-deck repo into a project

Repos created from older versions of this template (one `slides.md` at the
root) still build as before. To turn one into a project:

1. Move `components/`, `composables/`, `layouts/`, `global-bottom.vue`,
   `style.css`, `blog.css` and `vite.config.ts` into `shared/`, and copy
   `shared/package.json` and `shared/vite.config.ts` from this template.
2. Add the `psanity-shared` `file:` dependency and the `"slidev": {"addons"}`
   entry from this template's `package.json`, then `npm install`.
3. In shared components, import `@project/manifest.yaml` and
   `@shared/composables/…` instead of relative paths.
4. `mkdir -p presentations/<name> && git mv slides.md presentations/<name>/`
   (and `blog.md`). Versions that lived on branches can come over with
   `git show <branch>:slides.md > presentations/<name-v2>/slides.md`.
5. Drop any `out:` from the root manifest's `outputs:`, and run
   `presentation-sanity build`.
