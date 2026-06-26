---
name: presentations
description: Build high-craft, editable presentation decks (consultancy / investor / board / launch tier) as a PowerPoint .pptx or a native Google Slides document. Covers create-from-scratch, follow-an-existing-template, and targeted single-slide edits. Ships a python-pptx grid engine, a Google Slides API assembler, a template/theme-inheritance engine, a matplotlib chart kit, and an automated layout-quality gate. Use whenever a deck has to look like a strong analyst, editor, and designer built it together.
---

# Presentations

This skill produces decks that win the contact-sheet test: at thumbnail size the
deck reads as authored — a coherent visual system, varied slide rhythm, and one
clear idea per slide — and at readable size every non-appendix slide has a
claim, a single proof object, and no filler.

It is for serious work where "clean" is not the bar. A deck can pass every
mechanical check and still fail: if it looks like a generic SaaS dashboard, a
consulting card-grid, or a template that only had the company name swapped in,
it is not done — keep iterating.

**Announce at start:** "I'm using the presentations skill to build this deck."

## North star

- Every slide title is a **conclusion**, not a topic label.
- Every non-appendix slide carries exactly **one dominant proof object**.
- The deck uses **one visual system** end to end.
- Nothing is fabricated — not a metric, not a logo, not a source.

If a title still reads true after swapping the company name, it is too generic.
Sharpen it.

## Operating contract (build substrate)

The methodology below is substrate-agnostic. Two native, **editable** build
targets are supported, plus a controlled use of rendered images for the hardest
exhibits. Decide the target up front; it changes fonts, units, and chart
handling.

| | **PowerPoint (.pptx)** | **Native Google Slides** |
|---|---|---|
| Engine | `engines/pptx_deck.py` (python-pptx) | `engines/slides_api.py` (Slides API `batchUpdate`) |
| Template-follow | `engines/template_follow.py` (theme + clone-and-fill) | inherit theme tokens; rebuild natively |
| Unit / canvas | px → EMU (`1px = 9525 EMU`), 1280×720 | pt → EMU (`1pt = 12700 EMU`), 720×405 |
| Fonts | embed into the file **and** export a PDF | real **Google Fonts** names only |
| Charts / hard exhibits | matplotlib (or authored-shape) images, placed locally | matplotlib images hosted at a public URL |
| Render / QA | LibreOffice → PNG/PDF | Slides `getThumbnail` → PNG |
| Deliverable | the `.pptx` (+ `.pdf` reference) | the Slides URL (self-contained after insert) |

**Default to native, editable objects.** Keep titles, body, labels, KPI rails,
tables, and simple diagrams as real editable elements. Render to an image only
the genuinely hard exhibits (waterfall, swimlane, heatmap, dense combo charts) —
never the whole slide. Whole-slide image decks are allowed only when the user
explicitly asks for a presented-not-edited, image-led artifact.

For the mechanics of each path, read `docs/pipeline-pptx.md` and
`docs/pipeline-slides.md`. For bringing a user's corporate template, read
`docs/template-following.md`.

## Non-negotiable build rules

Each prevents a specific, real failure — a deck that looks perfect on the
machine that built it can still break in the viewer the user opens.

1. **Typeset in fonts the target viewer has.** PPTX: embed the font files into
   the package (`embed_fonts`) so PowerPoint/Keynote render them, *and* export a
   PDF (vector glyphs, correct everywhere). Google Slides and most web previews
   **ignore embedded fonts** and substitute by name — so use exact **Google
   Fonts** family names and take weight from the bold flag. An unknown name
   silently becomes Arial and the layout shifts.
2. **Lay out on an explicit grid.** 12 columns + an 8-unit baseline, margins and
   gutters defined once, every element snapped. Action title and a hairline rule
   on a fixed baseline on every content slide. Never eyeball positions.
3. **Measure every string.** Measure rendered width against the real font file
   (`Pillow.ImageFont.getlength`) and pre-wrap or auto-fit so text cannot
   overflow under fallback. Do not rely on viewer word-wrap for headings.
4. **Gate the layout automatically.** The build emits per-element geometry
   (`*.layout.json`); `engines/layout_check.py` flags text–text overlap, text
   overflowing a container, weak box padding, tight text boxes, and
   kicker-centerline drift. Errors block. Also inspect a `--grid` overlay and a
   contact sheet.
5. **The build machine lies.** Rendering with your fonts installed hides
   fallback failures. Confirm fidelity through the embedded-font PPTX + PDF, or
   through Slides thumbnails after insert — never the local render alone.

## Mandatory workflow

