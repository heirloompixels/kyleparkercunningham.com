#!/usr/bin/env python3
"""Point the built site's own links at the final address of what they name.

    python3 scripts/finalize_links.py      # after scripts/redirects.py

Every page that moved to the archive answers 301 (public/_redirects), so an
old link still works, but it costs the reader a hop and tells a crawler the
link is stale. Kyle, 2026-10-15: "everything gets updated to the final
source". This rewrites each `<a href>` in public/ whose target is a
redirected address to the redirect's own target, so the site links straight
to the archive page. It runs on the build, never on content/: the content
keeps naming the site's own pages, and a later change to where the archive
keeps something is picked up by the next build with nothing to edit.

Only anchors are rewritten. A page's canonical, its feeds and works.json (the
river service syncs that by the site's own slugs) keep the site's addresses.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
ORIGIN = "https://kyleparkercunningham.com"
ANCHOR = re.compile(r"(<a\b[^>]*?\bhref=)([\"'])(.*?)\2", re.S | re.I)


def main() -> int:
    rules = PUBLIC / "_redirects"
    if not rules.exists():
        sys.exit("public/_redirects is missing; run scripts/redirects.py first")
    to: dict[str, str] = {}
    for line in rules.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[0].startswith("/") and not line.startswith("#"):
            to[parts[0].rstrip("/") or "/"] = parts[1]

    def final(href: str) -> str | None:
        # Zola's templates escape some hrefs (`&#x2F;` for `/`); match the URL.
        href = html.unescape(href)
        path = href[len(ORIGIN):] if href.startswith(ORIGIN + "/") else href
        if not path.startswith("/") or path.startswith("//"):
            return None
        bare, sep, frag = path.partition("#")
        bare = bare.split("?", 1)[0]
        dst = to.get(bare.rstrip("/") or "/")
        return None if dst is None else dst + (sep + frag if sep else "")

    pages = changed = links = 0
    for page in PUBLIC.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        count = 0

        def swap(m: re.Match) -> str:
            nonlocal count
            dst = final(m.group(3))
            if dst is None:
                return m.group(0)
            count += 1
            return f"{m.group(1)}{m.group(2)}{html.escape(dst, quote=True)}{m.group(2)}"

        new = ANCHOR.sub(swap, text)
        pages += 1
        if count:
            page.write_text(new, encoding="utf-8")
            changed += 1
            links += count
    print(f"links: {links} on {changed} of {pages} pages now name the final address")
    return 0


if __name__ == "__main__":
    sys.exit(main())
