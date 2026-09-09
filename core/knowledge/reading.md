---
title: Reading from Jira
tags: read, get, search, jql, issue, comment, worklog, transition
---

## Reading from Jira

Reads never need approval. Do them freely and do them first.

### The tool surface

The server exposes exactly five tools. There are no per-entity tools, so every read is
`jira_get` with a REST path.

| Tool | Params |
| --- | --- |
| `jira_get` | `path` (required), `queryParams`, `jq`, `outputFormat` |
| `jira_post` | `path`, `body` (both required), `queryParams`, `jq`, `outputFormat` |
| `jira_put` | `path`, `body` (both required), `queryParams`, `jq`, `outputFormat` |
| `jira_patch` | `path`, `body` (both required), `queryParams`, `jq`, `outputFormat` |
| `jira_delete` | `path` (required), `queryParams`, `jq`, `outputFormat` |

Responses come back as TOON, an indented key-value format, not JSON. It is compact and
readable. Pass `outputFormat: "json"` only when you genuinely need JSON.

Use `jq` to narrow large responses rather than pulling everything and discarding it. An
issue with all fields is thousands of tokens; three fields is a few dozen.

### Common reads

```
issue         GET /rest/api/3/issue/{key}      queryParams: {"fields": "summary,status,assignee"}
search        GET /rest/api/3/search/jql       queryParams: {"jql": "...", "fields": "summary,status"}
comments      GET /rest/api/2/issue/{key}/comment
worklogs      GET /rest/api/2/issue/{key}/worklog
transitions   GET /rest/api/3/issue/{key}/transitions
projects      GET /rest/api/3/project/search
current user  GET /rest/api/3/myself
find a user   GET /rest/api/3/user/search      queryParams: {"query": "someone@example.com"}
```

Always pass `fields` when reading an issue. The default returns every field including
large custom ones.

Reads may use version 3 safely. The version 2 rule only concerns bodies you send, though
reading comments and worklogs from version 2 gives plain text instead of a document tree,
which is easier to quote back.

### JQL worth knowing

```
assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC
assignee = currentUser() AND updated >= -1d ORDER BY updated DESC
project = AR AND status = "In Progress"
key in (AR-664, AR-653)
```

Quote any status name containing a space. `currentUser()` avoids hardcoding an account id.

### Before any write

- Posting a comment? Read the comments first. If you are revising something you already
  said, edit that comment instead of adding another.
- Logging time? List the worklogs first and check no entry already covers that span.
- Changing status? Fetch the transitions. Which ones exist depends on the current status,
  so a list of all project statuses is not a substitute.
