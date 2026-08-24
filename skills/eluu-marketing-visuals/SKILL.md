---
name: eluu-marketing-visuals
description: >-
  Produce premium, Mercury-grade product-illustration images for social, website, and
  email — clean HTML/CSS/SVG rendered to PNG (never AI art). Use whenever you need a
  marketing visual, hero illustration, social post image, email hero, OG/share image,
  or feature-announcement graphic for an Eluu product. Compose a self-contained HTML
  file, render it to PNG with headless Chromium, then run a critic pass against the
  design laws and iterate.
---

# Eluu Marketing-Visual System

The playbook for premium product illustrations, deconstructed from 17 Mercury reference
compositions. Everything is **HTML/CSS/SVG rendered to PNG** through your own sandbox —
not AI art, not screenshots of a screenshot tool. This skill is self-contained: it needs
only Python + Playwright + Chromium, which you install below. It does NOT depend on any
external render service, harness, or capture tool.

## When to use
"make a social post image", "hero illustration for the website", "email hero graphic",
"OG / share image", "announce feature X visually", "premium product illustration".

## 0. Setup (once per sandbox)
The sandbox wipes pip installs between sessions, so run this at the start of a design task:
```
pip install playwright
playwright install chromium
```

## 1. The 6-layer model
Every composition decomposes into stacked layers, back → front. One image, one job.

| # | Layer | What it does |
|---|-------|--------------|
| 1 | **Canvas** | Tinted "paper" background + fine grain + soft top-light vignette. Never pure white. |
| 2 | **Context** | De-emphasized UI that sets the scene (blur / fade / grey). |
| 3 | **Focal** | 1–3 crisp components carrying the message. Exactly ONE clear hero. |
| 4 | **Connective** | Thin grey lines + elbows + node dots/arrows showing flow. |
| 5 | **Annotation** | A quiet pill label (icon chip + word) + muted subtitle; captions. |
| 6 | **Frame** | Device chrome (iOS / browser / MacBook) OR a bleed-crop off the edge. |

**Design law — one focal point.** Everything not focal must be pushed back by at least one
de-emphasis dial (T3). Two equally-sharp centered things read as noise.

## 2. Technique primitives (T1–T11)
The reusable toolkit, implemented in `assets/marketing.css`. Load the CSS, set a canvas
variant, build focal components, push everything else back with a dial.

| ID | Primitive | Recipe |
|----|-----------|--------|
| **T1** | Paper canvas | bg tint + fine grain + radial top-light. Variants: cream `#f2efec`, lavender `#eceaf6`, grey `#f3f3f6`. Classes `.mv-canvas--cream/--lav/--grey`. |
| **T2** | Soft elevation | layered box-shadow scale: `.mv-rest` / `.mv-raised` / `.mv-floating`. Low-opacity, large-blur, small-offset — diffuse, never hard. |
| **T3** | De-emphasis (4 dials) | `blur()` · `opacity` · gradient `mask-image` edge-fade · `saturate()` down. Classes `.mv-deemph*`, `.mv-fade-bottom/-right/-radial`. Combine dials; the focal layer keeps all at 0. |
| **T4** | Connector system | inline-SVG rounded-elbow path between two anchors + node dot + optional arrow. 1–1.5px, neutral `#c9c6d0`. Style hooks `.mv-connectors`, `.faint`, `.mv-node-dot`. |
| **T5** | Label motif | icon-pill chip + word + muted subtitle. Classes `.mv-label`, `.mv-label__chip`, `.mv-subtitle`. It captions — it never headlines. |
| **T6** | Device frames | iOS phone (9:41 bar), browser window, MacBook, or frameless bleed. Classes `.mv-phone`, `.mv-browser`. |
| **T7** | Hero product object | the recurring brand object = the Eluu **colleague profile card** (cover band + avatar + name/role + bio + skill chips + connections). Class `.mv-colleague-card`. Design once, reuse everywhere. |
| **T8** | Bleed & crop | a panel deliberately exceeds the canvas edge to imply a larger surface. Pairs with a T3 mask-fade. |
| **T9** | Entity chip / node | icon in a soft tinted circle + label + value. Class `.mv-node`. Category / list rows. |
| **T10** | Grain + lighting | fine noise overlay + top-light gradient across the whole canvas (baked into T1). The "premium" tell; keep it subtle (~3–5%). |
| **T11** | Exaggerate / pop-out | scale ONE component ~2.5–3× and lift it over the card edge (float shadow + optional pulse rings). Spotlight a single feature — the eye goes straight to it. |

### Palette & type discipline (Eluu)
- Focal cards on `#ffffff`, 16–24px radius. Text: strong `#1c1b1f`, sub `#5c5660`, soft `#9a938d`.
- Accent: Eluu maroon `#755a68` (buttons, focal chips, connector nodes).
- Type = **Inter**, using the intermediate weight scale **360 / 400 / 420 / 480 / 530**
  (`--w-*` vars). **480 is the ceiling for emphasis and headings — never 600/700.**
  Body 400 · labels/names 480 · display 480, largest 530.
- **Positive** letter-spacing on display (~0.01–0.02em); wide-set, architectural.
- Line-height: display 1.1–1.2, body 1.35–1.5. Never raw Mercury blue/purple except inside a
  literal product screenshot.

## 3. Pick a format
Each format = a layer recipe + named slots. Recipes live in `formats/<Fxx>/slots.md`; the
self-contained ones ship a ready `template.html` you copy and re-fill.

