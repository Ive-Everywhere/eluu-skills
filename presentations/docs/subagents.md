# Subagents

Decks are mostly a single-author craft — one mind owning the story and the
visual system produces a more coherent deck than a committee. So the default is
to build solo. Reach for subagents only when the work is genuinely
parallelisable and well-scoped, or when the user asks for them.

## Good uses

- **Source-metric extraction** — one agent reads the filings/IR materials and
  returns a clean `data.json` of exact figures and source dates, while you design.
- **Reference-deck critique** — one agent scores a supplied reference deck
  slide-by-slide so you know precisely where to beat it.
- **Final QA inspection / scoring** — an independent agent runs the comeback
  rubric and the layout gate on the rendered deck and reports findings, catching
  what the builder's eye has gone blind to.
- **Appendix implementation from a fixed spec** — once the appendix's tables and
  sources are fully specified, a worker can implement them in parallel.
- **Alternate prototype** — a second agent builds a different take on the
  hardest slide in a separate workspace, so you can pick the stronger one.

## The boundary

The main agent always owns the **final story, the visual system, integration,
and QA**. Subagents return data, critiques, or isolated slides — never the final
deck. Never ship a raw stitched deck assembled from independent slide workers:
without one owner enforcing the system, the contact sheet fragments into a
template pack.

## How to brief one

Give a subagent a closed, verifiable task: the exact inputs, the exact output
shape (a JSON schema, a scored rubric, a single slide module), and the
constraints. Vague briefs ("make some slides about X") produce work you have to
redo. The more the brief looks like a spec, the more useful the result.
