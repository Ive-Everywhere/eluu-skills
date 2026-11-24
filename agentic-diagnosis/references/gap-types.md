# Gap types

There are two kinds of gap. Look for both, in this order of effort: the first kind is easy to see and the second is usually worth more.

- **Fix gaps:** work the team does today that is slow, manual, dropped or uneven. Part A.
- **New work gaps:** work nobody does today, so no record of it exists. Part B.

## Part A: fix gaps (work that is done today)

Check every pipeline stage against these eight. Each has a signal you can look for in the tools and a usual answer.

| Gap type | What it looks like | Where to look | Usual answer |
|---|---|---|---|
| Slow | Items wait a long time before the stage starts or ends | Time in stage, time to first response, age of open items | Agent that starts the work when the item arrives, with a queue for the person |
| Manual | A person copies, compiles or reformats the same thing each time | Repeated requests in past sessions, weekly reports built by hand, spreadsheets fed by exports | Scheduled agent that produces it, with a dashboard or run log |
| Dropped | Items leave the stage with no next step, or nobody follows up | Records with no next activity, unanswered threads, stale deals or tickets | Agent that watches for silence and drafts the next step into an approval queue |
| One person | The stage stops when one person is away | One name on every record, one person asked every question in chat | Agent that holds the method, with that person as reviewer instead of doer |
| Not recorded | The work happens but the system of record does not show it | Meetings with no notes in the CRM, decisions only in chat | Agent that records it from the source, with a tracker board |
| No signal | Nobody knows the state until a review meeting | Status asked in chat, numbers assembled before each review | Metrics dashboard fed by a scheduled agent, with alerts on thresholds |
| Quality varies | The same task is done to different standards by different people | Rework, corrections, different formats for the same output | Agent that drafts to one standard, with a document review workspace |
| Two sources disagree | Two tools hold the same fact with different values | Reconciliation done by hand, disputes about which number is right | Agent that compares both and lists the differences in a reconciliation app |

## Part B: new work gaps (work that is not done at all)

The tools hold no record of work that never happens, so you cannot find these by reading activity. Find them by comparing what exists against what the goal needs.

| Gap type | What it looks like | How to find it | Usual answer |
|---|---|---|---|
| Missing step | A step that would raise the result of a stage, and nobody does it | For each stage ask what the best teams do here that this team does not. Check the catalogue for the department | Agent that does the step when the stage starts, and hands the result to the person who owns the stage |
| Missing moment | An event happens in the system of record and nothing follows | List the events the tools record (stage change, job change, renewal date, usage change, a contact leaving). Mark each one that triggers no action | Agent triggered by the event, with an approval queue for anything external |
| Missing channel | A whole route to the goal is not used | List the channels the goal could use (for revenue: outbound, inbound, partners, referrals, events, community, existing customers, search). Mark each with no activity in the tools | A small agent team that runs the channel as a test, with one owner and a results dashboard |
| Missing coverage | A group of accounts, customers or records nobody touches | Count records with no owner or no activity by segment: small accounts, old leads, lost deals, inactive customers | Agent that works the untouched group at low cost and passes the ones that respond to a person |
| Missing loop | Results never change how the work is done | Check whether won and lost outcomes, replies or churn reasons feed back into targeting, messaging or the playbook | Agent that reads outcomes on a schedule and proposes changes to a named owner |
| Too costly by hand | Work that is worth doing only when it costs almost nothing per item | Ask what the team would do for every account or every customer if it had ten more people | Agent that does it for every item and shows only the exceptions |

### Example: buying group for every deal

No one maps the people who decide a purchase, so deals run through one contact.

- **Agent:** when an account moves to a set stage, it identifies the buying group (the roles that decide, pay, use and block), finds who holds each role, and sends the account owner a short email with the group and who is missing from the deal.
- **Trigger:** stage change in the CRM.
- **App:** tracker board. One row per open deal: roles covered, roles missing, last contact with each.
- **Human handler:** the account owner acts on the list. The sales manager sees deals with missing roles.
- **Loop:** after each won or lost deal the agent compares the group that was involved with the result, and updates which roles matter for which kind of deal.
- **Metric:** share of open deals past that stage with every key role in contact, and win rate for those deals against the rest.

### Evidence for a new work gap

Absence is evidence when you can count it. Write the count: "0 of 41 open deals past proposal have more than two contacts", "no activity tagged partner in the last 90 days", "312 lost deals with no touch since they closed". A new work gap with a count is evidenced. One with no count is a `Guess`.

Ask one of the 5 questions about new work, for example: "What would you do for every account if you had ten more people?"

## Sizing a gap

For a new work gap, size the group it would reach (deals, accounts, records) and state the expected effect as an estimate. Suggest a small test with a stop date before a full build.

For a fix gap:

Use the first of these that the tools can supply:

1. Items affected per week multiplied by time per item.
2. Money at risk in the affected items (for example open deal value with no next step).
3. Delay in days against the team's own target.
4. The person's own statement, labelled as their estimate.
