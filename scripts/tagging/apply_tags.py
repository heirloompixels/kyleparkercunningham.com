#!/usr/bin/env python3
"""Write canonical tags into the `[taxonomies]` block of each oeuvre page.

Idempotent and re-runnable: the block is fully rewritten from tags.jsonl +
vocabulary.py every time, so changing a merge rule and re-running propagates the
change to every affected page. Never hand-edit a `[taxonomies]` block — it will be
overwritten. Edit tags.jsonl instead.

Placement follows the existing front-matter convention: `[taxonomies]` goes after
the scalar keys and before `[extra]`.

Requires `tags` to be declared in config.toml:

    taxonomies = [
      {name = "topics", feed = true},
      {name = "tags", feed = true},
    ]

Dry run by default; pass --apply to write.

Usage:  python3 scripts/tagging/apply_tags.py [--apply] [--only PATH_FRAGMENT]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from works import ROOT, load_joined   # noqa: E402

APPLY = "--apply" in sys.argv
ONLY = None
if "--only" in sys.argv:
    ONLY = sys.argv[sys.argv.index("--only") + 1]

TAXONOMIES_BLOCK = re.compile(r"\n\[taxonomies\]\n(?:(?!\n\[).)*", re.S)
WRAP = 76


def render(tags: list[str]) -> str:
    """A `[taxonomies]` block, wrapped so long tag lists stay readable."""
    inline = "tags = [" + ", ".join(f'"{t}"' for t in tags) + "]"
    if len(inline) <= WRAP:
        return "[taxonomies]\n" + inline + "\n"

    lines, current = [], "  "
    for tag in tags:
        piece = f'"{tag}",'
        if current != "  " and len(current) + len(piece) > WRAP:
            lines.append(current.rstrip())
            current = "  "
        current += piece + " "
    lines.append(current.rstrip().rstrip(","))
    return "[taxonomies]\ntags = [\n" + "\n".join(lines) + "\n]\n"


def splice(src: str, block: str) -> str:
    """Insert or replace the [taxonomies] block inside the front matter."""
    open_i = src.index("+++")
    close_i = src.index("+++", open_i + 3)
    fm = src[open_i + 3:close_i]
    rest = src[close_i:]

    if "[taxonomies]" in fm:
        fm = TAXONOMIES_BLOCK.sub("\n" + block, fm, count=1)
    elif "\n[extra]" in fm:
        fm = fm.replace("\n[extra]", "\n" + block + "\n[extra]", 1)
    else:
        fm = fm.rstrip("\n") + "\n\n" + block
    return src[:open_i] + "+++" + fm + rest


def main() -> int:
    works, untagged, orphaned = load_joined()
    if orphaned:
        print(f"ERROR: {len(orphaned)} tags.jsonl row(s) point at pages that don't exist.")
        for f in orphaned:
            print("   ", f)
        print("Fix tags.jsonl before applying.")
        return 1

    changed = unchanged = 0
    sections = []
    for work in works:
        if ONLY and ONLY not in work["file"]:
            continue
        # Zola only accepts [taxonomies] on pages, not sections — a section
        # _index.md fails the build with "unknown field `taxonomies`". Project-type
        # works are sections, so their row stays in tags.jsonl (it feeds the
        # manifest) but is never written to the page.
        if work["file"].endswith("_index.md"):
            sections.append(work["file"])
            continue
        path = ROOT / work["file"]
        src = path.read_text(encoding="utf-8")
        out = splice(src, render(work["canon"]))
        if out == src:
            unchanged += 1
            continue
        changed += 1
        if APPLY:
            path.write_text(out, encoding="utf-8")
        else:
            print(f"\n--- {work['file']}")
            print(render(work["canon"]).rstrip())

    verb = "wrote" if APPLY else "would change"
    print(f"\n{verb} {changed} page(s); {unchanged} already current.")
    if sections:
        print(f"{len(sections)} section _index.md skipped (Zola takes taxonomies on "
              f"pages only):")
        for f in sections:
            print("   ", f)
    if untagged:
        print(f"{len(untagged)} page(s) have no tags.jsonl row and were skipped:")
        for f in untagged:
            print("   ", f)
    if not APPLY:
        print("Dry run — pass --apply to write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
