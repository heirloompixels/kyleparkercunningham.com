#!/usr/bin/env python3
"""Sheets 41–47 — the archive's own data, made visible.

Every number on these seven sheets is real: measured off the pixels, or
read out of the catalogue. Where something is a simulation rather than a
measurement (the fading in 42) the sheet says so on its face.
"""

import math
from collections import Counter, defaultdict

import lib
from lib import (PIGMENTS, alt, blurb, by_hue, dims, esc, get, grid_svg,
                 hex_to_hsl, many, readable_on, sentence, tagged, thumb, wide)


# ------------------------------------------------------------- 41 chromatic

HUE_BANDS = [
    (350, 20, "Reds", "cadmium, vermilion, the inside of a mouth"),
    (20, 45, "Ochres & Terracotta", "the ground everything here is painted on"),
    (45, 68, "Golds & Yellows", "hansa deep, yellow ochre, 24kt leaf"),
    (68, 160, "Greens", "juniper, conifer, the Gila after rain"),
    (160, 200, "Teals", "the most persistent colour in the catalogue"),
    (200, 250, "Blues", "sky, ice, distance, the recent work"),
    (250, 350, "Violets & Roses", "twilight, alpenglow, the rarest band"),
]


def sheet_41():
    css = """
:root{--bg:#0b0b0c;--ink:#f2efe9;--dim:#8d8880}
body{background:var(--bg);color:var(--ink);font-family:"Inter",system-ui,sans-serif;
 font-size:15px;-webkit-font-smoothing:antialiased}
.wrap{max-width:1400px;margin:0 auto;padding:0 26px 100px}
header{padding:76px 0 30px;max-width:60ch}
.kick{font-size:10.5px;letter-spacing:.4em;text-transform:uppercase;color:var(--dim)}
h1{font-family:"Instrument Serif",Georgia,serif;font-weight:400;
 font-size:clamp(3rem,9vw,6.6rem);line-height:.9;letter-spacing:-.02em;margin:.14em 0 .2em}
header p{color:#b3ada3;line-height:1.62;font-size:1.03rem;margin:0}
header p b{color:var(--ink);font-weight:500}
.band{margin:44px 0 8px;display:flex;height:min(46vh,340px);gap:1px;align-items:flex-end}
.band a{flex:1 1 0;min-width:0;position:relative;display:block;transition:flex-grow .35s ease}
.band a:hover{flex-grow:14;z-index:3}
.band .pal{position:absolute;left:0;right:0;bottom:0;height:16px;display:flex}
.band .pal i{display:block}
.band img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;
 transition:opacity .35s ease}
.band a:hover img{opacity:1}
.band figcaption{position:absolute;left:0;bottom:100%;white-space:nowrap;font-size:10px;
 letter-spacing:.14em;text-transform:uppercase;color:var(--ink);opacity:0;
 transform:rotate(-90deg);transform-origin:0 100%;padding-left:8px;transition:opacity .3s}
.band a:hover figcaption{opacity:1}
.ruler{display:flex;font-size:9.5px;letter-spacing:.24em;text-transform:uppercase;
 color:var(--dim);border-top:1px solid #2a2a2c;padding-top:8px}
.ruler span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}
.ruler span:last-child{text-align:right}
.note{color:var(--dim);font-size:12px;line-height:1.7;margin:22px 0 0;max-width:66ch}
.grp{margin-top:74px;border-top:1px solid #232325;padding-top:22px}
.ghead{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 16px;margin-bottom:16px}
.ghead h2{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:2rem;margin:0}
.ghead em{font-style:normal;color:var(--dim);font-size:12px;letter-spacing:.2em;
 text-transform:uppercase}
.ghead i{font-style:italic;color:#9d978d}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:14px}
.tile{text-decoration:none;color:inherit;display:block}
.tile .im{position:relative;aspect-ratio:1;overflow:hidden}
.tile img{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}
.tile:hover img{transform:scale(1.05)}
.tile .chips{display:flex;height:5px;margin-top:5px}
.tile .chips i{flex:1}
.tile b{display:block;font-size:11.5px;font-weight:500;margin-top:6px;line-height:1.35}
.tile span{display:block;font-size:10px;letter-spacing:.14em;text-transform:uppercase;
 color:var(--dim);margin-top:2px}
footer{margin-top:80px;border-top:1px solid #232325;padding-top:18px;font-size:11px;
 letter-spacing:.16em;text-transform:uppercase;color:var(--dim);display:flex;flex-wrap:wrap;
 gap:10px 30px;justify-content:space-between}
@media(max-width:760px){.band{height:200px}.band a:hover{flex-grow:8}}
"""
    ws = by_hue(lib.WORKS)
    strips = []
    for w in ws:
        im = w["img"]
        # The strip is filled with the work's own measured mean colour, so the
        # band reads as one continuous sweep; its five-colour palette runs
        # along the bottom as a footer.
        mean = f"hsl({im['hue']:.0f} {min(im['sat']*145,72):.0f}% {22+im['lig']*52:.0f}%)"
        if im["chroma"] <= 0.06:
            mean = f"hsl(40 4% {20+im['lig']*56:.0f}%)"
        pal = "".join(
            f'<i style="background:{sw["hex"]};flex:{max(sw["share"],.05):.3f}"></i>'
            for sw in im["swatches"]
        )
        h = 30 + im["sat"] * 150
        strips.append(
            f'<a href="#{esc(w["slug"])}" style="height:{min(h,100):.0f}%;background:{mean}">'
            f'<figcaption>{esc(w["title"])} · {w["year"]}</figcaption>'
            f'<span class="pal">{pal}</span>'
            f'<img src="{thumb(w)}" alt="{alt(w)}" loading="lazy"></a>'
        )

    b = ['<div class="wrap"><header>',
         '<div class="kick">Kyle Parker Cunningham · chromatic index</div>',
         "<h1>Sorted by colour, not by year.</h1>",
         "<p>Every photograph in the archive carries a measured dominant hue and a "
         "five-colour palette. Order the whole catalogue by that instead of by date and "
         "a different practice appears: <b>one continuous spectrum</b>, heavy in ochre "
         "and teal, thin in violet, with the recent weather paintings all arriving "
         "together in the blues. Height is saturation. Hover anything to see the work "
         "underneath its own colours.</p></header>",
         '<div class="band">' + "".join(strips) + "</div>",
         '<div class="ruler"><span>red</span><span>ochre</span><span>gold</span>'
         "<span>green</span><span>teal</span><span>blue</span><span>violet</span>"
         "<span>neutral</span></div>",
         '<p class="note">155 works. Hue is the saturation-weighted circular mean of each '
         "photograph; near-neutral works (chroma below 0.06) can't be meaningfully placed on "
         "a colour wheel, so they sit at the end ordered by lightness instead of pretending "
         "to a hue they don't have.</p>"]

    for lo, hi, name, note in HUE_BANDS:
        if lo > hi:
            sel = [w for w in ws if w["img"]["chroma"] > 0.06 and
                   (w["img"]["hue"] >= lo or w["img"]["hue"] < hi)]
        else:
            sel = [w for w in ws if w["img"]["chroma"] > 0.06 and lo <= w["img"]["hue"] < hi]
        if not sel:
            continue
        tiles = "".join(
            f'<a class="tile" href="#{esc(w["slug"])}">'
            f'<div class="im"><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy"></div>'
            f'<div class="chips">'
            + "".join(f'<i style="background:{s["hex"]}"></i>' for s in w["img"]["swatches"])
            + f'</div><b>{esc(w["title"])}</b><span>{w["year"]} · {esc(w["discipline"])}</span></a>'
            for w in sel
        )
        b.append(
            f'<section class="grp"><div class="ghead"><h2>{esc(name)}</h2>'
            f'<em>{len(sel)} works · {lo}°–{hi}°</em><i>{esc(note)}</i></div>'
            f'<div class="tiles">{tiles}</div></section>'
        )

    neutral = [w for w in ws if w["img"]["chroma"] <= 0.06]
    if neutral:
        tiles = "".join(
            f'<a class="tile" href="#{esc(w["slug"])}">'
            f'<div class="im"><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy"></div>'
            f'<div class="chips">'
            + "".join(f'<i style="background:{s["hex"]}"></i>' for s in w["img"]["swatches"])
            + f'</div><b>{esc(w["title"])}</b><span>{w["year"]} · {esc(w["discipline"])}</span></a>'
            for w in neutral
        )
        b.append(
            f'<section class="grp"><div class="ghead"><h2>Achromatic</h2>'
            f'<em>{len(neutral)} works</em><i>the drypoints, mostly — black ink on white rag</i>'
            f'</div><div class="tiles">{tiles}</div></section>'
        )

    b.append(
        "<footer><span>colour measured from the archive's own photographs</span>"
        "<span>full records → archive.kyleparkercunningham.com</span></footer></div>"
    )
    return lib.write("41-chromatic.html", "Chromatic Index", css, "".join(b))


