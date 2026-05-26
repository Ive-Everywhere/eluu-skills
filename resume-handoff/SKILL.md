---
name: resume-handoff
description: Use right after running /compact in a long session, to read the most recent handoff document and re-establish enough context to continue the next sub-task.
---

# Resume Handoff

## Overview

After `/compact`, the older conversation has been collapsed into a summary. The handoff document on the hard disk is the authoritative source for what was decided and what's next. Read it, confirm understanding with the user, then continue the work.

**Announce at start:** "I'm using the resume-handoff skill to pick up from the most recent handoff."

## When to use

Use this when:

- The user just ran `/compact` and wants to continue the same job.
- The user has explicitly asked to resume from a handoff.
- A session has started fresh but a handoff document exists for the work you're being asked to continue.

## The process

### Step 1: Find the handoff

Look on the hard disk for the most recent file named `handoff-YYYY-MM-DD-HHMM.md`. If a plan document exists alongside it, note that too.

If multiple handoffs exist, take the latest one by timestamp. If none exists, stop and tell the user — don't guess.

### Step 2: Read and reconstruct

Read the handoff in full. Build a mental model of:

- The overall goal.
- What's been done and what hasn't.
- The decisions and preferences the user has already locked in.
- The exact next sub-task.
- Any open questions still owed an answer.

### Step 3: Confirm before continuing

Report back to the user in this exact shape — nothing more, nothing less:

```
Resuming from <filename>.

**Goal:** <one sentence>
**Done:** <comma-separated sub-task names>
**Next:** <next sub-task in one line>
**Open questions:** <list, or "none">

Ready to continue with <next sub-task>? Or do you want to adjust first?
```

Then **wait** for the user to confirm or redirect. Do not start the next sub-task until they reply.

### Step 4: Continue

Once confirmed:

- Honour the decisions and preferences from the handoff.
- Reference completed work by file rather than re-deriving it.
- If the next sub-task is itself large, plan to write another handoff at the end of it and prompt the user to `/compact` again.

## Remember

- **The handoff is authoritative.** If the compacted summary and the handoff disagree, trust the handoff.
- **Confirm before doing.** It's easy to misread a handoff and start the wrong sub-task. The confirm step is cheap and prevents wasted work.
- **Don't re-paraphrase the whole handoff back.** The user wrote it (or asked you to). Summarise to the four-line shape above and move on.
- **If anything is missing or unclear,** ask the user before continuing. Don't fabricate context.

## Pairs with

- [`create-handoff`](../create-handoff) — writes the handoff this skill reads.
