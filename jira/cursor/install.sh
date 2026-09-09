#!/usr/bin/env bash
# Wire this plugin into Cursor: MCP server in ~/.cursor/mcp.json, rule in <project>/.cursor/rules/.
# Usage: ./install.sh [project-dir]   (defaults to the current directory)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="${1:-$PWD}"

python3 - "$HERE" "$PROJECT" <<'PY'
import json, os, pathlib, shutil, sys, getpass, datetime

here, project = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

# 1. rule file into the project
dest = project / ".cursor" / "rules"
dest.mkdir(parents=True, exist_ok=True)
shutil.copy(here / "rules" / "jira.mdc", dest / "jira.mdc")
print("rule   ->", dest / "jira.mdc")

# 2. MCP server into the user's Cursor config, reusing Claude Code creds when present
cfg_path = pathlib.Path.home() / ".cursor" / "mcp.json"
cfg_path.parent.mkdir(parents=True, exist_ok=True)
cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() and cfg_path.read_text().strip() else {}
if cfg_path.exists():
    shutil.copy(cfg_path, cfg_path.with_name("mcp.json.bak-%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")))

claude = pathlib.Path.home() / ".claude" / "settings.json"
env = {}
if claude.exists():
    env = {k: v for k, v in (json.loads(claude.read_text()).get("env") or {}).items()
           if k.startswith("ATLASSIAN_")}
    if env.get("ATLASSIAN_API_TOKEN"):
        print("creds  -> reused from ~/.claude/settings.json")

for key, prompt, hidden in (("ATLASSIAN_SITE_NAME", "Atlassian site subdomain", False),
                            ("ATLASSIAN_USER_EMAIL", "Atlassian account email", False),
                            ("ATLASSIAN_API_TOKEN", "Atlassian API token", True)):
    if not env.get(key):
        env[key] = (getpass.getpass if hidden else input)("%s: " % prompt).strip()

cfg.setdefault("mcpServers", {})["jira"] = {
    "command": "npx",
    "args": ["-y", "@aashari/mcp-server-atlassian-jira@3.3.0"],
    "env": env,
}
cfg_path.write_text(json.dumps(cfg, indent=2) + "\n")
os.chmod(cfg_path, 0o600)
print("server ->", cfg_path, "(chmod 600)")
print("\nRestart Cursor, then check Settings > MCP for a connected 'jira' server.")
PY
