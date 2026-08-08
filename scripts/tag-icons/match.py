#!/usr/bin/env python3
"""Match oeuvre tags to candidate icons across every indexed style.

Matching is name-based: the literal tag name first, then each alias in order, then
the tag's last word as a long shot. Candidates are capped per style so one huge set
(Tabler, Material) can't crowd out the rest — the point of the sheet is comparison.

Run bare for a coverage report; import `candidates()` from build_mockup.py.

Usage:  python3 scripts/tag-icons/match.py [--gaps]
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts" / "tagging"))

from aliases import ALIASES  # noqa: E402

INDEX_PATH = ROOT / ".icon-sets" / "index.json"
_index_cache = None


def index():
    global _index_cache
    if _index_cache is None:
        if not INDEX_PATH.exists():
            raise SystemExit("No .icon-sets/index.json — run fetch_sets.py then index_sets.py.")
        _index_cache = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return _index_cache


def tag_counts():
    """Canonical tag -> number of works, straight from the tagging pipeline."""
    from works import load_joined
    works, _, _ = load_joined()
    return collections.Counter(t for w in works for t in w["canon"])


def lookup(name):
    return [(k, v["icons"][name]) for k, v in index().items() if name in v["icons"]]


def candidates(tag, per_style_cap=2, total_cap=14):
    """Ranked icon options for one tag, spread across styles."""
    names = [tag.replace(" ", "-")] + ALIASES.get(tag, [])
    if " " in tag:
        names.append(tag.split()[-1])
    seen, out, per = set(), [], collections.Counter()
    for nm in names:
        for skey, e in lookup(nm):
            sig = (skey, e["raw"])
            if sig in seen or per[skey] >= per_style_cap:
                continue
            seen.add(sig)
            per[skey] += 1
            s = index()[skey]
            out.append({"set": skey, "style": s["style"], "viewBox": s["viewBox"],
                        "mode": s["mode"], "name": e["raw"], "query": nm,
                        "body": e["body"], "emoji": e.get("emoji", "")})
            if len(out) >= total_cap:
                return out
    return out


def main() -> int:
    counts = tag_counts()
    matched, empty = {}, []
    for tag, n in counts.most_common():
        opts = candidates(tag)
        (matched.setdefault(tag, {"count": n, "options": opts}) if opts
         else empty.append((n, tag)))
    print(f"tags with at least one candidate: {len(matched)} / {len(counts)}")
    print(f"mean options per matched tag: "
          f"{sum(len(v['options']) for v in matched.values()) / max(1, len(matched)):.1f}")
    print(f"tags with none: {len(empty)}")
    if "--gaps" in sys.argv:
        print("\nunmatched, by works:")
        for n, t in sorted(empty, reverse=True):
            print(f"  {n:3d}  {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
