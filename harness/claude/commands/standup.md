---
description: Summarise your Jira activity for a standup
argument-hint: "[since when, default yesterday]"
---

Summarise recent Jira activity. Arguments: $ARGUMENTS

This is read only. Write nothing to Jira.

1. Read the daily files in `docs/jira/daily/` for the window, defaulting to the previous
   working day and today. They list the tickets touched and any time still ⏳.
2. Search for issues assigned to the current user updated in the window, defaulting to
   the last day: `assignee = currentUser() AND updated >= -1d ORDER BY updated DESC`.
3. For each, read the worklogs and comments the current user authored in that window.
4. Read `docs/jira/<KEY>.md` only for tickets found in steps 1–2.
5. Report as three short lists: what moved, what is in flight, what is blocked. Name each
   ticket by key and summary. Give each day's worked, logged and unlogged time from the
   daily file's totals block (never add durations up yourself), and list the ⏳ rows.
