#!/usr/bin/env python3
"""Index the downloaded sets: icon name -> svg body, per style.

Only line/outline styles are kept, plus Material-flat and OpenMoji-colour as the
two deliberate non-line options. Bodies are stripped of their <svg> wrapper so the
mockup can re-emit them at a common size with currentColor.

Writes .icon-sets/index.json (~30 MB, gitignored).

Usage:  python3 scripts/tag-icons/index_sets.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORK = ROOT / ".icon-sets"
OUT = WORK / "index.json"

# style key -> (glob under .icon-sets/, style class, viewBox, colour mode)
STYLES = {
    "lucide":        ("lucide-static-*/package/icons/*.svg",              "line", "0 0 24 24",   "stroke"),
    "tabler":        ("tabler-icons-*/package/icons/outline/*.svg",       "line", "0 0 24 24",   "stroke"),
    "phosphor":      ("phosphor-icons-core-*/package/assets/regular/*.svg", "line", "0 0 256 256", "fill"),
    "phosphor-thin": ("phosphor-icons-core-*/package/assets/thin/*.svg",  "line", "0 0 256 256", "fill"),
    "feather":       ("feather-icons-*/package/dist/icons/*.svg",         "line", "0 0 24 24",   "stroke"),
    "heroicons":     ("heroicons-*/package/24/outline/*.svg",             "line", "0 0 24 24",   "stroke"),
    "iconoir":       ("iconoir-*/package/icons/regular/*.svg",            "line", "0 0 24 24",   "stroke"),
    "bootstrap":     ("bootstrap-icons-*/package/icons/*.svg",            "flat", "0 0 16 16",   "fill"),
    "remix":         ("remixicon-*/package/icons/*/*-line.svg",           "line", "0 0 24 24",   "fill"),
    "mdi":           ("mdi-svg-*/package/svg/*.svg",                      "flat", "0 0 24 24",   "fill"),
}

BODY = re.compile(r"<svg[^>]*>(.*)</svg>", re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)
TITLE = re.compile(r"<(title|desc)>.*?</\1>", re.S)


def body_of(path: Path) -> str | None:
    src = COMMENT.sub("", path.read_text(encoding="utf-8", errors="ignore"))
    m = BODY.search(src)
    if not m:
        return None
    return TITLE.sub("", m.group(1)).strip() or None


def norm(name: str) -> str:
    n = name.lower()
    for suffix in ("-line", "-outline", "-thin", "-24", "-2"):
        if n.endswith(suffix):
            n = n[: -len(suffix)]
    return n.replace("_", "-").strip("-")


def main() -> int:
    if not WORK.exists():
        print("No .icon-sets/ — run scripts/tag-icons/fetch_sets.py first.")
        return 1

    index = {}
    for key, (glob, style, viewbox, mode) in STYLES.items():
        entries = {}
        for p in sorted(WORK.glob(glob)):
            b = body_of(p)
            if b:
                entries.setdefault(norm(p.stem), {"raw": p.stem, "body": b})
        if not entries:
            print(f"  {key:16s} — nothing matched {glob}")
            continue
        index[key] = {"style": style, "viewBox": viewbox, "mode": mode, "icons": entries}
        print(f"  {key:16s} {len(entries):6,d}  ({style})")

    # OpenMoji filenames are codepoints; map them through its own annotations.
    om = next(iter(sorted(WORK.glob("openmoji-*/package"))), None)
    if om:
        meta = json.loads((om / "data" / "openmoji.json").read_text(encoding="utf-8"))
        for variant, style in (("black", "line"), ("color", "colour")):
            entries = {}
            for row in meta:
                hexcode, ann = row.get("hexcode"), (row.get("annotation") or "").lower().strip()
                if not hexcode or not ann:
                    continue
                p = om / variant / "svg" / f"{hexcode}.svg"
                if not p.exists():
                    continue
                b = body_of(p)
                if not b:
                    continue
                key_name = ann.replace(" ", "-").replace(":", "").replace(",", "")
                entries.setdefault(key_name, {"raw": ann, "body": b, "emoji": row.get("emoji", "")})
            index[f"openmoji-{variant}"] = {
                "style": style, "viewBox": "0 0 72 72",
                "mode": "stroke" if variant == "black" else "fill", "icons": entries,
            }
            print(f"  {'openmoji-' + variant:16s} {len(entries):6,d}  ({style})")

    OUT.write_text(json.dumps(index), encoding="utf-8")
    total = sum(len(v["icons"]) for v in index.values())
    print(f"\nindexed {total:,} icons across {len(index)} styles "
          f"-> {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1048576:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
