---
title: Every number should know where it came from
outline: [2, 3]
---

# Every number should know where it came from

A result travels. It leaves an analysis script, lands on a lab-meeting slide,
gets copied onto a poster, then into a paper, then into the grant renewal.
Every hop is a copy, and copies drift: a digit gets transposed, a slide keeps
the number from before the last QC pass, and six months later nobody can say
which version is right.

When Nature surveyed 1,500 scientists about reproducibility \cite{baker2016},
the conversation was about whole experiments. It starts smaller than that,
with a number typed twice.

This post and [its deck](../slides/){target="_self"} are two printouts of one project. Every
number on both comes from a single file, and every one of them can tell you
where it came from.

## Click the number

We analyzed <DataValue var="num_samples" /> participants after QC. The primary
comparison came out at an effect size of <DataValue var="effect_size" />, with
$p$ = <DataValue var="p_value" />.

<!-- Keep a component tag off the start of a line: markdown-it treats a line
     beginning with `<Tag` as an HTML block and breaks the paragraph. -->

Click any of those three numbers. A panel slides in with the file the value was
read from, the command that produced it, and the date it was last updated.
Nothing is executed when the page builds. The panel is a record, kept next to
the value, of how the value was made.

\citet{sandve2013} put reproducible computational research as ten rules.
The first is to keep track of how every result was produced, and the ninth is
to connect textual statements to underlying results. A `<DataValue>` is the
ninth rule as a component: the sentence and the result it reports are the
same object, so they can't drift apart.

The effect size is Cohen's $d$, the difference in group means scaled by the
pooled standard deviation:

\begin{equation}
d = \frac{\bar{x}_1 - \bar{x}_2}{s_p},
\qquad
s_p = \sqrt{\frac{(n_1 - 1)\, s_1^2 + (n_2 - 1)\, s_2^2}{n_1 + n_2 - 2}}
\end{equation}

The math is rendered to SVG when the site builds, so it needs no JavaScript in
the browser and it prints cleanly.

## Change it once

Each number is typed exactly once, in `manifest.yaml`:

```yaml
variables:
  num_samples:
    value: 12453
    format: ","
    description: "Participants after QC filtering"
    source: "data/results.csv"
    command: "python scripts/qc.py data/raw/ --out data/results.csv"
    updated: "2026-09-30"
```

That one line feeds this post, the deck, the PDF handout and the PowerPoint
export. When the second batch of samples cleared QC, the count went from <DataValue
var="num_samples_2026q1" /> to <DataValue var="num_samples" />. That took one
edit and one rebuild, with no find-and-replace across slide decks.

<ManimFigure scene="one_source" caption="Edit once, and every printout follows. The same rendered video plays full-screen in the deck." />

## Old talks keep their numbers

Talks get given more than once. In this project, a new version is a folder,
forked from the last one:

```bash
presentation-sanity new kickoff/v2 --from kickoff/v1
```

The new folder records where it came from, and the project's index page shows
that lineage. When a number changes between versions, it gets a new key rather
than an edit. The March talk keeps reporting <DataValue
var="num_samples_2026q1" />, with its March provenance attached, and nothing it
said changes behind its back.

## A minimum standard

\citet{peng2011} argues that when full independent replication isn't possible,
reproducibility can serve as a minimum standard for judging a scientific claim.
A talk makes claims too. Making each number traceable to its source is the
cheapest part of meeting that standard, and with one source it costs nothing
extra to keep.

## Start yours

- **On GitHub:** "Use this template" on
  [presentation-sanity-template](https://github.com/yakaboskic/presentation-sanity-template),
  then run `python init.py`.
- **Without git:** `presentation-sanity init my-talk` in any folder. The
  [template's README](https://github.com/yakaboskic/presentation-sanity-template#starting-a-project)
  has the one-line `uvx` version, which needs nothing installed.
- **With an agent:** the project ships a `/presentation-sanity` skill for
  Claude Code, and the same skill in `.agents/skills/` for other agents.

The short version of this post is [the deck](../slides/){target="_self"}.

\bibliography
