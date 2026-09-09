# Working on this repo

Instructions for any coding agent editing this repository. Not the Jira skill itself,
which lives in `core/knowledge/`.

## The one rule

`core/` is the single source of truth. `harness/` is generated output.

Everything under these paths is written by `scripts/sync.py` and carries a generated
banner. Editing them by hand is wasted work, because the next sync overwrites it:

```
harness/claude/skills/jira/SKILL.md
harness/claude/skills/jira/references/*.md
harness/cursor/rules/jira.mdc
```

To change what the agent knows about Jira, edit `core/`, then run `scripts/sync.py`.

## Layout

```
core/                    editor-neutral, hand-written
  identity.yaml          name, description, trigger phrases, the version 2 gotcha
  rules.md               the five rules that always apply
  key-resolution.md      how to derive a ticket key from a branch
  knowledge/             the five reference documents

harness/                 per-editor adapters, mostly generated
  claude/                a Claude Code plugin: skill, agent, commands, MCP server
  cursor/                a Cursor rule, MCP server block, installer

scripts/
  sync.py                compose core/ into every harness
  validate.py            secrets, manifests, links, frontmatter, sync state
```

## Before committing

```bash
scripts/validate.py
```

It fails on credentials in the tree or in git history, unparseable JSON, broken relative
links, missing frontmatter, and harnesses that have drifted from `core/`.

## Adding a harness

Create `harness/<editor>/`, add a builder function in `scripts/sync.py`, and register its
output paths in `targets()`. Reuse `body()` to pull core fragments so the new harness
cannot drift either.

## Credentials

Never commit one. The MCP configs ship `${ATLASSIAN_*}` placeholders that resolve from
the environment at launch. Real values belong in `~/.claude/settings.json`, which is
outside any repository.
