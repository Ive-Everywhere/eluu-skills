---
name: presentations
description: Build high-craft, editable presentation decks — either as a PowerPoint .pptx or as a native Google Slides document. Use for investor/board decks, product launches, operating reviews, finance/metrics stories, and any slide work that has to look like a strong analyst, editor, and designer made it together. Ships a python-pptx grid engine, a Google Slides API assembler, a matplotlib chart kit, and an automated layout-quality gate.
---

# Presentations

Build decks that survive the contact-sheet test: at thumbnail size they read as
authored — a coherent visual system, varied slide rhythm, one clear idea per
slide — and at full size every slide has a claim, a proof object, and no filler.

This skill is for serious decks where "clean" isn't enough. It refuses
template-pack output: if a slide would look the same after swapping the company
name, it isn't done.

**Announce at start:** "I'm using the presentations skill to build this deck."

## When to use

- Investor / board / fundraising decks, operating and earnings reviews.
- Product launch, platform, and go-to-market narratives.
- Finance and metrics stories that are heavy on charts and tables.
- Any request to produce an **editable** deck (PowerPoint *or* Google Slides)
  at a high visual bar.

Do **not** use this for a one-line "make me 3 bullet points" ask, or when the
user explicitly wants a quick throwaway — it's more rigor than that needs.

## Two delivery targets — pick one up front

The methodology is identical; only the final substrate differs. Decide before
you build, because it changes fonts, units, and how charts are handled.

| | **PowerPoint (.pptx)** | **Native Google Slides** |
|---|---|---|
| Engine | `engines/pptx_deck.py` (python-pptx) | `engines/slides_api.py` (Slides API `batchUpdate`) |
| Unit / canvas | px → EMU (`1px = 9525 EMU`), 1280×720 | pt → EMU (`1pt = 12700 EMU`), 720×405 |
| Fonts | embed into the file **and** ship a PDF | use real **Google Fonts** names only |
| Charts | matplotlib PNGs placed locally | matplotlib PNGs hosted at a public URL |
| Render/QA | LibreOffice → PNG/PDF | Slides `getThumbnail` → PNG |
| Deliverable | the `.pptx` (+ `.pdf` reference) | the Slides URL (self-contained after insert) |

See `docs/pipeline-pptx.md` and `docs/pipeline-slides.md` for the full mechanics
of each path.

## Non-negotiable build rules

These exist because a deck can pass every visual check on the machine that built
it and still break in the viewer the user actually opens. Each rule prevents a
specific, real failure.

1. **Typeset in fonts the *target viewer* has.**
   - PPTX: embed the font files into the package (`embed_fonts` in
     `pptx_deck.py`) so PowerPoint/Keynote render them, **and** export a PDF —
     the PDF freezes glyphs as vectors and is correct in every viewer.
   - Google Slides (and most web previews) **ignore embedded fonts** and
     substitute by name. So write the run's font name as an exact **Google
     Fonts** family (`Inter`, `Roboto`, `Montserrat`, `JetBrains Mono`, …) and
     get weight from the bold flag. A name the viewer doesn't have (e.g. an
     optical-size or weight pseudo-family) silently falls back to Arial and the
     whole layout shifts.

2. **Lay out on an explicit grid.** A 12-column + 8px (or pt) baseline grid,
   with margins and gutters defined once. Snap every element to it. Put the
   slide's action title and a hairline rule at a fixed baseline on every content
   slide. Never eyeball positions — that misalignment is the number-one "this
   was machine-made" tell.

3. **Measure every string.** Before placing text, measure its rendered width
   against the actual font file (`Pillow.ImageFont.getlength`) and pre-wrap or
   auto-fit so it cannot overflow its box — regardless of which font the viewer
   ultimately uses. Don't rely on the viewer's word-wrap for headings.

4. **Verify with a layout gate, not just your eyes.** The build emits a
   per-element geometry record (`*.layout.json`); `engines/layout_check.py`
   reads it and flags text–text overlap, text overflowing a container,
   insufficient box padding, tight text boxes, and kicker-centerline drift.
   Errors are blocking. Also render a `--grid` overlay and a contact sheet and
   look at them.

