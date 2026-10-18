<a href="https://presentation.sanitism.dev/example/slides/"><img src="https://sanitism.dev/shots/deck.jpg" alt="The example deck's title slide: Every number in this talk knows where it came from. This deck reports 12,453 participants. Click that number." width="100%"></a>

# presentation-sanity-template

**A starter project for every talk you give about one subject: Slidev decks and VitePress blog posts that share one manifest, so every number, figure and manim scene exists once.**

Built with [presentation-sanity](https://github.com/yakaboskic/presentation-sanity), part of [Sanitism](https://sanitism.dev): built for autists to communicate their work, sanely.

**Live:** this repo builds and publishes itself at [presentation.sanitism.dev](https://presentation.sanitism.dev/): [the example deck](https://presentation.sanitism.dev/example/slides/) and [its blog post](https://presentation.sanitism.dev/example/blog/).

## Why one repo per project

A new talk on the same subject usually reuses most of the last one: the logos, the figures, the numbers, the manim scenes, a custom component or two. Keeping every presentation of a project in one repo means each of those exists once. A new version is a folder, not a branch or a copied repo.

Slidev and VitePress sit on the same substrate (Vite, Vue 3, markdown-it, Shiki), so the shared components, manifest and rendered assets work unchanged in both. `<DataValue var="num_samples" />` in a `blog.md` reads the same YAML as the same tag in a `slides.md`, and a manim scene renders once and plays everywhere.

## Start a project

**Keep it in git.** Click **Use this template**, clone your copy, then:

```bash
python init.py          # project name, authors, first presentation (run once)
```

`init.py` is a shim: it fetches the presentation-sanity version pinned in `pyproject.toml` with `uvx` and runs `presentation-sanity init --in-place`. It asks for each answer or takes flags (`python init.py --yes --title "My talks" --first kickoff --author "Me" --email me@lab.org`), renames `presentations/example/` to your first presentation, installs the [agent skill](#agent-skill), and removes itself along with this repo's demo workflow.

**Just give me a folder.** No GitHub needed; it needs [uv](https://docs.astral.sh/uv/):

```bash
uvx --from "presentation-sanity @ git+https://github.com/yakaboskic/presentation-sanity.git@v0.4.2" \
  presentation-sanity init my-talks --title "My talks" --first kickoff
```

Each release of presentation-sanity carries a snapshot of this template and pins the new project to itself. `--git` adds `git init` and a first commit, `--from gh:your-lab/your-template` starts from your lab's fork (`GH_TOKEN` for a private one), and existing files are never overwritten without `--force`.

## One-time setup

```bash
uv sync                 # presentation-sanity, with manim; commit the uv.lock it writes
npm install             # Slidev + VitePress, and links shared/
```

Rendering manim scenes needs native tools on the machine:

```bash
brew install ffmpeg cairo pango      # macOS; Linux: apt install ffmpeg libcairo2-dev libpango1.0-dev
# and LaTeX for MathTex (TeX Live, BasicTeX, …)
```

Rendered videos are **committed** next to their scenes. The first `build` renders every scene into `public/manim/`, and later builds re-render only the scenes that changed: commit the new `.webm` and `.poster.png` with the `.py`. Deploys ship what's committed instead of re-rendering. On a machine without those tools (a deploy runner, a co-author who only edits text), install without the `manim` group, `uv sync --no-default-groups`, and `build` uses the committed videos.

## What's inside

```
your-project/
├── init.py                 # one-time bootstrap (a shim over `presentation-sanity init`)
├── pyproject.toml          # presentation-sanity pinned to a release; manim in a default group
├── package.json            # Slidev + VitePress; links shared/ as a Slidev addon
├── manifest.yaml           # SHARED: variables, scenes, figures, bibliography, math,
│                           #   and defaults for every presentation's outputs
├── refs.bib                # the bibliography for \cite{}
├── scenes/one_source.py    # manim sources
├── public/                 # static assets served at / by every deck and blog
│   ├── manim/              #   rendered videos and last-frame posters
│   └── figures/            #   exported Excalidraw SVGs, logos, images
│
├── shared/                 # the shared Vue layer, a local Slidev addon
│   ├── package.json        #   (required: makes it an addon)
│   ├── vite.config.ts      #   publicDir, the YAML plugin, @project/@shared aliases
│   ├── components/         #   DataValue, ProvenancePanel, ManimFigure, FigureImage
│   ├── composables/
│   ├── layouts/manim.vue   #   a full-screen manim slide
│   ├── global-bottom.vue   #   mounts the provenance panel in every deck
│   ├── style.css           #   deck styles (every deck)
│   └── blog.css            #   blog styles (every blog)
│
├── presentations/
│   └── example/            # one presentation (init renames it)
│       ├── slides.md       #   the deck (Slidev)
│       ├── blog.md         #   the post (VitePress)
│       └── manifest.yaml   #   optional: date, venue, title, output overrides
│
├── .claude/skills/         # the presentation-sanity agent skill (added by init)
├── .agents/skills/         #   the same skill, for agents other than Claude Code
├── .github/workflows/pages.yml  # publishes THIS repo's demo; init.py removes it
│
├── .cache/                 # manim and figure caches, generated VitePress configs (gitignored)
└── site/                   # build output (gitignored)
    ├── index.html          #   a landing page listing every presentation
    └── example/{slides,blog}/
```

## Daily work

```bash
uv run presentation-sanity list                    # presentations, and what's built
uv run presentation-sanity check                   # every variable, scene, figure and \cite resolves
uv run presentation-sanity dev example:slides      # Slidev with hot reload    (localhost:3030)
uv run presentation-sanity dev example:blog        # VitePress with hot reload (localhost:5173)
uv run presentation-sanity build                   # everything → site/
uv run presentation-sanity build example           # one presentation
uv run presentation-sanity preview                 # serve site/ at localhost:8000
uv run presentation-sanity build-manim             # re-render only stale scenes
uv run presentation-sanity export pdf example      # → presentations/example/exports/
uv run presentation-sanity export-pptx example     # PPTX with embedded, playable videos
```

Commands take a **target**: a presentation id (its path under `presentations/`), optionally with an output, as in `example:blog`. Run a command from inside a presentation's folder and that presentation is the default. A grouping folder selects everything in it, so `build kickoff` builds every version of `kickoff`.

`build` parses the manifest, exports stale figures, renders stale manim scenes (both cached by content hash), builds each selected output and refreshes `site/index.html`. Shared artifacts are produced **once** and used by every presentation. `preview` exists because double-clicking `site/index.html` won't work: browsers refuse to load ES modules from `file://`.

## Presentations and versions

Any folder under `presentations/` that has a `slides.md` and/or a `blog.md` is a presentation, and its path is its id. Folders without one just group presentations, which is how versions stay together:

```
presentations/
├── kickoff/
│   ├── v1/slides.md            # id: kickoff/v1
│   └── nih-review/slides.md    # id: kickoff/nih-review
└── lab-meeting/slides.md       # id: lab-meeting
```

Start a presentation from scratch, or fork an existing one into a new version:

```bash
uv run presentation-sanity new lab-meeting --title "Where the numbers come from"
uv run presentation-sanity new kickoff/nih-review --from kickoff/v1 --title "Kickoff (NIH)"
```

`--from` copies the folder (skipping exports and Slidev's scratch state), sets the new title in the deck's headmatter, and records `from: kickoff/v1` in the copy's `manifest.yaml`; the landing page shows that lineage. Everything inside a presentation's folder belongs to it, and presentations don't nest.

**A presentation's own `manifest.yaml`** is optional and deliberately small: it describes the presentation and tunes its outputs. Shared inputs (variables, scenes, figures, bibliography, math) can only be declared in the project manifest, so they never fork.

```yaml
metadata:
  title: "Kickoff (NIH)"      # default: the deck's headmatter `title`
  date: "2026-11-04"
  venue: "NIH program review"
outputs:
  blog: false                 # skip this presentation's blog.md
```

**Numbers that change between versions.** Variables are project-wide on purpose: a number has one definition and one provenance trail. When a fact changes, add a new key rather than editing the old one (`num_samples_2026q1` next to `num_samples`) and point the new version at it. Older versions keep showing the number they presented.

## Numbers with provenance

```yaml
variables:
  num_samples:
    value: 12453
    format: ","                       # , .2e .3f .1%
    description: "Participants after QC filtering"
    source: "data/results.csv"        # or data: [a, b] for several inputs
    command: "python scripts/qc.py data/raw/ --out data/results.csv"
    updated: "2026-09-30"
```

In any deck or post, `<DataValue var="num_samples" />` renders `12,453`. **Click it** and a side panel slides in from the right with the provenance as a graph: inputs, then the command, then the value. `Esc`, the backdrop or the `×` closes it. Provenance is informational: nothing is executed when the page builds.

> [!TIP]
> Keep a component tag off the *start* of a line. markdown-it reads a line beginning with `<Tag` as an HTML block and closes the paragraph around it; `presentation-sanity check` warns when it finds one.

## Adding a manim scene

1. **Write it.** Add a class to `scenes/<name>.py` (subclass `manim.Scene`).
2. **Register it** under `scenes:` in `manifest.yaml`:
   ```yaml
   scenes:
     my_scene:
       source: "scenes/my_scene.py"
       class: "MyScene"
       quality: "h"          # l | m | h | p | k  (low → 4k)
       format: "webm"
   ```
3. **Use it** from any presentation. In a deck, full-screen:
   ```markdown
   ---
   layout: manim
   scene: my_scene
   ---
   ```
   In a post, inline: `<ManimFigure scene="my_scene" caption="What this shows." />`
4. **Render it:** `uv run presentation-sanity build-manim`. Later builds skip it until the `.py` or its manifest entry changes.

Both read `public/manim/<key>.webm` plus the last-frame poster `build-manim` extracts, so the finished frame shows wherever video can't play (first paint, PDF and PPTX export, print). `<ManimFigure>` plays when scrolled into view and pauses when scrolled out; its props are `format`, `caption`, `autoplay`, `loop`, `controls` and `width`.

<details>
<summary><b>The <code>manim</code> slide layout's options</b></summary>

The layout lives in `shared/layouts/manim.vue` (Slidev uses the filename as the layout name, so keep it lowercase). It handles autoplay, click-to-replay on revisit and aspect-ratio fit.

| Key | Default | Description |
|---|---|---|
| `scene` | required | The manifest scene key |
| `format` | `webm` | Video format and extension |
| `autoplay` | `true` | Replay on every slide entry |
| `controls` | `false` | Show video controls |
| `background` | `black` | The slide's background color |
| `replayKey` | `r` | Press while the slide is active to replay |
| `pauseKey` | `p` | Toggle pause, for stopping on a key frame |

</details>

## Math and citations

The blog renders LaTeX to **static SVG at build time** (MathJax, full package set): no client-side runtime, and it prints correctly. `$…$` and `$$…$$` work, and display environments (`align`, `equation`, `gather`, `multline`, `alignat`, `flalign`, `split`, `aligned`, `eqnarray`, `CD`, starred too) can be written bare:

```markdown
\begin{align}
h^2 &= \frac{\sigma^2_A}{\sigma^2_P} \\
    &= \frac{\sigma^2_A}{\sigma^2_A + \sigma^2_E}
\end{align}
```

Define macros in `manifest.yaml`, not with an in-document `\newcommand` (one TeX instance serves the whole build, so an in-document definition leaks into every later page):

```yaml
math:
  macros:
    Var: "\\operatorname{Var}"
    norm: ["\\left\\lVert #1 \\right\\rVert", 1]   # [expansion, arg count]
  tags: none            # none | ams | all
```

Cite the way you would in LaTeX: name your `.bib` files in the manifest, write `\cite{key}`, and put `\bibliography` where the list belongs.

```yaml
bibliography:
  sources: ["refs.bib"]
  style: numeric            # numeric → [1] | author-year → (Smith et al., 2020)
  sort: appearance          # appearance | author | year
```

| Command | numeric | author-year |
|---|---|---|
| `\cite{k}`, `\citep{k}` | `[1]` | `(Smith et al., 2020)` |
| `\citet{k}` | `Smith et al. [1]` | `Smith et al. (2020)` |
| `\cite{a,b}` | `[1, 2]` | `(Doe, 1996; Smith, 2020)` |
| `\cite[p. 12]{k}` | `[1, p. 12]` | `(Smith et al., 2020, p. 12)` |
| `\nocite{k}` | listed, no inline marker | |
| `\bibliography` | the reference list (`\printbibliography` works too) | |

Each post lists only the entries it cites, so one shared `.bib` serves the whole project. An unknown key shows a visible `[?key]` and logs a warning. Decks render math with KaTeX, so `math.macros` and citations currently reach the blogs only, and editing a `.bib` needs a `dev` restart.

## Sharing and overriding

`shared/` is a local **Slidev addon**: the root `package.json` lists it as a `file:` dependency and enables it for every deck. That matters because Slidev takes components, layouts and styles from the deck's own folder; without the addon, a deck in `presentations/<id>/` wouldn't see anything at the project root. VitePress gets the same components through the config presentation-sanity generates.

A presentation overrides any of it by adding the same file to its own folder:

| Put this in `presentations/<id>/` | Effect |
|---|---|
| `components/X.vue` | replaces `shared/components/X.vue` for this presentation (deck and blog) |
| `layouts/X.vue` | replaces the shared layout of that name |
| `style.css` | loads after `shared/style.css` |
| `blog.css` | loads after `shared/blog.css` |

Import project files through the aliases, so a component works from any folder:

```ts
import manifest from '@project/manifest.yaml'
import { showProvenance } from '@shared/composables/useProvenance'
```

Every deck and blog serves the project's `public/`, so `/figures/logo.svg` means the same file everywhere. Adding or removing a file like `shared/global-bottom.vue` while `dev` runs needs a restart (`r` in the Slidev terminal).

<details>
<summary><b>Theming the blogs</b></summary>

There is no config file to edit: each blog's VitePress config is generated from `manifest.yaml` on every build (in `.cache/vitepress/<id>/`, gitignored). The levers, lightest first:

**1. The manifest.** Everything under `outputs.blog:` (in the project manifest for every blog, or a presentation's for one) goes into the generated config:

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
      search: { provider: "local" }
    vitepress:                       # any OTHER top-level VitePress option
      appearance: dark
      lang: en-US
```

**2. `blog.css`.** `shared/blog.css` applies to every blog and a presentation's own loads after it, both imported last, so they override VitePress and the built-in citation styles. The default theme is driven by CSS variables (`--vp-c-brand-1`, `--vp-c-bg`, `--vp-font-family-base`, `--vp-layout-max-width`, …); the full list is in `node_modules/vitepress/dist/client/theme-default/styles/vars.css`.

**3. Frontmatter, per page.** `layout: doc` / `page` / `home`, plus `aside`, `sidebar`, `navbar`, `outline` and `pageClass`.

**4. Components.** Anything in `shared/components/` (or a presentation's `components/`) is registered globally under its filename, so a custom `<Callout>` drops straight into a `blog.md`.

Decks and blogs have separate stylesheets on purpose: `shared/style.css` is written against `.slidev-layout` and hides Slidev's chrome, which means nothing to a blog. For per-slide CSS, use a scoped `<style>` block in a `slides.md`.

</details>

## Agent skill

`init` installs a skill for coding agents into `.claude/skills/presentation-sanity/` (Claude Code: `/presentation-sanity [mode]`) and `.agents/skills/presentation-sanity/` (Codex, Cursor, Pi and others). It knows the project layout and the rules, with modes for `new`, `slides`, `blog`, `manim`, `figures`, `variables`, `cite`, `export`, `check` and `deploy`. It explains; the CLI does the work. `uv run presentation-sanity skills --force` reinstalls it from the installed tool.

## Publish

> [!WARNING]
> A GitHub Pages site is **public**, even when the repository is private.

```bash
uv run presentation-sanity pages init     # writes .github/workflows/pages.yml
```

Turn Pages on (Settings → Pages → Source: **GitHub Actions**) and push to `main`. The workflow installs without manim (`uv sync --no-default-groups`), runs `npm ci`, builds with the site's URL prefix as `--base`, and deploys `site/`. It never renders scenes or exports figures; it ships what's committed in `public/`, which is why rendered videos are committed. `pages init` warns when a declared scene or figure is missing or gitignored. This repo deploys its own demo the same way.

**Any static host works.** `site/` is self-contained: decks use hash routing (`#/2`) and blogs build real `.html` routes, so S3, R2 or Netlify need no rewrite rules.

```bash
uv run presentation-sanity build --base /my-talks/
aws s3 sync site/ s3://my-bucket/my-talks/ --acl public-read
```

Decks always build with a relative base, so they work under any prefix. Blogs need an absolute one, so each gets the prefix plus its own path (`/my-talks/kickoff/v1/blog/`). `<ManimFigure>` and the `manim` layout read `import.meta.env.BASE_URL`, so asset URLs follow.

## Upgrade presentation-sanity

The tool is pinned to a release tag in `pyproject.toml`, and `uv.lock` records the commit behind it:

```toml
dependencies = [
    "presentation-sanity @ git+https://github.com/yakaboskic/presentation-sanity.git@v0.4.2",
]
```

(The `manim` group's `"presentation-sanity[manim]"` has no URL of its own: uv takes it from this line, so there's one tag to change.) To upgrade, read the [release notes](https://github.com/yakaboskic/presentation-sanity/releases), change the tag on that line, then:

```bash
uv lock && uv sync                                  # resolve and install the new tag
uv run presentation-sanity skills --force           # the skill that matches the new tool
```

Edit the line rather than using `uv add` (which moves a git source into `[tool.uv.sources]`, a uv-only form), and avoid `@main`, which moves with every commit. Projects from an older template have `presentation-sanity[manim] @ …` on the dependency line itself; `presentation-sanity pages init` prints the edit that moves it into the group.

<details>
<summary><b>Moving a single-deck repo into a project</b></summary>

Repos made from older versions of this template (one `slides.md` at the root) still build as before. To turn one into a project:

1. Move `components/`, `composables/`, `layouts/`, `global-bottom.vue`, `style.css`, `blog.css` and `vite.config.ts` into `shared/`, and copy `shared/package.json` and `shared/vite.config.ts` from this template.
2. Add the `psanity-shared` `file:` dependency and the `"slidev": {"addons"}` entry from this template's `package.json`, then `npm install`.
3. In shared components, import `@project/manifest.yaml` and `@shared/composables/…` instead of relative paths.
4. `mkdir -p presentations/<name> && git mv slides.md presentations/<name>/` (and `blog.md`). Versions that lived on branches can come over with `git show <branch>:slides.md > presentations/<name-v2>/slides.md`.
5. Drop any `out:` from the root manifest's `outputs:`, and run `presentation-sanity build`.

</details>

## House rules

```yaml
# sanitism.yaml
principles:
  one_manifest: everything else is generated, never hand-edited
  every_number_has_a_source: the file, command and date travel with the value
  versions_are_folders: not branches, and not final_v3_REAL.docx
  one_repo_per_obsession: papers, proposals and talks share figures and numbers
  same_input_same_output: a rebuild never surprises your co-authors
```

## More

- [presentation-sanity](https://github.com/yakaboskic/presentation-sanity): the tool, every command, outputs and the generated config in detail.
- [document-sanity-template](https://github.com/yakaboskic/document-sanity-template): the same idea for papers and proposals.

---

<sub>Part of <a href="https://sanitism.dev">Sanitism</a>. MIT licensed.</sub>
