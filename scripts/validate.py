#!/usr/bin/env python3
"""Structural checks for this repo. Exits non-zero on any failure.

    scripts/validate.py

Checks: no credentials anywhere, JSON manifests parse, every markdown link resolves,
frontmatter is present where required, and the harnesses are in sync with core/.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
fails = []


def check(name, ok, detail=""):
    print("  %-44s %s%s" % (name, "PASS" if ok else "FAIL", "  " + detail if detail else ""))
    if not ok:
        fails.append(name)


def files(pattern):
    return [p for p in ROOT.rglob(pattern) if ".git/" not in str(p)]


print("secrets")
# an Atlassian token, or any key= assignment holding something token-shaped
pats = [r"ATATT[A-Za-z0-9_\-=]{20,}", r"\bxox[baprs]-[A-Za-z0-9-]{10,}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"]
hits = []
for p in files("*"):
    if p.is_dir() or p.suffix in {".png", ".jpg", ".pdf", ".svg"}:
        continue
    try:
        t = p.read_text()
    except (UnicodeDecodeError, OSError):
        continue
    for pat in pats:
        if re.search(pat, t):
            hits.append("%s (%s)" % (p.relative_to(ROOT), pat[:12]))
check("no credentials in the working tree", not hits, "; ".join(hits))
try:
    hist = subprocess.run(["git", "-C", str(ROOT), "grep", "-lE", pats[0]] +
                          subprocess.run(["git", "-C", str(ROOT), "rev-list", "--all"],
                                         capture_output=True, text=True).stdout.split(),
                          capture_output=True, text=True)
    check("no credentials in git history", hist.returncode != 0, hist.stdout.strip()[:80])
except Exception as e:
    check("no credentials in git history", False, str(e))

print("\nmanifests")
for j in files("*.json"):
    try:
        json.loads(j.read_text())
        ok, detail = True, ""
    except Exception as e:
        ok, detail = False, str(e)[:60]
    check("parses: %s" % j.relative_to(ROOT), ok, detail)

mk = ROOT / ".claude-plugin/marketplace.json"
if mk.exists():
    m = json.loads(mk.read_text())
    for pl in m.get("plugins", []):
        src = (ROOT / pl["source"]).resolve()
        check("marketplace source exists: %s" % pl["source"],
              (src / ".claude-plugin/plugin.json").exists(), str(src))

print("\nlinks")
bad = []
for md in files("*.md"):
    for _, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", md.read_text()):
        if target.startswith(("http", "#", "mailto:")):
            continue
        if not (md.parent / target.split("#")[0]).resolve().exists():
            bad.append("%s -> %s" % (md.relative_to(ROOT), target))
check("every relative markdown link resolves", not bad, "; ".join(bad[:3]))

print("\nfrontmatter")
need = files("core/knowledge/*.md") + files("harness/*/skills/*/*.md") + files("harness/*/rules/*.mdc")
missing = [str(p.relative_to(ROOT)) for p in need
           if not re.match(r"\A---\n.*?\n---\n", p.read_text(), re.S)]
check("frontmatter present in %d file(s)" % len(need), not missing, "; ".join(missing[:3]))

print("\nsync")
r = subprocess.run([sys.executable, str(ROOT / "scripts/sync.py"), "--check"],
                   capture_output=True, text=True)
check("harnesses match core/", r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout else "")

print("\n%s  (%d check(s) failed)" % ("FAILED" if fails else "ALL PASS", len(fails)))
sys.exit(1 if fails else 0)
