# Native Google Slides pipeline

Build the deck directly in Google Slides via the API so it stays natively
editable — real text boxes, shapes, tables, and images, not a screenshot. Engine:
`engines/slides_api.py`. Charts: `engines/chart_kit.py` PNGs served from a public
URL. Slides is judged as a *living document*, so favour the version that stays
clean and native over the one that only looks better as a one-off render.

## What you need

- Access to the Google Slides API (`presentations.create`,
  `presentations.batchUpdate`, `presentations.get`,
  `presentations.pages.getThumbnail`).
- A public static host for chart images (the `chart_kit.py` docstring shows a
  tiny generate-and-serve app).

There is no PPTX-import or Sheets-linked-chart step here — this path assembles
the deck natively.

## Units & fonts

A default 16:9 Slides page is **720 × 405 pt** (9144000 × 5143500 EMU). Work in
pt; `E(pt)` converts to EMU. **Typeset only in real Google Fonts names**
(`Inter`, `Roboto`, `Montserrat`, `JetBrains Mono`, …) — Slides ignores embedded
fonts and substitutes by name, so an unknown name silently becomes Arial and the
layout drifts. Take weight from the bold flag. Keep titles short enough to stay
one line; if a title only fits because of a narrow font, shorten the copy.

## Build bias for Slides

Keep the main skill's premium bar, but shift toward maximum *native usefulness*:

- Prefer fewer, more robust objects over delicate stacks of narrowly-aligned
  fragments — a teammate should be able to duplicate a slide, replace one number,
  or add a callout without breaking the layout.
- Use layout families that survive edits (title / section / proof / comparison /
  table / roadmap / image-led), not one-off slide sculptures.
- Flatten fragile depth: fewer hairline overlays, tiny masks, and nested
  transparent panels whose value disappears on render.
- Design for the browser thumbnail and live review: strong hierarchy, high
  contrast, generous spacing.

## Order of operations (this matters)

1. **Create.** `presentations.create(title)` → keep the `presentationId`. The
   response object is very large; extract just the id.
2. **Setup batch.** `setup_requests(slide_ids, dark_ids=...)` — delete the
   default slide, create N blank slides, set any dark page backgrounds.
3. **Text/shape batches.** Send the native content (kickers, titles, rules, KPI
   rails, tables, footers) grouped by slide. These never touch the network, so
   they always apply. Keep `objectId`s ≥ 5 chars and unique.
4. **Warm, then images.** HTTP GET every chart URL to wake the host, then send
   the image batch. `createImage` fetches the URL at insert time; a cold host
   can time out and — because `batchUpdate` is **atomic** — roll back the whole
   batch. After insert, Slides stores its own copy, so the deck is self-contained
   and the host can go away.
5. **Speaker notes.** Add notes per slide where the deck will be presented live —
   notes carry the talk track, not a crutch for a slide that lacks a claim.

## Why chunk and isolate images

`batchUpdate` is all-or-nothing. Chunk by slide group so a single bad request
only loses one group, and **always isolate `createImage` requests** from text —
a flaky image fetch can then never roll back your text. Build the payloads with a
generator and validate the JSON locally before sending.

## Verification — match the loop to the risk

After building, verify on the actual Slides artifact, not just the local render.
A successful API call or upload is never sufficient.

- **Confirm** the deck exists as a native Slides presentation, the slide count
  and order match the plan, and the major titles/sections are present.
- **Fast path** (low-risk slides): inspect native thumbnails / a contact-sheet
  view; fetch large per-slide thumbnails only for high-risk slides.
- **Strict per-slide loop** (high-risk slides, or any detected drift): pull each
  page's `getThumbnail` and inspect it. High-risk = dense tables, small labels,
  complex charts, custom font pairings, aggressive crops, heavy diagrams, layered
  transparency, or anything near a layout limit.
- **Check editability:** titles, body, labels, sources, tables, KPI values, chart
  labels, and major diagram labels remain real editable objects — not flattened.
- **Check for fallback / overflow / clipping / stale placeholder text.**

Record the verification tier used and any accepted Slides-specific limitation in
the QA ledger.

## Editing an existing Slides deck / template

If the target is an existing deck or template, treat it as truth for layout
system, typography, spacing, footers, and asset behaviour. Duplicate and fill the
closest native template slide before inventing a new frame. Match its
collaboration grammar (how title slides, section breaks, and appendices are
meant to be extended), not just its look. Migrate by narrative job first, not
visual mimicry. (See `template-following.md`.)

## Anti-patterns to avoid

- A deck that is just a PowerPoint render uploaded to Drive with poor native
  editability.
- Full-slide image backgrounds carrying all the meaningful content (only when the
  user explicitly asked for image-only slides).
- Titles or proof objects that only work because of brittle font metrics.
- Microscopic text or ultra-thin rules that collapse in browser thumbnails.
- Overbuilt panel grids that feel like a product dashboard instead of a deck.
- Slides that need PowerPoint-only transitions (Morph/Zoom) to make sense.

## Deliverable

The Google Slides URL is the deliverable
(`https://docs.google.com/presentation/d/<id>/edit`). Don't cite an intermediate
file. The fonts must be Google Fonts (per the rule above); the chart images are
embedded copies and stay put.
