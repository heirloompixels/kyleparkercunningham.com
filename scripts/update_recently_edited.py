#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
OUTPUT = ROOT / "data" / "recently_edited.json"

FRONTMATTER_RE = re.compile(r"^\+\+\+\s*$")


@dataclass
class Page:
    title: str
    permalink: str
    updated: str


def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not FRONTMATTER_RE.match(lines[0]):
        return {}
    # find closing +++
    for i in range(1, len(lines)):
        if FRONTMATTER_RE.match(lines[i]):
            raw = "\n".join(lines[1:i])
            try:
                return tomllib.loads(raw)
            except tomllib.TOMLDecodeError:
                return {}
    return {}


def permalink_for(path: Path) -> str:
    rel = path.relative_to(CONTENT)
    if rel.name == "_index.md":
        if rel.parent == Path("."):
            return "/"
        return f"/{rel.parent.as_posix()}/"
    if rel.name == "index.md":
        return f"/{rel.parent.as_posix()}/"
    return f"/{rel.with_suffix('').as_posix()}/"


def title_for(path: Path, frontmatter: dict) -> str:
    title = frontmatter.get("title")
    if title:
        return str(title)
    if path.name == "_index.md" and path.parent == CONTENT:
        return "Home"
    return path.parent.name.replace("-", " ").title()


def iso_time(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def main() -> None:
    pages: list[Page] = []
    for md in CONTENT.rglob("*.md"):
        frontmatter = read_frontmatter(md)
        title = title_for(md, frontmatter)
        permalink = permalink_for(md)
        updated = iso_time(md.stat().st_mtime)
        pages.append(Page(title=title, permalink=permalink, updated=updated))

    pages.sort(key=lambda p: p.updated, reverse=True)
    data = [page.__dict__ for page in pages]
    OUTPUT.write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
