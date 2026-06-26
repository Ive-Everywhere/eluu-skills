# presentations — Eluu PPT skill

Build high-craft, **editable** decks — as a PowerPoint `.pptx` or as a **native
Google Slides** document — that look like a strong analyst, editor, and designer
made them together. Covers building from scratch, **following a corporate
template**, and **targeted single-slide edits**. Investor/board decks, product
launches, operating reviews, finance/metrics stories.

This is an Eluu Labs skill. The agent-facing instructions live in
[`SKILL.md`](./SKILL.md); this README is the human quickstart.

## What's here

| Path | What it is |
|---|---|
| `SKILL.md` | The skill: task modes, deck-profile router, the full phased workflow, build rules, quality bar, precision contract, anti-patterns |
| `engines/pptx_deck.py` | python-pptx engine: 12-col grid, measured text, font embedding, layout recorder, demo deck |
| `engines/template_follow.py` | Template mode: extract a deck's theme (fonts/palette), inventory it, clone-and-fill slides preserving run formatting |
| `engines/layout_check.py` | Automated layout-quality gate (overlap / overflow / padding / kicker drift) |
| `engines/slides_api.py` | Google Slides `batchUpdate` request builders for a native deck |
| `engines/chart_kit.py` | Clean matplotlib charts + the serve-PNGs-for-Slides pattern |
| `docs/pipeline-pptx.md` | PowerPoint path: fonts, grid, embed, PDF, gotchas |
| `docs/pipeline-slides.md` | Native Google Slides path: API, hosted charts, verification tiers |
| `docs/template-following.md` | Inherit a corporate template; clone-and-fill; targeted edits |
| `docs/profiles.md` | Every deck profile and its mandatory proof objects |
| `docs/precision-contract.md` | Structured-visual rules for charts/diagrams/boxes/tables |
| `docs/design-system.md` | The design-system lock checklist |
| `docs/subagents.md` | When and how to parallelise with subagents |

## Three task modes

- **create** — build from a prompt and sources.
- **template-following** — bring your corporate `.pptx`; inherit its theme and
  clone-and-fill its slides so the result looks native to your deck.
- **targeted-edit** — add or replace one data/media slide in an existing deck.

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

Default to **native, editable objects**; render to an image only the hardest
exhibits (waterfall, swimlane, dense combo charts), never the whole slide.

## Quickstart (PowerPoint path)

```bash
pip install python-pptx Pillow matplotlib   # + LibreOffice (soffice) on PATH
# stage Inter / JetBrains Mono .ttf files in engines/fonts/ (or set DECK_FONT_DIR)
cd engines
python pptx_deck.py demo.pptx --layout out/layout
python layout_check.py out/layout
soffice --headless --convert-to pdf --outdir out demo.pptx
```

## Quickstart (template-following)

```bash
python engines/template_follow.py corporate.pptx     # print theme tokens + slide inventory
# then clone-and-fill in Python: extract_theme / inventory / clone_slide / replace_text
```

## Quickstart (Google Slides path)

See [`docs/pipeline-slides.md`](./docs/pipeline-slides.md): create a
presentation, send native text/shape batches, host your `chart_kit` PNGs at a
public URL, warm the host, send the image batch, then QA with page thumbnails.

## License

Apache-2.0 — see [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE). All prose and
code here were authored independently by Eluu Labs; the runtime dependencies
(python-pptx, Pillow, matplotlib, LibreOffice, Google Slides API) are used as-is
under their own licenses and are not redistributed.
