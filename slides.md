---
# Deck-level config (frontmatter on the first slide configures the whole deck).
# Full reference: https://sli.dev/custom/
theme: seriph
title: Presentation Sanity Demo
author: Your Name
info: |
  ## Demo deck for presentation-sanity
  - Markdown + Vue source of truth (Slidev)
  - Variable provenance via `<DataValue>` component
  - Manim scenes pre-rendered to webm
class: text-center
transition: slide-left
mdc: true
# Hash routing — works on any dumb static host (no SPA fallback needed).
# Switch to "history" if you have a host that can serve index.html on 404.
routerMode: hash
---

# presentation-sanity

A single source of truth for presentations.

<div class="abs-br m-6 text-xl opacity-60">
  Press <kbd>space</kbd> →
</div>

---
layout: default
---

# What this proves out

<v-clicks>

- **Slidev** as the renderer — markdown + Vue, static HTML output
- **Variables with provenance** — `<DataValue>` reads `manifest.yaml` directly
- **Manim** scenes pre-rendered to webm, embedded via `<SlidevVideo>`
- **PPTX export** via `slidev export --format pptx` (slides as full-bleed images)
- Everything servable from a static bucket — no webserver

</v-clicks>

---
layout: two-cols
---

# Data-driven content

Hover any underlined value to see provenance.

We analyzed <DataValue var="num_samples" /> samples and observed
$p = $<DataValue var="p_value" /> with mean effect size
<DataValue var="effect_size" />.

Edit `manifest.yaml` and Slidev hot-reloads. The `<DataValue>` component
imports `manifest.yaml` directly via `@modyfi/vite-plugin-yaml`.

::right::

```yaml
# manifest.yaml
variables:
  num_samples:
    value: 12453
    format: ","
    description: "Total samples after QC"
    source: "data/results.csv"
    updated: "2026-04-29"
```

The provenance fields (`source`, `command`, `updated`) are informational —
they show in the tooltip and document where the value came from, but
nothing is executed at build time.

---
layout: manim
scene: intro
---

scenes/intro.py → public/manim/intro.webm

---
layout: center
class: text-center
---

# Math is first-class

$$
\hat{\beta} = (X^\top X)^{-1} X^\top y
$$

<v-clicks>

KaTeX renders client-side. Mermaid, PlantUML, and Monaco-editable
code blocks are all built into Slidev — no extra setup.

</v-clicks>

---
layout: end
---

# That's it

Next: wire up the Python `presentation-sanity` package
to orchestrate manifest → data/variables.json → manim → slidev build.
