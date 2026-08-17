#!/usr/bin/env python3
"""Sheets 56–62 — time, cycle, lineage.

The seasons idea taken further than an issue: an almanac, a lunar year, a
day, an ephemeris. Then the three sheets about return — the pairs, the
motifs, and the works that have descendants.
"""

import math
from collections import Counter, defaultdict

import lib
from lib import (alt, blurb, dims, esc, get, many, revisits, sentence, tagged,
                 thumb, wide)


# --------------------------------------------------------------- 56 almanac

MONTHS = [
    ("January", "Wolf moon", "long nights, small plates",
     "Drypoint season. The press is cold and the plates are small because the "
     "studio is cold. Cut, proof, cut again.", ["riot-ghost", "boom-box"]),
    ("February", "Snow moon", "print specs and image prep",
     "The Periodic gets set. Newsprint stock confirmed, four pages, one colour.",
     ["ghost-thugs", "six"]),
    ("March", "Worm moon", "the ground thaws slowly",
     "The press comes back online. First hand-colouring of the year.",
     ["stole-the-rainbow-2", "pruning"]),
    ("April", "Pink moon", "seed and plate",
     "Garden goes in. Beetroot and sunflowers arrive on copper within the month.",
     ["origami-beetroot", "sunflowers"]),
    ("May", "Flower moon", "before the heat",
     "The last comfortable month to paint outside in the Chihuahuan desert.",
     ["prickly-pear", "nogal-canyon"]),
    ("June", "Strawberry moon", "solstice — the season opens",
     "The longest day. The new edition goes live; the first of the 200 go up.",
     ["solar-ascension", "out-there-on-the-horizon-a-solitary-cloud"]),
    ("July", "Buck moon", "monsoon builds",
     "Everything on this page that has a cloud in it was painted in the two "
     "months either side of now.", ["towers", "monsoon-bird"]),
    ("August", "Sturgeon moon", "monsoon",
     "Lightning season. Stay off the ridges. He did not, once.",
     ["bottled-lightning", "the-atmospheres-electric-finger"]),
    ("September", "Harvest moon", "equinox — the season closes",
     "Equal night. The edition retires whole to its permanent URL and a new one "
     "is composed.", ["corn-sky-connection", "three-blue-corn"]),
    ("October", "Hunter's moon", "the light goes long",
     "Low-angle sun. The best month for the studio's north window.",
     ["low-angle-sun-rays", "path-though-the-autumn-leaves"]),
    ("November", "Beaver moon", "inventory",
     "Everything gets measured, photographed, and written into the archive. "
     "This is the month the catalogue actually gets made.",
     ["autumnal-twilight", "transition"]),
    ("December", "Cold moon", "solstice — the turn",
     "Shortest day. Gold leaf, because it is the only thing that behaves like "
     "light when there isn't any.", ["cyclum-lunarem", "migratory-scavengers"]),
]


