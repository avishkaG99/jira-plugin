---
description: Summarise your Jira activity for a standup
argument-hint: "[since when, default yesterday]"
---

Summarise recent Jira activity. Arguments: $ARGUMENTS

This is read only. Write nothing to Jira.

1. Search for issues assigned to the current user updated in the window, defaulting to
   the last day: `assignee = currentUser() AND updated >= -1d ORDER BY updated DESC`.
2. For each, read the worklogs and comments the current user authored in that window.
3. Read any matching `docs/jira/<KEY>.md` journal entries for detail Jira does not carry.
4. Report as three short lists: what moved, what is in flight, what is blocked. Name each
   ticket by key and summary. Say the total time logged.
