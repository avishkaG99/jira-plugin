# Install

Three routes. All of them need the credentials step at the bottom.

## Paste this to an agent

Open the target project in Claude Code, Cursor, or any coding agent with shell access,
and paste this verbatim. Replace nothing except the last line if you only want one editor.

```text
Install the Jira agent tooling into this project.

1. Clone https://github.com/avishkaG99/jira-plugin.git to a scratch directory outside
   this project, or git pull if you already have it.
2. Run its installer against this project root:
       python3 <clone>/scripts/sync.py --install .
   That writes:
       .claude/skills/jira/          the skill and its five reference files
       .claude/agents/jira.md        the jira subagent
       .claude/commands/jira/        /jira:log /jira:update /jira:standup
       .cursor/rules/jira.mdc        the same conventions as a Cursor rule
       .mcp.json                     the jira MCP server definition
3. Do not hand-edit any file it wrote. They are generated from the clone's core/
   directory. To change behaviour, edit core/ there and re-run sync.py.
4. Tell me to add my Atlassian credentials to ~/.claude/settings.json under an "env"
   key: ATLASSIAN_SITE_NAME (subdomain only), ATLASSIAN_USER_EMAIL, ATLASSIAN_API_TOKEN.
   Never put the token in a project file, and never print it back to me.
5. Confirm what you wrote, then tell me to restart the editor so the MCP server loads.
```

## Claude Code, as a plugin

```json
{
  "extraKnownMarketplaces": {
    "areasim": { "source": { "source": "github", "repo": "avishkaG99/jira-plugin" } }
  },
  "enabledPlugins": { "jira@areasim": true }
}
```

Put that in the project's `.claude/settings.json`, or run `/plugin marketplace add
avishkaG99/jira-plugin` then `/plugin install jira@areasim` if your client has `/plugin`.
Restart to install.

Do not combine this with the direct install below. Two copies of a skill named `jira`
and two MCP servers named `jira` will collide.

## Cursor

```bash
./harness/cursor/install.sh /path/to/your/project
```

Copies the generated rule to `<project>/.cursor/rules/jira.mdc`, writes the server into
`~/.cursor/mcp.json` with permissions `600`, and reuses Claude Code credentials if they
are already set. Cursor gets the tools and conventions, not subagents or slash commands.

## Credentials

Get a token from https://id.atlassian.com/manage-profile/security/api-tokens, then add to
`~/.claude/settings.json`, which is personal and outside every repository:

```json
{
  "env": {
    "ATLASSIAN_SITE_NAME": "your-site",
    "ATLASSIAN_USER_EMAIL": "you@example.com",
    "ATLASSIAN_API_TOKEN": "..."
  }
}
```

`ATLASSIAN_SITE_NAME` is the subdomain only: `acme` for `https://acme.atlassian.net`.

Never put a token in a project settings file or in this repo. `scripts/validate.py`
fails the build if one appears in the tree or in git history.

## Verify

```bash
python3 scripts/validate.py     # structure, links, secrets, sync state
python3 scripts/preflight.py    # launch the MCP server and call Jira for real
```

Then restart the editor and confirm the server is connected: `/mcp` in Claude Code,
Settings then MCP in Cursor.
