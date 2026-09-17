---
title: The work journal
tags: journal, docs, notes, record
---

## The work journal

Each ticket gets `docs/jira/<KEY>.md` in the project. It is the working record, richer
than what reaches Jira, and it is what a progress comment gets summarised from.

```markdown
# AR-664 — Accept invite forces a sign-out

Status: In Progress · Branch: fix/ar-664-accept-invite-forced-signout

## Log
### 2026-09-09
- Reproduced on a fresh invite; the session cookie is cleared before the redirect.
- Logged 2h30m (worklog 10877). Comment 10432 posted.

## Decisions
- Keep the redirect, clear the cookie after the token exchange instead.

## Open questions
- Does the mobile client hit the same path?
```

Rules:

- Append under today's date. Never rewrite past entries.
- Record every id the API returns. A later edit targets that id instead of creating a
  duplicate comment or worklog.
- Convert relative dates to absolute before writing. "Yesterday" is useless in six weeks.
- Decisions and open questions are the parts worth keeping. A list of files touched is
  already in the git log.
- Create the file on first contact with a ticket, not at the end.
- **Every Jira write lands here too, in the same turn.** A worklog, comment, transition or
  field edit is only half done until the journal records what changed and why. The Jira
  entry is the short public version; this is where the reasoning that produced it lives, and
  it is the only copy if the Jira side is later edited or deleted. The same turn also updates
  the ticket's row in the daily file below.

## The daily file

`docs/jira/daily/<YYYY-MM-DD>.md`, one per local calendar day. It answers "what did I work
on that day, when, and is the time logged" without opening every ticket journal.

```markdown
# 2026-09-17

| Ticket | Summary | Time | Source | Jira writes | Logged |
|---|---|---|---|---|---|
| [AR-613](../AR-613.md) | Utilisation Dashboard Enhancements | 11:33–12:19 | session | description | ⏳ |
| [AR-620](../AR-620.md) | Customer view - List | 12:25–12:48 | session | description | ✅ 25m · worklog 11502 |
| [AR-4](../AR-4.md) | Meetings & Sync-ups | 14:00–14:45 | manual | — | ⏳ |
```

Rules:

- Create the file on first contact with any ticket that day. Add a row the first time a
  ticket is touched. A separate, later span on the same ticket is a new row.
- `Time` is local clock time, no offset. The offset belongs only in a worklog's `started`.
- `Source` is `session` when the agent saw the work happen: start is the first action on
  the ticket, end is the last. It is `manual` when the user reported the work (a meeting, a
  review, anything outside a session). **Record manual times exactly as given.** Never
  round, stretch or infer them.
- `Jira writes` holds short labels only: `description`, `comment 10432`,
  `→ In Progress`. Ids with reasoning go in the ticket journal.
- `Logged` is ⏳ until a worklog covers the row, then `✅ <duration> · worklog <id>`.
  Update it in the same turn as the worklog POST.
- Keep it thin. No narrative: it is an index into the ticket journals, and it only stays
  cheap to read while it stays short.
- Never rewrite a past day, except its `Logged` column when that day's time is logged later.
- Adding a row is a local write. It needs no approval, and it is not permission to post a
  worklog.

## The index

`docs/jira/README.md` lists every ticket journal: key, summary, journal status and the last
day worked, newest first, with links to the recent daily files. It is **generated**, never
edited by hand:

```
python3 jira-plugin/scripts/build_journal_index.py docs/jira
```

Run it after creating a new ticket journal or adding a new day's entry. Read the index
when the user names a ticket by description rather than key.
