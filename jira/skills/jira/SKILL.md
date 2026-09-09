---
name: jira
description: Read and update Jira Cloud issues, comments and worklogs, and keep the local per-ticket work journal in docs/jira/ in sync. Use whenever the user mentions a Jira key like AR-123, asks to update a ticket, move it to another status, log time or hours spent, add or edit a progress comment, create a ticket, or asks what they worked on. Also use when the current git branch carries a ticket key.
---

# Jira

Jira runs through the `jira` MCP server bundled with this plugin. Never write raw `curl`
against the Jira API and never install a Jira client.

## Approval rule

**Every write is drafted for the user before it is sent.** Show the exact comment text,
worklog, or field change and wait for a yes. Reads need no approval.

Approval covers the one write you described. It does not extend to a second write you
decide is also a good idea.

## Which tool

Dedicated tools, use these first:

| Task | Tool |
| --- | --- |
| Read an issue | `jira_get_issue` |
| Search by JQL | `jira_ls_issues` |
| List comments | `jira_ls_comments` |
| Post a comment | `jira_add_comment` |
| Create an issue | `jira_create_issue` |
| List projects, statuses | `jira_ls_projects`, `jira_ls_statuses` |

Everything else goes through the generic REST verbs `jira_get`, `jira_post`, `jira_put`,
`jira_patch`, `jira_delete`, which take a Jira API path and a JSON body.

```
worklogs      GET|POST  /rest/api/2/issue/{key}/worklog
              PUT|DELETE /rest/api/2/issue/{key}/worklog/{id}
transitions   GET|POST  /rest/api/3/issue/{key}/transitions
edit fields   PUT       /rest/api/3/issue/{key}
assignee      PUT       /rest/api/3/issue/{key}/assignee
edit comment  PUT       /rest/api/2/issue/{key}/comment/{id}
find a user   GET       /rest/api/3/user/search?query=<email>
whoami        GET       /rest/api/3/myself
```

## The v2 rule

**When your request body contains text you wrote, use `/rest/api/2/`. For everything
else use `/rest/api/3/`.**

Version 3 requires Atlassian Document Format, where a two-line note becomes a deep JSON
tree of paragraph, text and mark nodes. Version 2 takes the same field as a plain
string and converts it server side. So a worklog is simply:

```json
POST /rest/api/2/issue/AR-664/worklog
{
  "timeSpent": "2h30m",
  "started": "2026-09-09T09:00:00.000+0530",
  "comment": "Traced the forced sign-out to the session cookie clear."
}
```

`started` is strict: `YYYY-MM-DDTHH:mm:ss.SSS±hhmm`, milliseconds required, no colon in
the offset. Get the offset from `date +%z` rather than guessing. `timeSpent` uses Jira's
own units: `2h`, `45m`, `1h30m`, `1d`.

If a v2 call is ever rejected, fall back to v3 and build the Atlassian Document Format
body, but try v2 first.

## How to work

1. **Resolve the key.** Take it from the user, or read the branch:
   `git -C areasim-webapp branch --show-current` gives `fix/ar-664-...`, so `AR-664`.
   Check `areasim-backend` too, and ask if the two disagree.
2. **Read before you write.** Run `jira_ls_comments` or list worklogs first, so you
   update an existing entry rather than adding a near-duplicate.
3. **Never guess a status name.** `GET /rest/api/3/issue/{key}/transitions` returns what
   is actually reachable. Post the transition id, not a name.
4. **Log the write.** After any successful write, append to `docs/jira/<KEY>.md` and
   record the id the API returned, so a later edit can target that entry.
5. **Never invent progress.** A comment or worklog describes what the journal, the diff
   or the user actually said happened. If you cannot substantiate it, leave it out.

## The local work journal

Each ticket gets `docs/jira/<KEY>.md`. It is the working record, richer than what reaches
Jira, and it is what you summarise from when the user says "post the update".

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

Append under today's date. Never rewrite past entries. Convert relative dates to absolute
ones before writing.

## Project conventions

- Project key `AR`. Branches are `feature/ar-628-...`, `fix/ar-664-...`.
- Two repos sit under the project root: `areasim-backend` and `areasim-webapp`.
- Prefer editing an existing comment over posting a correction as a new one.