| ID | Name | Best for | Bundled |
|----|------|----------|---------|
| **F02** ★ | Hero + connector map (Input→Processor→Outputs) | flow story: "X in → colleague → results out" | template + slots |
| **F03** ★ | Focus-row via blur (Spotlight) | "notice THIS one among many" | template + slots |
| **F13** | Feature spotlight (Exaggerate one control) | "introducing X" — point at one feature | slots (recipe) |
| F01 | Dual-device showcase | feature pair / before-after | — |
| F04 | Two surfaces linked | integration / data flow | — |
| F05 | List + floating detail panel | "click a row → see detail" | — |
| F06 | Notification + resolution | alerts, guardrails | — |
| F09 | Conversation proof | receipts, agent replies | — |
| F11 | Single hero device | minimal, app-store style | — |
| F14 | UI-card collage | "the whole platform" hero | — |

★ = start here. **F02** is the benchmark; **F03** is the workhorse.

Picking heuristic: is the story a **flow** (something enters, the colleague acts, results
leave)? → F02. Is it "**one item matters among a set**"? → F03. Is it "**announce a single new
control**"? → F13. Otherwise map your idea onto the closest recipe above.

**Export aspects** (author once, re-render per aspect): OG `1200×630` · square `1080×1080` ·
portrait `1080×1350` · email hero `1120×480` · wide `1600×900`. Author at 2× and downscale on
export; keep a per-format safe margin so the focal element survives every crop.

## 4. Step-by-step (the maker loop)
1. **Classify** the request: channel (social / website / email) + aspect + the ONE message.
2. **Pick a format** (§3). Copy the bundled `formats/<Fxx>/template.html` as your start, or
   author a new self-contained HTML file when no template exists.
3. **Compose a self-contained HTML file.** Link the bundled CSS with a relative path:
   `<link rel="stylesheet" href="../../assets/marketing.css">` (relative to the file), OR
   inline just the classes you need inside a `<style>` block so the file stands alone. Wrap
   the whole composition in `<div class="mv-stage" id="stage">…</div>`, start with a
   `.mv-canvas` layer, then add focal components and push context back with T3 dials.
4. **Render to PNG** with the self-contained script:
   ```
   python3 render.py path/to/composition.html -o captures/out.png
   # per aspect, e.g. OG:  --w 1200 --h 630   square: --w 1080 --h 1080
   ```
   It shots the `#stage` element at 2× via headless Chromium.
5. **Critic pass** — run the Attention Audit (§5) against the rendered PNG. Squint at it.
6. **Iterate** — fix the first failing rule with a T-dial, re-render, re-audit. Ship only when
   every rule passes.

## 5. Critic pass — the Attention Audit (run on EVERY image)
The image works only if the eye lands where you intend, in the order you intend.
1. **State the eye-path** in one line: `1 → 2 → 3` (focal → coherent line → breadth/context).
2. **Squint test.** View the thumbnail. The focal element must still dominate. If two things
   compete, push one back with a T3 dial.
3. **One coherent line.** Exactly one full-emphasis path (e.g. input → hero → one output).
   Everything else is de-emphasized breadth.
4. **Dials point one way.** Focal = highest contrast + largest size + full sharpness + full
   opacity + on-brand accent. Context gets the opposite on every dial.
5. **Annotations recede.** Labels/captions/pills sit BELOW the focal object in weight and colour.
6. **One rounding + shadow + type scale** across all components.
7. **Real logos for real brands.** Use the actual logo (inline SVG, brand colour) — never a
   generic glyph, never a remote CDN.
8. **Core information only.** Every word/element must add information. Cut redundancy; make
   vague specifics concrete ("Connected to your stack" → "4 integrations connected").
9. **Subject commands the frame.** The focal object fills ~55–70% of width for a single-card
   hero, with tight even margins. No object marooned in whitespace.
10. **Real components only.** Any real app UI must come from an actual screenshot of the running
    product — never a hand-built lookalike. Only marketing-native props (paper canvas,
    connectors, headline, the exaggerated highlight) are yours to draw. NOTE: formats that need
    real app UI (F13, F14, F05, …) require you to supply the product screenshot from your own
    sandbox; the bundled F02/F03 templates are pure marketing-native CSS and need no app.
11. **Marketing text only when asked.** Add headlines/labels only when explicitly requested.
    Email/website images rely on their own surrounding copy — keep them clean.

## 6. Growing the catalogue (deconstruction protocol)
To add a new look from a reference: (1) classify channel/aspect/purpose; (2) segment into the 6
layers; (3) name the single focal element and its de-emphasis dials; (4) map each layer to T1–T11
(mint a new Tn with a recipe if a technique is missing); (5) match an existing Fxx or mint a new
one with a slots recipe; (6) file the reference with a short note. The catalogue only grows through
this protocol, so every entry is traceable and expressed in shared primitives.

## Files in this skill
- `assets/marketing.css` — the T1–T11 technique toolkit (load or inline this).
- `render.py` — self-contained HTML→PNG renderer (Playwright + headless Chromium).
- `formats/F02-hero-connector/` — benchmark template + slots recipe.
- `formats/F03-focus-row/` — workhorse template + slots recipe.
- `formats/F13-feature-spotlight/` — exaggerate/pop-out recipe (needs a real app screenshot).
