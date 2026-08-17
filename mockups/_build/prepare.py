#!/usr/bin/env python3
"""Build the sketchbook dataset.

Joins three sources into one JSON file the mockup generators read:

  1. the oeuvre database (archive.kyleparkercunningham.com), dumped to
     _build/raw/*.json by the MCP connector — titles, years, media, real
     dimensions, dominant colours, palettes, tags, relations;
  2. the work images living in content/oeuvre/<discipline>/<year>/<slug>/;
  3. colour analysis computed here from the pixels — hue/lightness/chroma
     for sorting, and a 6x6 average-colour grid per work.

It also writes web-sized derivatives into assets/w (1280px) and
assets/t (420px) as WebP, so a mockup can show 159 works without the
directory turning into a gigabyte.

    python3 mockups/_build/prepare.py
"""

import colorsys
import json
import os
import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
BUILD = ROOT / "mockups" / "_build"
RAW = BUILD / "raw"
ASSETS = ROOT / "mockups" / "assets"
WIDE = ASSETS / "w"
THUMB = ASSETS / "t"
OUT = BUILD / "oeuvre.json"

WIDE_MAX = 1280
THUMB_MAX = 420
GRID = 6


def load_table(name):
    """Read one of the MCP query dumps: {columns: [...], rows: [[...]]}."""
    data = json.loads((RAW / name).read_text())
    cols = data["columns"]
    out = []
    for row in data["rows"]:
        rec = {}
        for k, v in zip(cols, row):
            rec[k] = None if v == "NULL" else v
        out.append(rec)
    return out


