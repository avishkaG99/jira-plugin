---
title: Task workflows
tags: workflow, log-time, progress-update, transition, standup, create
---

## Task workflows

Each is a full sequence. Do not skip the read steps.

### Log time

1. Resolve the key. Ask if the branch is ambiguous.
2. `GET /rest/api/2/issue/{key}/worklog`. Check nothing already covers that span.
3. Read `docs/jira/<KEY>.md`. If the user gave no description, draft one from today's
   journal entries and the working tree diff.
4. Work out `started`. "This morning" needs a real timestamp with the local offset.
5. Show the user the duration, start time and description. Wait for approval.
6. `POST /rest/api/2/issue/{key}/worklog`.
7. Append to the journal with the returned worklog id.

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
5. Start a journal file for it.

### Standup summary

Read only. Write nothing.

1. `assignee = currentUser() AND updated >= -1d ORDER BY updated DESC`.
2. For each issue, read the worklogs and comments the user authored in that window.
3. Read matching journal files for detail Jira does not carry.
4. Report three lists: what moved, what is in flight, what is blocked. Name each by key
   and summary. State the total time logged.
