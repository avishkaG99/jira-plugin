---
title: Task workflows
tags: workflow, log-time, manual-work, daily-file, backfill, hours-worked, progress-update, transition, standup, create
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
8. Append to the journal with the returned worklog id, set the row's `Logged` to
   `✅ <duration> · worklog <id>`, and rebuild the index so the day's totals update, all in
   the same turn.

### Record manual work

For work the user did outside a session: meetings, reviews, testing, anything the agent
did not see.

1. Resolve the key. Ask if the user did not name one; do not guess from the branch.
2. Add a `manual` row to that day's daily file with the times exactly as given. Create the
   file if it does not exist yet.
3. If this is the first contact with the ticket, start its journal.
4. Rebuild the index, which also updates that day's totals.
5. Offer to draft the worklog. Adding the row is not approval to post one.

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

### Backfill past days

For days before the daily file existed. The journals are the source: only work they record
is backfilled.

1. Collect every worklog id recorded in `docs/jira/*.md`, with its ticket. Skip ids the journal
   attributes to someone else. The earliest journal date with a worklog is the start point;
   go no further back.
2. `GET /rest/api/2/issue/{key}/worklog` with `startedAfter` / `startedBefore` (epoch ms,
   local midnight) for those tickets, and take each recorded id's `started` and
   `timeSpentSeconds`. Worklogs the journals never recorded stay out.
3. One `worklog` row per id on its start date: `Time` = start plus duration, `Logged` =
   `✅ <duration> · worklog <id>`, summary from the journal's title line.
4. Fill `Jira writes` from that day's journal entries: descriptions, comment ids,
   transitions, deleted worklogs. Leave `—` when the journal records none.
5. A journal day that shows Jira writes but no worklog gets a `session` row with `—` time and
   ⏳. Do not estimate a duration.
6. Never overwrite an existing daily file. Then rebuild the index, and point out days where
   *Logged* exceeds *Worked*: overlapping worklogs, possibly double-booked time.

### Standup summary

Read only. Write nothing, locally or to Jira.

1. Read the daily files for the window, defaulting to the previous working day and today.
   They list every ticket touched and every span still ⏳.
2. `assignee = currentUser() AND updated >= -1d ORDER BY updated DESC`, to catch tickets
   that moved without a daily row.
3. For each issue, read the worklogs and comments the user authored in that window.
4. Read journal files only for tickets named in steps 1–2, for detail Jira does not carry.
5. Report three lists: what moved, what is in flight, what is blocked. Name each by key
   and summary. Give each day's worked, logged and unlogged totals from its daily file's
   totals block, and list the ⏳ rows. Don't add up durations yourself.

### Hours worked

Read only. For "how many hours did I work today / this week":

1. Read `docs/jira/README.md` for the last seven days, or the totals block of each daily
   file in the range. If `build_journal_index.py --check` reports stale files, rebuild first.
2. Report worked, logged and unlogged per day and the sum for the range, then the ⏳ rows.
3. Say plainly that only work the agent saw or the user reported is counted.
