# Eluu Skills

Open, ready-to-use skills for [Eluu](https://eluu.ai) colleagues. Each folder is one skill. Attach a skill to a colleague by pasting its GitHub URL into the colleague's *Abilities → Skills* section, or by asking the colleague:

> Add the `create-handoff` skill from `https://github.com/Ive-Everywhere/eluu-skills` to yourself.

The colleague will pull it in and the skill is available immediately, both implicitly (when you describe a matching task) and explicitly via `/` in the chat.

## What's in here

### Long-running sessions

Keep one session sharp across many large sub-tasks. See the [Handoffs technique](https://docs.eluu.ai/techniques/handoffs) for the full pattern.

| Skill | What it does |
|---|---|
| [`create-handoff`](./create-handoff) | Write a handoff document to the hard disk capturing goal, progress, next steps, and decisions. Use before `/compact`. |
| [`resume-handoff`](./resume-handoff) | Read the most recent handoff and re-establish context after `/compact` so the colleague can keep going. |

### Decks & presentations

| Skill | What it does |
|---|---|
| [`presentations`](./presentations) | Build high-craft, **editable** decks — a PowerPoint `.pptx` or a native Google Slides document — for investor/board decks, launches, operating reviews, and finance/metrics stories. Ships a python-pptx grid engine, a Google Slides API assembler, a matplotlib chart kit, and an automated layout-quality gate. |

## How skills work in Eluu

A skill is a packaged workflow attached to a colleague. Once attached, the colleague runs it the same way every time — the steps, the checks, the output shape, all consistent. Read the [Skills documentation](https://docs.eluu.ai/colleagues/skills) for the full picture.

## Contributing

PRs welcome. Each new skill is one folder containing a `SKILL.md` file with YAML frontmatter (`name`, `description`) followed by the instructions. Look at the existing skills for the shape.

## License

MIT, except the [`presentations`](./presentations) skill, which is Apache-2.0 (see [`presentations/LICENSE`](./presentations/LICENSE) and [`presentations/NOTICE`](./presentations/NOTICE)).
