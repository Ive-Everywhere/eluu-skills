# Patterns for teams of agents

Use these when you design the answer for a gap and when you group agents into teams.

## Personal agent or team agent

| Use a personal agent when | Use a team agent when |
|---|---|
| The work depends on one person's own accounts, inbox, calendar or network | The work runs on shared records |
| The output is in that person's voice and they must approve each item | The output is the same whoever reads it |
| Each person has a different book of accounts or territory | One queue serves the whole team |

A team usually needs both: one personal agent per person for their own outreach and preparation, and one or two team agents for the shared pipeline.

## Pattern: personal agent with a daily review queue

One agent per person. It works from that person's own accounts overnight or through the day and fills one queue. The person reviews the queue once a day and approves, edits or rejects each item. Nothing leaves without that approval.

Example for a business development rep:

- **Agent:** personal outreach agent. It reads the rep's LinkedIn activity (new connections, profile views, posts and job changes in their accounts), matches each signal to an account in the CRM, and drafts an email for each one.
- **Trigger:** daily, plus any new signal on a named account.
- **App:** approval queue. One row per draft: the person, the signal that triggered it, the draft, and Approve, Edit or Skip.
- **Human handler:** the rep reviews their own queue each morning. The manager sees approval rate and replies across the pod.
- **Metric:** replies per approved email, and drafts approved without edits.
- **Stop:** no more than a set number of touches per person with no reply.
- **Check before suggesting:** the rep's own LinkedIn session is needed, and automated browsing is limited by LinkedIn's terms. State this as a need and let the person decide.

The same pattern fits an account manager (renewal and expansion signals), a recruiter (candidate signals) and a support lead (accounts going quiet).

## Pattern: agent team per manager

Mirror the org chart. Each manager or pod lead owns one agent team:

- One personal agent per person in the pod.
- One or two team agents for the pod's shared work (pipeline hygiene, weekly numbers, handovers).
- One shared app where the manager sees every agent's output, the approvals waiting, and the pod's numbers.

The manager is the human handler for the team agents and sees the results of the personal ones. A leader above several managers gets a roll-up app, not more agents. There is no agent at the head of an agent team.

## Plans and billing

A team can connect more than one AI subscription, so each agent team can run on its own plan. That keeps cost and responsibility with the same manager.

Suggest the simplest setup that covers the load:

- One or two model subscriptions per manager, shared at team level, so billing sits with the manager and not with each person.
- Add a second subscription when the pod's agents run at the same hours or when one heavy job (large research batches) would use up the limit for everyone.
- State which agents share which subscription, and name the heavy jobs to schedule outside working hours.

Do not quote prices or limits unless you read them from the workspace's own plan settings.

## Handovers between agents

Where one agent's output is another's input, name the record that carries it (a CRM field, a row in the app, a file). Put a person between two agents whenever the first agent's output can cause an external action by the second.

## What not to suggest

- A head agent: an orchestrator, a manager agent, or any agent whose job is to run or supervise other agents. The manager is a person. Give them an app.
- An agent for work that happens less than once a month. Suggest a saved prompt.
- An agent that needs a tool the team does not have and will not buy.
- An agent whose only reviewer is the person who is already the bottleneck, unless the review is much shorter than the work it replaces.
- Two agents writing to the same record with no owner for conflicts.
