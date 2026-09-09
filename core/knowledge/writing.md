---
title: Writing to Jira
tags: write, post, put, comment, worklog, transition, adf, version-2
---

## Writing to Jira

**Draft every write for the user and wait for approval before sending it.**

Every write is `jira_post`, `jira_put`, `jira_patch` or `jira_delete` with a `path` and a
`body`. There are no per-entity tools. Responses come back as TOON, not JSON.

### The version 2 rule

> When the request body contains text you wrote, use `/rest/api/2/`.
> For everything else, use `/rest/api/3/`.

Version 3 requires Atlassian Document Format. A two-line note becomes a nested tree of
`doc`, `paragraph`, `text` and `marks` nodes, which is slow to build and easy to get
wrong. Version 2 accepts the same field as a plain string and converts it server side.
Both versions are live on Jira Cloud.

If a version 2 call is ever rejected, fall back to version 3 and build the document
format body. Try version 2 first.

### Comments

```
add     POST /rest/api/2/issue/{key}/comment      { "body": "text" }
edit    PUT  /rest/api/2/issue/{key}/comment/{id} { "body": "text" }
```

Prefer editing over posting a correction as a second comment. Keep comments short and
factual. The detail belongs in the journal.

### Worklogs

```
add     POST   /rest/api/2/issue/{key}/worklog
edit    PUT    /rest/api/2/issue/{key}/worklog/{id}
delete  DELETE /rest/api/2/issue/{key}/worklog/{id}
```

```json
{
  "timeSpent": "2h30m",
  "started": "2026-09-09T09:00:00.000+0530",
  "comment": "Traced the forced sign-out to the session cookie clear."
}
```

`timeSpent` uses Jira units: `2h`, `45m`, `1h30m`, `1d`. A day is whatever the project
configures, usually eight hours, so prefer hours to days.

`started` is strict and rejects anything else:

```
YYYY-MM-DDTHH:mm:ss.SSS±hhmm
```

Milliseconds are required and the offset has no colon. Get the offset from `date +%z`
rather than guessing. Defaults to now if you omit it, but be explicit when logging time
for earlier in the day.

### Transitions

```
list  GET  /rest/api/3/issue/{key}/transitions
move  POST /rest/api/3/issue/{key}/transitions   { "transition": { "id": "31" } }
```

Always list first and post the id. Names differ per workflow and per current status.

### Fields

```
edit      PUT /rest/api/3/issue/{key}            { "fields": { ... } }
assignee  PUT /rest/api/3/issue/{key}/assignee   { "accountId": "..." }
```

Common shapes:

```json
{ "fields": {
  "summary": "New summary",
  "labels": ["frontend", "regression"],
  "priority": { "name": "High" },
  "customfield_10016": 5
} }
```

`labels` replaces the whole list, it does not append. Read the current labels first.
Unassign by sending `"accountId": null`. Resolve an account id from an email with
`GET /rest/api/3/user/search?query=<email>`.

A description sent this way needs document format, so write descriptions with
`PUT /rest/api/2/issue/{key}` and a plain string instead.

### Creating an issue

`POST /rest/api/2/issue`. There is no dedicated create tool, so version 2 matters here:
it lets the description be a plain string.

```json
{ "fields": {
  "project": { "key": "AR" },
  "issuetype": { "name": "Bug" },
  "summary": "...",
  "description": "plain text is fine on version 2",
  "parent": { "key": "AR-600" }
} }
```

### After every successful write

Append to `docs/jira/<KEY>.md` and record the id the API returned, so a later edit can
target that entry. See [journal.md](journal.md).
