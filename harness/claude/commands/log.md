---
description: Log time against the current ticket and record it in the work journal
argument-hint: "<duration> [what you did]"
---

Log work against Jira. Arguments: $ARGUMENTS

1. Resolve the issue key from the current git branch. Ask if it is ambiguous.
2. List the existing worklogs on that issue and check this entry would not duplicate one.
3. Read today's `docs/jira/daily/<YYYY-MM-DD>.md` for the time spans on that key. If the
   user reports work with no row yet, add it as a `manual` row with the times exactly as
   given.
4. Read `docs/jira/<KEY>.md` if it exists. If the user gave no description, draft one
   from today's journal entries and the working tree diff.
5. Show the user the duration, start time and description you are about to submit.
   Wait for approval.
6. On approval, POST to `/rest/api/2/issue/<KEY>/worklog`, then append the entry and the
   returned worklog id to the journal under today's date, set the daily row's `Logged` to
   `✅ <duration> · worklog <id>`, and run
   `python3 jira-plugin/scripts/build_journal_index.py docs/jira` to update the day's totals.
