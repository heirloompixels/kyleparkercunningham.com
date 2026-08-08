#!/usr/bin/env python3
"""Downscale each work's main image into a scratch directory for visual review.

Tagging needs the images looked at, not just their alt text — palette, surface,
composition and scale don't survive into prose. Full-size masters are far too heavy
to read in bulk, so this writes a ~480px copy of each work's first `art_image`,
named by an index that matches the order `works.py` reports.

Output goes to .tagging-review/ at the repo root (gitignored, safe to delete).

Requires ImageMagick (`brew install imagemagick`).

Usage:  python3 scripts/tagging/review_images.py [--all] [--size 480]
        --all   every image on every work, not just the first
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from works import ROOT, load_works   # noqa: E402

OUTDIR = ROOT / ".tagging-review"
CONTENT = ROOT / "content"

SIZE = 480
if "--size" in sys.argv:
    SIZE = int(sys.argv[sys.argv.index("--size") + 1])
ALL = "--all" in sys.argv


def main() -> int:
    if not subprocess.run(["which", "magick"], capture_output=True).stdout:
        print("ImageMagick not found — brew install imagemagick")
        return 1

    OUTDIR.mkdir(exist_ok=True)
    (OUTDIR / ".gitignore").write_text("*\n", encoding="utf-8")

    works = load_works()
    made = skipped = missing = 0
    index = []
    for i, work in enumerate(works):
        images = work["images"] if ALL else work["images"][:1]
        for j, image in enumerate(images):
            src = CONTENT / image["path"]
            if not src.exists():
                missing += 1
                print(f"  missing: {image['path']}  ({work['file']})")
                continue
            out = OUTDIR / (f"{i:03d}_{j}.jpg" if ALL else f"{i:03d}.jpg")
            index.append(f"{out.name}\t{work['title']}\t{work['file']}")
            if out.exists():
                skipped += 1
                continue
            subprocess.run(
                ["magick", f"{src}[0]", "-resize", f"{SIZE}x{SIZE}>", "-quality", "80", str(out)],
                check=False, capture_output=True,
            )
            made += 1

    (OUTDIR / "index.tsv").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"{OUTDIR.relative_to(ROOT)}/ — {made} written, {skipped} already present, "
          f"{missing} missing source")
    print(f"index.tsv maps each file back to its work.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
