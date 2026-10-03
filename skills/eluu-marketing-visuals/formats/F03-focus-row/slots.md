# F03 — Focus row via blur

## Semantic pattern: **Spotlight — one in focus, many in breadth**
Use when the message is "notice THIS one, and know there are more." A single list card; the
focal row is sharp + tinted with a status pill; siblings are blurred (T3) so they read as
breadth without competing.

## Slots
| Slot | Role | Emphasis |
|------|------|----------|
| `{title}` + `{count}` | list header | strong title, muted count |
| `{rows[]}` = {avatar, name, meta, right} | the set | breadth |
| `{focusIndex}` | the one row to spotlight | **sharp + `--focus` tint + status pill** |

## Attention audit (recorded)
- **Eye-path:** (1) focus row (sharp + tinted + "On shift" pill) → (2) blurred roster as breadth.
- One focal ✓ · blur dial on siblings ✓ · the status pill answers "why is this one focal" ✓
- One rounding/type scale ✓ · core info only ✓ (role, not a paragraph).

## Variants (swap subject, keep exactly one sharp row)
Colleague roster (shown) · integrations list (one just-connected) · jobs list (one running now) ·
activity feed (one event highlighted) · inbox (one message that matters).

Render: `python3 render.py formats/F03-focus-row/template.html -o captures/f03.png`