def sheet_56():
    css = """
:root{--paper:#f4efe0;--ink:#211c12;--red:#93331f;--dim:#7c745f;--rule:#cec4a9}
body{background:var(--paper);color:var(--ink);font-family:"Fraunces",Georgia,serif;
 font-size:16px}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px 90px}
header{text-align:center;padding:58px 0 22px;border-bottom:5px double var(--ink)}
.over{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.4em;
 text-transform:uppercase;color:var(--dim)}
h1{font-weight:400;font-size:clamp(2.6rem,8.6vw,5.6rem);line-height:.94;margin:.14em 0 .1em;
 letter-spacing:-.02em;font-variation-settings:"SOFT" 40,"WONK" 1}
.byline{font-style:italic;color:var(--dim);font-size:1.06rem}
.strap{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 26px;margin-top:14px;
 font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.22em;
 text-transform:uppercase;color:var(--dim)}
.wheel{display:grid;grid-template-columns:minmax(0,260px) minmax(0,1fr);gap:34px;
 align-items:center;padding:34px 0;border-bottom:1px solid var(--rule)}
.wheel svg{width:100%;height:auto}
.wheel p{margin:0 0 12px;line-height:1.66;color:#3a3427;max-width:56ch}
.wheel p b{font-weight:600}
.months{display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));gap:0}
.m{border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:20px 20px 22px}
.m .no{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.24em;
 text-transform:uppercase;color:var(--red)}
.m h2{font-weight:400;font-size:1.7rem;margin:.1em 0 .04em;letter-spacing:-.01em}
.m .moon{font-style:italic;color:var(--dim);font-size:.94rem}
.m .doing{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--ink);border-top:1px solid var(--rule);
 border-bottom:1px solid var(--rule);padding:6px 0;margin:12px 0 10px}
.m p{margin:0 0 12px;font-size:.95rem;line-height:1.58;color:#3a3427}
.m .pair{display:flex;gap:7px}
.m .pair a{flex:1;text-decoration:none}
.m .pair img{width:100%;aspect-ratio:1;object-fit:cover;border:1px solid var(--rule)}
.m .pair span{display:block;font-family:"IBM Plex Mono",monospace;font-size:8.5px;
 letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin-top:4px;line-height:1.4}
.tables{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:26px;
 margin-top:40px;border-top:5px double var(--ink);padding-top:24px}
.tables h3{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.26em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:0 0 10px}
.tables table{width:100%;border-collapse:collapse;font-size:.9rem}
.tables td{padding:3px 0;border-bottom:1px dotted var(--rule)}
.tables td:last-child{text-align:right;font-family:"IBM Plex Mono",monospace;font-size:.78rem;
 color:var(--dim)}
.lore{font-style:italic;line-height:1.6;color:#3a3427;font-size:.96rem}
@media(max-width:700px){.wheel{grid-template-columns:minmax(0,1fr)}}
"""
    # A real year wheel: each month's wedge carries the mean colour of the works
    # this almanac assigns to it.
    wedges = []
    for i, (name, moon, doing, note, slugs) in enumerate(MONTHS):
        ws = many(*slugs)
        if ws:
            im = ws[0]["img"]
            col = f"hsl({im['hue']:.0f} {min(im['sat']*140,64):.0f}% {32+im['lig']*40:.0f}%)"
        else:
            col = "#c9bfa4"
        a0 = math.radians(i * 30 - 90)
        a1 = math.radians((i + 1) * 30 - 90)
        x0, y0 = 110 + math.cos(a0) * 100, 110 + math.sin(a0) * 100
        x1, y1 = 110 + math.cos(a1) * 100, 110 + math.sin(a1) * 100
        wedges.append(
            f'<path d="M110,110 L{x0:.1f},{y0:.1f} A100,100 0 0,1 {x1:.1f},{y1:.1f} Z" '
            f'fill="{col}" stroke="#f4efe0" stroke-width="1.2"/>'
        )
        am = (a0 + a1) / 2
        wedges.append(
            f'<text x="{110+math.cos(am)*76:.1f}" y="{110+math.sin(am)*76+3:.1f}" '
            f'font-size="9" fill="rgba(255,255,255,.9)" text-anchor="middle" '
            f'font-family="monospace">{name[:1]}</text>'
        )
    for r, lab in ((100, ""),):
        wedges.append(f'<circle cx="110" cy="110" r="{r}" fill="none" stroke="#211c12"/>')
    wedges.append('<circle cx="110" cy="110" r="34" fill="#f4efe0" stroke="#211c12"/>')
    wedges.append('<text x="110" y="106" font-size="10" text-anchor="middle" '
                  'font-family="monospace" fill="#7c745f">SEASON</text>')
    wedges.append('<text x="110" y="121" font-size="16" text-anchor="middle" '
                  'font-family="monospace" fill="#211c12">XIII</text>')

    b = ['<div class="wrap"><header>',
         '<div class="over">Agile Meteor Press · issued yearly · price: nothing</div>',
         "<h1>The Studio Almanac</h1>",
         '<div class="byline">Being a calendar of the working year, with the moons, '
         "the light, and what is on the easel</div>",
         '<div class="strap"><span>Thirteenth season</span><span>2026</span>'
         "<span>lat 33.128 N</span><span>Truth or Consequences, N.M.</span></div></header>"]

    b.append(
        '<section class="wheel"><svg viewBox="0 0 220 220" role="img" '
        'aria-label="the working year as a wheel, each month coloured by its work">'
        + "".join(wedges) + "</svg><div>"
        "<p>An <b>edition</b> is a magazine issue: it opens, it runs, it retires. An "
        "<b>almanac</b> is different — it assumes you will come back, and it tells you what "
        "to expect before it happens. That is the better fit for a practice that has run "
        "on solstices and equinoxes since 2017.</p>"
        "<p>The seasons already work this way. Season XIII opened at the June solstice and "
        "closes at the September equinox. What an almanac adds is the <b>whole ring visible "
        "at once</b>, so a visitor in February can see that August is lightning and December "
        "is gold leaf, and decide to come back.</p></div></section>"
    )

    b.append('<div class="months">')
    for i, (name, moon, doing, note, slugs) in enumerate(MONTHS, 1):
        ws = many(*slugs)
        pair = "".join(
            f'<a href="#{esc(w["slug"])}"><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">'
            f'<span>{esc(w["title"])}<br>{w["year"]}</span></a>' for w in ws
        )
        b.append(
            f'<section class="m"><div class="no">{i:02d}</div><h2>{esc(name)}</h2>'
            f'<div class="moon">{esc(moon)}</div>'
            f'<div class="doing">{esc(doing)}</div>'
            f'<p>{esc(note)}</p><div class="pair">{pair}</div></section>'
        )
    b.append("</div>")

    top_tags = list(lib.tag_counts("tags", 8).items())[:8]
    b.append(
        '<div class="tables"><div><h3>Table I · the seasons in force</h3><table>'
        "<tr><td>XIII · Everything That Can Be Carried</td><td>summer 2026 · live</td></tr>"
        "<tr><td>XII · The Ground Thaws Slowly</td><td>spring 2026 · retired</td></tr>"
        "<tr><td>XI · Long Nights, Small Plates</td><td>winter 2025 · retired</td></tr>"
        "<tr><td>X</td><td>autumn 2025 · retired</td></tr></table></div>"
        "<div><h3>Table II · what recurs</h3><table>"
        + "".join(f"<tr><td>{esc(t)}</td><td>{n} works</td></tr>" for t, n in top_tags)
        + "</table></div>"
        "<div><h3>Table III · fixed feasts</h3><table>"
        "<tr><td>Vernal equinox</td><td>edition composed</td></tr>"
        "<tr><td>Summer solstice</td><td>edition opens</td></tr>"
        "<tr><td>Autumnal equinox</td><td>edition retires</td></tr>"
        "<tr><td>Winter solstice</td><td>gold leaf</td></tr></table></div>"
        '<div><h3>Weather lore</h3><p class="lore">“On occasions, the electrons get out of '
        "balance. Randomly you just happen to be in that place at the wrong moment, right "
        "time, and the atmospheres' electricity chooses to flow through your body.”</p>"
        '<p style="font-family:\'IBM Plex Mono\',monospace;font-size:9.5px;letter-spacing:.14em;'
        "text-transform:uppercase;color:#7c745f\">— the artist, on <i>Bottled Lightning</i></p>"
        "</div></div></div>"
    )
    return lib.write("56-almanac.html", "The Studio Almanac", css, "".join(b))


# --------------------------------------------------------------- 57 lunarem

