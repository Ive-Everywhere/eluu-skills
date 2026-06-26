# Template-following & targeted edits

When the user supplies their own deck — a corporate `.pptx`, a brand template,
or an existing Slides deck — that deck is the **canonical, editable starting
point**, not a loose reference. The job is to inherit its visual system exactly
and fill in content, or to insert a single new slide that looks native to it.

Default to this mode whenever the ask includes "template", "follow this", "use
this style", "same layout", "corporate template", "our deck", or an attached
reusable file. Do not treat such a file as a quality reference to beat.

## Two sub-modes

- **template-following** — produce a multi-slide deck whose every output slide is
  a duplicated source slide with content swapped in place.
- **targeted-edit** — add or replace one data/media slide in an existing deck,
  leaving everything else untouched.

## Required artifacts

Before building, write three files (and keep the source deck):

- **`template-audit.txt`** — for each source slide and the deck as a whole:
  - *preserve:* visual rules that must survive (type, palette, spacing, chrome).
  - *improve:* weak spots that may be upgraded if asked.
  - *do-not-imitate:* source artifacts that should not be copied forward.
  - *brand/assets:* which logos, colours, imagery, type, and crop language are
    official and verified.
  - *exact-clone:* typography, spacing, inherited placeholders, and slide
    skeletons that must remain unchanged.
  - *insertion-contract:* how a new slide or object joins the existing deck.
- **`template-frame-map.json`** — every output slide mapped to a source slide
  (a source slide may map to several outputs), with the content that fills it.
- **`deviation-log.txt`** — any place you departed from the source system, with
  the reason. Keep this short; departures should be rare and justified.

## Inherit the theme, don't reinvent it

`engines/template_follow.py` extracts the source deck's **theme tokens** — the
font scheme (major/minor) and the colour palette (dk1/lt1/dk2/lt2/accent1–6) —
straight from the package theme. Use those tokens as the design-system lock:
typeset new content in the inherited fonts and colour the new objects with the
inherited palette. Do **not** impose fresh typography ranges or a new palette
unless the user explicitly asks to restyle.

```python
import template_follow as t
theme = t.extract_theme("corporate.pptx")   # {fonts:{major,minor}, colors:{...}}
inv   = t.inventory("corporate.pptx")        # per-slide shape/placeholder list
```

`inventory()` lists each slide's shapes, placeholders, and text — the raw
material for `template-audit.txt` and `template-frame-map.json`.

## Clone-and-fill, don't rebuild

A template-following output slide must come from a **duplicated source slide**,
with copied elements edited in place — never a blank slide rebuilt to imitate the
source. Cloning preserves the exact masters, placeholders, spacing, and chrome
that make the deck look native; a rebuild always drifts.

```python
prs = t.load("corporate.pptx")
# duplicate the chosen source slide, then swap its text/values in place
slide = t.clone_slide(prs, source_index=4)
t.replace_text(slide, {"{{TITLE}}": "Q4 results", "{{KPI1}}": "$24.2M"})
prs.save("filled.pptx")
```

`clone_slide` copies a source slide's XML (shapes, formatting, placeholders) into
a new slide so all inherited styling carries over. `replace_text` walks the
copied shapes and swaps text **run by run**, preserving each run's font, size,
colour, and weight — so a number changes without the styling changing.

If no source slide can support a requested output, report the blocker and the
closest source-slide options rather than inventing a new frame.

## Targeted-edit specifics

- **targeted-edit-data:** finish the exact calculations first (the numbers, the
  ranking, the deltas), then build the one slide to match the deck's existing
  data-slide grammar — same chart style, same labels, same footnote treatment.
- **targeted-edit-media:** verify identity/source for every headshot, logo, or
  screenshot; match the deck's crop ratio and placement; change nothing outside
  the inserted objects.

## QA gate for these modes

The gate is **source-slide fidelity**, not reference-beating. Verify:

- every output slide traces to a mapped source slide in `template-frame-map.json`
- typography, palette, spacing, and chrome match the source at thumbnail size
- inherited placeholders and brand assets are preserved; no lookalike marks were
  invented to fill a gap
- a new/edited slide looks **native** to the deck, not pasted in from elsewhere
- the readability checks (overflow, padding, contrast) still pass on
  new/edited content — apply them only to what you changed

Run the layout gate on the new/edited slides; leave inherited source decoration
intact even if a script flags it as "decorative."
