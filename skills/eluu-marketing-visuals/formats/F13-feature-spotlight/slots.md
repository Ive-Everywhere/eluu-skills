# F13 — Feature spotlight (exaggerated component)

## Semantic pattern: **Point at ONE feature**
Show a real UI surface, then scale ONE control far beyond its real size and pop it out over the
card edge (T11) so the eye goes straight to the feature being announced. Use for "introducing X".

## Technique introduced: **T11 — Exaggerate / pop-out**
Take a component in its real place, scale it ~2.5–3×, lift it above the card (float shadow) and
let it break the card boundary. Optional concentric pulse rings for an "active" control. This is
the highlight move — one exaggerated element, everything else at true scale.

## Slots
| Slot | Role | Emphasis |
|------|------|----------|
| `{surface}` | the real UI (here: chat composer) | true scale, calm |
| `{state}` | the live state line (here: "Listening…") | small, muted |
| `{content}` | what's happening (transcribed text + interim greyed + caret) | body 400, interim in `--ink-soft` |
| `{hero-control}` | the ONE exaggerated component (T11) — the waveform mic | **2.8× + popped out + pulse rings** |

## Exports (voice typing)
- `exports/voice-typing-social.png` — **social** version (`social.html`): uses the **REAL in-app
  composer** (harness export, `composer-real.png`) + exaggerated mic in its place + the
  "Introducing / Voice typing" headline in Mercury type. This is the canonical version.
- `exports/voice-mode-email-hero.png` — **email-hero** version (`email.html`, ~2.33:1), same REAL
  composer, no headline (email copy carries the message, rule 11). (`template.html` = the original
  hand-built draft, kept only for reference — do not ship.)

## Component sourcing (learned the hard way)
The composer is **not hand-built** — it's the real `new-chat` screen's composer, captured with
`toolkit/render.py` element mode: load `designs/products/new-chat/screen.html`, `js_step` sets the
textarea value + tags the composer `id="cap"`, element-screenshot `#cap`. `render.py inline_images`
then embeds that PNG into the composition. Real components only (CATALOGUE rule 10).

## Attention audit (recorded)
- **Eye-path:** (1) exaggerated waveform mic → (2) the transcribed text being "spoken" → (3) "Listening…" state.
- One focal (the mic) ✓ · exaggeration + rings carry the emphasis ✓ · interim-grey sells "voice" ✓
- Core info only ✓ (no label needed — the email headline names the feature) · Inter 400/480, measured ✓

## Variants
Any single control: a Send/Run button, a new toggle, a "Schedule" control, an integration button.
Keep exactly one exaggerated element; the rest of the surface stays true-scale and quiet.

Render: `python3 render.py formats/F13-feature-spotlight/template.html --w 1600 --h 760 -o captures/f13.png`