5. **The build machine lies.** Rendering with the fonts installed hides
   font-fallback failures. Confirm fidelity through the embedded-font PPTX + PDF
   (PowerPoint path) or through Slides thumbnails after insert (Slides path) —
   never from the local render alone.

## Workflow

1. **Scope** — confirm the delivery target, the audience, and the data source.
   If the deck is finance/metrics and the user has no figures, either get them
   or use clearly-labelled *illustrative* data — **never present invented
   numbers as real**.
2. **Pick the deck profile** (see `docs/profiles.md`). The profile sets which
   proof objects are mandatory and what the failure modes are.
3. **Write the claim spine** — every non-appendix slide as: a 1–3 word kicker
   (its role), a claim title (a conclusion, not a topic), one proof object
   (chart / table / diagram / comparison), and a short, sourced support note.
   A title you could reuse after swapping the company name is not sharp enough.
4. **Lock the design system** (see `docs/design-system.md`) — canvas, grid,
   background system, a disciplined 3-colour palette (neutral + one accent + one
   support), one type pairing, chart grammar, and footer/source grammar.
5. **Plan the contact sheet** — at least 5 distinct macro-layout families for a
   ~10-slide deck; no 3 consecutive slides sharing a layout; at most 2 card-grid
   slides. The thumbnail strip should look authored before any detail is read.
6. **Build** with the engine for your target.
7. **Render → run the layout gate → score → iterate.** Fix the weakest 2–4
   slides, then re-render. Don't stop because a file exists.
8. **Deliver** the artifact (and, for PPTX, the PDF reference).

## Quality bar

Score the rendered contact sheet and full-size slides. Each dimension 0–5:
*story* (titles are claims, the sequence has an arc), *specificity* (fails the
noun-swap test), *rhythm* (varied macro layouts), *whitespace*, *chart clarity*
(one sentence per chart, direct labels, continuous geometry), *typography*,
*restraint* (no filler boxes/badges), *precision* (exact metrics + sources),
*coherence* (one visual system). Ship at **≥ 40 / 45**, with **no dimension
below 4**. Above the score sits the profile gate — a deck fails if its profile's
mandatory proof objects are missing or unsupported, no matter how pretty.

## Blocking anti-patterns

Fix before delivery: a title that states a topic instead of a conclusion; more
than one dominant proof object on a slide; a chart with a legend where direct
labels would read better; a chart that shows data but doesn't prove its title; a
connected series rendered as detached strokes; a connector that floats or points
nowhere meaningful; equal-role boxes that are misaligned or unevenly padded; a
repeated KPI rail missing a value on one item; a value lost to low contrast;
three consecutive slides with the same composition; body copy that only fills
space; an appendix that's clean but unreadable; rounded cards used as default
scaffolding; any fabricated logo, metric, or source; and — for charts — faking
per-point colour with hidden helper series instead of authoring the chart
cleanly.

## What's in this skill

```
presentations/
  SKILL.md                  this file
  LICENSE                   Apache-2.0
  NOTICE                    copyright + authorship/provenance
  README.md                 repo-facing overview + quickstart
  engines/
    pptx_deck.py            python-pptx grid/measure/embed engine + demo deck
    layout_check.py         automated layout-quality gate (reads *.layout.json)
    slides_api.py           Google Slides batchUpdate request builder
    chart_kit.py            matplotlib chart helpers + Eluu-hosting pattern
  docs/
    pipeline-pptx.md        PowerPoint path: fonts, grid, embed, PDF, gotchas
    pipeline-slides.md      native Google Slides path: API, hosted charts, cold-start
    profiles.md             deck profiles and their mandatory proof objects
    design-system.md        the design-system lock checklist
```

## Dependencies

- `python-pptx`, `Pillow`, `matplotlib` — `pip install python-pptx Pillow matplotlib`
- `libreoffice` (`soffice`) on PATH for PNG/PDF rendering (PPTX path only)
- For the Google Slides path: access to the Google Slides API, and any public
  static host for chart images (the `chart_kit.py` notes show a tiny
  generate-and-serve app).

All dependencies are open-source and used as-is at runtime; none are
redistributed by this skill.
