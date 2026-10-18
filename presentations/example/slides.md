---
# Deck-level config: frontmatter on the first slide configures the whole deck.
# Full reference: https://sli.dev/custom/
theme: seriph
title: Every number knows where it came from
author: Your Name
info: |
  The example deck of presentation-sanity-template: why a talk's numbers
  should come from one place, shown by a deck whose numbers do.
transition: slide-left
mdc: true
# Hash routing works on any dumb static host (no SPA fallback needed).
# Switch to "history" if your host serves index.html on 404.
routerMode: hash
# The cover. A color here (not an image URL) keeps seriph from fetching its
# default stock photo; style.css layers the gradient on top.
background: "#0d1b22"
class: hero
---

# Every number in this talk knows where it came from

This deck reports <DataValue var="num_samples" /> participants. Click that number.

<div class="hero-hint">space to advance · click any underlined number</div>

<!--
Open on the claim, then prove it immediately: the number on this slide is
live. Clicking it slides in where it came from.
-->

---

# Same result. Three places. Three numbers.

<!-- Hand-typed on purpose: this slide shows the failure mode. Every other
     number in this deck comes from manifest.yaml through <DataValue>. -->

<div class="grid grid-cols-3 gap-6 mt-10">
  <div class="drift-card">
    <div class="drift-where">Lab meeting slides, March</div>
    <div class="drift-number">11,982</div>
  </div>
  <div class="drift-card">
    <div class="drift-where">Conference poster</div>
    <div class="drift-number">12,435</div>
  </div>
  <div class="drift-card">
    <div class="drift-where">Paper, Table 1</div>
    <div class="drift-number">12,453</div>
  </div>
</div>

<v-click>

<p class="punchline">Which one is right? Without digging, nobody can say. That is what happens to every number you copy by hand.</p>

</v-click>

<!--
Every lab has this slide. The March number was right in March, the poster has
a transposed digit, the paper is current. Nothing says which is which.
-->

---
layout: center
class: text-center
---

# Click it.

<div class="big-number"><DataValue var="num_samples" /></div>

<p class="big-caption">participants after QC filtering</p>

<v-click>

<p class="mt-8 opacity-80">Its source file, the command that produced it, and the date, one click away.<br>For reviewers, for co-authors, and for you in six months.</p>

</v-click>

<div class="footnote">Sandve et al. (2013), Ten Simple Rules for Reproducible Computational Research. Rule 9: connect textual statements to underlying results.</div>

<!--
Click the number live. The panel shows input file, then command, then value.
Press Esc to close it.
-->

---
layout: two-cols-header
---

# Change it once. It changes everywhere.

::left::

```yaml
# manifest.yaml: the only place it's typed
variables:
  num_samples:
    value: 12453
    format: ","
    source: data/results.csv
    command: python scripts/qc.py …
    updated: "2026-09-30"
```

::right::

<div class="reads-from">

The same line feeds every printout:

- **This deck:** <DataValue var="num_samples" /> participants
- **<a href="../blog/">The blog post</a>:** the same tag, the same file
- **PDF handout:** `export pdf`
- **PowerPoint:** `export-pptx`, with the animation still playing

</div>

<v-click>

<p class="punchline">Edit one line and rebuild, and all four agree. No find-and-replace across forty slides.</p>

</v-click>

---
layout: manim
scene: one_source
---

Edit once. Every printout follows.

<!--
The animation is a manim scene rendered once to public/manim/one_source.webm.
The blog post embeds the same file. Press r to replay, p to pause.
-->

---

# The March talk still shows March's number

<div class="grid grid-cols-2 gap-8 mt-8">
  <div class="version-card">
    <code>presentations/kickoff/v1/</code>
    <div class="version-when">March lab meeting</div>
    <div class="version-number">n = <DataValue var="num_samples_2026q1" /></div>
  </div>
  <div class="version-card">
    <code>presentations/kickoff/v2/</code>
    <div class="version-when">October review</div>
    <div class="version-number">n = <DataValue var="num_samples" /></div>
  </div>
</div>

```bash
presentation-sanity new kickoff/v2 --from kickoff/v1    # a version is a folder
```

<v-click>

<p class="punchline">A changed number gets a new key, so an old version never silently changes. Click both numbers to see their provenance.</p>

</v-click>

---
layout: center
class: text-center
---

# Start yours

<div class="start-grid">
  <div><strong>On GitHub</strong><br>“Use this template” on presentation-sanity-template, then <code>python init.py</code></div>
  <div><strong>Without git</strong><br>One command, in any folder:<br><code>presentation-sanity init</code></div>
  <div><strong>With an agent</strong><br><code>/presentation-sanity</code> in Claude Code, or any agent that reads <code>.agents/skills/</code></div>
</div>

<p class="mt-10 opacity-70">The long version of this talk is <a href="../blog/">the blog post</a>, built from the same manifest.</p>

<div class="footnote">presentation-sanity is part of Sanitism: built for autists to communicate their work, sanely.</div>
