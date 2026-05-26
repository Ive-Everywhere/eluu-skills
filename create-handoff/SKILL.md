---
name: create-handoff
description: Use when wrapping up a large chunk of work in a long session, just before running /compact, so the next stage of the same session can pick up without losing context.
---

# Create Handoff

## Overview

Write a handoff document to the hard disk that captures everything a future stage of this session (or a fresh reader) needs to keep going. The handoff is the one artifact that survives `/compact` and lets the work continue without re-explaining.

**Announce at start:** "I'm using the create-handoff skill to write a handoff document before we compact."

## When to use

Use this when:

- A large sub-task has just finished and the next one is about to start.
- The session has been running long enough that earlier details are starting to blur.
- The user has asked for a handoff, or is about to run `/compact`.

Do **not** use this for short sessions or one-off asks — it's overhead the work doesn't need.

## What goes in a handoff

A handoff document is short, structured, and stands alone. It includes:

1. **Goal** — the one-sentence reason this session exists.
2. **Plan** — the named sub-tasks, with status for each (done, in progress, not started).
3. **What's complete** — a bullet per finished sub-task with a one-line outcome and links to any files produced on the hard disk.
4. **What's next** — the next sub-task in plain language: what to do, where the inputs live, what the output should look like.
5. **Decisions & preferences** — anything the user clarified mid-session that the next stage needs to honour. Things like tone choices, naming conventions, files to avoid, sources to prefer.
6. **Open questions** — anything unresolved the user still owes an answer on.

## The process

1. Re-read the session history. Identify the goal, the plan, what got done, what's next.
2. Save the handoff to the hard disk as `handoff-YYYY-MM-DD-HHMM.md` (UTC). If a plan document already exists for this session, save the handoff alongside it.
3. Use this structure exactly:

```markdown
# Handoff — <session goal in one line>

*Created: <YYYY-MM-DD HH:MM UTC>*

## Goal

<One sentence.>

## Plan status

- [x] <Sub-task 1>
- [x] <Sub-task 2>
- [ ] <Sub-task 3> ← next
- [ ] <Sub-task 4>

## What's complete

- **<Sub-task 1>** — <one-line outcome>. <link to artifact if any>
- **<Sub-task 2>** — <one-line outcome>. <link to artifact if any>

## What's next

<Plain-language description of the next sub-task. Include inputs, expected output, and where to save it.>

## Decisions & preferences

- <Decision 1 — short reason>
- <Decision 2 — short reason>

## Open questions

- <Question still owed an answer, or "None.">
```

4. After saving, tell the user three things and nothing else:
   - The filename.
   - The next sub-task in one line.
   - This exact line: *"Ready to `/compact`. After it finishes, run `/resume` (or ask me to resume from the handoff)."*

## Remember

- **Be specific.** "Drafted the section" is useless. "Drafted the Q3 revenue section, 240 words, saved to `q3-report-draft.md`" is a handoff.
- **Link, don't paraphrase.** If a file already exists on the hard disk, link to it. Don't restate its contents in the handoff.
- **No fluff.** Keep the document under one screen if possible. The whole point is fast pickup.
- **Honour what the user has decided.** If they corrected tone, length, scope, or naming earlier in the session, capture it in *Decisions & preferences* so the next stage doesn't redrift.

## Pairs with

- [`resume-handoff`](../resume-handoff) — reads the handoff after `/compact` and re-establishes context.
