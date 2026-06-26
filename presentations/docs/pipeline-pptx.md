# PowerPoint (.pptx) pipeline

Engine: `engines/pptx_deck.py` (python-pptx). Render/QA: LibreOffice. The output
is an editable `.pptx` plus a `.pdf` reference that renders identically anywhere.

## Setup

```bash
pip install python-pptx Pillow matplotlib
# LibreOffice (soffice) must be on PATH for rendering.
```

Stage your `.ttf` files in a `fonts/` directory and point `STYLE`/`EMBED` in
`pptx_deck.py` at them. The font files are used to **measure** text (so it can't
overflow) and to **embed** into the package.

## Build

Author one builder that calls the engine helpers (`slide`, `header`, `block`,
`label`, `rect`, `line`, `kicker`, `footer`) on the 12-column grid, then:

```python
import pptx_deck as d
# ... build your slides ...
d.save("out/MyDeck.pptx", layout_dir="out/layout")   # also embeds fonts
```

`save(layout_dir=...)` writes a `*.layout.json` per slide for the gate, then
embeds the fonts into the file.

## Render

```bash
soffice --headless --convert-to pdf --outdir out out/MyDeck.pptx
pdftoppm -png -r 110 out/MyDeck.pdf out/slide      # per-slide PNGs to inspect
```

Build a contact sheet from the PNGs (Pillow) and look at it at thumbnail size —
the deck should read as authored before any detail.

## Gate

```bash
python engines/layout_check.py out/layout
```

Errors block (overlap, overflow, kicker drift, out-of-bounds). Warnings are
advisory — tight display leading and intentional label/value groupings are
expected; confirm against the render.

Optionally build a `--grid` overlay variant (draw the columns + baseline + rules)
to *see* that everything snaps.

## Why both a PPTX and a PDF

The `.pptx` is the editable source; with fonts embedded, PowerPoint and Keynote
render it as designed. But many viewers (Google Slides, web previews, Quick Look)
ignore embedded fonts and substitute by name, which shifts the layout. The
exported **PDF freezes glyphs as vectors** and is pixel-correct everywhere — ship
it as the reference copy. Judge fidelity from the PDF, not from the render on the
machine that has your fonts installed.

## Common gotchas

- `pip` and `python3` can resolve to different interpreters — verify
  `python3 -c "import pptx"` after installing.
- Empty output directories can be pruned by sync between steps — create them
  right before writing, or write a file into them immediately.
- Set `shape.shadow.inherit = False` to kill python-pptx's default drop shadow.
- Use `ROUNDED_RECTANGLE` `adjustments[0]` for corner radius; keep it small.
