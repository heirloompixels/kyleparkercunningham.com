#!/usr/bin/env python3
"""mockups/index.html — the contact sheet for the whole sketchbook.

Not one of the thirty-four. It is the wall you pin them to: a live
thumbnail of every sheet, grouped by the question it is trying to answer.
"""

import subprocess
from pathlib import Path

import lib
import sheets

MOCKUPS = Path(__file__).resolve().parents[1]

FAMILIES = [
    ("I", "Routes", "the site as a way through, not a container", range(36, 41)),
    ("II", "Instruments", "the archive's own data, made visible", range(41, 48)),
    ("III", "Objects", "the site as a physical thing", range(48, 56)),
    ("IV", "Cycles", "time, season, the working year", range(56, 60)),
    ("V", "Lineage", "return, motif, descent", range(60, 63)),
    ("VI", "Experiments", "six that take a risk each", range(63, 69)),
    ("VII", "Synthesis", "everything learned, inside the existing design language", range(69, 70)),
]

OLD = [
    (n, f, t) for n, f, t in [
        (31, "31-the-ledger-home.html", "The Ledger"),
        (32, "32-the-specimen-home.html", "The Specimen"),
        (33, "33-the-index-home.html", "The Index"),
        (34, "34-the-wall-home.html", "The Wall"),
        (35, "35-the-reel-home.html", "The Reel"),
    ]
]


def shoot_previews():
    """One 1200×900 crop of each sheet, for the contact sheet."""
    from playwright.sync_api import sync_playwright

    out = MOCKUPS / "assets" / "sheets"
    out.mkdir(parents=True, exist_ok=True)
    targets = [(num, fn) for num, fn, _, _ in sheets.SHEETS]
    targets += [(n, f) for n, f, _ in OLD]
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for num, fn in targets:
            dest = out / f"{num}.webp"
            src = MOCKUPS / fn
            if not src.exists():
                continue
            page = br.new_page(viewport={"width": 1280, "height": 960}, device_scale_factor=1)
            page.goto(f"file://{src}", wait_until="load")
            page.wait_for_timeout(500)
            # Several sheets open on a deliberately empty screen — a contact
            # sheet of blank cards is useless, so drop past the hero to
            # whichever band actually carries the idea.
            page.evaluate(
                "()=>{document.querySelector('.sk-switch')?.remove();"
                "for(const i of document.images)i.loading='eager';"
                "const h=document.documentElement.scrollHeight;"
                "const horiz=getComputedStyle(document.body).overflowY==='hidden';"
                "window.scrollTo(0, horiz ? 0 : Math.min(h*0.16, 620));}"
            )
            page.wait_for_timeout(1100)
            page.screenshot(path=str(dest.with_suffix(".png")))
            page.close()
        br.close()

    from PIL import Image
    for png in out.glob("*.png"):
        im = Image.open(png).convert("RGB")
        im.thumbnail((640, 480), Image.LANCZOS)
        im.save(png.with_suffix(".webp"), "WEBP", quality=72, method=5)
        png.unlink()