def pick_image(bundle: Path, slug: str):
    """Choose the best photograph in a work's bundle.

    Prefers a filename that echoes the slug, then the largest file, and
    skips anything that reads as a detail/progress/wall shot when a plain
    view exists.
    """
    cands = [
        p
        for p in sorted(bundle.iterdir())
        if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
    ]
    if not cands:
        return None
    key = slug.replace("-", "").replace("_", "").lower()

    def score(p):
        stem = p.stem.replace("-", "").replace("_", "").lower()
        s = 0
        if key and key in stem:
            s -= 100
        if stem in key:
            s -= 60
        for bad in ("close", "progress", "wall", "detail", "install", "phase"):
            if bad in stem:
                s += 40
        s -= min(p.stat().st_size // 100_000, 20)
        return s

    return sorted(cands, key=score)[0]


def analyse(img: Image.Image):
    """Colour facts a mockup can sort and draw with."""
    rgb = img.convert("RGB")

    small = rgb.resize((GRID, GRID), Image.LANCZOS)
    grid = ["#%02x%02x%02x" % small.getpixel((x, y)) for y in range(GRID) for x in range(GRID)]

    # Dominant colours by quantisation, ordered by area.
    q = rgb.resize((160, 160), Image.LANCZOS).quantize(colors=6, method=Image.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    swatches = []
    for count, idx in counts:
        r, g, b = pal[idx * 3 : idx * 3 + 3]
        swatches.append({"hex": "#%02x%02x%02x" % (r, g, b), "share": round(count / 25600, 3)})

    # Average colour in HSL, for hue sorting. Averaging hues naively wraps
    # badly at red, so average the unit vectors instead.
    import math

    tiny = rgb.resize((48, 48), Image.LANCZOS)
    xs = ys = 0.0
    sat = lig = 0.0
    n = 48 * 48
    for px in tiny.getdata():
        h, l, s = colorsys.rgb_to_hls(px[0] / 255, px[1] / 255, px[2] / 255)
        weight = s  # grey pixels shouldn't vote on hue
        xs += math.cos(h * 2 * math.pi) * weight
        ys += math.sin(h * 2 * math.pi) * weight
        sat += s
        lig += l
    hue = (math.degrees(math.atan2(ys, xs)) + 360) % 360
    return {
        "grid": grid,
        "swatches": swatches[:5],
        "hue": round(hue, 1),
        "sat": round(sat / n, 3),
        "lig": round(lig / n, 3),
        "chroma": round(math.hypot(xs, ys) / n, 3),
    }


def derive(src: Path, slug: str):
    img = Image.open(src)
    img.load()
    if img.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        conv = img.convert("RGBA")
        bg.paste(conv, mask=conv.split()[-1])
        img = bg
    else:
        img = img.convert("RGB")

    w, h = img.size
    facts = analyse(img)

    for target, folder, quality in ((WIDE_MAX, WIDE, 74), (THUMB_MAX, THUMB, 70)):
        dest = folder / f"{slug}.webp"
        if dest.exists():
            continue
        scale = min(1.0, target / max(w, h))
        out = img if scale == 1.0 else img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        out.save(dest, "WEBP", quality=quality, method=5)

    facts["w"] = w
    facts["h"] = h
    facts["ratio"] = round(w / h, 4)
    return facts


def main():
    WIDE.mkdir(parents=True, exist_ok=True)
    THUMB.mkdir(parents=True, exist_ok=True)

    works = {r["slug"]: r for r in load_table("works.json")}
    for r in load_table("details.json"):
        works.setdefault(r["slug"], {}).update(r)

    terms = {}
    for r in load_table("terms.json"):
        parsed = {}
        for chunk in (r["terms"] or "").split("|"):
            if ":" not in chunk:
                continue
            kind, name = chunk.split(":", 1)
            parsed.setdefault(kind, []).append(name)
        terms[r["slug"]] = parsed

    related = {}
    for r in load_table("related.json"):
        related.setdefault(r["slug"], []).append(
            {"slug": r["other_slug"], "title": r["other_title"], "year": r["other_year"], "relation": r["relation"]}
        )

    # Where each work's photograph lives on disk.
    bundles = {}
    for md in (CONTENT / "oeuvre").rglob("index.md"):
        bundle = md.parent
        rel = bundle.relative_to(CONTENT / "oeuvre")
        parts = rel.parts
        if len(parts) < 2:
            continue
        bundles[bundle.name] = {"path": bundle, "discipline": parts[0], "folder_year": parts[1] if len(parts) > 2 else None}

    out = []
    missing = []
    for slug, rec in works.items():
        b = bundles.get(slug)
        img_facts = None
        if b:
            src = pick_image(b["path"], slug)
            if src:
                img_facts = derive(src, slug)
                img_facts["source"] = str(src.relative_to(ROOT))
        if not img_facts:
            missing.append(slug)
            continue

        t = terms.get(slug, {})
        item = {
            "slug": slug,
            "title": rec.get("title") or slug.replace("-", " "),
            "year": int(rec["year"]) if rec.get("year") and str(rec["year"]).isdigit() else None,
            "date_made": rec.get("date_made"),
            "medium": rec.get("medium"),
            "status": rec.get("status"),
            "stage": rec.get("stage"),
            "description": rec.get("description"),
            "place": rec.get("created_place"),
            "holder": rec.get("current_holder"),
            "minutes": int(rec["making_minutes"]) if rec.get("making_minutes") else None,
            "h_mm": int(rec["height_mm"]) if rec.get("height_mm") else None,
            "w_mm": int(rec["width_mm"]) if rec.get("width_mm") else None,
            "discipline": (t.get("category") or [b["discipline"].title()])[0],
            "materials": t.get("material", []),
            "techniques": t.get("technique", []),
            "tags": t.get("tag", []),
            "related": related.get(slug, []),
            "img": img_facts,
        }
        out.append(item)

    out.sort(key=lambda r: (-(r["year"] or 0), r["title"].lower()))
    OUT.write_text(json.dumps(out, indent=1))

    total = sum(f.stat().st_size for f in list(WIDE.iterdir()) + list(THUMB.iterdir()))
    print(f"{len(out)} works with imagery, {len(missing)} without")
    print(f"derivatives: {total/1_048_576:.1f} MB across {len(list(WIDE.iterdir()))} wide + {len(list(THUMB.iterdir()))} thumb")
    print("no image:", ", ".join(sorted(missing)[:20]))


if __name__ == "__main__":
    main()