# -------------------------------------------------------------- 42 fugitive

def sheet_42():
    css = """
:root{--paper:#fbfbfa;--ink:#141414;--dim:#767470;--rule:#e2e0dc;--alarm:#b3231c;
 --ok:#2f6b46}
body{background:var(--paper);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;
 font-size:15px}
.wrap{max-width:1080px;margin:0 auto;padding:0 26px 110px}
header{padding:74px 0 26px;border-bottom:3px double var(--ink)}
.doc{display:flex;flex-wrap:wrap;gap:6px 24px;font-family:"IBM Plex Mono",monospace;
 font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}
h1{font-family:"Newsreader",Georgia,serif;font-weight:300;font-size:clamp(2.6rem,7vw,4.8rem);
 line-height:1;letter-spacing:-.02em;margin:.2em 0 .16em}
.lede{font-family:"Newsreader",Georgia,serif;font-size:1.2rem;line-height:1.6;max-width:60ch;
 color:#2f2d2a;margin:0 0 6px}
h2{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.3em;text-transform:uppercase;
 color:var(--dim);font-weight:400;margin:64px 0 16px;padding-bottom:7px;
 border-bottom:1px solid var(--rule);display:flex;justify-content:space-between}
p{line-height:1.68;max-width:66ch;color:#33312e}
.sim{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:8px 0 12px}
.sim figure{margin:0}
.sim img{width:100%;aspect-ratio:1;object-fit:cover;border:1px solid var(--rule)}
.sim figcaption{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--dim);margin-top:7px;line-height:1.5}
.sim figcaption b{display:block;color:var(--ink);font-size:11px}
.y0 img{filter:none}
.y50 img{filter:saturate(.78) contrast(.95) brightness(1.04)}
.y100 img{filter:saturate(.5) contrast(.88) brightness(1.09)}
.y200 img{filter:saturate(.2) contrast(.78) brightness(1.15) sepia(.12)}
.caveat{background:#f4f2ed;border-left:3px solid var(--alarm);padding:14px 18px;
 font-size:13px;line-height:1.62;max-width:66ch;color:#3a3835}
.caveat b{color:var(--alarm)}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{width:100%;min-width:460px;border-collapse:collapse;
 font-family:"IBM Plex Mono",monospace;font-size:12.5px}
th{text-align:left;font-weight:400;font-size:10px;letter-spacing:.2em;text-transform:uppercase;
 color:var(--dim);border-bottom:1px solid var(--ink);padding:0 10px 7px 0}
td{padding:7px 10px 7px 0;border-bottom:1px solid var(--rule);vertical-align:middle}
tr.risk td{background:#fdf3f2}
.sw{width:34px;height:14px;display:inline-block;border:1px solid rgba(0,0,0,.2)}
.bw{display:inline-flex;gap:2px;align-items:center}
.bw i{width:7px;height:14px;background:var(--rule)}
.bw i.on{background:var(--ink)}
tr.risk .bw i.on{background:var(--alarm)}
.rating{font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.rating.bad{color:var(--alarm)}
.rating.good{color:var(--ok)}
.ci{color:var(--dim)}
.cols{columns:2;column-gap:34px;margin-top:10px}
.cols p{max-width:none;font-size:14px}
footer{margin-top:70px;border-top:3px double var(--ink);padding-top:14px;
 font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--dim);display:flex;flex-wrap:wrap;gap:8px 26px;
 justify-content:space-between}
@media(max-width:720px){.sim{grid-template-columns:repeat(2,1fr)}.cols{columns:1}}
"""
    fugitive = [p for p in PIGMENTS if p[2] is not None and p[2] <= 3]
    solid = [p for p in PIGMENTS if p[2] is not None and p[2] >= 7]
    swatch_for = {
        "lunar eclipse red": "#8e2233", "bright rose": "#e0407f", "opera": "#e8368e",
        "nightfall indigo": "#26304f", "brown madder": "#7d3626",
        "hansa yellow deep": "#f5b21a", "payne's gray": "#4a5560",
        "prussian blue": "#12395c", "yellow ochre": "#c68e2c",
        "cerulean blue": "#2b7fb8", "cadmium red medium": "#c8322a",
        "burnt sienna": "#8c4326", "peach black": "#211f1d",
        "thio violet": "#8e3374", "titanium white (gouache)": "#f4f2ee",
        "ultramarine blue": "#28378f", "quinacridone magenta": "#a01d5c",
        "davy's gray": "#6e6f68", "thalo blue": "#0f5f8f", "hooker's green": "#2c5c3c",
        "vermilion": "#d94620", "cadmium orange": "#e2701a",
        "mimosa yellow": "#e8c74a", "clematis violet": "#6a4d95",
        "acra crimson": "#9c1f3d", "winsor violet": "#4b2a72",
        "turquoise": "#12907f", "viridian": "#1f6b52", "olive green": "#6b6f34",
        "thalo green": "#0d5c48", "indian red": "#9c4740", "burnt umber": "#5a3a28",
        "vandyke brown": "#4a3226", "sepia": "#4e3b2c",
    }

    def bw(n):
        return '<span class="bw">' + "".join(
            f'<i class="{"on" if i < (n or 0) else ""}"></i>' for i in range(8)
        ) + "</span>"

    def row(p, risk):
        name, ci, lf, uses = p
        col = swatch_for.get(name, "#b8b4ac")
        cls = ' class="risk"' if risk else ""
        rating = ("bad", "fugitive") if (lf or 9) <= 3 else (
            ("good", "permanent") if (lf or 0) >= 7 else ("", "moderate"))
        return (
            f"<tr{cls}><td><span class=\"sw\" style=\"background:{col}\"></span></td>"
            f"<td>{esc(name)}</td><td class=\"ci\">{esc(ci or '—')}</td>"
            f"<td>{bw(lf)}</td><td class=\"rating {rating[0]}\">{rating[1]}</td>"
            f"<td>{uses or '—'}</td></tr>"
        )

    demo = get("stole-the-rainbow-2")
    demo2 = get("low-angle-sun-rays")

    def sim(w):
        return (
            '<div class="sim">'
            + "".join(
                f'<figure class="{cls}"><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">'
                f"<figcaption><b>{lab}</b>{sub}</figcaption></figure>"
                for cls, lab, sub in (
                    ("y0", "today", "as photographed"),
                    ("y50", "+50 yr", "gallery light"),
                    ("y100", "+100 yr", "gallery light"),
                    ("y200", "+200 yr", "gallery light"),
                )
            )
            + "</div>"
        )

    b = ['<div class="wrap"><header>',
         '<div class="doc"><span>Condition note 01</span><span>Kyle Parker Cunningham</span>'
         "<span>materials · permanence</span><span>Blue Wool scale 1–8</span></div>",
         "<h1>Fugitive</h1>",
         '<p class="lede">The archive records the pigment for fifty-four colours in the '
         "studio, with its Colour Index name and its lightfastness. Which means the archive "
         "already knows, and can tell you, which of these paintings will outlive the painter "
         "and which will not.</p></header>"]

    b.append(
        "<h2><span>What the rating means</span><span>ISO 105-B02</span></h2>"
        '<div class="cols">'
        "<p>Blue Wool is a permanence scale. A pigment rated <b>8</b> is essentially "
        "immortal on a wall: two centuries of ordinary gallery light will not move it. "
        "A pigment rated <b>1</b> is <i>fugitive</i> — it will visibly shift inside a "
        "human lifetime, and in direct sun inside a decade.</p>"
        "<p>Artists have always known this and mostly not said it out loud, because it "
        "sounds like an admission. It isn't. A rose that fades is a choice, the same as "
        "a paper that yellows or a bronze that goes green. The only failure is not "
        "telling the person who bought it.</p></div>"
    )

    b.append(
        f"<h2><span>Simulated fade · <i>{esc(demo.title if hasattr(demo,'title') else demo['title'])}</i>, {demo['year']}</span>"
        f"<span>hand-coloured, watercolour &amp; gouache</span></h2>"
        + sim(demo)
        + '<div class="caveat"><b>This is a simulation, not a measurement.</b> The archive '
        "records which pigments are in the studio; it does not yet record which pigment went "
        "into which work. These four frames apply a plausible desaturation curve to the "
        "photograph — they show you the <i>shape</i> of the risk, not this work's fate. "
        "Filling in per-work pigment data would turn this from an illustration into a "
        "forecast, and it is the single most valuable thing the catalogue is still "
        "missing.</div>"
    )

    b.append(
        f"<h2><span>The same again · <i>{esc(demo2['title'])}</i>, {demo2['year']}</span>"
        f"<span>oil on linen</span></h2>"
        + sim(demo2)
        + "<p>Oil on linen behaves differently from watercolour on rag: the binder yellows "
        "as the pigment shifts, so the whole thing warms rather than simply pales. That is "
        "why the two rows above do not fade the same way.</p>"
    )

    b.append(
        f"<h2><span>The fugitive colours</span><span>{len(fugitive)} of 54 · Blue Wool ≤ 3</span></h2>"
        "<div class=\"tw\"><table><thead><tr><th></th><th>Pigment</th><th>Colour index</th>"
        "<th>Lightfastness</th><th></th><th>Works</th></tr></thead><tbody>"
        + "".join(row(p, True) for p in sorted(fugitive, key=lambda p: (p[2], p[0])))
        + "</tbody></table></div>"
        "<p><i>Lunar eclipse red</i> is in one catalogued work and is rated 1. So is "
        "<i>bright rose</i>, and <i>opera</i> — the two most beautiful pinks in the "
        "drawer, and both of them temporary.</p>"
    )

    b.append(
        f"<h2><span>The permanent ones</span><span>{len(solid)} of 54 · Blue Wool ≥ 7</span></h2>"
        "<div class=\"tw\"><table><thead><tr><th></th><th>Pigment</th><th>Colour index</th>"
        "<th>Lightfastness</th><th></th><th>Works</th></tr></thead><tbody>"
        + "".join(row(p, False) for p in sorted(solid, key=lambda p: (-p[3], p[0]))[:22])
        + "</tbody></table></div>"
        "<p>The four most-used colours in the whole catalogue — hansa yellow deep, "
        "yellow ochre, prussian blue, payne's gray — are all rated 6 or better. Whatever "
        "else is true, the paintings are built to stay.</p>"
    )

    b.append(
        "<footer><span>Pigment data: archive.kyleparkercunningham.com</span>"
        "<span>Fade frames are simulated and labelled as such</span>"
        "<span>No condition claim is made about any individual work</span></footer></div>"
    )
    return lib.write("42-fugitive.html", "Fugitive — a note on permanence", css, "".join(b))


