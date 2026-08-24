# F02 — Hero object + connector map

## Semantic pattern: **Input → Processor → Outputs**
A flow/pipeline story. A trigger (input) enters a central actor (the processor / hero object),
which fans out to results (outputs). Use whenever the message is "X comes in, the colleague
handles it, these things come out." The hero is always the Processor.

## Slots
| Slot | Role | Emphasis | Example (proof) |
|------|------|----------|-----------------|
| `{input}` | the trigger/source (T9 node, real logo) | focal, crisp | Slack "New request · #ops" |
| `{processor}` | the hero object (T7 colleague profile card) | **the one focal hero** | Riley — Product Manager |
| `{output-main}` | the ONE coherent-line result | focal, crisp | "Metrics review · Mon 8:00 AM" |
| `{output-breadth[]}` | 2+ other results signifying breadth | de-emphasised (opacity ~.42) | "Weekly update", "Month-end recon" |
| `{label}` + `{subtitle}` | quiet caption (T5) | recedes below hero | "Colleagues / One hire runs your whole ops" |

## Layer recipe
Canvas (cream) · Connective (bright path input→processor→output-main; faint branches to breadth)
· Focal (processor + input + output-main) · Context (breadth outputs faded) · Annotation (caption).

## Attention audit (recorded)
- **Eye-path:** (1) Riley profile card → (2) bright line Slack → Riley → Metrics review → (3) faded breadth.
- One coherent line ✓ · dials aligned on hero ✓ · caption recedes ✓ · one rounding/shadow/type scale ✓
- Real logos (Slack, Linear) inlined ✓ · core info only ✓ (no "Autonomous colleague", no card wordmark).

## Variants (same pattern, swap the subject)
- Sources→colleague→channels · Data in→colleague→reports · Ticket→colleague→resolution+notify.
- Reverse it (many inputs → one output) for an aggregation story; keep exactly one bright line.

Render: `python3 render.py formats/F02-hero-connector/template.html --wait 800 -o captures/f02.png`
