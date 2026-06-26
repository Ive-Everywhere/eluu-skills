# Design-system lock

Lock these before writing a single slide. The point is consistency you can
defend at thumbnail size — one system, not eleven one-off slide sculptures.

**Canvas & grid.** Fix the size (1280×720 px for PPTX, 720×405 pt for Slides),
margins, a 12-column grid with a defined gutter, and an 8-unit baseline. Put the
action title and a hairline rule at the *same* baseline on every content slide.

**Background system.** Usually two surfaces: a light "paper" for content and a
dark "ink" for cover, section, and closing slides. Alternate them for rhythm.
Avoid default pale-dashboard backgrounds and generic gradients.

**Palette — three colours, with rules.** A neutral/base, one accent, and one
support colour. Decide what each *means* (e.g. accent = the load-bearing object /
the future; support = context / the status quo) and use it only that way. Don't
let one colour dominate without a deliberate contrast. Never use colour as pure
decoration.

**Type — one pairing.** A display/headline face and a utilitarian face for
labels; optionally a mono for kickers and technical tags. Use real, installed (or
embeddable) families. For PPTX, embed them; for Google Slides, use real Google
Fonts names. Suggested readable ranges (px, scale for pt): cover/section claims
56–72, slide titles 34–52, body 18–26, table/chart labels 12–16, kicker/source
9–12.

**Kicker grammar.** A small accent marker + a letter-spaced, all-caps mono label,
optically centred on one line. Name the pair `kicker-marker` / `kicker-label` so
the layout gate can verify their centres line up.

**Chart grammar.** Direct labels on marks; no separate legend where a label
works. Values in the label face; state units once. The chart proves one
sentence — the slide's title.

**Diagram & connector grammar.** A small recurring kit of node, lane, and
connector shapes. Connectors attach to the objects they relate and only carry an
arrowhead when direction is meaningful. Boxes imply a real grouping; equal-role
boxes share exact height, padding, and treatment.

**Container grammar.** Hairline rules over boxes for separation. Use a filled
container only when it encodes a real group/lane/stage. Minimum interior padding
~12px single-line, ~16px multi-line or on dark fills. No decorative boxes around
prose; no rounded cards as default scaffolding.

**Footer / source / page-marker grammar.** One footer system, identical on every
content slide: brand mark, source line, and an `NN / NN` page marker. Don't let
it drift between slides.

**Banned motifs.** Feature-card grids as a default; teal/navy/purple SaaS
gradients; decorative icons or badges; drop shadows as decoration; any fabricated
metric, logo, or source.

Write all of this down (a short `design-system.txt`) before building, and a
`contact-sheet plan` listing the macro layout for each slide — at least five
distinct families across a ten-slide deck, with no three consecutive slides
sharing one.
