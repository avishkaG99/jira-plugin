---
title: areaSim project conventions
tags: conventions, areasim, project-key, branches, workflow, statuses
---

## areaSim conventions

### Projects

`AR` is AreaSim. `AB` is Absence Tracker. Assume `AR` unless told otherwise.

### Repositories

Two repos sit under the project root and both carry ticket branches:

```
areasim-backend
areasim-webapp
```

Branch names are `feature/ar-628-...`, `fix/ar-664-...`, so `AR-628` and `AR-664`. If the
two repos are on different tickets, ask which one the user means rather than picking.

### Workflow statuses

The `AR` workflow has more than the usual three. Observed reachable states include:

```
To Do · In Progress · Mob Elaboration · Construction
Verification · UAT · Ready for Deployment · Blocked · Done
```

This list is context for recognising what a user means. It is not a substitute for
fetching the transitions, which depend on the current status and on permissions.

### Credentials

Supplied to the MCP server as environment variables from `~/.claude/settings.json`:
`ATLASSIAN_SITE_NAME`, `ATLASSIAN_USER_EMAIL`, `ATLASSIAN_API_TOKEN`. Never read that
file into the conversation, never echo the token, and never write a credential into a
project settings file or the plugin repo.
