# Structured-visual precision contract

Charts, diagrams, connectors, boxes, tables, and flows are high-risk proof
objects. Treat each as a **geometry system**, not decoration. A visual that
looks plausible at a glance but is geometrically wrong is worse than a simpler
visual that is correct.

## Before authoring any structured visual, define

- what the visual must **prove** (it maps to the slide's claim title)
- the primary **reading order**
- each **node / mark / series** and what it means
- each **edge / connector** and what relationship it encodes
- each **container / box** and what grouping or containment it means
- the intended **alignment, spacing, and label-attachment** rules

If you can't answer these, you're decorating, not proving — stop and rethink the
proof object.

## Hard build rules

**Series & lines.** A connected series is one continuous editable path (or a
verified native chart series), passing through every intended marker in the
correct order after render/export. Never fake a line with rotated rectangles,
disconnected strokes, floating slashes, or decorative arrows — these export as
detached marks.

**Connectors.** In a diagram, a connector visibly attaches to the correct source
and target, follows the intended direction, avoids unrelated objects, and
terminates cleanly without ambiguous crossings. Use real connector attachment
(e.g. connect a shape to a shape), not free-floating line segments. Use an
arrowhead only when direction is meaningful; when it is, keep heads consistent,
legible, and semantically correct.

**Boxes & containers.** A box implies a real grouping, comparison, lane, stage,
or containment. Remove any container that only decorates prose. Equal-role boxes
share exact height, alignment, padding, border logic, and text treatment unless
the hierarchy is intentionally different. Text inside a box has enough padding
and never sits against an edge, collides with a rule, or relies on shrink-to-fit
as the default. Use ≥ 12px interior vertical padding for single-line boxed copy
and ≥ 16px for 2+ lines or dark-background copy; if a box only looks right with
near-zero bottom room, enlarge the box or shorten the copy. Text that starts
inside a filled callout and spills past its edge is a hard failure, even if a
layout script no longer classes the overflowed line as an in-box child.

**Labels.** Every label anchors to the mark, series, box, or connector it
describes. A viewer should never have to guess which label belongs to which
object. Prefer direct labels on marks over a separate legend.

**Repeated grammars.** A repeated metric rail / KPI stack renders its full
grammar on every item: if the pattern is `value + label + context`, every item
shows all three with adequate contrast against its background. No blank value
slots, no same-colour-on-background text.

**Tables & matrices.** Preserve row/column grammar under thumbnail review:
headers, baselines, alignment, and emphasis stay visually consistent.

**Preview overrides the script.** A preview-visible defect — an orphan label, a
missing value in a repeated pattern, a marker on top of copy, anything that
looks accidental at full size — is a build failure even when export and layout
checks pass silently.

**Simpler beats patched.** If a chart or diagram needs many exceptions to stay
clear, rebuild it as a simpler visual rather than patching around geometry
defects.

## Native-chart caveats (python-pptx / Slides)

- Try the native chart first when the API can express it cleanly.
- Do not fake per-point bar colours with hidden zero-valued helper series. If a
  native chart can't express the visual cleanly, rebuild it with editable shapes
  and direct labels, or render it as an embedded image.
- For lines / trends / connected series, prefer a verified native line chart; if
  authored from primitives, draw one continuous polyline through the data
  points — never a stack of short rotated segments.
- Some chart-styling calls are fragile across export engines (e.g. styling
  gridlines on certain python-pptx versions). Verify on a fresh render before
  relying on them; otherwise author the chart from shapes or as an image.
- Record the chart-construction choice (native / authored shapes / image) in the
  QA ledger.

## Decoration ban

Do not introduce decorative custom SVGs, blobs, badges, ornaments, or icon-like
shape stacks that encode no data, hierarchy, or verified brand identity.
Editable primitives are for charts, diagrams, and abstract product flows — never
a licence to fabricate brand marks or fill whitespace. In template-following or
targeted-edit, do **not** strip inherited source-deck decoration merely because
it is decorative; preserve the source's chrome.
