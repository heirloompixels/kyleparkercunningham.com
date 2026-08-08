#!/usr/bin/env python3
"""Read content/oeuvre/ into a list of work records, and join them to the tag data.

A record is everything the tagging pass needs to see about one work: its front
matter, its body prose with shortcodes stripped, and every image with its alt text.

Records are keyed by repo-relative path (`content/oeuvre/.../index.md`), never by
position — works get added and the ordering shifts, but the path is stable. This is
also the key used by tags.jsonl.

Usage:  python3 scripts/tagging/works.py          # summary of what's on disk
        python3 scripts/tagging/works.py --json   # full records to stdout
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OEUVRE = ROOT / "content" / "oeuvre"
TAGS = Path(__file__).resolve().parent / "tags.jsonl"

# Section landing pages that are themselves a work (a project rather than an
# object) and so carry their own tags. Everything else named _index.md is a
# plain section index and is skipped.
PROJECT_INDEXES = {
    "content/oeuvre/philosophy/2026/meaning-is-use/_index.md",
}

SHORTCODE_RE = re.compile(r"\{\{.*?\}\}", re.S)
ART_IMAGE_RE = re.compile(r"art_image\((.*?)\)\s*\}\}", re.S)


def _scalar(fm: str, key: str) -> str:
    m = re.search(r'^%s\s*=\s*"?([^"\n]*)"?\s*$' % re.escape(key), fm, re.M)
    return m.group(1).strip() if m else ""


def parse(path: Path) -> dict:
    src = path.read_text(encoding="utf-8")
    parts = src.split("+++")
    fm = parts[1] if len(parts) > 2 else ""
    body = "+++".join(parts[2:]).strip()

    images = []
    for m in ART_IMAGE_RE.finditer(src):
        args = m.group(1)
        p = re.search(r'path="([^"]+)"', args)
        alt = re.search(r'alt="([^"]*)"', args, re.S)
        cap = re.search(r'caption="([^"]*)"', args, re.S)
        images.append({
            "path": p.group(1) if p else "",
            "alt": " ".join((alt.group(1) if alt else "").split()),
            "caption": (cap.group(1) if cap else "").strip(),
        })

    # Project landing pages carry a dateline rather than a `year`; fall back to
    # the year in the path, which is where the oeuvre tree keeps it anyway.
    year = _scalar(fm, "year")
    if not year:
        m = re.search(r"/((?:19|20)\d{2})/", str(path))
        year = m.group(1) if m else ""

    return {
        "file": str(path.relative_to(ROOT)),
        "title": _scalar(fm, "title"),
        "year": year,
        "weight": _scalar(fm, "weight"),
        "date": _scalar(fm, "date"),
        "category": _scalar(fm, "category"),
        "medium": _scalar(fm, "medium"),
        "dimensions": _scalar(fm, "dimensions"),
        "status": _scalar(fm, "status"),
        "prose": SHORTCODE_RE.sub("", body).strip(),
        "images": images,
        "has_tags": "[taxonomies]" in fm,
    }


def load_works() -> list[dict]:
    """Every tag-bearing page under content/oeuvre/, sorted by path."""
    paths = [p for p in OEUVRE.rglob("index.md")]
    paths += [ROOT / rel for rel in PROJECT_INDEXES]
    return sorted((parse(p) for p in paths), key=lambda w: w["file"])


def load_tags() -> dict[str, dict]:
    """tags.jsonl keyed by repo-relative path. Empty dict if not written yet."""
    if not TAGS.exists():
        return {}
    rows = {}
    for line in TAGS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            rows[r["file"]] = r
    return rows


def load_joined() -> tuple[list[dict], list[str], list[str]]:
    """Returns (works with `note`/`tags`/`canon` attached, untagged, orphaned).

    untagged = work pages with no row in tags.jsonl (newly added work).
    orphaned = rows in tags.jsonl whose page no longer exists (renamed/deleted).
    """
    from vocabulary import canon

    works = load_works()
    tags = load_tags()
    joined, untagged = [], []
    for w in works:
        row = tags.get(w["file"])
        if row is None:
            untagged.append(w["file"])
            continue
        w["note"] = row["note"]
        w["tags"] = row["tags"]
        w["canon"] = canon(row["tags"])
        joined.append(w)
    orphaned = sorted(set(tags) - {w["file"] for w in works})
    return joined, untagged, orphaned


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    joined, untagged, orphaned = load_joined()
    if "--json" in sys.argv:
        json.dump(joined, sys.stdout, indent=1, ensure_ascii=False)
        sys.exit(0)

    from collections import Counter
    print(f"tagged works:     {len(joined)}")
    print(f"by category:      {dict(Counter(w['category'] or '—' for w in joined))}")
    print(f"images:           {sum(len(w['images']) for w in joined)}")
    print(f"prose words:      {sum(len(w['prose'].split()) for w in joined):,}")
    print(f"already applied:  {sum(1 for w in joined if w['has_tags'])} pages carry [taxonomies]")
    if untagged:
        print(f"\nUNTAGGED ({len(untagged)}) — new work needing a tags.jsonl row:")
        for f in untagged:
            print("  ", f)
    if orphaned:
        print(f"\nORPHANED ({len(orphaned)}) — tags.jsonl rows with no page:")
        for f in orphaned:
            print("  ", f)
