---
title: Reading from Jira
tags: read, get, search, jql, issue, comment, worklog, transition
---

## Reading from Jira

Reads never need approval. Do them freely and do them first.

### Dedicated tools

| Task | Tool | Notes |
| --- | --- | --- |
| One issue | `jira_get_issue` | Pass the key, e.g. `AR-664` |
| Search | `jira_ls_issues` | Takes JQL |
| Comments | `jira_ls_comments` | Newest first is usually what you want |
| Projects | `jira_ls_projects` | |
| Statuses | `jira_ls_statuses` | All statuses in the project, not what is reachable now |

### Generic reads

Anything without a dedicated tool goes through `jira_get` with a REST path.

```
worklogs      GET /rest/api/2/issue/{key}/worklog
transitions   GET /rest/api/3/issue/{key}/transitions
current user  GET /rest/api/3/myself
find a user   GET /rest/api/3/user/search?query=someone@example.com
```

Reads may use version 3 safely. The version 2 rule only concerns bodies you send.

### JQL worth knowing

```
assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC
assignee = currentUser() AND updated >= -1d ORDER BY updated DESC
project = AR AND status = "In Progress"
key in (AR-664, AR-653)
```

Quote any status name containing a space. `currentUser()` avoids hardcoding an account id.

### Before any write

- Posting a comment? Run `jira_ls_comments` first. If you are revising something you
  already said, edit that comment instead of adding another.
- Logging time? List the worklogs first and check no entry already covers that span.
- Changing status? Fetch the transitions. The names available depend on the current
  status, so the full status list is not a substitute.
