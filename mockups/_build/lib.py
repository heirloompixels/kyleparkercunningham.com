#!/usr/bin/env python3
"""Shared scaffolding for the sketchbook mockups.

Every mockup is a single self-contained HTML file that reads its imagery
from ../assets and its facts from the real oeuvre. This module loads that
dataset, provides the slicing helpers the sketches keep needing (by motif,
by hue, by year, the revisit pairs), and writes the file out with a small
switcher so all thirty-four can be walked in a browser.
"""

import html
import json
import math
import re
from pathlib import Path

BUILD = Path(__file__).resolve().parent
MOCKUPS = BUILD.parent
DATA = json.loads((BUILD / "oeuvre.json").read_text())

# Relations in the archive are stored one way round; a revisit is
# symmetric, so mirror them here.
_by_slug = {w["slug"]: w for w in DATA}
for _w in DATA:
    for _r in list(_w["related"]):
        _other = _by_slug.get(_r["slug"])
        if _other and not any(x["slug"] == _w["slug"] for x in _other["related"]):
            _other["related"].append(
                {"slug": _w["slug"], "title": _w["title"], "year": _w["year"], "relation": _r["relation"]}
            )

WORKS = DATA
BY_SLUG = _by_slug

# ---------------------------------------------------------------- selection


def get(slug):
    return BY_SLUG[slug]


def many(*slugs):
    return [BY_SLUG[s] for s in slugs if s in BY_SLUG]


def tagged(*tags, all_of=False):
    """Works carrying any (or all) of these tags/materials/techniques."""
    want = {t.lower() for t in tags}

    def vocab(w):
        return {t.lower() for t in w["tags"] + w["materials"] + w["techniques"] + [w["discipline"]]}

    test = (lambda v: want <= v) if all_of else (lambda v: bool(want & v))
    return [w for w in WORKS if test(vocab(w))]


def with_image(works=None):
    return [w for w in (works or WORKS) if w.get("img")]


def by_year(works=None):
    out = {}
    for w in works or WORKS:
        out.setdefault(w["year"] or 0, []).append(w)
    return dict(sorted(out.items()))


def by_hue(works=None):
    """Sorted around the colour wheel; near-neutral works trail at the end."""
    ws = list(works or WORKS)
    chromatic = [w for w in ws if w["img"]["chroma"] > 0.06]
    neutral = [w for w in ws if w["img"]["chroma"] <= 0.06]
    chromatic.sort(key=lambda w: w["img"]["hue"])
    neutral.sort(key=lambda w: w["img"]["lig"])
    return chromatic + neutral


def revisits():
    """Pairs where a motif came back in a later year, oldest first."""
    seen, pairs = set(), []
    for w in WORKS:
        for r in w["related"]:
            other = BY_SLUG.get(r["slug"])
            if not other:
                continue
            key = tuple(sorted([w["slug"], other["slug"]]))
            if key in seen:
                continue
            seen.add(key)
            a, b = sorted([w, other], key=lambda x: x["year"] or 0)
            pairs.append((a, b, (b["year"] or 0) - (a["year"] or 0)))
    pairs.sort(key=lambda p: -p[2])
    return pairs


def tag_counts(kind="tags", minimum=2):
    counts = {}
    for w in WORKS:
        for t in w[kind]:
            counts[t] = counts.get(t, 0) + 1
    return dict(sorted(((k, v) for k, v in counts.items() if v >= minimum), key=lambda kv: -kv[1]))


