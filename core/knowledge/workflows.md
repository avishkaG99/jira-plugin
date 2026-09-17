---
title: Task workflows
tags: workflow, log-time, manual-work, daily-file, progress-update, transition, standup, create
---

## Task workflows

Each is a full sequence. Do not skip the read steps.

### Log time

1. Resolve the key. Ask if the branch is ambiguous.
2. `GET /rest/api/2/issue/{key}/worklog`. Check nothing already covers that span.
3. Read the day's `docs/jira/daily/<YYYY-MM-DD>.md`. Its rows for the key give the time
   spans and which are still ⏳. If the user reports work that has no row yet, add it as a
   `manual` row first (see "Record manual work").
4. Read `docs/jira/<KEY>.md`. If the user gave no description, draft one from that day's
   journal entries and the working tree diff.
5. Work out `started` from the row's start time plus the local offset (`date +%z`). A
   duration comes from the row, or from the user; never stretch a `session` span to fill
   the day.
6. Show the user the duration, start time and description. Wait for approval.
7. `POST /rest/api/2/issue/{key}/worklog`.
8. Append to the journal with the returned worklog id, and set the row's `Logged` to
   `✅ <duration> · worklog <id>` in the same turn.

### Record manual work

For work the user did outside a session: meetings, reviews, testing, anything the agent
did not see.

1. Resolve the key. Ask if the user did not name one; do not guess from the branch.
2. Add a `manual` row to that day's daily file with the times exactly as given. Create the
   file if it does not exist yet.
3. If this is the first contact with the ticket, start its journal and rebuild the index.
4. Offer to draft the worklog. Adding the row is not approval to post one.

### Post a progress update

1. Resolve the key.
2. `GET /rest/api/3/issue/{key}` with `fields=summary,status` for current state, and
   `GET /rest/api/2/issue/{key}/comment` for what has been said.
3. Compose from the journal's newest entries plus commits on the branch since it
   diverged. Keep it to what changed and what is next.
4. If this revises a comment you posted earlier, edit that one.
5. Show the exact text. Wait for approval.
6. Post, then record the comment id in the journal.

### Change status

1. `GET /rest/api/3/issue/{key}/transitions`.
2. Match what the user asked to a transition in that list. If nothing matches, tell them
   what is available rather than picking the nearest.
3. Confirm the target status with the user.
4. `POST` the transition id.
5. Note the status change in the journal.

If they also want a comment, post it in the same call using the `update.comment` block
rather than making two requests.

### Create an issue

1. Confirm project, type, summary, and parent if it is a subtask.
2. Draft the description and show it.
3. `POST /rest/api/2/issue`.
4. Report the new key and its browse URL.
5. Start a journal file for it, add a row to today's daily file, and rebuild the index.

### Standup summary

Read only. Write nothing, locally or to Jira.

1. Read the daily files for the window, defaulting to the previous working day and today.
   They list every ticket touched and every span still ⏳.
2. `assignee = currentUser() AND updated >= -1d ORDER BY updated DESC`, to catch tickets
   that moved without a daily row.
3. For each issue, read the worklogs and comments the user authored in that window.
4. Read journal files only for tickets named in steps 1–2, for detail Jira does not carry.
5. Report three lists: what moved, what is in flight, what is blocked. Name each by key
   and summary. State the total time logged, and list any ⏳ rows as unlogged time.
