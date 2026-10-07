#!/usr/bin/env python3
"""Write data/recently_edited.json: every rendered content page, newest edit
first, for the dashboard. Permalinks follow Zola's rules and dates come from
git (see zola_paths.py)."""
from __future__ import annotations

import json

from zola_paths import CONTENT, ROOT, git_updated, is_rendered, permalink_for, split_frontmatter, title_for

OUTPUT = ROOT / "data" / "recently_edited.json"


def main() -> None:
    pages = []
    for md in sorted(CONTENT.rglob("*.md")):
        rel = md.relative_to(CONTENT)
        fm, _ = split_frontmatter(md)
        if not is_rendered(rel, fm):
            continue
        pages.append({"title": title_for(rel, fm), "permalink": permalink_for(rel, fm),
                      "updated": git_updated(md)})
    pages.sort(key=lambda p: (p["updated"], p["permalink"]), reverse=True)
    OUTPUT.write_text(json.dumps(pages, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