def main():
    css = """
:root{--bg:#111112;--panel:#191919;--ink:#f0ede6;--dim:#8b867c;--hot:#d8623c;--line:#282828}
body{background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;
 font-size:15px}
.wrap{max-width:1500px;margin:0 auto;padding:0 26px 100px}
header{padding:70px 0 26px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,420px);
 gap:44px;align-items:end;border-bottom:1px solid var(--line)}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.36em;
 text-transform:uppercase;color:var(--hot)}
h1{font-family:"Instrument Serif",Georgia,serif;font-weight:400;
 font-size:clamp(2.8rem,8vw,5.6rem);line-height:.92;letter-spacing:-.02em;margin:.14em 0 0}
header p{margin:0;color:#a8a297;line-height:1.7;font-size:.96rem}
header p b{color:var(--ink);font-weight:600}
header p a{color:var(--hot)}
.fam{margin-top:64px}
.famhead{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 16px;
 border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:20px}
.famhead .rn{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.3em;
 color:var(--hot)}
.famhead h2{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:2rem;
 margin:0}
.famhead em{font-style:italic;color:var(--dim);font-size:.94rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(256px,1fr));gap:22px}
.card{text-decoration:none;color:inherit;display:block;background:var(--panel);
 border:1px solid var(--line);transition:border-color .2s,transform .2s}
.card:hover{border-color:var(--hot);transform:translateY(-3px)}
.card .shot{aspect-ratio:4/3;overflow:hidden;background:#0d0d0d;border-bottom:1px solid var(--line)}
.card img{width:100%;height:100%;object-fit:cover;object-position:top center}
.card .body{padding:12px 14px 14px}
.card .n{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.24em;
 color:var(--dim)}
.card b{display:block;font-size:1.08rem;font-weight:600;margin:3px 0 3px;letter-spacing:-.01em}
.card span{display:block;font-size:.85rem;color:#a8a297;line-height:1.5}
.prior{margin-top:70px;border-top:1px solid var(--line);padding-top:22px}
.prior h2{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.3em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:0 0 6px}
.prior p{max-width:64ch;color:#a8a297;line-height:1.7;font-size:.92rem;margin:0 0 18px}
.prior .grid{grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px}
.prior .card b{font-size:.96rem}
.how{margin-top:70px;border-top:1px solid var(--line);padding-top:24px;
 display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:30px}
.how h3{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.26em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:0 0 8px}
.how p{margin:0;color:#a8a297;line-height:1.72;font-size:.9rem}
.how code{font-family:"IBM Plex Mono",monospace;color:var(--hot);font-size:.86rem}
@media(max-width:820px){header{grid-template-columns:minmax(0,1fr)}}
"""
    by_num = {n: (f, t, tag) for n, f, t, tag in sheets.SHEETS}

    b = ['<div class="wrap"><header><div>',
         '<div class="kick">Sketchbook · 17 August 2026 · thirty-four sheets</div>',
         "<h1>New directions<br>for the site.</h1></div>",
         "<p><b>archive.kyleparkercunningham.com now holds the catalogue</b> — 295 works, "
         "every measurement, every provenance line. So this site no longer has to be one. "
         "Every sheet here is an attempt at the thing an archive can't do for itself: a "
         "route through it. Notes, findings and what I'd keep are in "
         "<a href=\"../sketchbook.md\">sketchbook.md</a>.</p></header>"]

    for roman, name, note, rng in FAMILIES:
        cards = []
        for n in rng:
            if n not in by_num:
                continue
            fn, title, tag = by_num[n]
            cards.append(
                f'<a class="card" href="{fn}">'
                f'<div class="shot"><img src="assets/sheets/{n}.webp" alt="" loading="lazy"></div>'
                f'<div class="body"><span class="n">{n}</span><b>{lib.esc(title)}</b>'
                f"<span>{lib.esc(tag)}</span></div></a>"
            )
        b.append(
            f'<section class="fam"><div class="famhead"><span class="rn">{roman}</span>'
            f"<h2>{lib.esc(name)}</h2><em>{lib.esc(note)}</em></div>"
            f'<div class="grid">{"".join(cards)}</div></section>'
        )

    b.append(
        '<section class="prior"><h2>Earlier run · sheets 31–35, 5 August</h2>'
        "<p>The previous five directions, kept here for comparison. Their finding — that the "
        "site is either continuity, identity, retrieval, the work, or impact — is what this "
        "run is arguing with: with a real catalogue standing behind it, retrieval stops being "
        "one of the five options and becomes the thing the site hands off.</p>"
        '<div class="grid">'
        + "".join(
            f'<a class="card" href="{f}">'
            f'<div class="shot"><img src="assets/sheets/{n}.webp" alt="" loading="lazy"></div>'
            f'<div class="body"><span class="n">{n}</span><b>{lib.esc(t)}</b></div></a>'
            for n, f, t in OLD
        )
        + "</div></section>"
    )

    b.append(
        '<div class="how"><div><h3>All real</h3><p>Every image is a photograph of a real work '
        "from <code>content/oeuvre/</code>. Every number — hue, lightness, dimensions, tags, "
        "pigment lightfastness, the relations between works — is read from the archive or "
        "measured off the pixels. No lorem, no placeholder, no invented statistic.</p></div>"
        "<div><h3>Self-contained</h3><p>Each sheet is one HTML file with its CSS inline. "
        "Imagery lives in <code>assets/w</code> and <code>assets/t</code>; the eighteen "
        "typefaces are self-hosted in <code>assets/fonts</code>. Nothing here needs a "
        "network.</p></div>"
        "<div><h3>Rebuilding</h3><p><code>python3 mockups/_build/prepare.py</code> rebuilds "
        "the dataset and derivatives; <code>gen1…gen5</code> write the sheets; "
        "<code>shoot.py</code> screenshots them at 1440 and 390 and reports overflow, broken "
        "images and console errors.</p></div>"
        "<div><h3>Two prices not shown</h3><p>The archive holds 108 valuations and a private "
        "note per work. None of it appears on any sheet. A public route through the work "
        "does not need to know what anything sold for.</p></div></div></div>"
    )

    lib.write("index.html", "Sketchbook — kyleparkercunningham.com", css, "".join(b))
    print("index.html")


if __name__ == "__main__":
    import sys

    for s in sheets.SHEETS:
        lib.register(*s)
    if "--shots" in sys.argv:
        shoot_previews()
    main()