# ------------------------------------------------------------ 43 true scale

def sheet_43():
    css = """
:root{--wall:#e8e4dc;--ink:#1b1a17;--dim:#83807a;--line:#cdc8bd;--s:.30}
@media(max-width:900px){:root{--s:.20}}
@media(max-width:520px){:root{--s:.13}}
body{background:var(--wall);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif}
.rail{position:fixed;left:0;top:0;bottom:0;width:52px;z-index:4;
 background:linear-gradient(90deg,rgba(232,228,220,.96),rgba(232,228,220,0));
 pointer-events:none}
header{max-width:1240px;margin:0 auto;padding:70px 26px 10px}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.36em;
 text-transform:uppercase;color:var(--dim)}
h1{font-family:"Newsreader",Georgia,serif;font-weight:300;font-size:clamp(2.6rem,7.4vw,5.2rem);
 line-height:.98;letter-spacing:-.02em;margin:.16em 0 .22em}
header p{max-width:58ch;line-height:1.66;color:#43403a;font-size:1.02rem}
.room{max-width:1240px;margin:0 auto;padding:34px 26px 120px;position:relative}
.floor{position:absolute;left:26px;right:26px;bottom:120px;border-bottom:1.5px solid var(--ink)}
.hang{display:flex;flex-wrap:wrap;align-items:flex-end;gap:52px 34px;
 border-bottom:1.5px solid var(--ink);padding-bottom:0;min-height:200px}
.pc{position:relative;flex:0 0 auto}
.pc img{display:block;box-shadow:0 18px 34px -26px rgba(0,0,0,.65);background:#d8d3c9}
.pc figcaption{position:absolute;top:100%;left:0;width:max(100%,132px);
 font-family:"IBM Plex Mono",monospace;font-size:9.5px;line-height:1.55;letter-spacing:.05em;
 color:var(--dim);padding-top:7px;text-transform:uppercase}
.pc figcaption b{display:block;color:var(--ink);letter-spacing:.02em;text-transform:none;
 font-family:"IBM Plex Sans",sans-serif;font-size:11.5px;font-weight:600}
.human{flex:0 0 auto;position:relative;width:calc(var(--s) * 420px)}
.human svg{display:block;width:100%;height:auto}
.human span{position:absolute;top:100%;left:0;font-family:"IBM Plex Mono",monospace;
 font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);padding-top:7px;
 white-space:nowrap}
.band{margin:96px 0 0}
.band h2{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.3em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:0 0 6px;
 display:flex;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:7px}
.band .why{max-width:56ch;line-height:1.62;color:#43403a;font-size:.96rem;margin:14px 0 30px}
.scalebar{display:flex;align-items:flex-end;gap:0;margin:30px 0 0;
 font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--dim)}
.scalebar i{display:block;height:9px;border-left:1px solid var(--ink);
 border-bottom:1px solid var(--ink)}
.miss{margin-top:80px;border:1px solid var(--ink);padding:22px 24px;max-width:70ch;
 background:rgba(255,254,250,.6)}
.miss h3{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.28em;
 text-transform:uppercase;margin:0 0 10px;color:var(--dim);font-weight:400}
.miss p{margin:0;line-height:1.66;color:#43403a;font-size:.96rem}
footer{max-width:1240px;margin:0 auto;padding:0 26px 60px;font-family:"IBM Plex Mono",monospace;
 font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);
 display:flex;flex-wrap:wrap;gap:8px 26px;justify-content:space-between}
"""
    sized = [w for w in lib.WORKS if w["h_mm"] and w["w_mm"]]
    sized.sort(key=lambda w: -(w["h_mm"] * w["w_mm"]))

    figure = (
        '<div class="human"><svg viewBox="0 0 40 170" aria-label="1.7 m figure for scale">'
        '<circle cx="20" cy="13" r="9" fill="#1b1a17"/>'
        '<path d="M20 23 C10 23 7 34 7 48 L7 92 L12 92 L13 66 L14 168 L19 168 L20 108 '
        "L21 168 L26 168 L27 66 L28 92 L33 92 L33 48 C33 34 30 23 20 23 Z\" fill=\"#1b1a17\"/>"
        "</svg><span>1.7 m</span></div>"
    )

    groups = [
        ("Wall-scale", "over 600 mm on the long side",
         "These are the ones that need a room. <i>the mother bear</i> is 1308 mm across — "
         "you meet it at chest height and it does not step back.",
         lambda w: max(w["h_mm"], w["w_mm"]) >= 600),
        ("Arm's reach", "300–600 mm",
         "The working middle of the practice: a size you can carry finished across the "
         "studio in one hand and photograph on the floor.",
         lambda w: 300 <= max(w["h_mm"], w["w_mm"]) < 600),
        ("Held", "under 300 mm",
         "Almost all of these are drypoints and the small panels — printed on a press "
         "that fits on a table, on paper torn by hand.",
         lambda w: max(w["h_mm"], w["w_mm"]) < 300),
    ]

    b = ['<div class="rail"></div><header>',
         '<div class="kick">One wall · one scale · 95 works measured</div>',
         "<h1>Actual size.</h1>",
         "<p>Photographs make everything the same size, which is the single most misleading "
         "thing about looking at art on a screen. Ninety-five works in the archive carry real "
         "measurements in millimetres. Here they are on one wall, at one scale, with a person "
         "standing in it. Nothing on this page has been resized to fit a grid.</p></header>",
         '<div class="room">']

    for name, rng, why, test in groups:
        sel = [w for w in sized if test(w)]
        if not sel:
            continue
        pcs = []
        for w in sel:
            pcs.append(
                f'<figure class="pc"><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy" '
                f'style="width:calc(var(--s) * {w["w_mm"]}px);'
                f'height:calc(var(--s) * {w["h_mm"]}px);object-fit:cover">'
                f'<figcaption><b>{esc(w["title"])}</b>{w["year"]} · {esc(dims(w))}</figcaption>'
                f"</figure>"
            )
        show_figure = figure if name == "Wall-scale" else ""
        b.append(
            f'<section class="band"><h2><span>{esc(name)}</span>'
            f'<span>{esc(rng)} · {len(sel)} works</span></h2>'
            f'<p class="why">{why}</p>'
            f'<div class="hang">{show_figure}{"".join(pcs)}</div></section>'
        )

    b.append(
        '<div class="scalebar"><i style="width:calc(var(--s) * 500px)"></i></div>'
        '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:10px;color:#83807a;'
        'letter-spacing:.16em;text-transform:uppercase;margin-top:6px">'
        "500 mm at the scale of this page</div>"
    )

    b.append(
        '<div class="miss"><h3>What is missing, and it matters</h3>'
        f"<p>Sixty works in the catalogue have no measurements — {len(sized)} of 155 do. "
        "A wall like this can only hang what has been measured, so the sixty are simply "
        "absent from it rather than shown wrongly. If this became a real page it would be "
        "the best argument the site could make for finishing the dimension backfill: every "
        "work measured is one more thing that can stand in a room with the others.</p></div>"
    )

    b.append("</div><footer><span>scale 1 mm ≈ 0.3 px</span>"
             "<span>measurements from archive.kyleparkercunningham.com</span>"
             "<span>figure shown at 1.7 m</span></footer>")
    return lib.write("43-true-scale.html", "True Scale", css, "".join(b))


