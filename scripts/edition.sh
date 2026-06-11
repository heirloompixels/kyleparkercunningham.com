#!/usr/bin/env bash
# Manage the living homepage editions.
#
#   ./scripts/edition.sh new <slug> "<Title>" [season|project]   scaffold a staged edition
#   ./scripts/edition.sh serve                                   build in real time (drafts visible)
#   ./scripts/edition.sh list                                    show all editions + status
#   ./scripts/edition.sh promote <slug>                          go live (retires the current one)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
EDITIONS="content/editions"

cmd="${1:-help}"

case "$cmd" in

  new)
    slug="${2:?usage: edition.sh new <slug> \"<Title>\" [season|project]}"
    title="${3:?usage: edition.sh new <slug> \"<Title>\" [season|project]}"
    kind="${4:-season}"
    python3 - "$slug" "$title" "$kind" << 'PYEOF'
import sys, re
from pathlib import Path
from datetime import date

slug, title, kind = sys.argv[1], sys.argv[2], sys.argv[3]
editions = Path("content/editions")
target = editions / slug
if target.exists():
    sys.exit(f"error: {target} already exists")

def roman(n):
    vals = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),
            (50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
    out = ""
    for v, s in vals:
        while n >= v: out += s; n -= v
    return out

count = sum(1 for d in editions.iterdir() if d.is_dir() and (d / "index.md").exists())
numeral = roman(count + 1)
today = date.today().isoformat()
label = "Season" if kind == "season" else "Edition"

target.mkdir(parents=True)
(target / "index.md").write_text(f'''+++
title = "{title}"
date = {today}
draft = true

[extra]
kind = "{kind}"
numeral = "{numeral}"
status = "staging"
lifespan = "Lives ..."
cover = ""
cover_alt = ""
cover_tag = "{label} {numeral}"
deck = ""
dateline = "Truth or Consequences, New Mexico · 33.13° N, 107.25° W"
ornament = "❦"
sign_off = ""
+++

<!--
  STAGED EDITION — invisible in production builds (draft = true).
  Build in real time:   ./scripts/edition.sh serve
  Preview at:           http://127.0.0.1:1111/editions/{slug}/
  Go live:              ./scripts/edition.sh promote {slug}

  Vocabulary: plate, diptych, wallquote, marginalia, interlude (see an
  earlier edition's index.md for usage). Drop an edition.css next to this
  file for per-edition art direction.
-->

Begin here.
''')
print(f"created {target}/index.md  ({label} {numeral}, staging)")
print(f"  build:    ./scripts/edition.sh serve")
print(f"  preview:  http://127.0.0.1:1111/editions/{slug}/")
PYEOF
    ;;

  promote)
    slug="${2:?usage: edition.sh promote <slug>}"
    python3 - "$slug" << 'PYEOF'
import sys, re
from pathlib import Path
from datetime import date

slug = sys.argv[1]
editions = Path("content/editions")
target = editions / slug / "index.md"
if not target.exists():
    sys.exit(f"error: {target} not found")

today = date.today().isoformat()

def front_matter(text):
    m = re.match(r"^\+\+\+\n(.*?)\n\+\+\+", text, re.S)
    return m.group(1) if m else ""

def set_status(text, status):
    return re.sub(r'(^status\s*=\s*")[^"]*(")', rf'\g<1>{status}\g<2>', text, count=1, flags=re.M)

# retire whichever edition is currently live
for d in sorted(editions.iterdir()):
    f = d / "index.md"
    if not f.is_file() or d.name == slug: continue
    text = f.read_text()
    fm = front_matter(text)
    if re.search(r'^status\s*=\s*"live"', fm, re.M):
        new = set_status(text, "retired")
        if not re.search(r'^retired\s*=', fm, re.M):
            new = re.sub(r'(^status\s*=\s*"retired")', rf'\g<1>\nretired = "{today}"', new, count=1, flags=re.M)
        # flip the display tense: "Lives ..." -> "lived ..."
        new = re.sub(r'(^lifespan\s*=\s*")Lives\b', r'\g<1>lived', new, count=1, flags=re.M)
        f.write_text(new)
        print(f"retired:  {d.name}")

# promote the target
text = target.read_text()
text = set_status(text, "live")
text = re.sub(r'^draft\s*=\s*true\n', '', text, count=1, flags=re.M)
if not re.search(r'^published\s*=', front_matter(text), re.M):
    text = re.sub(r'(^status\s*=\s*"live")', rf'\g<1>\npublished = "{today}"', text, count=1, flags=re.M)
target.write_text(text)
print(f"now live: {slug}")
print("rebuild + deploy to publish the new front page.")
PYEOF
    ;;

  list)
    python3 << 'PYEOF'
import re
from pathlib import Path

editions = Path("content/editions")
rows = []
for d in sorted(editions.iterdir()):
    f = d / "index.md"
    if not f.is_file(): continue
    text = f.read_text()
    m = re.match(r"^\+\+\+\n(.*?)\n\+\+\+", text, re.S)
    fm = m.group(1) if m else ""
    def get(key, default=""):
        mm = re.search(rf'^{key}\s*=\s*"([^"]*)"', fm, re.M)
        return mm.group(1) if mm else default
    draft = bool(re.search(r'^draft\s*=\s*true', fm, re.M))
    rows.append((d.name, get("numeral"), get("kind"), get("status"), "draft" if draft else "", get("title")))

if not rows:
    print("no editions yet — ./scripts/edition.sh new <slug> \"<Title>\"")
else:
    w = max(len(r[0]) for r in rows)
    for slug, numeral, kind, status, draft, title in rows:
        flag = {"live": "●", "staging": "○", "retired": "·"}.get(status, "?")
        print(f"  {flag} {slug:<{w}}  {numeral:>5}  {kind:<8}{status:<9}{draft:<7}{title}")
PYEOF
    ;;

  serve)
    python3 scripts/update_recently_edited.py
    exec zola serve --drafts
    ;;

  *)
    sed -n '2,7p' "$0"
    ;;
esac
