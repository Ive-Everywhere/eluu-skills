---
name: agentic-diagnosis
description: Diagnose where agents and apps would help a person and their team. Maps the team's pipeline from connected tools and past work, finds the gaps, and delivers a simple report: the workflows agents can run in priority order, the agents and apps for each team, and the outcome and metric for each one. Use when the user asks "where can agents help us", "what should I automate", "suggest agents and apps for my team", "diagnose my pipeline", "what agents should my team have", or asks for an AI plan for a department.
argument-hint: "<team, department or pipeline to diagnose, or 'me and my team'>"
---

# Agentic Diagnosis

Find the gaps in how a team's work moves. Deliver one short report: the workflows agents can run, in priority order, with the agents and apps each team needs and the outcome each workflow should produce.

This skill suggests. It does not build agents, create apps, send messages or change any record. Building starts only after the person picks from the report.

## Rules

1. **Evidence before suggestions.** Every workflow cites what it is based on: a tool record, a past session, a scheduled job, a file, or the person's answer. A workflow with no evidence is labelled `Guess` and ranks below every evidenced one.
2. **Read only.** Use connected tools to read. Do not write, send, enrol, post or edit anywhere during a diagnosis.
3. **No invented numbers.** A metric shows today's value only when you read it from a tool. Otherwise write "not measured". A rule or threshold is not a count. A target needs a basis you can name (the team's own goal, or the definition of done). Otherwise write "to agree". Never state money or hours without the arithmetic.
4. **Gap first, agent second.** Start from the work and the goal, find the gap, then pick or design the agent. Use the catalogue as a checklist, not as a list to copy.
5. **Look for work that is not done, not only work that is slow.** Part B of `references/gap-types.md` is required.
6. **Each workflow is a whole job, not a chat bot.** It has a trigger, the agent's steps, the person who approves, and a result. Name it for the work it does (Launch Desk, Reply Desk).
7. **Name tools by class.** Write CRM, support desk, call recorder. Add the team's own product in brackets only when you read it from the workspace.
8. **No head agents.** Do not suggest an orchestrator or an agent that runs other agents. A manager gets an app and is the reviewer.
9. **Every agent has an app and a reviewer.** Anything that leaves the company is drafted by the agent and approved by a named person.
10. **Ask at most 5 questions, once, and wait.** Do not skip this because you are in an automatic mode.
11. **People and roles need evidence too.** A team, role or manager you did not read or hear about is a `Guess`. Do not build an org chart from what is typical.
12. **Keep it simple.** Short names, one line per cell, plain words. No section the template does not have. Do not name yourself, another agent or the session in the report.

## Workflow

### 1. Set the scope

Name the scope in one line: the person, the team or teams, and the pipeline (for example "outbound to closed deal"). With no scope given, use the person's own role and the teams they manage.

### 2. Read what exists (tools first)

Read in this order and note the source of every fact:

1. Memory and files: role, team members, goals, existing agents and jobs.
2. Past sessions and scheduled jobs: what the person already asks agents to do, and what they redo by hand.
3. Connected tools: the system of record for the pipeline, then email, calendar and chat.
4. Existing agents and apps, so you do not suggest something that already exists.

List which tools you could read and which you could not.

### 3. Draw the pipeline map

Write the pipeline as stages in order. For each stage note who does it today, where it is recorded, the volume, and what moves it on.

### 4. Ask what the tools could not answer

Show the draft map in a few lines, then ask up to 5 short questions in one message: who is on each team, what each pod or role owns, which stage worries the person most, who approves external actions, and one question about work the team does not do today. **Stop here and end your turn.** Continue only after the answers.

With no person present (a scheduled run), skip the questions, say so in the report, and label as `Guess` everything the answers would have settled.

### 5. Find the gaps

Make two passes with `references/gap-types.md`:

1. **Fix gaps (Part A):** work that is slow, manual, dropped or uneven.
2. **New work gaps (Part B):** work nobody does today. Count the absence where you can.

Keep the biggest gaps per team. Where a new work gap exists for a team, include at least one.

### 6. Turn each gap into a workflow

For each gap write:

- **Workflow:** a short name, and one sentence in this shape: "When [trigger], the agent [does the work]. [Person] [approves or acts]."
- **Agent:** which agent runs it. One agent can run several workflows. Mark it `personal` (one per person) or `team` (shared). See `references/patterns.md`.
- **App:** the page the team opens to see and act on the work. One shape: tracker board, approval queue, metrics dashboard, document review, run log, or reconciliation.
- **Reviewer:** the named person or role who approves and is accountable.
- **Outcome and metric:** what changes, the one number that shows it, today's value, and the target (rule 3).
- **Based on:** the evidence, or `Guess`.
- **Needs first:** access or decisions required before it can start.

Use `references/catalogue.md` to name agents and apps and to check coverage.

### 7. Group by team

Group the agents the way the people are grouped: one set per manager or pod. For each team list its agents, the workflows each one runs, the apps, the reviewer, and the AI plan (see "Plans and billing" in `references/patterns.md`).

### 8. Rank

Rank every workflow on value (cost of the gap) and ease (tools connected, one owner, low risk). Evidenced workflows first, every `Guess` after them. Mark exactly three to start first. A prerequisite such as connecting a tool is not a workflow: put it under "Needed first".

### 9. Deliver the report

Write one self-contained HTML file from `assets/report-template.html`. Replace every placeholder, repeat the rows, delete the comments. Save it in the workspace root folder `reports/` as `agentic-diagnosis-<team>-<date>.html`. This path overrides any other rule you have about where task files go.

The report has four parts and nothing else:

1. **Top:** one sentence on what was diagnosed, and the three workflows to start first.
2. **Workflows in priority order:** one table. Rank, workflow, team and reviewer, outcome and metric, based on.
3. **Agents and apps by team:** one small table per team. Agent, the workflows it runs, the app.
4. **Basis:** what was read, what was not, the guesses, and what is needed first.

In chat, reply with the three workflows to start. Then ask which ones to build.

### 10. Write back

Save to memory: the scope, the pipeline map, the top gaps with their evidence, and what the person chose.

## Quality bar (check before delivering)

- The questions were asked and answered before the report was written, or the report says no person was present.
- Every workflow cites its evidence or is labelled `Guess`. No `Guess` ranks above an evidenced workflow.
- Exactly three workflows are marked to start first.
- Both gap passes were made.
- No number is invented. No rule or threshold is shown as a count. Targets have a basis or say "to agree".
- Every workflow has a trigger, an agent, an app, a reviewer and a metric.
- Tools are named by class. No head agents. No invented roles.
- No suggested agent or app already exists on the workspace.
- The report has only the four parts, one line per cell, no placeholder or comment left.
- Nothing was written, sent or changed during the diagnosis.

## Requirements

Python: none
System: none. The report is one self-contained HTML file. It loads the Instrument Sans font from Google Fonts at view time and falls back to the system font without network access.
Integrations: none required. The diagnosis is better with read access to the team's system of record (for example the CRM), email, calendar and chat. It never writes to them.
