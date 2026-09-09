---
description: Draft and post a progress comment on the current ticket
argument-hint: "[what to say, or leave blank to summarise the journal]"
---

Post a progress update to Jira. Arguments: $ARGUMENTS

1. Resolve the issue key from the current git branch. Ask if it is ambiguous.
2. Read the issue and its existing comments.
3. Compose the update. If the user gave no text, summarise the newest entries in
   `docs/jira/<KEY>.md` plus the commits on this branch since it diverged.
4. If your update revises a comment you posted earlier, edit that comment rather than
   adding a second one.
5. Show the exact text and wait for approval before sending.
6. On approval, post it and record the comment id in the journal.
