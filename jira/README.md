# jira

Jira Cloud issues, comments and worklogs inside Claude Code, plus a per-ticket work
journal in `docs/jira/`.

## What is in it

- **MCP server** (`.mcp.json`) — `@aashari/mcp-server-atlassian-jira`, launched by `npx`,
  authenticated with an Atlassian API token. Dedicated tools for issues, comments and
  search, plus generic REST verbs that reach every other endpoint including worklogs.
- **Skill** (`skills/jira/`) — how to drive it. Which tool for which job, the approval
  rule, the v2 rule for text bodies, worklog time formats, journal conventions.
- **Agent** (`agents/jira.md`) — a `jira` subagent for ticket work in a side thread.
- **Commands** — `/jira:log`, `/jira:update`, `/jira:standup`.

## Install

```bash
/plugin marketplace add ~/Desktop/Projects/areaSim/jira-plugin
/plugin install jira@areasim
```

## Credentials

Create a token at https://id.atlassian.com/manage-profile/security/api-tokens, then add
an `env` block to `~/.claude/settings.json`:

```json
{
  "env": {
    "ATLASSIAN_SITE_NAME": "your-site",
    "ATLASSIAN_USER_EMAIL": "you@example.com",
    "ATLASSIAN_API_TOKEN": "paste-it-here"
  }
}
```

`ATLASSIAN_SITE_NAME` is only the subdomain. For `https://acme.atlassian.net` it is
`acme`. Keep the token out of the project directory and out of any chat transcript.

Restart Claude Code, then check the server is up with `/mcp`.

## Safety

Reads run freely. Every write is drafted for you and sent only after you approve it.
That rule lives in the skill and in the agent, so it holds in both the main session and
the subagent.

## Swapping the backend

To use Atlassian's official hosted server instead, which signs in with OAuth and needs no
token, replace `.mcp.json` with:

```json
{ "mcpServers": { "jira": { "type": "sse", "url": "https://mcp.atlassian.com/v1/sse" } } }
```

Check that time tracking is covered before you commit to it. The tool set is fixed by
Atlassian and worklogs may not be included.