1. Confirm the **task mode** and **delivery target**.
2. Read the source and any reference (Phase 0).
3. Write the **claim spine** (Phase 1).
4. Lock the **design system** (Phase 2).
5. Plan the **contact sheet** (Phase 3).
6. **Build** editable slides (Phase 4).
7. Render previews + layout JSON, run the **gate**.
8. Score against the **comeback rubric** (Phase 5).
9. **Iterate** the weakest slides; re-render.
10. Pass **mechanical verification** (Phase 6) before export.
11. Write the **QA ledger** and **clean up** scratch (Phase 7).

## Task modes

- **create** — no deck/template supplied; build from the prompt and sources.
- **template-following** — a source/template `.pptx` (or an existing Slides
  deck) is supplied whose slide skeletons and visual system must be inherited.
  Preserve its typography, palette, spacing, layout, and brand chrome unless the
  user asks to restyle. Inventory the source, map every output slide to a source
  slide, then clone-and-fill. See `docs/template-following.md`.
- **targeted-edit** — small changes to an existing deck (add/replace one
  data or media slide). Preserve the deck's visual system; use readability
  guidance only as a QA check on the new/edited content.

When both a source deck and a separate *quality reference* exist, keep them
distinct: the source deck supplies content, required sections, and facts; the
reference supplies the quality bar and proves a stronger output is possible. Do
not clone a reference — beat it on story precision, composition variety, chart
clarity, whitespace, and render quality.