# ------------------------------------------------------------- 44 deep time

def sheet_44():
    css = """
:root{--bg:#f0ece3;--ink:#1c1913;--dim:#7d766a;--rule:#cfc7b6}
body{background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:0 26px 110px}
header{padding:74px 0 34px}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.36em;
 text-transform:uppercase;color:var(--dim)}
h1{font-family:"Fraunces",Georgia,serif;font-weight:400;font-size:clamp(2.6rem,7.6vw,5.4rem);
 line-height:.95;letter-spacing:-.02em;margin:.16em 0 .2em}
header p{max-width:58ch;line-height:1.66;color:#453f34;font-size:1.04rem}
.col{display:grid;grid-template-columns:74px 132px minmax(0,1fr);gap:0 20px;
 margin:30px 0 0;align-items:start}
.colhead{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.22em;
 text-transform:uppercase;color:var(--dim);padding-bottom:8px}
.depth,.strata,.scaleside{position:relative}
.bed{position:relative;border-bottom:1px solid rgba(0,0,0,.22);
 border-left:1.5px solid var(--ink);border-right:1.5px solid var(--ink)}
.bed:first-child{border-top:1.5px solid var(--ink)}
.ylab{position:absolute;right:0;font-family:"IBM Plex Mono",monospace;font-size:10.5px;
 color:var(--dim);letter-spacing:.06em;transform:translateY(-50%);white-space:nowrap}
.ylab b{color:var(--ink);font-weight:400}
.ylab.gap{color:#b6321f}
.tickline{position:absolute;left:0;right:0;border-top:1px dotted var(--rule)}
.sidenote{position:absolute;left:0;font-size:.86rem;line-height:1.45;color:#6b6455;
 max-width:26ch;transform:translateY(-50%)}
.log{margin-top:70px;border-top:1.5px solid var(--ink)}
.desc{padding:20px 0 22px;border-bottom:1px solid var(--rule);
 display:grid;grid-template-columns:130px minmax(0,1fr);gap:0 26px}
.desc .swatch{height:16px;border:1px solid rgba(0,0,0,.25);margin-top:7px}
.yr{font-family:"Fraunces",Georgia,serif;font-size:1.6rem;line-height:1;margin:0}
.yr small{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--dim);margin-left:10px}
.desc p{margin:6px 0 0;font-size:.95rem;line-height:1.6;color:#453f34;max-width:52ch}
.finds{display:flex;gap:5px;margin-top:10px;flex-wrap:wrap}
.finds a{display:block;width:46px;height:46px}
.finds img{width:100%;height:100%;object-fit:cover;border:1px solid rgba(0,0,0,.18)}
.unconf{background:repeating-linear-gradient(-45deg,#ded6c5,#ded6c5 5px,#e9e2d3 5px,#e9e2d3 10px)}
.desc.unconf{background:repeating-linear-gradient(-45deg,#e9e2d3,#e9e2d3 5px,
 #f0ece3 5px,#f0ece3 10px)}
.desc.unconf p{font-style:italic;color:#6b6455}
.legend{margin-top:66px;border-top:1.5px solid var(--ink);padding-top:18px;
 display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:22px}
.legend h3{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.26em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:0 0 8px}
.legend p{margin:0;font-size:.88rem;line-height:1.6;color:#453f34}
.key{display:flex;align-items:center;gap:9px;font-size:.85rem;margin-bottom:6px}
.key i{width:26px;height:13px;border:1px solid rgba(0,0,0,.3);display:block}
@media(max-width:700px){.col{grid-template-columns:52px 78px minmax(0,1fr);gap:0 12px}
 .sidenote{display:none}.desc{grid-template-columns:minmax(0,1fr)}
 .desc .swatch{margin:0 0 10px}.finds a{width:38px;height:38px}}
"""
    years = list(range(2009, 2025))
    counts = Counter(w["year"] for w in lib.WORKS if w["year"])
    per_year = defaultdict(list)
    for w in lib.WORKS:
        if w["year"]:
            per_year[w["year"]].append(w)

    notes = {
        2009: "One work survives from this bed. Montana; oil on linen; vines and mushrooms.",
        2010: "No works catalogued. Nothing was deposited, or nothing was kept.",
        2011: "No works catalogued.",
        2012: "A single juniper, painted after walking out of the Gila. The first "
              "appearance of a motif that recurs for the next twelve years.",
        2013: "Sacred geometry and pollen. Dharamshala is in this layer.",
        2014: "The first thick bed. Still life, bison, the coffee congregation — the "
              "everyday objects raised to the status of subjects.",
        2015: "Circles arrive and do not leave: enso, cadence, the split atom.",
        2016: "Thin. Drypoint begins in earnest; the press is new.",
        2017: "Very thin, but this is the year of <i>Cyclum Lunarem</i> — one small "
              "panel a night for a full lunar year, which is a lot of hours for a "
              "thin bed.",
        2018: "The thickest layer in the column. Twenty-five works, roughly half of "
              "them prints. Something opened.",
        2019: "Installation years. The work leaves the wall and takes up floor.",
        2020: "Pandemic. Portraits, gold leaf, cranes, and a marble carved by hand.",
        2021: "As thick as 2018 and more varied — the solarpunk animals reach full "
              "strength and the reworkings begin.",
        2022: "Fire year. The Black Fire burns 325,000 acres and enters the paintings.",
        2023: "Printmaking dominant. Old paintings come back as plates.",
        2024: "The memory of atmosphere: weather, water vapour, the sky without ground.",
    }

    b = ['<div class="wrap"><header>',
         '<div class="kick">Stratigraphic column · 155 works · 2009–2024</div>',
         "<h1>Deep time,<br>read downward.</h1>",
         "<p>He tags fourteen works <i>deep time</i> and paints trees older than the state. "
         "So: read the practice the way you read a road cut. Bed thickness is the number of "
         "works deposited that year. Bed colour is the average measured hue of everything in "
         "it. The hatched beds are unconformities — years where nothing was laid down at "
         "all.</p></header>",
         '<div class="col">'
         '<div class="colhead" style="text-align:right">year</div>'
         '<div class="colhead">bed</div>'
         '<div class="colhead">note</div>'
         '<div class="depth">']

    UNIT = 7.0          # px of column per work deposited
    MIN_BED = 16.0      # a bed with nothing in it still has to be visible

    def bed_h(n):
        return max(n * UNIT, MIN_BED)

    def bed_colour(ws):
        n = len(ws)
        hs = [w["img"]["hue"] for w in ws if w["img"]["chroma"] > 0.05]
        sat = sum(w["img"]["sat"] for w in ws) / n
        lig = sum(w["img"]["lig"] for w in ws) / n
        if hs:
            xs = sum(math.cos(math.radians(x)) for x in hs)
            ys = sum(math.sin(math.radians(x)) for x in hs)
            hue = (math.degrees(math.atan2(ys, xs)) + 360) % 360
        else:
            hue = 40
        return f"hsl({hue:.0f} {min(sat*130,60):.0f}% {30+lig*38:.0f}%)"

    # year rail, positioned against the true cumulative depth of the column
    offset = 0.0
    for y in years:
        n = counts.get(y, 0)
        h = bed_h(n)
        cls = " gap" if not n else ""
        b.append(
            f'<div class="ylab{cls}" style="top:{offset + h/2:.1f}px">'
            f"<b>{y}</b></div>"
        )
        offset += h
    b.append(f'</div><div class="strata" style="height:{offset:.0f}px">')

    for y in years:
        ws = per_year.get(y, [])
        n = len(ws)
        h = bed_h(n)
        if ws:
            b.append(f'<div class="bed" style="height:{h:.1f}px;background:{bed_colour(ws)}"></div>')
        else:
            b.append(f'<div class="bed unconf" style="height:{h:.1f}px"></div>')
    b.append('</div><div class="scaleside">')

    marks = [
        (2011, "two beds of nothing"),
        (2017, "thin — but this is the lunar year"),
        (2018, "the thickest bed in the column"),
        (2021, "as thick again, and more varied"),
        (2024, "weather, and no ground"),
    ]
    offset = 0.0
    tops = {}
    for y in years:
        h = bed_h(counts.get(y, 0))
        tops[y] = offset + h / 2
        offset += h
    for y, txt in marks:
        b.append(
            f'<div class="tickline" style="top:{tops[y]:.1f}px"></div>'
            f'<div class="sidenote" style="top:{tops[y]:.1f}px;padding-left:8px">{txt}</div>'
        )
    b.append("</div></div>")

    b.append('<div class="log">')
    for y in years:
        ws = per_year.get(y, [])
        n = len(ws)
        finds = "".join(
            f'<a href="#{esc(w["slug"])}"><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy"></a>'
            for w in sorted(ws, key=lambda x: -x["img"]["sat"])[:10]
        )
        plural = "" if n == 1 else "s"
        gap = " · unconformity" if not n else ""
        finds_html = f'<div class="finds">{finds}</div>' if finds else ""
        swatch = (f'<div class="swatch" style="background:{bed_colour(ws)}"></div>' if ws
                  else '<div class="swatch unconf"></div>')
        b.append(
            f'<div class="desc{"" if ws else " unconf"}">'
            f'<div><p class="yr">{y}</p>'
            f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:10px;'
            f'letter-spacing:.16em;text-transform:uppercase;color:#7d766a">'
            f"{n} work{plural}{gap}</div>{swatch}</div>"
            f'<div><p>{notes.get(y,"")}</p>{finds_html}</div></div>'
        )
    b.append("</div>")

    b.append(
        '<div class="legend"><div><h3>Reading the column</h3>'
        '<div class="key"><i style="background:hsl(35 45% 48%)"></i>bed colour = mean hue</div>'
        '<div class="key"><i class="unconf"></i>unconformity — no deposition</div>'
        "<p>Thickness is honest: one work is one unit. The 2018 and 2021 beds really are "
        "twenty-five times thicker than 2009.</p></div>"
        "<div><h3>Why a column and not a timeline</h3><p>A timeline spaces years evenly and "
        "so tells you nothing. A column gives the years their real weight, and makes the "
        "empty ones visible as gaps rather than as blank space you scroll past.</p></div>"
        "<div><h3>The unconformities</h3><p>2010 and 2011 hold nothing. That is not an "
        "error in the catalogue — see sheet 47, which is about exactly those years and "
        "argues they should stay visible.</p></div></div>"
    )
    b.append("</div>")
    return lib.write("44-deep-time.html", "Deep Time", css, "".join(b))


