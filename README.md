# Eluu Skills

Open, ready-to-use skills for [Eluu](https://eluu.ai) agents. Each folder is one skill. Attach a skill to an agent by pasting its GitHub URL into the agent's *Abilities → Skills* section, or by asking the agent:

> Add the `create-handoff` skill from `https://github.com/Ive-Everywhere/eluu-skills` to yourself.

The agent will pull it in and the skill is available immediately, both implicitly (when you describe a matching task) and explicitly via `/` in the chat.

## What's in here

### Long-running sessions

Keep one session sharp across many large sub-tasks. See the [Handoffs technique](https://docs.eluu.ai/techniques/handoffs) for the full pattern.

| Skill | What it does |
|---|---|
| [`create-handoff`](./create-handoff) | Write a handoff document to the hard disk capturing goal, progress, next steps, and decisions. Use before `/compact`. |
| [`resume-handoff`](./resume-handoff) | Read the most recent handoff and re-establish context after `/compact` so the agent can keep going. |

### Decks & presentations

| Skill | What it does |
|---|---|
| [`presentations`](./presentations) | Build high-craft, **editable** decks, either a PowerPoint `.pptx` or a native Google Slides document, for investor and board decks, launches, operating reviews, and finance stories. Ships a python-pptx grid engine, a Google Slides API assembler, a matplotlib chart kit, and an automated layout-quality gate. |

### Spreadsheets & documents

| Skill | What it does |
|---|---|
| [`spreadsheets`](./spreadsheets) | Build `.xlsx` and Google Sheets that look professionally made: real number formats, freeze panes, sized columns, restrained fills, structural borders, conditional formatting and native charts. Builds the workbook locally, renders it to check the layout, then imports it as a native Google Sheet so the formatting survives. |
| [`pdf`](./pdf) | Read, create, render and visually verify PDFs where layout matters, including fillable AcroForms. Renders every page to PNG and inspects it before delivery, and for forms adds a structural check because a clean render can still hide stale field data. |

### Explaining and exploring

| Skill | What it does |
|---|---|
| [`visualize`](./visualize) | Build a self-contained interactive visualization, simulation, chart or mockup to show how something works, what changes when an input moves, or how two things compare. |

### Reusable templates

| Skill | What it does |
|---|---|
| [`template-creator`](./template-creator) | Turn a reference document, deck or spreadsheet into a reusable template skill, so later work inherits its structure and styling instead of being rebuilt each time. |

## How skills work in Eluu

A skill is a packaged workflow attached to an agent. Once attached, the agent runs it the same way every time: the steps, the checks, the output shape, all consistent. Read the [Skills documentation](https://docs.eluu.ai/colleagues/skills) for the full picture.

## Requirements

Some skills need packages or binaries in the agent sandbox. Each `SKILL.md` ends with a `## Requirements` section listing what it uses. In short:

| Skill | Needs |
|---|---|
| `spreadsheets` | `openpyxl`, LibreOffice (`soffice`) and Poppler (`pdftoppm`) for layout checks and formula recalculation, Drive and Sheets integrations for Google output |
| `pdf` | `reportlab`, `pdfplumber`, `pypdf`, Poppler (`pdftoppm`, `pdfinfo`) |
| `visualize` | Python 3, no external services |
| `template-creator` | Node.js, Drive integration for Google sources |

## Contributing

PRs welcome. Each new skill is one folder containing a `SKILL.md` file with YAML frontmatter (`name`, `description`) followed by the instructions. Look at the existing skills for the shape.

## License

MIT, with two exceptions.

- [`presentations`](./presentations) is Apache-2.0. See [`presentations/LICENSE`](./presentations/LICENSE) and [`presentations/NOTICE`](./presentations/NOTICE).
- [`spreadsheets`](./spreadsheets), [`pdf`](./pdf), [`visualize`](./visualize) and [`template-creator`](./template-creator) are adapted for the Eluu agent harness from published Codex output skills. They are provided as-is, and Eluu makes no additional licence grant over them.
