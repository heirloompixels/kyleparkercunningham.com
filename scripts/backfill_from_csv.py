#!/usr/bin/env python3
"""One-time backfill: copy medium / dimensions / status from the Oeuvre CSV
into the [extra] front matter of matching painting pages.

Conservative by design:
  - paintings only (the CSV contains no other disciplines)
  - only unambiguous title matches (one CSV row <-> one page), year-checked
  - never overwrites a value that already exists in front matter
  - dry run by default; pass --apply to write

Usage:  python3 scripts/backfill_from_csv.py [--apply]
"""
import csv, re, sys
from pathlib import Path
from collections import defaultdict

CSV_PATH = Path("/Users/kpc/www/kyleparkercunningham.com/Kyle Oeuvre/Oeuvre-Table 1.csv")
ROOT = Path(__file__).resolve().parent.parent
PAINTINGS = ROOT / "content" / "oeuvre" / "painting"
APPLY = "--apply" in sys.argv

# Year mismatches confirmed by Kyle (2026-06): these works were started in the
# CSV year and reworked in the year the page sits under. Cyclic Repetition is
# the inverse (CSV year is later), so it gets year_reworked instead.
YEAR_OVERRIDES = {
    "rhino-radar-arm-fauna": {"year_started": "2016"},
    "cydney-and-val": {"year_started": "2020"},
    "preservation-cactus": {"year_started": "2018"},
    "cyclic-repetition": {"year_reworked": "2022"},
}

MEDIUM_FIXUPS = {
    "Oil on LInen": "Oil on Linen",
    "OIL ON Linen": "Oil on Linen",
    "Acylic and Latex on Canvas": "Acrylic and Latex on Canvas",
    "Acrylica and Spraypaint on Diabond, Oil": "Acrylic and Spraypaint on Diabond, Oil",
    "Acrylic and Latex Cavans": "Acrylic and Latex on Canvas",
}

def norm(s):
    if not s: return ""
    s = s.lower().strip().replace("&", " and ").replace("_", " ").replace("-", " ")
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

# ---- load CSV ----
csv_rows = []
with open(CSV_PATH, newline="") as f:
    for row in csv.DictReader(f):
        title = (row.get("Title") or "").strip()
        if not title: continue
        medium = (row.get("Medium") or "").strip()
        medium = MEDIUM_FIXUPS.get(medium, medium)
        size = re.sub(r"\s+", " ", (row.get("Size") or "").strip())
        unit = (row.get("Unit") or "").strip() or "inches"
        if size and re.fullmatch(r"[\d\s./xX×]+", size):
            dimensions = f"{size} {unit}"
        else:
            dimensions = size  # descriptive sizes kept verbatim, no unit appended
        sold = bool((row.get("Date Sold") or "").strip() or (row.get("Buyer") or "").strip())
        loan = (row.get("Loan Location") or "").strip()
        status = "sold" if sold else ("on loan" if loan else "")
        csv_rows.append({
            "title": title, "norm": norm(title),
            "year": (row.get("Date Painted") or "").strip(),
            "medium": medium, "dimensions": dimensions,
            "status": status, "location": loan,
            "remarks": (row.get("Remarks") or "").strip(),
        })

# ---- load painting pages ----
pages = []
for p in PAINTINGS.glob("*/*/index.md"):
    txt = p.read_text()
    m = re.search(r'^\s*title\s*=\s*"([^"]+)"', txt, re.M)
    slug = p.parts[-2]
    title = m.group(1) if m else slug
    pages.append({
        "path": p, "year": p.parts[-3], "slug": slug, "title": title,
        "norm": norm(title), "slug_norm": norm(slug), "text": txt,
    })

# ---- match: exact normalized title/slug, unambiguous, year-compatible ----
csv_by_norm = defaultdict(list)
for r in csv_rows:
    csv_by_norm[r["norm"]].append(r)

matches, skipped = [], []
for pg in pages:
    cands = csv_by_norm.get(pg["norm"], []) or csv_by_norm.get(pg["slug_norm"], [])
    if not cands:
        continue
    year_ok = [c for c in cands if not c["year"] or c["year"] == pg["year"]]
    if len(year_ok) == 1:
        matches.append((pg, year_ok[0], {}))
    elif len(year_ok) > 1:
        skipped.append((pg, f"ambiguous: {len(year_ok)} CSV rows match"))
    elif pg["slug"] in YEAR_OVERRIDES and len(cands) == 1:
        matches.append((pg, cands[0], YEAR_OVERRIDES[pg["slug"]]))
    else:
        skipped.append((pg, f"year mismatch: CSV says {', '.join(c['year'] or '?' for c in cands)}, page is {pg['year']}"))

# ---- write front matter ----
def add_extra(text, fields):
    """Add missing keys to [extra] (creating the section if needed)."""
    m = re.match(r"^(\+\+\+\n)(.*?)(\n\+\+\+)(.*)$", text, re.S)
    fm, body = m.group(2), m.group(4)
    todo = {}
    for k, v in fields.items():
        if not v: continue
        if re.search(rf'^\s*{k}\s*=', fm, re.M): continue  # never overwrite
        todo[k] = v
    if not todo:
        return text, []
    lines = "\n".join(f'{k} = "{v}"' for k, v in todo.items())
    if re.search(r"^\[extra\]\s*$", fm, re.M):
        fm = re.sub(r"(^\[extra\]\s*$)", rf"\g<1>\n{lines}", fm, count=1, flags=re.M)
    else:
        fm = fm + f"\n\n[extra]\n{lines}"
    return f"+++\n{fm}\n+++{body}", list(todo.keys())

updated, untouched = [], []
for pg, row, extra_fields in matches:
    fields = {
        "medium": row["medium"],
        "dimensions": row["dimensions"],
        "status": row["status"],
        "location": row["location"],
    }
    fields.update(extra_fields)
    new_text, added = add_extra(pg["text"], fields)
    if added:
        if APPLY:
            pg["path"].write_text(new_text)
        updated.append((pg, fields, added))
    else:
        untouched.append(pg)

# ---- report ----
mode = "APPLIED" if APPLY else "DRY RUN (pass --apply to write)"
print(f"== Backfill {mode} ==")
print(f"painting pages: {len(pages)} | CSV rows: {len(csv_rows)} | matched: {len(matches)}")
print(f"updated: {len(updated)} | already complete: {len(untouched)} | skipped: {len(skipped)}\n")

for pg, fields, added in updated:
    bits = ", ".join(f"{k}={fields[k]!r}" for k in added)
    print(f"  + {pg['year']}/{pg['slug']:44s} {bits}")

if skipped:
    print("\n-- skipped (needs a human) --")
    for pg, why in skipped:
        print(f"  ! {pg['year']}/{pg['slug']:44s} {why}")

unmatched = [pg for pg in pages if not csv_by_norm.get(pg["norm"]) and not csv_by_norm.get(pg["slug_norm"])]
print(f"\n-- no CSV row found: {len(unmatched)} pages (mostly post-2023 work; add to spreadsheet) --")

remarks = [(pg, row["remarks"]) for pg, row, _ in matches if row["remarks"]]
if remarks:
    print("\n-- CSV remarks not copied (review for page prose) --")
    for pg, rem in remarks:
        print(f"  * {pg['year']}/{pg['slug']}: {rem}")