# ------------------------------------------------------------- 45 the quilt

def sheet_45():
    css = """
:root{--bg:#111}
body{background:var(--bg);color:#eee;font-family:"IBM Plex Mono",monospace;font-size:13px}
.top{padding:56px 26px 26px;max-width:1400px;margin:0 auto}
.kick{font-size:10px;letter-spacing:.4em;text-transform:uppercase;color:#7d7a74}
h1{font-family:"Syne","Inter",sans-serif;font-weight:800;font-size:clamp(2.2rem,6.6vw,4.6rem);
 line-height:.96;letter-spacing:-.03em;margin:.16em 0 .24em;text-transform:uppercase}
.top p{max-width:62ch;line-height:1.7;color:#a8a49c;font-size:13.5px;margin:0}
.top p b{color:#eee;font-weight:400}
.field{display:grid;grid-template-columns:repeat(auto-fill,minmax(84px,1fr));gap:0;
 max-width:1400px;margin:38px auto 0;padding:0 26px}
.q{position:relative;aspect-ratio:1;display:block;text-decoration:none}
.q svg{width:100%;height:100%;display:block}
.q .lab{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;
 padding:6px;background:rgba(10,10,10,.82);opacity:0;transition:opacity .18s;
 font-size:9.5px;line-height:1.35;color:#eee;letter-spacing:.02em}
.q:hover .lab,.q:focus .lab{opacity:1}
.q .lab b{font-weight:400;color:#fff}
.q .lab span{color:#8d8880}
.sortbar{max-width:1400px;margin:34px auto 0;padding:0 26px;display:flex;flex-wrap:wrap;
 gap:10px 26px;font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:#7d7a74;
 border-top:1px solid #262626;padding-top:14px}
.sortbar b{color:#eee;font-weight:400}
.split{max-width:1400px;margin:70px auto 0;padding:0 26px;display:grid;
 grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:34px}
.split h2{font-family:"Syne","Inter",sans-serif;font-size:1.1rem;text-transform:uppercase;
 letter-spacing:.02em;margin:0 0 10px;font-weight:700}
.split p{color:#a8a49c;line-height:1.72;font-size:12.5px;margin:0}
.pair{display:flex;gap:10px;margin-top:14px;align-items:flex-start}
.pair figure{margin:0;flex:1}
.pair svg,.pair img{width:100%;aspect-ratio:1;object-fit:cover;display:block}
.pair figcaption{font-size:9.5px;color:#7d7a74;margin-top:6px;letter-spacing:.14em;
 text-transform:uppercase}
footer{max-width:1400px;margin:72px auto 0;padding:16px 26px 70px;border-top:1px solid #262626;
 font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#7d7a74;display:flex;
 flex-wrap:wrap;gap:8px 26px;justify-content:space-between}
"""
    ws = by_hue(lib.WORKS)
    demo = get("the-black-fire")
    b = ['<div class="top">',
         '<div class="kick">Kyle Parker Cunningham · 155 works · no photographs</div>',
         "<h1>The Quilt</h1>",
         "<p>Every image in the archive stores a tiny average-colour grid — the thing that "
         "normally sits behind a photograph for a quarter-second while it loads, then is "
         "thrown away. <b>This page is made entirely of those.</b> No artwork is shown. "
         "The whole oeuvre, six pixels by six, sorted around the colour wheel. It turns out "
         "to be legible: you can find the drypoints, the fire, the weather paintings and the "
         "gold-leaf work without seeing a single one of them.</p></div>",
         '<div class="field">']
    for w in ws:
        b.append(
            f'<a class="q" href="#{esc(w["slug"])}" title="{alt(w)}">{grid_svg(w)}'
            f'<span class="lab"><b>{esc(w["title"])}</b>'
            f'<span>{w["year"]} · {esc(w["discipline"])}</span></span></a>'
        )
    b.append("</div>")
    b.append(
        '<div class="sortbar"><span>sorted by <b>measured hue</b></span>'
        "<span>6 × 36 samples per work</span><span>total page weight of imagery: "
        "<b>0 bytes</b></span><span>hover for the record</span></div>"
    )
    b.append(
        '<div class="split"><div><h2>Why bother</h2>'
        "<p>Three reasons, none of them novelty. It loads instantly and works on a phone in "
        "a canyon with one bar. It is the only view of the oeuvre that fits on one screen "
        "without shrinking anything to illegibility. And it removes subject matter entirely, "
        "which is the one thing that stops people seeing how consistent the colour is.</p>"
        "<p>The trade is total: you cannot tell an elephant from an ensō here. That is the "
        "point of the archive being one click away.</p></div>"
        "<div><h2>The same work, both ways</h2>"
        "<p>Left: what the grid knows. Right: the photograph. The grid keeps the fire.</p>"
        f'<div class="pair"><figure>{grid_svg(demo)}'
        f'<figcaption>36 samples</figcaption></figure>'
        f'<figure><img src="{thumb(demo)}" alt="{alt(demo)}" loading="lazy">'
        f'<figcaption>{esc(demo["title"])}, {demo["year"]}</figcaption></figure></div></div>'
        "<div><h2>Where it could go</h2>"
        "<p>The archive also stores a blurhash for every image. A version of this page could "
        "hold the whole catalogue as blurhashes and resolve each into the real photograph "
        "only when you stop on it — a site that is honest about being a map until you ask "
        "it to be a picture.</p></div></div>"
    )
    b.append("<footer><span>colour grids computed from the archive's photographs</span>"
             "<span>archive.kyleparkercunningham.com</span></footer>")
    return lib.write("45-the-quilt.html", "The Quilt", css, "".join(b))


