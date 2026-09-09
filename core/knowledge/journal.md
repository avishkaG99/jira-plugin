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
