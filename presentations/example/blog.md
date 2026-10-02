---
title: A single source of truth for slides and writing
outline: [2, 3]
---

# A single source of truth

This page and `slides.md` are two printouts of the same presentation, and
every presentation in the project shares one `manifest.yaml`, one `shared/`
set of components, one set of manim scenes, and one `public/` folder of
rendered artifacts. Nothing is duplicated; only the renderer differs.

## Data with provenance

The same `<DataValue>` component backs both formats. We analyzed <DataValue
var="num_samples" /> samples and observed $p$ = <DataValue var="p_value" />
with a mean effect size of <DataValue var="effect_size" />.

<!-- Keep a component tag off the start of a line: markdown-it treats a
     line beginning with `<Tag` as an HTML *block* and closes the surrounding
     paragraph around it. Wrapping mid-line (as above) keeps it inline. -->

Click any underlined value and the provenance panel slides in from the
right, showing `inputs → command → variable` as a vertical graph — the
identical panel the deck uses, mounted here through VitePress's
`layout-bottom` slot instead of Slidev's `global-bottom.vue`.

Because the component imports `manifest.yaml` directly, editing a value
hot-reloads both dev servers.

```yaml
# manifest.yaml
variables:
  num_samples:
    value: 12453
    format: ","
    description: "Total samples after QC filtering"
    source: "data/results.csv"
    updated: "2026-04-29"
```

## Manim scenes as figures

A scene renders once to `public/manim/<key>.webm`. The deck shows it
full-bleed via `layout: manim`; here the same file is an inline figure that
plays when it scrolls into view:

<ManimFigure scene="intro" caption="scenes/intro.py → public/manim/intro.webm" />

The poster frame is the *last* frame of the animation — usually the finished
diagram — so the figure reads correctly before playback and when printed.

## Math is first-class

LaTeX renders to static SVG at build time — no client-side JavaScript, and it
prints correctly. Inline math like $\hat{\beta} = (X^\top X)^{-1} X^\top y$ sits
in running text, and display environments are written the way you would in a
`.tex` file, with no `$$` fence:

\begin{align}
h^2 &= \frac{\sigma^2_A}{\sigma^2_P} \\
    &= \frac{\sigma^2_A}{\sigma^2_A + \sigma^2_E}
\end{align}

`$$ … $$` still works and is required for anything nested, like `cases` or a
matrix. Macros come from `math.macros` in the manifest, so they mean the same
thing in every output: $\Var(X)$, $\RR^n$, $\norm{v}$.

Code blocks use Shiki — the same highlighter Slidev uses, so a snippet looks
identical in both printouts.

## Citations

Cite the way you would in LaTeX. `\cite{visscher2008}` renders a linked
label \cite{visscher2008}, several keys collapse into one bracket
\cite{visscher2008,falconer1996}, `\citet` reads as text —
\citet{falconer1996} is the standard reference — and a locator rides along:
\cite[p. 160]{falconer1996}.

Entries come from the `.bib` files named in `bibliography.sources`, and
`\bibliography` marks where the list goes. Both the label style (`numeric` or
`author-year`) and the ordering are manifest settings, so switching from `[1]`
to `(Visscher et al., 2008)` is a one-line change that renumbers the in-text
markers and the list together.

\bibliography

## Building

```bash
presentation-sanity dev example:blog     # vitepress hot-reload
presentation-sanity dev example          # slidev hot-reload
presentation-sanity build                # every presentation → site/
presentation-sanity list                 # what this project holds
```