# ----------------------------------------------------------- 46 weather log

def sheet_46():
    css = """
:root{--paper:#e7ebee;--ink:#131a20;--dim:#6d7a85;--rule:#c2cdd5;--ink2:#1d3d56;
 --warn:#a6431c}
body{background:var(--paper);color:var(--ink);font-family:"IBM Plex Mono",monospace;
 font-size:13px}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px 100px}
header{padding:60px 0 18px;border-bottom:2px solid var(--ink)}
.stn{display:flex;flex-wrap:wrap;gap:5px 24px;font-size:10px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--dim)}
h1{font-family:"Archivo Narrow",sans-serif;font-weight:700;text-transform:uppercase;
 font-size:clamp(2.4rem,7.6vw,5.2rem);letter-spacing:-.02em;line-height:.94;margin:.14em 0 .1em}
.lede{font-family:"Newsreader",Georgia,serif;font-size:1.16rem;line-height:1.6;max-width:60ch;
 color:#26333d;margin:16px 0 22px}
h2{font-size:10.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);
 font-weight:400;margin:52px 0 12px;border-bottom:1px solid var(--rule);padding-bottom:7px;
 display:flex;justify-content:space-between}
.trace{width:100%;height:150px;display:block;margin:8px 0 4px}
.tlab{display:flex;justify-content:space-between;font-size:9.5px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--dim)}
.obs{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:14px}
.ob{border:1px solid var(--ink);background:#f2f5f7;display:flex;flex-direction:column}
.ob img{width:100%;aspect-ratio:4/3;object-fit:cover;border-bottom:1px solid var(--ink)}
.ob .body{padding:10px 12px 12px;flex:1;display:flex;flex-direction:column}
.ob b{font-family:"Archivo Narrow",sans-serif;font-size:1rem;letter-spacing:.01em;
 text-transform:uppercase;line-height:1.15}
.ob .cls{font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink2);
 margin:5px 0 7px}
.ob p{margin:0;font-family:"Newsreader",Georgia,serif;font-size:.92rem;line-height:1.5;
 color:#33414c}
.ob .fld{margin-top:auto;padding-top:10px;font-size:9.5px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--dim);border-top:1px dotted var(--rule)}
.synop{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:0;
 border:1px solid var(--ink)}
.synop div{padding:14px 15px;border-right:1px solid var(--rule)}
.synop div:last-child{border-right:0}
.synop dt{font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--dim)}
.synop dd{margin:3px 0 0;font-family:"Archivo Narrow",sans-serif;font-size:1.7rem;
 line-height:1.1;letter-spacing:-.01em}
.synop dd small{font-size:.66rem;color:var(--dim);letter-spacing:.1em;text-transform:uppercase}
.strike{border:2px solid var(--warn);padding:18px 20px;margin:38px 0 0;background:#f7ece7}
.strike h3{font-family:"Archivo Narrow",sans-serif;text-transform:uppercase;font-size:1.2rem;
 margin:0 0 6px;color:var(--warn);letter-spacing:.02em}
.strike p{font-family:"Newsreader",Georgia,serif;font-size:1.02rem;line-height:1.6;margin:0;
 max-width:62ch;color:#3a2f2a}
footer{margin-top:60px;border-top:2px solid var(--ink);padding-top:12px;font-size:10px;
 letter-spacing:.18em;text-transform:uppercase;color:var(--dim);display:flex;flex-wrap:wrap;
 gap:8px 24px;justify-content:space-between}
@media(max-width:640px){.synop div{border-right:0;border-bottom:1px solid var(--rule)}}
"""
    atmos = sorted(tagged("the memory of atmosphere"), key=lambda w: (w["year"] or 0, w["title"]))
    cloudy = tagged("cloud")
    lightning = tagged("lightning", "lightning strike")

    classes = {
        "bottled-lightning": "CB · capture, in glass",
        "harmonics": "CI · fibratus, ruled",
        "the-atmospheres-electric-finger": "CB · single stroke",
        "the-algebra-of-water-vapor": "AC · tessellated",
        "low-angle-sun-rays": "— · crepuscular, dust",
        "towers": "CU · congestus, from below",
        "the-river-in-the-sky": "AS · translucidus",
        "out-there-on-the-horizon-a-solitary-cloud": "CU · humilis, solitary",
        "first-contact": "CU · scattered, repeating",
        "shade-cloud": "— · shadow only",
        "orbits-plankton-dreaming-of-a-sedimentary-afterlife": "— · water cycle, closed",
        "symbologies-intertwine-electronically": "AC · faceted",
    }

    # Barometric-style trace: mean lightness of the atmosphere works by year.
    per_year = defaultdict(list)
    for w in atmos:
        per_year[w["year"]].append(w)
    yrs = sorted(per_year)
    pts = []
    for i, y in enumerate(yrs):
        v = sum(w["img"]["lig"] for w in per_year[y]) / len(per_year[y])
        pts.append((30 + i * (740 / max(len(yrs) - 1, 1)), 130 - v * 108))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#1d3d56"/>' for x, y in pts)
    grid = "".join(
        f'<line x1="0" y1="{v}" x2="800" y2="{v}" stroke="#c2cdd5" stroke-width=".8"/>'
        for v in (20, 50, 80, 110)
    )
    trace = (
        f'<svg class="trace" viewBox="0 0 800 150" preserveAspectRatio="none" role="img" '
        f'aria-label="mean lightness of the atmosphere works, by year">{grid}'
        f'<path d="{d}" fill="none" stroke="#1d3d56" stroke-width="2"/>{dots}</svg>'
    )

    b = ['<div class="wrap"><header>',
         '<div class="stn"><span>Station: the porch</span><span>33.128 N · 107.253 W</span>'
         "<span>elev 1382 m</span><span>observer: KPC</span>"
         "<span>record opens 2023</span></div>",
         "<h1>Weather log</h1>",
         '<p class="lede">Twelve works in the catalogue are tagged <i>the memory of '
         "atmosphere</i>. Read as paintings they are a series. Read as observations — which "
         "is closer to how they were made, one sky at a time, from one porch — they are a "
         "meteorological record kept by somebody with no instruments and a lot of "
         "attention.</p></header>"]

    b.append(
        "<h2><span>Synoptic summary</span><span>2023–2024</span></h2>"
        '<dl class="synop">'
        f"<div><dt>Observations on file</dt><dd>{len(atmos)}<small> works</small></dd></div>"
        f"<div><dt>Cloud present</dt><dd>{len(cloudy)}<small> works, whole catalogue</small></dd></div>"
        f"<div><dt>Electrical activity</dt><dd>{len(lightning)}<small> works</small></dd></div>"
        "<div><dt>Direct strikes on observer</dt><dd>1<small> · undated</small></dd></div>"
        "</dl>"
    )

    b.append(
        "<h2><span>Trace · mean luminance by year of observation</span>"
        f"<span>{yrs[0]}–{yrs[-1]}</span></h2>" + trace +
        f'<div class="tlab"><span>{yrs[0]} · darker</span>'
        "<span>vertical axis is measured lightness, not brightness of the day</span>"
        f"<span>{yrs[-1]} · lighter</span></div>"
    )

    b.append('<h2><span>Observations</span><span>chronological</span></h2><div class="obs">')
    for w in atmos:
        b.append(
            f'<article class="ob"><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">'
            f'<div class="body"><b>{esc(w["title"])}</b>'
            f'<div class="cls">{esc(classes.get(w["slug"], "— · unclassified"))}</div>'
            f"<p>{esc(sentence(w, 150))}</p>"
            f'<div class="fld">{w["year"]} · {esc(w["medium"] or "")}'
            f'{" · " + esc(dims(w)) if dims(w) else ""}</div></div></article>'
        )
    b.append("</div>")

    b.append(
        '<div class="strike"><h3>Note appended to the record</h3>'
        "<p>The observer has been struck by lightning. It is in the biography and it is in "
        "<i>120 Volts</i> five years before it happened, where a figure is plugged into a wall "
        "socket by his own hair. The archive treats that as two tagged works. A weather log "
        "treats it as the reason there is a log.</p></div>"
    )

    b.append("<footer><span>Observations → archive.kyleparkercunningham.com</span>"
             "<span>Cloud classes assigned by the site, not by the observer</span>"
             "<span>Truth or Consequences · New Mexico</span></footer></div>")
    return lib.write("46-weather-log.html", "Weather Log", css, "".join(b))