Template-like phrasing ("template", "follow this", "use this style", "same
layout", "corporate template", "source deck", or an attached reusable file)
routes to template-following, not to a loose quality reference.

## Deck-profile router

After task mode, choose exactly one **primary** profile. This is hard routing,
not a label: the profile decides which proof objects, source rules, asset rules,
and QA gates are blocking. If several apply, pick the one with the highest
delivery risk as primary and list the rest as secondary gates in the claim
spine. Read the matching section of `docs/profiles.md` for any non-trivial deck.

- **finance-ir** — earnings, investor, board, operating reviews, financial
  analysis. Exact reported figures, unit discipline, source footnotes, bridges,
  tables, disclosure logic.
- **product-platform** — SaaS/platform/product narratives. Architecture and
  workflow maps, adoption proof, product-to-business linkage; no generic
  feature-card grids.
- **gtm-growth** — GTM, marketing, growth, subscription, mobility, engagement.
  A visible growth loop/funnel, segment or cohort proof, a monetization bridge,
  brand-aware rhythm.
- **engineering-platform** — developer, AI, infra, data, security. Accurate
  system diagrams, technical labels that survive executive simplification,
  metrics tied to the architecture.
- **strategy-leadership** — investor-day, board, transformation, market
  strategy. Chapter discipline, a market frame that returns in the operating
  plan, explicit bets, transition slides that carry the thesis.
- **consumer-retail** — lookbooks, brand, campaign, lifestyle, image-led
  storytelling. Real assets or explicit provenance, image quality, editorial
  hierarchy, client-ready copy.
- **appendix-heavy** — dense tables, disclosures, source packs. Index/page
  markers, readable small-type thresholds, table grammar, source-density rules.
- **template-following** — a supplied template/source deck is canonical;
  clone/edit only. Requires `template-audit.txt`, `template-frame-map.json`, and
  `deviation-log.txt`. Follow `docs/template-following.md`; add a domain profile
  (e.g. finance-ir) as a secondary gate.
- **targeted-edit-data** — add/edit a data or comparison slide. Exact
  calculations before any visual work; a native-looking insertion.
- **targeted-edit-media** — add headshots, logos, screenshots, or media.
  Identity/source verification, consistent crops, preserved layout grammar.

Record the routing in `profile-plan.txt`: task mode, primary profile, secondary
gates, required proof objects, source/asset requirements, brand-authenticity
constraints, profile QA gates, and known missing inputs.

## Phase 0 — source & reference read

For every source or reference deck: render it to PNGs/PDF pages, make a contact
sheet, extract slide text, and identify which slides are content sources, which
are visual targets, and which are anti-patterns.

For source links and finance/product narratives, exhaust official materials
(earnings decks, supplements, filings, IR PDFs) before omitting customer,
cohort, module, bookings, retention, guidance, or mix metrics. Extract exact
figures and source dates. **Never invent a missing metric to make a chart
prettier.** If you must use sample numbers, label them illustrative.

**Brand-authenticity gate.** Treat logos, mascots, app icons, product UI,
character marks, and partner/customer marks as identity assets. Do not draw,
trace, approximate, or stylise an official mark from scratch. Use a verified
source asset with provenance, a user-supplied asset, or none — and rely on
colour, typography, layout, product language, and sourced metrics as brand cues
instead. Record every identity asset in `source-notes.txt` with provenance.

Create as needed: `source-notes.txt`, `reference-audit.txt`, `data.json` (when
metrics/charts are used), and — for template-following / targeted-edit —
`template-audit.txt`, `template-frame-map.json`, `deviation-log.txt`.

## Phase 1 — claim spine (binding)

Before designing, write the story as slide claims. Every non-appendix slide:

- a **kicker** — 1–3 words naming the slide's role (e.g. `EXPANSION DRIVERS`)
- a **claim title** — a conclusion, not a topic
- a **proof object** — one chart, table, timeline, diagram, or comparison
- a **support note** — concise, factual, sourced

A single thin chart usually fails for finance/product slides — prefer one
dominant proof object plus a compact context rail, variance table, or callout
stack. Reject a proof object whose metric movement is too small to carry the
claim. Product/architecture maps must show product-to-business linkage (module
or workflow → adoption → expansion/monetization → efficiency).

Write `claim-spine.txt`: thesis, audience, one-line arc, and a slide list with
claim, proof object, source, and omission notes per slide.

## Phase 2 — design-system lock

Write `design-system.txt` before building. Define: slide size; background
system; a type pairing (installed/embeddable for PPTX, Google Fonts for Slides);
a disciplined palette (a neutral/base, one accent, one support — each with a
meaning, never decorative); chart grammar; diagram/connector grammar; container
grammar; source/footer grammar; page-marker grammar; title/kicker grammar;
data-label grammar; the brand-asset policy; allowed layout families; and banned
motifs. See `docs/design-system.md`.

For create mode, default to readable ranges (px): cover/section claims 56–72,
titles 34–52, body 18–26, chart/table labels 12–16, source/footer 9–11. For
template-following / targeted-edit, **record and preserve** the inherited system
— do not impose fresh ranges or palettes unless asked to restyle.

Use a canonical kicker construction so QA can verify alignment: name the marker
and label as a pair (`kicker-marker` / `kicker-label`), share their vertical
centre within ≤1px, and middle-align the label with enough height that glyphs
don't sit low after export.

## Phase 3 — contact-sheet plan

Write `contact-sheet-plan.txt`. For a ~10-slide deck use at least **5 distinct
macro-layout families** (cover+rail, editorial map, bar proof with margin notes,
mix/donut with ranked table, line + KPI stack, sequential bars + summary rail,
two-series cash chart, roadmap timeline, dense appendix table, dark source
page, …). Hard gates: no more than 2 card-grid slides in 10; no 3 consecutive
slides sharing a macro layout; no repeated `title + subtitle + boxed-panel-grid`
cadence; no rounded-card default; no decorative boxes around prose. The contact
sheet must look authored before any detail is read.

## Phase 4 — editable build

Build with the engine for the chosen target. Prefer native editable shapes,
lines, text, tables, and chart-like constructs. Native charts are fine when they
express the chart cleanly; an authored editable chart (shapes + direct labels)
or a rendered chart image is acceptable when it gives better labelling. For
template-following, **clone the mapped source slide and edit copied elements in
place** rather than rebuilding from blank — see `docs/template-following.md`.

Follow the **structured-visual precision contract** (`docs/precision-contract.md`)
for every chart, diagram, connector, box, table, and flow. In brief: connected
series are one continuous path through their markers; connectors visibly attach
to the right source and target and only carry an arrowhead when direction
matters; equal-role boxes share exact height, padding, and treatment; labels
anchor to the object they describe; repeated KPI/metric rails render every piece
of their grammar on every item; and a preview-visible defect overrides any
silent layout-script pass.

Do not introduce decorative SVGs, blobs, badges, ornaments, or icon-stacks that
encode no data, hierarchy, or verified identity. Editable primitives are for
charts/diagrams/flows, never a licence to fabricate brand marks.

## Phase 5 — comeback rubric

Score the rendered contact sheet and full-size slides in
`qa/comeback-scorecard.txt`. Each dimension 0–5: **story** (titles are claims,
sequence has an arc), **specificity** (fails the noun-swap test), **rhythm**
(varied macro layouts), **whitespace**, **chart clarity** (one sentence per
chart, direct labels, continuous/attached geometry), **typography**,
**restraint** (no filler boxes/badges/clutter), **precision** (exact metrics and
sources), **coherence** (one visual system), and **reference delta** (visibly
better than the supplied reference, when one exists).

Minimum to ship: total ≥ 44/50 with a reference, else ≥ 40/45; no dimension
below 4; reference delta ≥ 4 when a reference exists (else mark `n/a` and do not
claim reference-beating). The **profile gate is pass/fail and sits above the
score** — a deck fails if its profile's mandatory proof objects are missing or
unsupported, however high the visual score. For template-following, the gate is
source-slide fidelity, not reference-beating.

## Phase 6 — mechanical verification

Before delivery: confirm the file exists, is non-empty, and has the expected
slide count; confirm no empty media; render every final slide to PNG and inspect
the contact sheet at thumbnail size and the full-size renders. Verify repeated
grammars (KPI rails, step sequences, legends, forecast strips) for completeness
and contrast — no blank value slots, no same-colour-on-background text, no
decorative marks colliding with the read path. For every chart/diagram/matrix/
connector/box system, verify the intended geometry at full size: continuous
lines through the right markers; aligned baselines; connectors attached and
pointing the intended way; equal-role boxes aligned and evenly padded; kickers
optically centred; boxed prose with visible top/bottom breathing room. Run the
layout gate and fix all errors; warnings may remain only as known
false-positives from intentional construction with a clean render. Inspect for
any unverified logo/app-icon/mascot/product-UI/partner mark and remove it.

## Phase 7 — QA ledger & cleanup

Write `qa/comeback-scorecard.txt`: final score by dimension; primary profile and
gate pass/fail; reference comparison; tool/runtime caveats; package checks;
render checks; and accepted warnings/tradeoffs. Name the remaining weak spots —
do not leave it as vague praise.

Then clean up scratch: planning/QA text notes, preview/contact-sheet images,
generated per-run modules, layout JSON, and temporary images. Keep only final
deliverables (and any reusable engine the user wants). Do not attach scratch in
the final response, and keep the response short and artifact-focused.

## Blocking anti-patterns

Fix before delivery: a topic title instead of a conclusion; more than one
dominant proof object; a legend where direct labels read better; a chart that
shows data but doesn't prove its title; a connected series drawn as detached
strokes / floating slashes / a path that misses its markers; line or connector
geometry that changes meaning after export; a connector that floats, attaches to
the wrong object, or points ambiguously; decorative arrows; a box system
implying a grouping the content doesn't support; equal-role boxes misaligned or
unevenly padded; a label detached from its object; a repeated KPI rail missing a
value/label/context on any item; a marker sitting on top of copy; a value lost
to low contrast; a table/matrix losing row/column grammar at thumbnail size; a
proof object too thin for its claim; an architecture diagram with no
adoption/monetization/efficiency linkage; containers louder than content;
rounded cards as default scaffolding; three consecutive same-composition slides;
a contact sheet that reads as a template pack; body copy that only fills space;
a clean-but-unreadable appendix; wrapped labels / collisions / cramped callouts;
a drifting footer/source/page-marker; a kicker whose marker and label aren't
optically centred; boxed prose pinned to an edge; default typography with no
intent; a low-res logo or rough crop; a fabricated or approximated official
logo/mascot/app-icon/product-UI; a brand-like icon used to fill whitespace;
unprovenanced partner/customer logos or screenshots; an unsupported metric or
vague source; output that only matches the reference instead of beating it.

## Subagents

Use subagents when the user asks for them, or for parallelisable, well-scoped
sub-jobs: source-metric extraction, reference-deck critique, final QA
inspection/scoring, appendix implementation from a fixed spec, or an alternate
prototype in a separate workspace. The main agent always owns the final story,
visual system, integration, and QA — never ship a raw stitched deck from
independent slide workers. See `docs/subagents.md`.

## Iteration rule

Do not stop at the first export unless the rubric passes. Iterate the weakest
2–4 slides first, then re-render the full deck; prefer a bold rebuild of a weak
slide over cosmetic nudges. If a tool or model can't reach the bar, say exactly
why and name the remaining weakest slides. A file existing is not "done." For
template-following, iterate against source-slide fidelity, not reference-beating.

## What's in this skill

```
presentations/
  SKILL.md                  this file
  LICENSE                   Apache-2.0
  NOTICE                    copyright + authorship/provenance
  README.md                 repo-facing overview + quickstart
  engines/
    pptx_deck.py            python-pptx grid/measure/embed engine + demo deck
    template_follow.py      theme extraction + clone-and-fill for template mode
    layout_check.py         automated layout-quality gate (reads *.layout.json)
    slides_api.py           Google Slides batchUpdate request builder
    chart_kit.py            matplotlib chart helpers + hosting pattern
  docs/
    pipeline-pptx.md        PowerPoint path: fonts, grid, embed, PDF, gotchas
    pipeline-slides.md      native Google Slides path: API, hosted charts, QA tiers
    template-following.md   inherit a corporate template; clone-and-fill; targeted edits
    profiles.md             every deck profile and its mandatory proof objects
    precision-contract.md   structured-visual rules for charts/diagrams/boxes/tables
    design-system.md        the design-system lock checklist
    subagents.md            when and how to parallelise with subagents
```

## Dependencies

- `python-pptx`, `Pillow`, `matplotlib` — `pip install python-pptx Pillow matplotlib`
- `libreoffice` (`soffice`) on PATH for PNG/PDF rendering (PPTX path)
- Google Slides path: access to the Slides API + any public static host for chart
  images (see `chart_kit.py`)

All dependencies are open-source and used as-is at runtime; none are
redistributed by this skill.
