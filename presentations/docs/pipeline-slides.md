# Native Google Slides pipeline

Build the deck directly in Google Slides via the API so it stays natively
editable — real text boxes, shapes, tables, and images, not a screenshot. Engine:
`engines/slides_api.py` (request builders). Charts: `engines/chart_kit.py` PNGs
served from a public URL.

## What you need

- Access to the Google Slides API (`presentations.create`, `presentations.batchUpdate`,
  `presentations.get`, `presentations.pages.getThumbnail`).
- A public static host for chart images (any host works; the `chart_kit.py`
  docstring shows a tiny generate-and-serve app you can deploy).

There is no PPTX-import or Sheets-linked-chart step here — this path assembles
the deck natively.

## Units & fonts

A default 16:9 Slides page is **720 × 405 pt** (9144000 × 5143500 EMU). Work in
pt; `E(pt)` converts to EMU. **Typeset only in real Google Fonts names**
(`Inter`, `Roboto`, `Montserrat`, `JetBrains Mono`, …) — Slides ignores embedded
fonts and substitutes by name, so an unknown name silently becomes Arial and the
layout drifts. Get weight from the bold flag.

## Order of operations (this matters)

1. **Create.** `presentations.create(title)` → keep the `presentationId`. The
   response object is very large; extract just the id.
2. **Setup batch.** `setup_requests(slide_ids, dark_ids=...)` — delete the default
   slide, create N blank slides, set any dark page backgrounds.
3. **Text/shape batches.** Send the native content (kickers, titles, rules, KPI
   rails, tables, footers) grouped by slide. These never touch the network, so
   they always apply. Keep `objectId`s ≥ 5 chars and unique.
4. **Warm, then images.** HTTP GET every chart URL to wake the host, then send the
   image batch. `createImage` fetches the URL at insert time; a cold host can
   time out and — because `batchUpdate` is **atomic** — roll back the whole batch.
   After insert, Slides stores its own copy, so the deck is self-contained and
   the host can go away.
5. **QA.** `presentations.pages.getThumbnail` per page → fetch the PNG → inspect.
   Verify the KPI rails, tables, and charts; confirm no fallback/overlap/clipping.

## Why chunk and isolate images

`batchUpdate` is all-or-nothing. Chunk requests by slide group so a single bad
request only loses one group, and **always isolate `createImage` requests** from
text — that way a flaky image fetch can never roll back your text. Build the
request payloads with a generator and validate the JSON locally before sending.

## Deliverable

The Google Slides URL is the deliverable
(`https://docs.google.com/presentation/d/<id>/edit`). Don't cite an intermediate
file. If the user will edit in Google Slides, the fonts you used must be Google
Fonts (they are, if you followed the rule above); the chart images are embedded
copies and stay put.