# The pigment table, straight from the archive: name, colour index,
# Blue Wool lightfastness 1-8, and how many catalogued works use it.
PIGMENTS = [
    ("hansa yellow deep", "PY97", 6, 6), ("payne's gray", None, 7, 5),
    ("prussian blue", "PB27", 6, 5), ("yellow ochre", "PY43", 8, 5),
    ("cerulean blue", None, 8, 4), ("cadmium red medium", "PR108", 7, 4),
    ("burnt sienna", None, 7, 4), ("peach black", "PBk1+PBk6", 7, 4),
    ("thio violet", "PR88", 6, 3), ("titanium white (gouache)", "PW6", 8, 3),
    ("ultramarine blue", "PB29", 8, 3), ("quinacridone magenta", "PR122", 6, 1),
    ("davy's gray", "PBk19+PG17+PBk6+PW4", 7, 1), ("thalo blue", "PB15:3", 8, 1),
    ("hooker's green", None, 7, 1), ("vermilion", None, None, 1),
    ("cadmium orange", "PO20", 7, 1), ("lunar eclipse red", "PY110+PR122+BV7+BV15", 1, 1),
    ("mimosa yellow", "PY159+PB29+PG17", 8, 1), ("clematis violet", "PY159+PB29+PV23", 5, 1),
    ("acra crimson", "PV19", 7, 0), ("winsor violet", "PV23", 6, 0),
    ("bright rose", "BV11:1", 1, 0), ("opera", "PR122+BV10", 1, 0),
    ("turquoise", "PB15:3+PG7", 7, 0), ("viridian", "PG18", 8, 0),
    ("thalo green", "PG7", 7, 0), ("indian red", "PR101", 8, 0),
    ("burnt umber", "PBr7", 7, 0), ("vandyke brown", "PBk6+PR101", 7, 0),
    ("brown madder", "PR83", 2, 0), ("sepia", "PBk6+PBr7", 7, 0),
    ("bourke's parrot pink", "PY159+BV10+PR122", 1, 0),
    ("trumpet vine red", "PY159+PR177", 5, 0),
    ("cherry blossom pink", "PR233+PO73+PW6", 6, 0),
    ("flamingo orange", "PR233+PO73", 6, 0),
    ("pampas grass yellow", "PR233+PY43+PY83", 5, 0),
    ("full moon yellow", None, 6, 0),
    ("japanese bush warbler green", "PG17+PY42+PY43", 8, 0),
    ("wonder forest green", "PY43+PG50", 8, 0),
    ("peafowl green", "PY159+PR232+PG7+PB15", 7, 0),
    ("ocean blue", "PY159+PB15", 6, 0),
    ("jade vine blue", "PV47+PG7+PB15+PW6", 6, 0),
    ("nightfall indigo", None, 2, 0),
    ("earthshine violet", "PB29+PR177+PR122", 5, 0),
    ("twilight purple", "PV47+PR233+PO13", 4, 0),
    ("daybreak orange", "PG50+PO73+PR254", 6, 0),
    ("eurasian jay rose grey", "PB29+PG18+PO73", 6, 0),
    ("hazy moon yellow", "PY159+PBk6+PB15", 6, 0),
    ("echinops green grey", "PB29+PG17", 8, 0),
    ("shoebill blue grey", "PB71+PB29+PBk11", 8, 0),
    ("moonlit night blue", "PB29+PBk6", 8, 0),
    ("rainy-night moon black", "PB29+PR101", 8, 0),
]

# ------------------------------------------------------------------ helpers


def esc(s):
    return html.escape(str(s or ""), quote=True)


def wide(w):
    return f"assets/w/{w['slug']}.webp"


def thumb(w):
    return f"assets/t/{w['slug']}.webp"


def alt(w):
    bits = [w["title"]]
    if w["medium"]:
        bits.append(w["medium"].lower())
    if w["year"]:
        bits.append(str(w["year"]))
    return esc(", ".join(bits))


def dims(w, unit="in"):
    if not (w["h_mm"] and w["w_mm"]):
        return None
    if unit == "in":
        return f"{w['h_mm']/25.4:.0f} × {w['w_mm']/25.4:.0f} in"
    return f"{w['h_mm']} × {w['w_mm']} mm"


def sentence(w, limit=170):
    """First sentence of the artist's own note on a work."""
    d = (w["description"] or "").strip()
    if not d:
        return ""
    d = re.sub(r"\s+", " ", d)
    m = re.match(r"(.+?[.!?])(\s|$)", d)
    s = m.group(1) if m else d
    if len(s) > limit:
        s = s[: limit - 1].rsplit(" ", 1)[0] + "…"
    return s