def sheet_57():
    css = """
:root{--night:#0a0c14;--ink:#e8e2d2;--gold:#c9a227;--dim:#6f6a5c}
body{background:var(--night);color:var(--ink);font-family:"Cormorant Garamond",Georgia,serif;
 font-size:17px;
 background-image:radial-gradient(ellipse at 50% -10%,#182036 0%,transparent 60%)}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px 100px}
header{text-align:center;padding:14vh 0 6vh}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.42em;
 text-transform:uppercase;color:var(--gold)}
h1{font-weight:300;font-size:clamp(3rem,10vw,7rem);line-height:.94;margin:.14em 0 .2em;
 letter-spacing:-.02em}
header p{max-width:52ch;margin:0 auto;color:#a49d8c;line-height:1.68}
header p i{color:var(--ink)}
.cycle{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:2px;margin:8vh 0 0}
.day{position:relative;aspect-ratio:1;background:#0a0c14;display:block;text-decoration:none;
 overflow:hidden}
/* The disc is an aperture, not a sticker: the work is only visible where the
   moon is lit. At new moon you get nothing; at full you get the whole crop. */
.day .disc{position:absolute;inset:0;display:grid;place-items:center}
.day .disc i{position:relative;display:block;width:64%;aspect-ratio:1;border-radius:50%;
 overflow:hidden;box-shadow:0 0 0 1px rgba(201,162,39,.4),0 0 22px rgba(201,162,39,.09)}
.day .disc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 transition:none}
.day .disc u{position:absolute;inset:0;display:block}
.day .full{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;
 transition:opacity .4s ease}
.day:hover .full{opacity:1}
.day:hover .disc{opacity:0;transition:opacity .4s ease}
.day .n{position:absolute;left:6px;top:5px;font-family:"IBM Plex Mono",monospace;
 font-size:9px;letter-spacing:.14em;color:var(--gold);z-index:2}
.day .t{position:absolute;left:6px;right:6px;bottom:5px;font-family:"IBM Plex Mono",monospace;
 font-size:8.5px;letter-spacing:.06em;color:#cfc7b2;opacity:0;transition:opacity .3s;
 line-height:1.35;z-index:2;text-transform:uppercase}
.day:hover .t{opacity:1}
.legend{display:flex;flex-wrap:wrap;gap:8px 28px;justify-content:space-between;margin-top:14px;
 font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.22em;
 text-transform:uppercase;color:var(--dim)}
.story{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:34px;
 margin-top:9vh;border-top:1px solid #1e2330;padding-top:30px}
.story h2{font-weight:400;font-size:1.5rem;margin:0 0 8px;font-style:italic;color:var(--gold)}
.story p{margin:0 0 12px;line-height:1.7;color:#a49d8c}
.story p b{color:var(--ink);font-weight:400}
.hero{margin:8vh 0 0}
.hero img{width:100%;height:auto}
.hero figcaption{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.18em;
 text-transform:uppercase;color:var(--dim);margin-top:12px;display:flex;flex-wrap:wrap;
 gap:6px 24px;justify-content:space-between}
@media(max-width:640px){.cycle{grid-template-columns:repeat(4,minmax(0,1fr))}}
"""
    ws = [w for w in lib.WORKS if w["img"]]
    ws = sorted(ws, key=lambda w: w["img"]["lig"])
    # 28 works, darkest at new moon, brightest at full — the work is chosen by
    # its own measured luminance, which is the only honest way to do this.
    picks = []
    step = max(len(ws) // 14, 1)
    waxing = ws[::step][:14]
    picks = waxing + list(reversed(waxing))[:14]

    b = ['<div class="wrap"><header>',
         '<div class="kick">Cyclum Lunarem · twenty-eight days · one work each</div>',
         "<h1>Lunarem</h1>",
         "<p>In 2017 he painted <i>the moons from an entire summer, starting on the summer "
         "solstice and completed on the autumnal equinox — each moon painted upon a 3⅜″ "
         "square prepared with linen and a traditional gesso ground, gilded with 24kt gold "
         "leaf.</i> This is that structure turned into a way of moving through everything "
         "else — twenty-eight nights, and the work only visible where the moon is "
         "lit.</p></header>",
         '<div class="cycle">']

    for i, w in enumerate(picks[:28]):
        phase = i / 28
        lit = 1 - abs(1 - phase * 2)          # 0 at new, 1 at full
        if phase <= 0.5:                       # waxing — lit on the right
            shade = (f"linear-gradient(90deg,#0a0c14 0%,#0a0c14 {(1-lit)*100:.0f}%,"
                     f"transparent {(1-lit)*100:.0f}%)")
        else:                                  # waning — lit on the left
            shade = (f"linear-gradient(90deg,transparent 0%,transparent {lit*100:.0f}%,"
                     f"#0a0c14 {lit*100:.0f}%)")
        b.append(
            f'<a class="day" href="#{esc(w["slug"])}">'
            f'<img class="full" src="{thumb(w)}" alt="" loading="lazy" aria-hidden="true">'
            f'<span class="n">{i+1:02d}</span>'
            f'<span class="disc"><i><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">'
            f'<u style="background:{shade}"></u></i></span>'
            f'<span class="t">{esc(w["title"])}</span></a>'
        )
    b.append("</div>")
    b.append(
        '<div class="legend"><span>new</span><span>first quarter</span><span>full</span>'
        "<span>last quarter</span><span>new</span></div>"
    )

    demo = get("cyclum-lunarem")
    b.append(
        f'<figure class="hero"><img src="{wide(demo)}" alt="{alt(demo)}" loading="lazy">'
        f"<figcaption><span>{esc(demo['title'])}, {demo['year']}</span>"
        f"<span>{esc(demo['medium'] or '')}</span>"
        f"<span>one panel per night, solstice to equinox</span></figcaption></figure>"
    )

    b.append(
        '<div class="story"><div><h2>Why a lunar month</h2>'
        "<p>Because a website that changes four times a year is a magazine, and a website "
        "that changes every night is a practice. Twenty-eight is a small enough number that "
        "somebody could actually see all of it, and a long enough cycle that coming back is "
        "worth it.</p></div>"
        "<div><h2>How the works were chosen</h2><p>By <b>measured luminance</b>. The darkest "
        "work in the catalogue sits at new moon; the lightest at full; everything else is "
        "placed on the waxing and waning limbs by where its own light falls. No editorial "
        "hand at all — which is either the joke or the point.</p></div>"
        "<div><h2>What it would take</h2><p>Nothing. The phase is arithmetic and the "
        "luminance is already stored. A real version would compute today's phase, open on "
        "that panel, and be a different front page every night for a month without anybody "
        "composing anything.</p></div></div></div>"
    )
    return lib.write("57-lunarem.html", "Lunarem", css, "".join(b))


# ---------------------------------------------------------------- 58 the day

HOURS = [
    (5, "#0d1424", "#8fa3c0", "first light", "me-own-juniper",
     "Nothing is up yet. This is the hour he walks."),
    (7, "#2b3244", "#d6c0a4", "the north window opens", "espresso-machine",
     "Coffee, and the still lifes that are really about coffee."),
    (9, "#7d8496", "#f2ecdf", "working light", "the-berry-picker",
     "The only three hours the studio's light is truly neutral."),
    (11, "#b9bcc0", "#ffffff", "high", "equilateral-equilibrium",
     "Flat, bright, unhelpful. Good for measuring, bad for colour."),
    (13, "#c8b79a", "#fffaf0", "heat", "prickly-pear",
     "In the Chihuahuan desert this hour is spent indoors, cutting plates."),
    (15, "#c9a276", "#fff3e0", "the monsoon builds", "towers",
     "Two months a year, the sky does all the work."),
    (17, "#b9714a", "#ffe6c8", "low angle", "low-angle-sun-rays",
     "Rays from the sun captured by water vapour and dust at a low angle."),
    (19, "#6d4a53", "#f0d0c4", "alpenglow", "alpenglow-at-mineral-creek-with-the-adults-after-the-babies-have-gone-to-sleep",
     "After the babies have gone to sleep."),
    (21, "#2f3350", "#c9c6dd", "dark", "bison-at-sunset",
     "Small paintings, close to the lamp."),
    (23, "#141a2e", "#a6a3bd", "night watch", "cyclum-lunarem",
     "One panel. Gold leaf, because it is the only thing that behaves like light."),
    (2, "#080a12", "#7c7a92", "the middle of the night", "riot-ghost",
     "Dense black, crosshatched, and nobody to show it to."),
]


def sheet_58():
    css = """
body{margin:0;font-family:"Instrument Serif",Georgia,serif;color:#fff;background:#080a12}
.hr{min-height:100svh;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
 align-items:center;gap:min(6vw,70px);padding:10vh 6vw;position:relative}
.hr .clock{position:absolute;left:6vw;top:5vh;font-family:"IBM Plex Mono",monospace;
 font-size:11px;letter-spacing:.34em;text-transform:uppercase;opacity:.72}
.hr h2{font-weight:400;font-size:clamp(2.4rem,7vw,5rem);line-height:.98;margin:0 0 .3em;
 letter-spacing:-.02em}
.hr p{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:1.02rem;line-height:1.66;
 max-width:34ch;margin:0 0 1.6em;opacity:.86}
.hr .tomb{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.2em;
 text-transform:uppercase;opacity:.66;line-height:1.9;border-top:1px solid currentColor;
 padding-top:10px;max-width:32ch}
.hr img{width:100%;height:auto;box-shadow:0 40px 90px -50px rgba(0,0,0,.9)}
.hr:nth-child(even) figure{order:-1}
.open,.close{min-height:100svh;display:grid;place-items:center;text-align:center;padding:10vh 7vw}
.open h1{font-size:clamp(3rem,11vw,8rem);font-weight:400;line-height:.9;margin:0 0 .3em;
 letter-spacing:-.03em}
.open p,.close p{font-family:"IBM Plex Sans",system-ui,sans-serif;max-width:44ch;
 line-height:1.7;opacity:.8;margin:0 auto}
.open small,.close small{display:block;margin-top:2.6em;font-family:"IBM Plex Mono",monospace;
 font-size:10px;letter-spacing:.34em;text-transform:uppercase;opacity:.6}
@media(prefers-reduced-motion:no-preference){
 .hr>*{animation:fade linear both;animation-timeline:view();animation-range:entry 2% cover 30%}
 @keyframes fade{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:none}}
}
@media(max-width:820px){.hr{grid-template-columns:minmax(0,1fr);gap:30px;padding:12vh 7vw}
 .hr:nth-child(even) figure{order:0}}
"""
    b = ['<section class="open" style="background:#0d1424">'
         "<div><h1>A day in the studio,<br>as the light finds it.</h1>"
         "<p>Most artist sites are organised by what a thing is. This one is organised by "
         "when you would be looking at it. Scroll from before dawn to the middle of the "
         "night; the page changes colour as the day does, and each hour brings the work that "
         "belongs to it.</p>"
         "<small>a live version would open at your own hour · scroll</small></div></section>"]
    for hour, bg, fg, label, slug, note in HOURS:
        w = get(slug)
        b.append(
            f'<section class="hr" style="background:{bg};color:{fg}">'
            f'<span class="clock">{hour:02d}:00 · {esc(label)}</span>'
            f"<div><h2>{esc(w['title'])}</h2><p>{esc(note)}</p>"
            f'<div class="tomb">{w["year"]} · {esc(w["medium"] or w["discipline"])}'
            f'{"<br>" + esc(dims(w)) if dims(w) else ""}</div></div>'
            f'<figure style="margin:0"><img src="{wide(w)}" alt="{alt(w)}" loading="lazy">'
            f"</figure></section>"
        )
    b.append(
        '<section class="close" style="background:#080a12"><div>'
        "<p>Eleven hours, eleven works. The other hundred and forty-four are awake "
        "whenever you are.</p>"
        "<small>archive.kyleparkercunningham.com</small></div></section>"
    )
    return lib.write("58-the-day.html", "The Day", css, "".join(b))


# ------------------------------------------------------------- 59 ephemeris

def sheet_59():
    css = """
:root{--paper:#fdfdfb;--ink:#101010;--dim:#8a8a86;--rule:#e0e0dc;--red:#8c1d18}
body{background:var(--paper);color:var(--ink);font-family:"IBM Plex Mono",monospace;
 font-size:12px;line-height:1.55}
.wrap{max-width:1160px;margin:0 auto;padding:0 22px 90px}
header{padding:56px 0 14px;border-bottom:2px solid var(--ink);display:grid;
 grid-template-columns:minmax(0,1fr) auto;gap:22px;align-items:end}
h1{font-family:"Bodoni Moda",Georgia,serif;font-weight:400;font-size:clamp(2.4rem,7vw,4.6rem);
 line-height:.94;letter-spacing:-.01em;margin:0}
.sub{font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);
 margin-bottom:10px}
.meta{text-align:right;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
 color:var(--dim);line-height:2}
.note{font-family:"Bodoni Moda",Georgia,serif;font-size:1.06rem;line-height:1.6;max-width:64ch;
 margin:20px 0 0;color:#2c2c2a}
h2{font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);
 font-weight:400;margin:44px 0 0;border-bottom:1px solid var(--ink);padding-bottom:6px;
 display:flex;justify-content:space-between}
.tw{overflow-x:auto}
table{width:100%;min-width:660px;border-collapse:collapse;font-variant-numeric:tabular-nums}
th{text-align:right;font-weight:400;font-size:9px;letter-spacing:.18em;text-transform:uppercase;
 color:var(--dim);padding:8px 8px 6px 0;border-bottom:1px solid var(--rule)}
th:first-child,td:first-child{text-align:left}
td{padding:4px 8px 4px 0;border-bottom:1px solid var(--rule);text-align:right;
 white-space:nowrap}
td:first-child{white-space:normal;font-family:"Bodoni Moda",Georgia,serif;font-size:14px}
td em{font-style:italic;color:var(--dim)}
tr:hover td{background:#f4f2ec}
.swatch{display:inline-block;width:20px;height:9px;border:.5px solid rgba(0,0,0,.25);
 vertical-align:middle}
.mag{color:var(--red)}
.foot{margin-top:44px;border-top:2px solid var(--ink);padding-top:12px;
 display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:22px}
.foot h3{font-size:9.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--dim);
 font-weight:400;margin:0 0 6px}
.foot p{margin:0;line-height:1.7;color:#2c2c2a;font-size:11.5px}
@media(max-width:640px){header{grid-template-columns:minmax(0,1fr)}.meta{text-align:left}}
"""
    motifs = ["elephant", "whale", "juniper", "cloud", "circle", "triangle", "skull",
              "bee", "owl", "bison", "space helmet", "glass jar", "machine", "portrait",
              "still life", "lightning", "deep time", "post-collapse", "concentric",
              "hand", "tree", "rocket", "mask", "flight"]

    rows = []
    for m in motifs:
        ws = [w for w in tagged(m) if w["year"]]
        if len(ws) < 2:
            continue
        yrs = sorted(w["year"] for w in ws)
        hs = [w["img"]["hue"] for w in ws if w["img"]["chroma"] > 0.05]
        if hs:
            xs = sum(math.cos(math.radians(h)) for h in hs)
            ys = sum(math.sin(math.radians(h)) for h in hs)
            hue = (math.degrees(math.atan2(ys, xs)) + 360) % 360
        else:
            hue = 40
        sat = sum(w["img"]["sat"] for w in ws) / len(ws)
        lig = sum(w["img"]["lig"] for w in ws) / len(ws)
        col = f"hsl({hue:.0f} {min(sat*140,66):.0f}% {30+lig*42:.0f}%)"
        gaps = [yrs[i + 1] - yrs[i] for i in range(len(yrs) - 1)]
        longest = max(gaps) if gaps else 0
        areas = [w["h_mm"] * w["w_mm"] for w in ws if w["h_mm"] and w["w_mm"]]
        mag = (-2.5 * math.log10(sum(areas) / len(areas) / 10000)) if areas else None
        rows.append((m, len(ws), yrs[0], yrs[-1], yrs[-1] - yrs[0], longest, hue, col, mag))

    rows.sort(key=lambda r: (-r[4], -r[1]))

    b = ['<div class="wrap"><header><div>',
         '<div class="sub">Oeuvre ephemeris · epoch 2009.0 · 155 bodies</div>',
         "<h1>Ephemeris</h1></div>",
         '<div class="meta">Kyle Parker Cunningham<br>archive.kyleparkercunningham.com<br>'
         "computed 2026 Aug 17</div></header>",
         '<p class="note">An ephemeris is a table of where things are and when they will '
         "return. It is dense, ugly, entirely numeric, and astronomers have preferred it to "
         "every prettier alternative for four hundred years — because you can find one line "
         "in it in a second. This is the oeuvre in that form: every recurring motif, its "
         "first and last appearance, its period, and the longest it has ever been out of the "
         "sky.</p>"]

    b.append(
        '<h2><span>Table I · recurring motifs</span><span>sorted by span</span></h2>'
        '<div class="tw"><table><thead><tr><th>Motif</th><th>n</th><th>First</th><th>Last</th>'
        "<th>Span</th><th>Max gap</th><th>Hue</th><th>Colour</th><th>Mag.</th></tr></thead><tbody>"
    )
    for m, n, first, last, span, gap, hue, col, mag in rows:
        magtxt = f'<span class="mag">{mag:+.1f}</span>' if mag is not None else "<em>—</em>"
        b.append(
            f"<tr><td>{esc(m)}</td><td>{n}</td><td>{first}</td><td>{last}</td>"
            f"<td>{span} yr</td><td>{gap} yr</td><td>{hue:.0f}°</td>"
            f'<td><span class="swatch" style="background:{col}"></span></td>'
            f"<td>{magtxt}</td></tr>"
        )
    b.append("</tbody></table></div>")

    pairs = revisits()[:12]
    b.append(
        '<h2><span>Table II · returns</span><span>the catalogue\'s own relations</span></h2>'
        '<div class="tw"><table><thead><tr><th>Object</th><th>Epoch</th><th>Return</th>'
        "<th>Period</th><th>Medium at first</th><th>Medium at return</th>"
        "</tr></thead><tbody>"
    )
    for a, c, delta in pairs:
        b.append(
            f'<tr><td>{esc(a["title"])}</td><td>{a["year"]}</td><td>{c["year"]}</td>'
            f"<td>{delta} yr</td><td><em>{esc(a['discipline'].lower())}</em></td>"
            f"<td><em>{esc(c['discipline'].lower())}</em></td></tr>"
        )
    b.append("</tbody></table></div>")

    b.append(
        '<div class="foot"><div><h3>Magnitude</h3><p>Borrowed honestly from astronomy and '
        "computed the same way: −2.5 log₁₀ of the motif's mean area in cm², so smaller "
        "numbers are bigger objects. It is a joke that happens to work.</p></div>"
        "<div><h3>Max gap</h3><p>The longest the motif has been absent between two "
        "appearances. The largest values in the table are the interesting ones — those are "
        "the things he came back to after years of not.</p></div>"
        "<div><h3>Why this and not a grid</h3><p>Because a grid of 155 thumbnails answers "
        "'what does it look like' and nothing else. This answers 'when', 'how often', and "
        "'is it due back' — and fits on one screen.</p></div></div></div>"
    )
    return lib.write("59-ephemeris.html", "Ephemeris", css, "".join(b))


# ------------------------------------------------------------- 60 the return

def sheet_60():
    css = """
:root{--paper:#f7f5f0;--ink:#191713;--dim:#8b8579;--rule:#e0dbd1;--accent:#1f3f5b}
body{background:var(--paper);color:var(--ink);font-family:"Literata",Georgia,serif;
 font-size:17px;line-height:1.62}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px 110px}
header{padding:14vh 0 6vh;max-width:56ch}
.kick{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:10.5px;letter-spacing:.32em;
 text-transform:uppercase;color:var(--dim)}
h1{font-weight:300;font-size:clamp(2.8rem,8.6vw,5.6rem);line-height:.96;margin:.16em 0 .24em;
 letter-spacing:-.02em}
header p{color:#3f3a31;margin:0}
.pair{margin:8vh 0 0;border-top:1px solid var(--rule);padding-top:26px}
.gap{display:flex;align-items:baseline;gap:0 16px;flex-wrap:wrap;margin-bottom:18px}
.gap .yrs{font-family:"IBM Plex Sans",sans-serif;font-size:10.5px;letter-spacing:.24em;
 text-transform:uppercase;color:var(--accent)}
.gap .big{font-weight:300;font-size:clamp(2rem,5vw,3.4rem);line-height:1;letter-spacing:-.02em}
.gap .sub{color:var(--dim);font-size:.94rem;font-style:italic}
.two{display:grid;grid-template-columns:minmax(0,1fr) 78px minmax(0,1fr);gap:0;
 align-items:center}
.two figure{margin:0}
.two img{width:100%;height:auto;box-shadow:0 20px 40px -34px rgba(0,0,0,.7)}
.two figcaption{font-family:"IBM Plex Sans",sans-serif;font-size:10.5px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--dim);margin-top:11px;line-height:1.6}
.two figcaption b{display:block;font-family:"Literata",serif;font-size:1.05rem;
 letter-spacing:0;text-transform:none;color:var(--ink);font-weight:400}
.link{display:grid;place-items:center;position:relative}
.link svg{width:100%;height:44px;overflow:visible}
.link span{position:absolute;top:calc(50% + 16px);font-family:"IBM Plex Sans",sans-serif;
 font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--dim);
 white-space:nowrap}
.said{max-width:54ch;margin:22px 0 0;color:#3f3a31;font-size:1rem}
.rest{margin-top:10vh;border-top:1px solid var(--rule);padding-top:24px}
.rest h2{font-family:"IBM Plex Sans",sans-serif;font-size:10.5px;letter-spacing:.3em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:0 0 16px}
.restlist{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px 26px;
 font-size:.94rem}
.restlist div{border-bottom:1px solid var(--rule);padding-bottom:8px}
.restlist b{font-weight:400}
.restlist span{display:block;font-family:"IBM Plex Sans",sans-serif;font-size:10px;
 letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin-top:3px}
@media(max-width:760px){.two{grid-template-columns:minmax(0,1fr);gap:22px}
 .link{height:52px}.link svg{transform:rotate(90deg);height:36px}}
"""
    pairs = revisits()
    top = pairs[:6]
    b = ['<div class="wrap"><header>',
         '<div class="kick">Twenty-eight pairs in the catalogue</div>',
         "<h1>What he came<br>back to.</h1>",
         "<p>The archive stores relations between works — this one is a version of that one, "
         "made later. It is the single most interesting structure in the whole database and "
         "the hardest thing to see in a grid sorted by year, because the two halves of a pair "
         "are usually hundreds of thumbnails apart. Here they are side by side, longest "
         "interval first.</p></header>"]

    for a, c, delta in top:
        arrow = (
            '<svg viewBox="0 0 78 44" aria-hidden="true">'
            '<path d="M2,22 C26,22 52,22 70,22" fill="none" stroke="#1f3f5b" '
            'stroke-width="1.2" stroke-dasharray="3 4"/>'
            '<path d="M64,17 L72,22 L64,27" fill="none" stroke="#1f3f5b" stroke-width="1.2"/>'
            "</svg>"
        )
        b.append(
            f'<section class="pair"><div class="gap">'
            f'<span class="yrs">{a["year"]} → {c["year"]}</span>'
            f'<span class="big">{delta} years later</span>'
            f'<span class="sub">{esc(a["discipline"].lower())} → {esc(c["discipline"].lower())}</span>'
            f"</div>"
            f'<div class="two">'
            f'<figure><img src="{wide(a)}" alt="{alt(a)}" loading="lazy">'
            f'<figcaption><b>{esc(a["title"])}</b>{a["year"]} · '
            f'{esc(a["medium"] or a["discipline"])}</figcaption></figure>'
            f'<div class="link">{arrow}<span>{delta} yr</span></div>'
            f'<figure><img src="{wide(c)}" alt="{alt(c)}" loading="lazy">'
            f'<figcaption><b>{esc(c["title"])}</b>{c["year"]} · '
            f'{esc(c["medium"] or c["discipline"])}</figcaption></figure></div>'
            f'<p class="said">{esc(sentence(c, 200) or sentence(a, 200))}</p></section>'
        )

    b.append('<section class="rest"><h2>The other twenty-two returns</h2>'
             '<div class="restlist">')
    for a, c, delta in pairs[6:]:
        b.append(
            f'<div><b>{esc(a["title"])}</b> → <b>{esc(c["title"])}</b>'
            f'<span>{a["year"]} → {c["year"]} · {delta} yr</span></div>'
        )
    b.append("</div></section></div>")
    return lib.write("60-the-return.html", "The Return", css, "".join(b))


# ------------------------------------------------------------ 61 motif atlas

ATLAS = [
    ("The elephant", "elephant",
     "He starts with a real one. <i>Arm Fauna</i> is about Satao, the great tusker "
     "poached in 2014, and everything after it carries that. The elephant becomes the "
     "animal that gets given equipment — a kite, a radio, an airship — and never "
     "stops being a memorial."),
    ("The whale", "whale",
     "Begins in the air, not the water. Whales fly in the early paintings; later they "
     "carry trees across oceans in coracles. The only motif here that changes its "
     "element."),
    ("The alligator juniper", "juniper",
     "One species, one canyon, a decade. This is the motif that most rewards the "
     "chronological order — the drawings get slower and the trees get older at "
     "different rates."),
    ("The space helmet", "space helmet",
     "Put it on an animal and you have made a claim about the future; put it on a "
     "person and you have made a joke about the present. It is the clearest "
     "single test of whether a work is hopeful."),
    ("The circle", "circle",
     "Ensō, concentric ring, orbit, cell, lunar disc. The single most persistent form "
     "in the catalogue and the one he describes as 'the oldest mark we make'."),
    ("The glass jar", "glass jar",
     "Lightning, oxygen, a cactus, sea ice. Whatever is in the jar is a thing he "
     "thinks is running out."),
]


def sheet_61():
    css = """
:root{--paper:#efece4;--ink:#1a1815;--dim:#807a6e;--rule:#d5cfc2;--red:#8f2f20}
body{background:var(--paper);color:var(--ink);font-family:"Newsreader",Georgia,serif;
 font-size:17px}
.wrap{max-width:1240px;margin:0 auto;padding:0 22px 100px}
header{padding:66px 0 24px;border-bottom:3px solid var(--ink);
 display:grid;grid-template-columns:minmax(0,1fr) minmax(0,340px);gap:34px;align-items:end}
.kick{font-family:"Archivo Narrow",sans-serif;font-size:10.5px;letter-spacing:.34em;
 text-transform:uppercase;color:var(--dim)}
h1{font-weight:300;font-size:clamp(2.6rem,7.6vw,5rem);line-height:.94;margin:.14em 0 0;
 letter-spacing:-.02em}
header p{margin:0;line-height:1.62;color:#3c372e;font-size:1rem}
.plate{margin:62px 0 0}
.ptop{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 16px;
 border-bottom:1px solid var(--ink);padding-bottom:8px;margin-bottom:18px}
.ptop h2{font-weight:400;font-size:clamp(1.7rem,3.6vw,2.5rem);margin:0;letter-spacing:-.01em}
.ptop .n{font-family:"Archivo Narrow",sans-serif;font-size:10.5px;letter-spacing:.28em;
 text-transform:uppercase;color:var(--red)}
.ptop .c{font-family:"Archivo Narrow",sans-serif;font-size:10.5px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--dim);margin-left:auto}
.pbody{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr);gap:34px;
 align-items:start}
.pbody>p{margin:0;line-height:1.68;color:#3c372e;font-size:1.02rem}
.run{display:flex;gap:0;align-items:flex-end;overflow-x:auto;padding-bottom:14px;
 scrollbar-width:thin;border-bottom:1px solid var(--rule);
 -webkit-mask-image:linear-gradient(90deg,#000 92%,transparent);
 mask-image:linear-gradient(90deg,#000 92%,transparent)}
.run a{flex:0 0 auto;text-decoration:none;color:inherit;padding-right:16px;position:relative}
.run img{height:132px;width:auto;display:block;box-shadow:0 12px 22px -18px rgba(0,0,0,.6)}
.run .yr{font-family:"Archivo Narrow",sans-serif;font-size:10px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--dim);margin-top:8px;display:block}
.run .yr b{display:block;color:var(--ink);font-weight:600;font-size:11px;max-width:150px;
 white-space:normal;line-height:1.3}
.run .jump{position:absolute;left:0;top:0;background:var(--red);color:#fff;
 font-family:"Archivo Narrow",sans-serif;font-size:9px;letter-spacing:.14em;
 text-transform:uppercase;padding:2px 6px;z-index:2}
.tl{display:flex;height:5px;margin-top:14px;gap:1px}
.tl i{flex:1;background:var(--rule)}
.tl i.on{background:var(--red)}
.tlab{display:flex;justify-content:space-between;font-family:"Archivo Narrow",sans-serif;
 font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin-top:5px}
@media(max-width:820px){header,.pbody{grid-template-columns:minmax(0,1fr)}}
"""
    years = list(range(2009, 2025))
    b = ['<div class="wrap"><header><div>',
         '<div class="kick">Atlas of recurring motifs · plates I–VI</div>',
         "<h1>Every elephant.<br>Every ensō.</h1></div>",
         "<p>A catalogue sorted by year scatters a motif across fifteen scroll-lengths. "
         "An atlas gathers it. Each plate below is one subject, every catalogued appearance "
         "of it, in order, with the intervals marked — because the intervals are where the "
         "thinking happened.</p></header>"]

    for i, (name, tag, note) in enumerate(ATLAS, 1):
        ws = sorted([w for w in tagged(tag) if w["year"]], key=lambda w: w["year"])
        present = {w["year"] for w in ws}
        roman = ["I", "II", "III", "IV", "V", "VI"][i - 1]
        run = []
        prev = None
        for w in ws:
            jump = ""
            if prev and w["year"] - prev >= 3:
                jump = f'<span class="jump">+{w["year"]-prev} yr</span>'
            run.append(
                f'<a href="#{esc(w["slug"])}">{jump}'
                f'<img src="{thumb(w)}" alt="{alt(w)}" loading="lazy" '
                f'style="width:{132*w["img"]["ratio"]:.0f}px;object-fit:cover">'
                f'<span class="yr"><b>{esc(w["title"])}</b>{w["year"]} · '
                f'{esc(w["discipline"].lower())}</span></a>'
            )
            prev = w["year"]
        bars = "".join(
            f'<i class="on"></i>' if y in present else "<i></i>" for y in years
        )
        b.append(
            f'<section class="plate"><div class="ptop"><span class="n">Plate {roman}</span>'
            f'<h2>{esc(name)}</h2><span class="c">{len(ws)} appearances · '
            f'{ws[0]["year"]}–{ws[-1]["year"]}</span></div>'
            f'<div class="pbody"><p>{note}</p>'
            f'<div><div class="run">{"".join(run)}</div>'
            f'<div class="tl">{bars}</div>'
            f'<div class="tlab"><span>{years[0]}</span>'
            f"<span>filled = a year the motif appears</span>"
            f"<span>{years[-1]}</span></div></div></div></section>"
        )
    b.append("</div>")
    return lib.write("61-motif-atlas.html", "Motif Atlas", css, "".join(b))


# -------------------------------------------------------------- 62 genealogy

def sheet_62():
    css = """
:root{--paper:#fbfaf7;--ink:#15130f;--dim:#8b8579;--line:#b9b2a3;--red:#8c2b1c}
body{background:var(--paper);color:var(--ink);font-family:"EB Garamond",Georgia,serif;
 font-size:17px}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px 100px}
header{padding:66px 0 26px;max-width:58ch}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.34em;
 text-transform:uppercase;color:var(--dim)}
h1{font-weight:400;font-size:clamp(2.6rem,8vw,5.2rem);line-height:.94;margin:.14em 0 .22em;
 letter-spacing:-.01em}
header p{line-height:1.64;color:#3b372f;margin:0}
.tree{margin-top:40px}
.gen{display:grid;grid-template-columns:150px minmax(0,1fr);gap:0 26px;
 border-top:1px solid var(--line);padding:22px 0}
.gen .lab{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--dim);line-height:1.8;padding-top:4px}
.gen .lab b{display:block;font-family:"EB Garamond",serif;font-size:1.3rem;
 letter-spacing:0;text-transform:none;color:var(--ink);font-weight:400}
.line{display:flex;flex-wrap:wrap;gap:26px}
.node{position:relative;width:158px}
.node img{width:100%;aspect-ratio:1;object-fit:cover;border:1px solid #ded8ca;
 box-shadow:0 10px 20px -16px rgba(0,0,0,.6)}
.node b{display:block;font-size:1rem;line-height:1.28;margin-top:8px;font-weight:400}
.node span{display:block;font-family:"IBM Plex Mono",monospace;font-size:9.5px;
 letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin-top:3px;line-height:1.5}
.node.child::before{content:"";position:absolute;left:-17px;top:-24px;width:1px;bottom:50%;
 background:var(--line)}
.node.child::after{content:"";position:absolute;left:-17px;top:50%;width:17px;height:1px;
 background:var(--line)}
.node .rel{position:absolute;right:6px;top:6px;background:var(--red);color:#fff;
 font-family:"IBM Plex Mono",monospace;font-size:8.5px;letter-spacing:.14em;
 text-transform:uppercase;padding:2px 6px}
.fam{border:1px solid var(--line);padding:22px 24px;margin-top:34px;background:#fff}
.fam h2{font-weight:400;font-size:1.5rem;margin:0 0 4px}
.fam .who{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--dim);margin-bottom:16px}
.fam p{max-width:60ch;line-height:1.62;color:#3b372f;margin:16px 0 0}
.legend{margin-top:44px;border-top:1px solid var(--line);padding-top:20px;
 display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:24px}
.legend h3{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.24em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:0 0 6px}
.legend p{margin:0;line-height:1.66;font-size:.94rem;color:#3b372f}
@media(max-width:720px){.gen{grid-template-columns:minmax(0,1fr);gap:12px}
 .node.child::before{display:none}.node.child::after{display:none}}
"""
    families = [
        ("The coffee congregation", "three works, one devotion",
         ["espresso-machine", "coffee-carafe", "aeropress"],
         "Two paintings in 2014 and a drypoint in 2018, all of the same three objects on "
         "the same counter. The archive relates all three to each other, which makes this "
         "the only complete family in the catalogue — nothing else has three members that "
         "all point at one another."),
        ("Butterfly Conundrum", "painting, 2015 → drypoint, 2021 → painting, 2022",
         ["butterfly_conundrum", "butterfly-conundrum", "docile"],
         "A butterfly tethered to a tool. Painted, then cut into copper six years later, "
         "then painted again the year after that as <i>Docile</i> — where the tether is "
         "still there but the violence has gone out of it."),
        ("Rocket Propelled Clovis Point", "painting, 2020 → intaglio, 2022",
         ["rocket-propelled-clovis-point", "rocket-propelled-clovis-point-intaglio"],
         "A 13,000-year-old projectile point with a rocket on it, made during the pandemic "
         "and re-cut two years later as a turtle carrying the same idea on its shell."),
        ("The juniper transplants", "2020 → 2021 → 2022 → 2023",
         ["alligator-juniper-nogal", "transplanter", "nogal-canyon", "gardner"],
         "The longest living line. A drawn tree becomes a tree carried across an ocean by "
         "an octopus in a coracle, becomes the canyon it grew in, becomes a gardener."),
        ("Faces, ten years apart", "2015 → 2022",
         ["substantial", "visible"],
         "<i>Substantial</i> and <i>Visible</i>. Same scale, same closeness, same "
         "psychological pressure — one in grisaille, one in lavender and red, and seven "
         "years of being looked at in between."),
    ]

    b = ['<div class="wrap"><header>',
         '<div class="kick">Descent, reworking, and the works with children</div>',
         "<h1>Genealogy</h1>",
         "<p>Four works in the catalogue carry the tag <i>reworked painting</i>: they are "
         "not finished objects but ancestors, painted over or scratched back into copper "
         "years later. Twenty-eight more are related as pairs. Laid out as descent rather "
         "than as a list, the practice stops looking like output and starts looking like a "
         "small number of ideas that keep having children.</p></header>",
         '<div class="tree">']

    for name, who, slugs, note in families:
        ws = many(*slugs)
        if not ws:
            continue
        ws.sort(key=lambda w: w["year"] or 0)
        b.append(f'<div class="fam"><h2>{esc(name)}</h2><div class="who">{esc(who)}</div>')
        b.append('<div class="gen" style="border-top:0;padding-top:0">'
                 f'<div class="lab">Generation I<b>{ws[0]["year"]}</b></div>'
                 f'<div class="line">'
                 f'<div class="node"><img src="{thumb(ws[0])}" alt="{alt(ws[0])}" loading="lazy">'
                 f'<b>{esc(ws[0]["title"])}</b><span>{ws[0]["year"]} · '
                 f'{esc(ws[0]["discipline"].lower())}</span></div></div></div>')
        rest = ws[1:]
        if rest:
            b.append(
                f'<div class="gen"><div class="lab">Descendants'
                f'<b>{rest[0]["year"]}–{rest[-1]["year"]}</b></div><div class="line">'
            )
            for w in rest:
                rel = "reworked" if "reworked painting" in w["tags"] else (
                    "cross-medium" if w["discipline"] != ws[0]["discipline"] else "pendant")
                b.append(
                    f'<div class="node child"><span class="rel">{rel}</span>'
                    f'<img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">'
                    f'<b>{esc(w["title"])}</b><span>{w["year"]} · '
                    f'{esc(w["discipline"].lower())} · '
                    f'+{(w["year"] or 0)-(ws[0]["year"] or 0)} yr</span></div>'
                )
            b.append("</div></div>")
        b.append(f"<p>{note}</p></div>")
    b.append("</div>")

    b.append(
        '<div class="legend"><div><h3>Reworked</h3><p>The earlier work no longer exists in '
        "the state it was catalogued in. Four works say this out loud; there are certainly "
        "more.</p></div>"
        "<div><h3>Cross-medium</h3><p>Same image, different material, later. Sixteen works "
        "carry the <i>cross-medium motif</i> tag.</p></div>"
        "<div><h3>What's missing</h3><p>The archive can express <i>pendant</i>, <i>study</i>, "
        "<i>reworked</i> and <i>series</i>, but every relation in the catalogue today is "
        "typed as <i>other</i>. Using the specific types would make this page draw itself.</p>"
        "</div></div></div>"
    )
    return lib.write("62-genealogy.html", "Genealogy", css, "".join(b))


def main():
    for fn in (sheet_56, sheet_57, sheet_58, sheet_59, sheet_60, sheet_61, sheet_62):
        print(fn())


if __name__ == "__main__":
    import sheets

    for s in sheets.SHEETS:
        lib.register(*s)
    main()
