#!/usr/bin/env python3
"""Launch the MCP server exactly as the editor will, and prove it reaches Jira.

    scripts/preflight.py [--project DIR]

Verifies, without needing an editor restart: credentials resolve, the server starts,
the handshake succeeds, the tools the skill relies on exist, and a real read returns
data. Read-only. Nothing is written to Jira.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import time

REQUIRED = {"jira_get", "jira_post", "jira_put", "jira_patch", "jira_delete"}
fails = []


def check(name, ok, detail=""):
    print("  %-40s %s%s" % (name, "PASS" if ok else "FAIL", "  " + detail if detail else ""))
    if not ok:
        fails.append(name)
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", default=".", help="project holding .mcp.json (default: cwd)")
    ap.add_argument("--issue", help="also read this issue's worklogs, e.g. AR-659")
    a = ap.parse_args()

    print("credentials")
    settings = pathlib.Path.home() / ".claude" / "settings.json"
    cfg = json.loads(settings.read_text()).get("env", {}) if settings.exists() else {}
    creds = {k: v for k, v in cfg.items() if k.startswith("ATLASSIAN_")}
    for key in ("ATLASSIAN_SITE_NAME", "ATLASSIAN_USER_EMAIL", "ATLASSIAN_API_TOKEN"):
        v = creds.get(key, "")
        check(key, bool(v), ("set, length %d" % len(v)) if "TOKEN" in key else v)
    if fails:
        print("\nFAILED: fill these in %s under \"env\"" % settings)
        return 1

    mcp_path = pathlib.Path(a.project) / ".mcp.json"
    if not check("finds %s" % mcp_path, mcp_path.exists()):
        return 1
    spec = json.loads(mcp_path.read_text())["mcpServers"]["jira"]

    print("\nserver")
    env = dict(os.environ)
    env.update(creds)
    proc = subprocess.Popen([spec["command"]] + spec["args"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, env=env, bufsize=1)

    def send(obj):
        proc.stdin.write(json.dumps(obj) + "\n")
        proc.stdin.flush()

    def wait(msg_id, timeout=240):
        end = time.time() + timeout
        while time.time() < end:
            line = proc.stdout.readline()
            if not line:
                if proc.poll() is not None:
                    return {"error": {"message": "server exited %s: %s"
                                      % (proc.returncode, proc.stderr.read()[:300])}}
                continue
            try:
                m = json.loads(line)
            except json.JSONDecodeError:
                continue
            if m.get("id") == msg_id:
                return m
        return {"error": {"message": "timed out after %ss" % timeout}}

    try:
        send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2024-11-05", "capabilities": {},
            "clientInfo": {"name": "preflight", "version": "1"}}})
        r = wait(1)
        info = r.get("result", {}).get("serverInfo", {})
        if not check("handshake", "result" in r,
                     "%s %s" % (info.get("name", ""), info.get("version", ""))
                     or str(r.get("error"))[:80]):
            return 1
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})

        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tools = {t["name"] for t in wait(2).get("result", {}).get("tools", [])}
        missing = sorted(REQUIRED - tools)
        check("exposes the tools the skill uses", not missing,
              "missing " + ", ".join(missing) if missing else "%d tool(s)" % len(tools))

        print("\nlive reads")
        def call(path, label):
            send({"jsonrpc": "2.0", "id": call.n, "method": "tools/call",
                  "params": {"name": "jira_get", "arguments": {"path": path}}})
            res = wait(call.n)
            call.n += 1
            body = "".join(c.get("text", "") for c in res.get("result", {}).get("content", []))
            ok = "result" in res and not res["result"].get("isError")
            return check(label, ok, body.strip().splitlines()[0][:60] if ok else
                         str(res.get("error") or body)[:70])
        call.n = 3

        call("/rest/api/3/myself", "authenticates as a real account")
        call("/rest/api/3/project/search", "can list projects")
        if a.issue:
            call("/rest/api/2/issue/%s/worklog" % a.issue, "can read worklogs on %s" % a.issue)
    finally:
        proc.terminate()

    print("\n%s  (%d check(s) failed)" % ("ALL PASS" if not fails else "FAILED", len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