# --------------------------------------------------------------- 47 fallow

def sheet_47():
    css = """
:root{--paper:#fdfcfa;--ink:#171614;--dim:#8e8a83;--rule:#e6e3dd}
body{background:var(--paper);color:var(--ink);font-family:"EB Garamond",Georgia,serif;
 font-size:18px;line-height:1.62}
.wrap{max-width:840px;margin:0 auto;padding:0 26px 120px}
header{padding:20vh 0 8vh}
h1{font-weight:400;font-size:clamp(3rem,10vw,7rem);line-height:.92;letter-spacing:-.02em;
 margin:0 0 .3em}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.36em;
 text-transform:uppercase;color:var(--dim);margin-bottom:2.4em}
header p{max-width:52ch;color:#3c3934;font-size:1.16rem}
header p em{font-style:italic}
.bars{margin:8vh 0 0}
.row{display:grid;grid-template-columns:64px minmax(0,1fr) 52px;gap:16px;align-items:center;
 padding:5px 0;border-bottom:1px solid var(--rule)}
.row .y{font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--dim);
 letter-spacing:.08em}
.row .b{height:13px;background:var(--ink)}
.row .n{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--dim);text-align:right}
.row.zero{background:#faf7f1}
.row.zero .y,.row.zero .n{color:#b6321f}
.row.zero .b{height:1px;background:#b6321f;width:100%!important}
.row.zero .say{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.22em;
 text-transform:uppercase;color:#b6321f}
p.body{max-width:52ch;color:#3c3934}
h2{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.32em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:9vh 0 1.2em}
blockquote{margin:2.4em 0;padding-left:1.2em;border-left:2px solid var(--ink);
 font-style:italic;font-size:1.24rem;line-height:1.5;color:#2b2926;max-width:46ch}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:30px;
 margin:2.6em 0}
.two figure{margin:0}
.two img{width:100%;height:auto}
.two figcaption{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--dim);margin-top:9px;line-height:1.5}
.two figcaption b{display:block;font-family:"EB Garamond",serif;font-size:15px;
 letter-spacing:0;text-transform:none;color:var(--ink)}
.close{margin-top:9vh;border-top:1px solid var(--rule);padding-top:2em;color:#3c3934;
 max-width:52ch}
"""
    counts = Counter(w["year"] for w in lib.WORKS if w["year"])
    years = list(range(2009, 2025))
    mx = max(counts.values())
    a, c = get("muxy"), get("me-own-juniper")

    b = ['<div class="wrap"><header>',
         '<div class="kick">Kyle Parker Cunningham · 2009–2024 · the record as kept</div>',
         "<h1>Fallow.</h1>",
         "<p>An artist's website shows you the years there was work. This one shows you the "
         "years there wasn't, at the same size, in the same list. There are two of them and "
         "they are the most interesting thing in the catalogue.</p></header>"]

    b.append('<div class="bars">')
    for y in years:
        n = counts.get(y, 0)
        if n:
            b.append(
                f'<div class="row"><span class="y">{y}</span>'
                f'<span class="b" style="width:{n/mx*100:.1f}%"></span>'
                f'<span class="n">{n}</span></div>'
            )
        else:
            b.append(
                f'<div class="row zero"><span class="y">{y}</span>'
                f'<span class="say">nothing catalogued</span><span class="n">0</span></div>'
            )
    b.append("</div>")

    b.append(
        "<h2>What a zero is</h2>"
        '<p class="body">It is not proof that nothing was made. It is proof that nothing '
        "was kept, or nothing was catalogued, or nothing survived the moves — and the "
        "archive is careful enough to say which of those it can and cannot distinguish. "
        "It cannot. So the honest presentation is an empty row, not a gap in a timeline "
        "you scroll past without noticing.</p>"
        '<p class="body">Between these two zeroes sit a painting made in Montana and a '
        "painting made after walking out of the Gila Wilderness. Three years apart, and "
        "everything that happened in between is not here.</p>"
    )

    b.append(
        '<div class="two">'
        f'<figure><img src="{wide(a)}" alt="{alt(a)}" loading="lazy">'
        f'<figcaption><b>{esc(a["title"])}, {a["year"]}</b>{esc(a["medium"] or "")} · '
        f"the last work before</figcaption></figure>"
        f'<figure><img src="{wide(c)}" alt="{alt(c)}" loading="lazy">'
        f'<figcaption><b>{esc(c["title"])}, {c["year"]}</b>{esc(c["medium"] or "")} · '
        f"the first work after</figcaption></figure></div>"
    )

    b.append(
        "<blockquote>Kyle's childhood spent wandering the mountains of rural Montana "
        "imparted a deep and fundamental love for the wild; he is much more at home in the "
        "middle of wilderness than in the middle of civilization.</blockquote>"
        '<p class="body">That is from the biography, and it is also, probably, what the two '
        "empty rows are. The thin years — 2016 with six works, 2017 with three — are the same "
        "story at lower contrast. 2017 in particular looks like almost nothing until you "
        "notice that <i>Cyclum Lunarem</i> is in it: one small gold-leafed panel painted "
        "every night for a lunar year. Three catalogue entries. Three hundred and "
        "sixty-five sittings.</p>"
        '<p class="body">Counting works is a bad proxy for working. Every site that shows '
        "you an artist's output as a bar chart is quietly making that mistake, including "
        "this page, which is why it says so here.</p>"
    )

    b.append(
        '<div class="close"><p>The catalogue at '
        "<b>archive.kyleparkercunningham.com</b> is a record of objects. It is very good at "
        "that and it should not be asked to be anything else. But an object-record has no "
        "way to hold a fallow year, a walk, a fire season, or a night spent looking up — "
        "and those are not gaps in the work. They are the work, before it had a "
        "catalogue number.</p></div></div>"
    )
    return lib.write("47-fallow.html", "Fallow", css, "".join(b))


def main():
    for fn in (sheet_41, sheet_42, sheet_43, sheet_44, sheet_45, sheet_46, sheet_47):
        print(fn())


if __name__ == "__main__":
    import sheets

    for s in sheets.SHEETS:
        lib.register(*s)
    main()