def blurb(w, limit=320):
    d = re.sub(r"\s+", " ", (w["description"] or "").strip())
    if len(d) > limit:
        d = d[: limit - 1].rsplit(" ", 1)[0] + "…"
    return d


def hex_to_hsl(hx):
    hx = hx.lstrip("#")
    r, g, b = (int(hx[i : i + 2], 16) / 255 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0.0, 0.0, l
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60, s, l


def readable_on(hx):
    """Black or white text over this background."""
    hx = hx.lstrip("#")
    r, g, b = (int(hx[i : i + 2], 16) / 255 for i in (0, 2, 4))
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "#000" if lum > 0.55 else "#fff"


def grid_svg(w, size=6, gap=0.0, radius=0):
    """The work's 6x6 average-colour grid, as inline SVG."""
    cells = w["img"]["grid"]
    n = int(math.sqrt(len(cells)))
    out = [f'<svg viewBox="0 0 {n} {n}" preserveAspectRatio="none" aria-hidden="true">']
    for i, c in enumerate(cells):
        x, y = i % n, i // n
        out.append(
            f'<rect x="{x+gap/2}" y="{y+gap/2}" width="{1-gap}" height="{1-gap}" '
            f'rx="{radius}" fill="{c}"/>'
        )
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------- output

SHEETS = []  # (number, filename, title, tagline) — filled by register()


def register(num, filename, title, tagline):
    SHEETS.append((num, filename, title, tagline))


SWITCHER_CSS = """
.sk-switch{position:fixed;right:12px;bottom:12px;z-index:99999;font:400 11px/1.35
 ui-monospace,SFMono-Regular,Menlo,monospace;color:#111;max-width:min(300px,calc(100vw - 24px));
 print-color-adjust:exact}
.sk-switch summary{list-style:none;cursor:pointer;background:#111;color:#fff;padding:5px 9px;
 border-radius:2px;letter-spacing:.08em;text-transform:uppercase;display:inline-block;
 box-shadow:0 1px 10px rgba(0,0,0,.28);user-select:none}
.sk-switch summary::-webkit-details-marker{display:none}
.sk-switch[open] summary{border-radius:2px 2px 0 0}
.sk-switch .sk-panel{background:#fbfaf8;border:1px solid #111;max-height:min(64vh,520px);
 overflow:auto;padding:6px;box-shadow:0 6px 30px rgba(0,0,0,.3)}
.sk-switch a{display:block;padding:3px 5px;color:#111;text-decoration:none;border-radius:2px;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sk-switch a:hover{background:#111;color:#fff}
.sk-switch a.now{background:#e4dfd6;font-weight:700}
.sk-switch b{color:#8a8378;font-weight:400;margin-right:6px}
@media print{.sk-switch{display:none}}
"""


def switcher(current):
    rows = []
    for num, fn, title, _ in sorted(SHEETS):
        cls = ' class="now"' if fn == current else ""
        rows.append(f'<a href="{fn}"{cls}><b>{num}</b>{esc(title)}</a>')
    return (
        '<details class="sk-switch"><summary>sketchbook</summary>'
        '<div class="sk-panel">' + "".join(rows) + "</div></details>"
    )


BASE = """*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0}
img{max-width:100%;display:block}
a{color:inherit}
"""


def write(filename, title, css, body, fonts="", head="", lang_class=""):
    """Emit one self-contained mockup.

    Typefaces are self-hosted in assets/fonts, so a mockup opened from a
    USB stick on a plane looks exactly like one opened on the studio wifi.
    """
    doc = f"""<!doctype html>
<html lang="en"{lang_class}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<link rel="stylesheet" href="assets/fonts/fonts.css">{head}
<style>
{BASE}{css}
{SWITCHER_CSS}</style>
</head>
<body>
{body}
{switcher(filename)}
</body>
</html>
"""
    (MOCKUPS / filename).write_text(doc)
    return filename
