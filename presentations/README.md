# presentations — Eluu PPT skill

Build high-craft, **editable** decks — as a PowerPoint `.pptx` or as a **native
Google Slides** document — that look like a strong analyst, editor, and designer
made them together. Investor/board decks, product launches, operating reviews,
finance/metrics stories.

This is an Eluu Labs skill. The agent-facing instructions live in
[`SKILL.md`](./SKILL.md); this README is the human quickstart.

## What's here

| Path | What it is |
|---|---|
| `SKILL.md` | The skill: when to use, the two delivery targets, the non-negotiable build rules, workflow, quality bar, anti-patterns |
| `engines/pptx_deck.py` | python-pptx engine: 12-col grid, measured text, font embedding, layout recorder, demo deck |
| `engines/layout_check.py` | Automated layout-quality gate (overlap / overflow / padding / kicker drift) |
| `engines/slides_api.py` | Google Slides `batchUpdate` request builders for a native deck |
| `engines/chart_kit.py` | Clean matplotlib charts + the serve-PNGs-for-Slides pattern |
| `docs/pipeline-pptx.md` | PowerPoint path: fonts, grid, embed, PDF, gotchas |
| `docs/pipeline-slides.md` | Native Google Slides path: API, hosted charts, cold-start |
| `docs/profiles.md` | Deck profiles and their mandatory proof objects |
| `docs/design-system.md` | The design-system lock checklist |

## The core idea

A good deck survives the **contact-sheet test**: at thumbnail size it reads as
authored; at full size every slide has a claim, one proof object, and no filler.
Five rules make that hold up in the viewer the user actually opens:

1. Typeset in fonts the **target viewer** has (embed + ship a PDF for PowerPoint;
   real Google Fonts names for Slides).
2. Lay out on an explicit **grid**; snap everything.
3. **Measure** every string so it can't overflow.
4. **Gate** the layout automatically, not just by eye.
5. The build machine lies — verify through the PDF / Slides thumbnails.

## Quickstart (PowerPoint path)

```bash
pip install python-pptx Pillow matplotlib   # + LibreOffice (soffice) on PATH
# stage Inter / JetBrains Mono .ttf files in engines/fonts/ (or set DECK_FONT_DIR)
cd engines
python pptx_deck.py demo.pptx --layout out/layout
python layout_check.py out/layout
soffice --headless --convert-to pdf --outdir out demo.pptx
```

## Quickstart (Google Slides path)

See [`docs/pipeline-slides.md`](./docs/pipeline-slides.md). In short: create a
presentation, send native text/shape batches, host your `chart_kit` PNGs at a
public URL, warm the host, send the image batch, then QA with page thumbnails.

## License

Apache-2.0 — see [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE). All prose and
code here were authored independently by Eluu Labs; the runtime dependencies
(python-pptx, Pillow, matplotlib, LibreOffice, Google Slides API) are used as-is
under their own licenses and are not redistributed.
