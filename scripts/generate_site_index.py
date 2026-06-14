#!/usr/bin/env python3
"""Walk the content tree and emit data/site_index.json — every rendered page,
grouped, with an authorship tag read from `extra.author`.

Authorship is by PROSE: who wrote the visible words on the page.
  - "kyle"      (default) — Kyle's writing
  - "claude"    — prose written by Claude (set explicitly in front matter)
  - "structure" — no authored prose at all (section indexes, generated views);
                  derived automatically, never a person.

Mirrors update_recently_edited.py (same permalink/title logic). Runs at build
time; the manifest template loads the JSON via load_data().
"""
from __future__ import annotations

import json
import re
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
OUTPUT = ROOT / "data" / "site_index.json"

FRONTMATTER_RE = re.compile(r"^\+\+\+\s*$")

# First path segment -> display group. Anything else falls to "Other pages".
GROUPS = {
    "oeuvre": "Oeuvre",
    "projects": "Projects",
    "editions": "Editions",
    "log": "Log",
    "cinema": "Cinema",
    "about": "About & information",
    "installations": "Installations",
}
GROUP_ORDER = ["Home", "Oeuvre", "Projects", "Editions", "Log", "Cinema",
               "About & information", "Installations", "Other pages"]


def split_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not FRONTMATTER_RE.match(lines[0]):
        return {}, text
    for i in range(1, len(lines)):
        if FRONTMATTER_RE.match(lines[i]):
            raw = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1:])
            try:
                return tomllib.loads(raw), body
            except tomllib.TOMLDecodeError:
                return {}, body
    return {}, text


def permalink_for(rel: Path) -> str:
    if rel.name == "_index.md":
        return "/" if rel.parent == Path(".") else f"/{rel.parent.as_posix()}/"
    if rel.name == "index.md":
        return f"/{rel.parent.as_posix()}/"
    return f"/{rel.with_suffix('').as_posix()}/"


def title_for(rel: Path, fm: dict) -> str:
    if fm.get("title"):
        return str(fm["title"])
    if rel.name == "_index.md" and rel.parent == Path("."):
        return "Home"
    return rel.parent.name.replace("-", " ").replace("_", " ").title()


def has_prose(body: str) -> bool:
    """True if the body has human-written words once shortcodes / template tags /
    HTML / comments are stripped out."""
    b = re.sub(r"\{\{.*?\}\}", " ", body, flags=re.S)   # {{ shortcode() }}
    b = re.sub(r"\{%.*?%\}", " ", b, flags=re.S)         # {% block %}
    b = re.sub(r"<!--.*?-->", " ", b, flags=re.S)        # comments
    b = re.sub(r"<[^>]+>", " ", b)                        # html tags
    return bool(re.sub(r"\s+", "", b))


def author_for(rel: Path, fm: dict, body: str) -> str:
    extra = fm.get("extra", {}) or {}
    explicit = extra.get("author")
    if explicit in ("kyle", "claude", "structure"):
        return explicit
    # No authored prose on a section index or generated view -> structural.
    if not has_prose(body) and (rel.name == "_index.md" or rel.stem == "dashboard"):
        return "structure"
    return "kyle"


def main() -> None:
    entries = []
    for md in CONTENT.rglob("*.md"):
        rel = md.relative_to(CONTENT)
        fm, body = split_frontmatter(md)
        if fm.get("draft") is True:
            continue  # excluded from production builds
        seg = rel.parts[0] if rel.parts and rel.name != "_index.md" or len(rel.parts) > 1 else "home"
        first = rel.parts[0] if rel.name != "_index.md" or rel.parent != Path(".") else "home"
        group = "Home" if (rel.name == "_index.md" and rel.parent == Path(".")) \
            else GROUPS.get(first, "Other pages")
        entries.append({
            "title": title_for(rel, fm),
            "permalink": permalink_for(rel),
            "path": rel.parent.as_posix() if rel.parent != Path(".") else "",
            "group": group,
            "author": author_for(rel, fm, body),
            "is_section": rel.name == "_index.md",
        })

    # stable sort: group order, then sections first, then title
    entries.sort(key=lambda e: (
        GROUP_ORDER.index(e["group"]) if e["group"] in GROUP_ORDER else len(GROUP_ORDER),
        not e["is_section"],
        e["path"],
        e["title"].lower(),
    ))

    totals = {"kyle": 0, "claude": 0, "structure": 0}
    for e in entries:
        totals[e["author"]] += 1

    OUTPUT.write_text(json.dumps({
        "generated": True,
        "total": len(entries),
        "totals": totals,
        "group_order": GROUP_ORDER,
        "pages": entries,
    }, indent=2), encoding="utf-8")
    print(f"site_index.json: {len(entries)} pages "
          f"({totals['kyle']} kyle, {totals['claude']} claude, {totals['structure']} structure)")


if __name__ == "__main__":
    main()
