#!/usr/bin/env python3
"""Download and unpack the open-source icon sets into .icon-sets/ (gitignored).

The sets are ~350 MB unpacked, so they are fetched rather than committed. Only the
alias table in aliases.py is repo state; everything downloaded here is disposable.

Versions float deliberately — an icon set gaining icons is good news, and the
matcher degrades gracefully when a name disappears. If a licence changes on
upgrade, `aliases.SETS` is the record to correct.

Usage:  python3 scripts/tag-icons/fetch_sets.py [--force]
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[1]
WORK = ROOT / ".icon-sets"

from aliases import SETS  # noqa: E402

FORCE = "--force" in sys.argv


def main() -> int:
    if shutil.which("npm") is None:
        print("npm not found — needed to fetch the icon packages.")
        return 1

    WORK.mkdir(exist_ok=True)
    (WORK / ".gitignore").write_text("*\n", encoding="utf-8")

    got, skipped, failed = 0, 0, []
    for pkg, (label, licence, _obligation) in SETS.items():
        stem = pkg.replace("@", "").replace("/", "-")
        existing = sorted(WORK.glob(f"{stem}-*/package/package.json"))
        if existing and not FORCE:
            skipped += 1
            continue

        r = subprocess.run(["npm", "pack", pkg, "--silent"],
                           cwd=WORK, capture_output=True, text=True)
        if r.returncode != 0:
            failed.append((pkg, r.stderr.strip().splitlines()[-1:] or ["unknown error"]))
            continue
        tgz = next(iter(sorted(WORK.glob(f"{stem}-*.tgz"))), None)
        if tgz is None:
            failed.append((pkg, ["npm pack produced no tarball"]))
            continue
        dest = WORK / tgz.stem
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir()
        with tarfile.open(tgz) as tf:
            tf.extractall(dest, filter="data")
        tgz.unlink()
        got += 1
        print(f"  {label:16s} {licence}")

    print(f"\nfetched {got}, already present {skipped}"
          + (f", failed {len(failed)}" if failed else ""))
    for pkg, why in failed:
        print(f"  FAILED {pkg}: {why[0]}")

    # Re-read every licence from the packages themselves and flag drift.
    drift = []
    for pkg, (label, licence, _o) in SETS.items():
        stem = pkg.replace("@", "").replace("/", "-")
        pj = next(iter(sorted(WORK.glob(f"{stem}-*/package/package.json"))), None)
        if not pj:
            continue
        actual = json.loads(pj.read_text(encoding="utf-8")).get("license", "?")
        if actual != licence:
            drift.append((label, licence, actual))
    if drift:
        print("\nLICENCE DRIFT — update aliases.SETS and re-check the obligations:")
        for label, was, now in drift:
            print(f"  {label}: recorded {was}, package says {now}")
    else:
        print("licences match aliases.SETS")

    total = sum(1 for _ in WORK.rglob("*.svg"))
    print(f"{total:,} svg files under {WORK.relative_to(ROOT)}/")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
