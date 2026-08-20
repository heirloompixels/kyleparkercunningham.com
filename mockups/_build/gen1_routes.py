#!/usr/bin/env python3
"""Sheets 36–40 — routes.

The premise of the whole sketchbook: archive.kyleparkercunningham.com is
the catalogue, so this site does not need to be one. It needs to be the
set of ways *through*. These five all take that literally.
"""

import math
import random

import lib
from lib import esc, get, many, tagged, thumb, wide, alt, sentence, blurb, dims

FONTS_MAP = "https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@400;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&display=swap"


# --------------------------------------------------------------- 36 trailhead

ROUTES = [
    dict(
        name="The Juniper Trail",
        sub="Adobe Canyon → Nogal Canyon → the Gila",
        note="One tree, drawn for twelve years. He walks to the same alligator "
        "junipers, and each time the drawing gets slower. This is the route to take "
        "if you want to understand patience as a subject rather than a virtue.",
        slugs=["me-own-juniper", "alligator-juniper-2", "alligator-juniper",
               "alligator-juniper-nogal", "nogal-canyon", "transplanter"],
        grade="steady, with one long climb",
    ),
    dict(
        name="Survival Notes",
        sub="the near-future loop",
        note="Animals in breathing apparatus, machines grazing, mutual aid by "
        "airship. Twenty-eight works over ten years arguing that the future is "
        "neither utopia nor collapse but a lot of improvised gear.",
        slugs=["airdrop", "bonsai-giant-sequoia", "paper-neck-giraffes", "there-once-was-ice-here",
               "bison-robotics", "transplanter", "rhino-radar", "space-owl", "vacation"],
        grade="long, mostly level",
    ),
    dict(
        name="The Memory of Atmosphere",
        sub="a high traverse, weather exposed",
        note="Lightning that struck him, clouds bottled in glass, water vapour "
        "solved as algebra. The newest sustained body of work and the one that "
        "most rewards being walked in order.",
        slugs=["bottled-lightning", "the-atmospheres-electric-finger", "harmonics",
               "the-algebra-of-water-vapor", "low-angle-sun-rays", "towers",
               "the-river-in-the-sky", "out-there-on-the-horizon-a-solitary-cloud"],
        grade="exposed; turn back in weather",
    ),
    dict(
        name="The Circle Route",
        sub="a loop that returns to the trailhead",
        note="Enso after enso, concentric ring after concentric ring, from 2015 to "
        "2024. The shortest route here and the one people finish differently than "
        "they started.",
        slugs=["cadence", "enso", "pink-and-yellow", "path-though-the-autumn-leaves",
               "autumnal-twilight", "transition", "twenty-one-years"],
        grade="easy; do it twice",
    ),
    dict(
        name="Truth or Consequences",
        sub="town loop, 2 hours",
        note="The people and the ground of one small New Mexico town on the Rio "
        "Grande — portraits, blue corn, the Black Fire seen from the porch.",
        slugs=["cydney-and-val", "ken", "three-blue-corn", "the-black-fire",
               "future-capacitor", "tecate"],
        grade="flat, shaded, water available",
    ),
]


def sheet_36():
    css = """
:root{--paper:#f2ecdc;--ink:#2a2418;--contour:#b3854a;--water:#5d87a1;--forest:#5c7050;
 --red:#a8352a}
body{background:var(--paper);color:var(--ink);
 font-family:"Archivo Narrow","Helvetica Neue",Arial,sans-serif;font-size:16px}
.sheet{max-width:1180px;margin:0 auto;padding:0 22px 90px}
.contours{position:fixed;inset:0;z-index:0;opacity:.5;pointer-events:none}
.sheet,header{position:relative;z-index:1}
header{padding:64px 0 34px;border-bottom:2px solid var(--ink)}
.quad{font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--contour)}
h1{font-family:"Newsreader",Georgia,serif;font-weight:300;font-size:clamp(2.6rem,7vw,5rem);
 margin:.18em 0 .1em;line-height:.98;letter-spacing:-.015em}
.legend{display:flex;flex-wrap:wrap;gap:8px 26px;font-size:12px;letter-spacing:.12em;
 text-transform:uppercase;color:#6e6350;margin-top:20px}
.intro{max-width:56ch;font-family:"Newsreader",Georgia,serif;font-size:1.16rem;line-height:1.6;
 margin:26px 0 0;color:#453c2c}
.route{padding:44px 0;border-bottom:1px dashed #bfb298}
.rhead{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 16px}
.rnum{font-size:12px;letter-spacing:.3em;color:var(--red)}
.rname{font-family:"Newsreader",Georgia,serif;font-size:clamp(1.7rem,3.4vw,2.5rem);
 font-weight:400;margin:0}
.rsub{font-style:italic;color:#7a6e58;font-family:"Newsreader",Georgia,serif}
.rbody{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,300px);gap:34px;
 margin-top:20px;align-items:start}
.rnote{font-family:"Newsreader",Georgia,serif;font-size:1.04rem;line-height:1.62;max-width:54ch;
 color:#3d3527;margin:0 0 22px}
.profile{width:100%;height:96px;display:block}
.plabel{display:flex;justify-content:space-between;font-size:10.5px;letter-spacing:.15em;
 text-transform:uppercase;color:#8b7f68;margin-top:5px}
.strip{display:flex;gap:6px;margin-top:20px;overflow-x:auto;padding-bottom:6px;
 scrollbar-width:thin;-webkit-mask-image:linear-gradient(90deg,#000 90%,transparent);
 mask-image:linear-gradient(90deg,#000 90%,transparent)}
.strip a{flex:0 0 auto;width:104px;text-decoration:none}
.strip img{width:104px;height:78px;object-fit:cover;filter:saturate(.9)}
.strip span{display:block;font-size:10px;letter-spacing:.06em;text-transform:uppercase;
 color:#7a6e58;margin-top:5px;line-height:1.3}
.stats{border:1.5px solid var(--ink);padding:14px 16px;background:rgba(255,253,246,.72)}
.stats dt{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8b7f68}
.stats dd{margin:2px 0 12px;font-size:1.28rem;font-family:"Newsreader",Georgia,serif}
.stats dd small{font-size:.72rem;color:#7a6e58;font-family:"Archivo Narrow",sans-serif;
 letter-spacing:.08em;text-transform:uppercase}
.marks{margin-top:12px;font-size:11px;line-height:1.7;color:#6e6350;border-top:1px solid #cfc3aa;
 padding-top:10px}
.register{margin-top:56px;border:2px solid var(--ink);padding:26px}
.register h2{font-family:"Newsreader",Georgia,serif;font-weight:400;margin:0 0 4px;font-size:1.5rem}
.register p{max-width:60ch;font-family:"Newsreader",Georgia,serif;color:#453c2c;line-height:1.6}
.reglist{columns:3;column-gap:26px;font-size:12.5px;line-height:2;margin-top:14px}
.reglist a{text-decoration:none;border-bottom:1px solid #cfc3aa;display:block;
 break-inside:avoid;width:fit-content;max-width:100%}
.reglist a:hover{border-color:var(--red);color:var(--red)}
@media(max-width:820px){.rbody{grid-template-columns:minmax(0,1fr)}.reglist{columns:2}}
@media(max-width:520px){.reglist{columns:1}}
"""

    # Elevation profile drawn from each work's measured lightness: light
    # paintings sit high on the ridge, dark ones drop into the canyon.
    def profile(works):
        # Lightness varies over a narrow band across the whole oeuvre, so a
        # raw plot gives every route the same flat horizon. Stretching each
        # route across its own min and max is what a real elevation profile
        # does: it shows the terrain you are actually walking, not the
        # terrain relative to sea level.
        ls = [w["img"]["lig"] for w in works]
        lo, hi = min(ls), max(ls)
        rng_ = max(hi - lo, 0.001)
        pts = []
        n = len(works)
        for i, w in enumerate(works):
            x = 20 + i * (760 / max(n - 1, 1))
            y = 84 - ((w["img"]["lig"] - lo) / rng_) * 68
            pts.append((x, y))
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
        for i in range(1, len(pts)):
            x0, y0 = pts[i - 1]
            x1, y1 = pts[i]
            mx = (x0 + x1) / 2
            d += f" C{mx:.1f},{y0:.1f} {mx:.1f},{y1:.1f} {x1:.1f},{y1:.1f}"
        fill = d + f" L{pts[-1][0]:.1f},94 L{pts[0][0]:.1f},94 Z"
        dots = "".join(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#a8352a"/>' for x, y in pts
        )
        return (
            '<svg class="profile" viewBox="0 0 800 96" preserveAspectRatio="none" '
            'aria-label="elevation profile drawn from the measured lightness of each work">'
            f'<path d="{fill}" fill="#b3854a" opacity=".16"/>'
            f'<path d="{d}" fill="none" stroke="#2a2418" stroke-width="1.6"/>{dots}</svg>'
        )

    rng = random.Random(7)
    lines = []
    for i in range(16):
        y = 40 + i * 62
        d = f"M-20,{y}"
        for x in range(0, 1700, 60):
            d += f" q30,{rng.randint(-22, 22)} 60,{rng.randint(-9, 9)}"
        lines.append(f'<path d="{d}" fill="none" stroke="#b3854a" stroke-width="1"/>')
    contours = (
        '<svg class="contours" viewBox="0 0 1500 1000" preserveAspectRatio="xMidYMid slice">'
        + "".join(lines)
        + "</svg>"
    )

    b = [contours, '<div class="sheet">']
    b.append(
        "<header>"
        '<div class="quad">Kyle Parker Cunningham · quadrangle series · 2009–2026</div>'
        "<h1>Trailhead</h1>"
        '<p class="intro">The full catalogue lives at <b>archive.kyleparkercunningham.com</b> — '
        "every record, every measurement, every state. This is the other thing an archive needs "
        "and rarely has: marked routes through it. Five are open. Each has a distance, a grade, "
        "and a reason to walk it.</p>"
        '<div class="legend"><span>◆ 5 routes open</span><span>155 works catalogued</span>'
        "<span>elevation = lightness, stretched per route</span><span>revised summer, season XIII</span></div>"
        "</header>"
    )

    for n, r in enumerate(ROUTES, 1):
        ws = many(*r["slugs"])
        yrs = [w["year"] for w in ws if w["year"]]
        span = f"{min(yrs)}–{max(yrs)}"
        discs = sorted({w["discipline"] for w in ws})
        miles = len(ws) * 0.4 + round(len(r["note"]) / 900, 1)
        strip = "".join(
            f'<a href="#{esc(w["slug"])}"><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">'
            f'<span>{esc(w["title"])}<br>{w["year"]}</span></a>'
            for w in ws
        )
        b.append(
            f'<section class="route"><div class="rhead"><span class="rnum">ROUTE {n:02d}</span>'
            f'<h2 class="rname">{esc(r["name"])}</h2><span class="rsub">{esc(r["sub"])}</span></div>'
            f'<div class="rbody"><div><p class="rnote">{esc(r["note"])}</p>'
            f'{profile(ws)}<div class="plabel"><span>{esc(ws[0]["title"])} · {ws[0]["year"]}</span>'
            f'<span>{esc(ws[-1]["title"])} · {ws[-1]["year"]}</span></div>'
            f'<div class="strip">{strip}</div></div>'
            f'<dl class="stats"><dt>Distance</dt><dd>{len(ws)} works <small>≈ {miles:.1f} mi</small></dd>'
            f"<dt>Years crossed</dt><dd>{span}</dd>"
            f'<dt>Grade</dt><dd style="font-size:1rem;line-height:1.4">{esc(r["grade"])}</dd>'
            f'<dt>Surface</dt><dd style="font-size:1rem">{esc(", ".join(discs))}</dd>'
            f'<div class="marks">Trail markers are the works themselves. Every one links '
            f"through to its full record in the archive.</div></dl></div></section>"
        )

    others = [w for w in lib.WORKS if w["year"] and w["year"] >= 2018][:36]
    b.append(
        '<section class="register"><h2>Trail register</h2>'
        "<p>Everything not on a marked route. Nothing here is lost — it is only "
        "unrouted, and some of the best walking is.</p>"
        '<div class="reglist">'
        + "".join(f'<a href="#{esc(w["slug"])}">{esc(w["title"])}</a>' for w in others)
        + "</div></section></div>"
    )
    return lib.write("36-trailhead.html", "Trailhead — Kyle Parker Cunningham",
                     css, "".join(b), fonts=FONTS_MAP)


# ------------------------------------------------------------- 37 field guide

KEY = [
    ("1a", "Wears breathing apparatus, helmet or mask", "→ 2"),
    ("1b", "Breathes the air as it is", "→ 5"),
    ("2a", "Apparatus is glass, and holds a whole atmosphere", "→ <i>Vitrine-bearers</i>, pl. III"),
    ("2b", "Apparatus is worn on the face", "→ 3"),
    ("3a", "Animal", "→ <i>Suited fauna</i>, pl. I"),
    ("3b", "Human", "→ <i>Suited figures</i>, pl. IV"),
    ("5a", "Carries or is joined to a machine", "→ <i>Grafted machines</i>, pl. II"),
    ("5b", "Unaugmented; ancient", "→ <i>Deep-time relicts</i>, pl. V"),
]

PLATES = [
    ("I", "Suited fauna", "Animalia · apparatus worn",
     "The founding population. An animal takes on the gear of the species that "
     "endangered it, and wears it without comment. Note that the apparatus is always "
     "hand-made, never sleek: rubber, glass, cord, salvage.",
     ["bonsai-giant-sequoia", "paper-neck-giraffes", "space-owl", "astro-bee", "there-once-was-ice-here"]),
    ("II", "Grafted machines", "Mechanica · symbiotic",
     "Antennae, satellite dishes, radar. The machine is not a rider but a graft — it "
     "has grown into the animal and neither would now survive the separation.",
     ["rhino-radar", "bison-robotics", "flicker-rhino", "cyclic-repetition", "tubed-pachydeerm"]),
    ("III", "Vitrine-bearers", "Conservata · in glass",
     "Whole systems kept in jars: lightning, oxygen, a cactus, the sea ice. The "
     "commonest specimen in the recent record and the most anxious.",
     ["bottled-lightning", "bottled-oxygen", "preservation-cactus", "pinned"]),
    ("IV", "Suited figures", "Homo · tethered",
     "The human members. Usually alone, usually tethered to something they are "
     "walking, and usually smaller in the frame than you expect.",
     ["pet-walk", "deep-sea", "submerged", "vacation", "boom-box"]),
    ("V", "Deep-time relicts", "Reliquiae · unaugmented",
     "No gear at all. Trees older than the state, megafauna that did not make it, a "
     "clovis point. They are here to set the scale everything else is measured against.",
     ["me-own-juniper", "saber-tooth-puma", "alligator-juniper-nogal",
      "rocket-propelled-clovis-point", "crystal-tooth-whale"]),
]


def sheet_37():
    css = """
:root{--paper:#f6f2e7;--ink:#211d17;--rule:#c9c0aa;--red:#8f2d22;--olive:#5d6647}
body{background:var(--paper);color:var(--ink);font-family:"Newsreader",Georgia,serif;
 font-size:17px;line-height:1.55}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px 96px}
header{text-align:center;padding:70px 0 30px}
.imprint{font-family:"Archivo Narrow",sans-serif;font-size:10.5px;letter-spacing:.42em;
 text-transform:uppercase;color:#8a8069}
h1{font-size:clamp(2.4rem,6.4vw,4.2rem);font-weight:300;font-style:italic;margin:.14em 0 .06em;
 letter-spacing:-.01em}
.sub{font-family:"Archivo Narrow",sans-serif;font-size:12px;letter-spacing:.3em;
 text-transform:uppercase;color:#6c6350}
.rule{height:0;border-top:2.5px solid var(--ink);border-bottom:1px solid var(--ink);
 padding-bottom:3px;margin:30px 0 0}
.preface{max-width:62ch;margin:34px auto 0;text-align:left;font-size:1.1rem;
 line-height:1.6;color:#3c352a}
.keybox{margin:52px 0;border:1px solid var(--ink);padding:26px 28px;background:#fbf8f0}
.keybox h2{font-family:"Archivo Narrow",sans-serif;font-size:11px;letter-spacing:.34em;
 text-transform:uppercase;margin:0 0 16px;color:var(--red)}
.key{font-family:"Archivo Narrow",sans-serif;font-size:14.5px;line-height:1.95}
.key div{display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:12px;
 border-bottom:1px dotted var(--rule);padding:3px 0}
.key b{color:var(--red);font-weight:600}
.key em,.key i{font-family:"Newsreader",serif}
.plate{margin:64px 0 0;border-top:2px solid var(--ink);padding-top:8px}
.ptop{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 14px}
.pno{font-family:"Archivo Narrow",sans-serif;font-size:11px;letter-spacing:.3em;color:var(--red)}
.pname{font-size:1.9rem;font-weight:400;margin:.1em 0}
.plat{font-style:italic;color:#7b7259}
.pgrid{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:34px;margin-top:18px}
.figs{display:flex;flex-wrap:wrap;gap:26px 20px;align-items:flex-end;
 border:1px solid var(--rule);background:#fbf9f2;padding:22px 20px 18px}
.figs figure{flex:0 1 auto}
.figs figure img{height:clamp(84px,11vw,124px);width:auto;max-width:100%}
figure{margin:0}
figure img{width:100%;height:auto;background:#eae4d5;mix-blend-mode:multiply}
figcaption{font-family:"Archivo Narrow",sans-serif;font-size:10.5px;line-height:1.4;
 letter-spacing:.05em;color:#5f5745;margin-top:7px;text-transform:uppercase}
figcaption b{color:var(--red);font-weight:600;display:block}
.pnote{font-size:1rem;color:#3c352a}
.range{margin-top:18px;border-top:1px solid var(--rule);padding-top:10px}
.range h3{font-family:"Archivo Narrow",sans-serif;font-size:10px;letter-spacing:.28em;
 text-transform:uppercase;color:#8a8069;margin:0 0 8px}
.years{display:flex;gap:2px;align-items:flex-end;height:44px}
.years i{flex:1;background:#e6e0cf;min-height:3px;align-self:flex-end}
.years i.on{background:var(--olive)}
.yl{display:flex;justify-content:space-between;font-family:"Archivo Narrow",sans-serif;
 font-size:9.5px;color:#8a8069;letter-spacing:.1em;margin-top:4px}
footer{margin-top:76px;border-top:2px solid var(--ink);padding-top:20px;
 font-family:"Archivo Narrow",sans-serif;font-size:11.5px;letter-spacing:.1em;color:#6c6350;
 display:flex;flex-wrap:wrap;gap:10px 30px;justify-content:space-between}
@media(max-width:800px){.pgrid{grid-template-columns:minmax(0,1fr)}.key div{grid-template-columns:38px 1fr;
 }.key div span:last-child{grid-column:2}}
"""
    years = list(range(2009, 2027))
    b = ['<div class="wrap"><header>',
         '<div class="imprint">Desert Archaic · field guides of the near future</div>',
         "<h1>A Field Guide to the Creatures</h1>",
         '<div class="sub">Kyle Parker Cunningham · 155 specimens · second edition</div>',
         '<div class="rule"></div>',
         '<p class="preface">The archive can tell you that thirty-one works carry the tag '
         "<i>animist solarpunk</i> and nine carry <i>space helmet</i>. It cannot tell you that "
         "these are one continuous population, or how to recognise a member of it in the wild. "
         "That is what a guide is for. Begin at the key; it will take four questions at most.</p>",
         "</header>"]

    b.append('<section class="keybox"><h2>Key to the plates</h2><div class="key">')
    for a, q, dest in KEY:
        b.append(f"<div><b>{a}</b><span>{q}</span><span>{dest}</span></div>")
    b.append("</div></section>")

    for roman, name, latin, note, slugs in PLATES:
        ws = many(*slugs)
        figs = "".join(
            f'<figure><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">'
            f"<figcaption><b>fig. {i}</b>{esc(w['title'])} · {w['year']}<br>"
            f"{esc((w['medium'] or '').lower())}</figcaption></figure>"
            for i, w in enumerate(ws, 1)
        )
        present = {w["year"] for w in ws}
        bars = "".join(
            f'<i class="on" style="height:{30 + (y % 3) * 10}%"></i>' if y in present else "<i></i>"
            for y in years
        )
        b.append(
            f'<section class="plate"><div class="ptop"><span class="pno">PLATE {roman}</span>'
            f'<h2 class="pname">{esc(name)}</h2><span class="plat">{esc(latin)}</span></div>'
            f'<div class="pgrid"><div class="figs">{figs}</div>'
            f'<div><p class="pnote">{esc(note)}</p>'
            f'<div class="range"><h3>Range in the record</h3>'
            f'<div class="years">{bars}</div>'
            f'<div class="yl"><span>{years[0]}</span><span>{years[-1]}</span></div></div>'
            f"</div></div></section>"
        )

    b.append(
        "<footer><span>Specimen records: archive.kyleparkercunningham.com</span>"
        "<span>Nomenclature is the author's own and has no standing</span>"
        "<span>Truth or Consequences, New Mexico</span></footer></div>"
    )
    return lib.write("37-field-guide.html", "A Field Guide to the Creatures",
                     css, "".join(b), fonts=FONTS_MAP)


# ----------------------------------------------------------------- 38 docent

DOCENT = [
    ("me-own-juniper", "Start here. He was twenty-nine and had just walked out of the Gila."),
    ("substantial", "Six years later, the faces get bigger than the canvas can hold."),
    ("cyclum-lunarem", "Then a year of only looking up, one small panel per night."),
    ("the-mother-bear", "This one happened in front of him, in Montana, and he painted it afterwards."),
    ("the-black-fire", "This one he watched from the porch for three months."),
    ("bottled-lightning", "He has been struck by lightning. Consider that while you look at the jar."),
    ("the-river-in-the-sky", "And now the weather itself, without the ground under it."),
]


def sheet_38():
    css = """
:root{--paper:#faf8f4;--ink:#16130f;--dim:#8b8478}
body{background:var(--paper);color:var(--ink);font-family:"Newsreader",Georgia,serif}
.intro{min-height:100svh;display:grid;place-items:center;padding:8vh 6vw;text-align:center}
.intro p{max-width:22ch;font-size:clamp(2rem,6.5vw,4.4rem);line-height:1.06;font-weight:300;
 letter-spacing:-.022em;margin:0}
.intro small{display:block;margin-top:2.4em;font-family:"Archivo Narrow",sans-serif;font-size:11px;
 letter-spacing:.34em;text-transform:uppercase;color:var(--dim)}
.stop{min-height:100svh;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
 align-items:center;gap:min(7vw,90px);padding:12vh 7vw;max-width:1500px;margin:0 auto}
.stop:nth-child(even) .art{order:2}
.said{font-size:clamp(1.5rem,3.4vw,2.9rem);line-height:1.18;font-weight:300;letter-spacing:-.015em;
 margin:0 0 1.1em;max-width:20ch;text-wrap:balance}
.art img{width:100%;height:auto;box-shadow:0 30px 90px -50px rgba(0,0,0,.6)}
.tomb{font-family:"Archivo Narrow",sans-serif;font-size:11px;letter-spacing:.18em;
 text-transform:uppercase;color:var(--dim);line-height:2;border-top:1px solid #ddd6c9;
 padding-top:12px;max-width:34ch}
.tomb b{color:var(--ink);font-weight:600}
.his{font-size:1.06rem;line-height:1.62;color:#4a4338;max-width:38ch;margin:1.4em 0 1.6em;
 font-style:italic}
.end{min-height:80svh;display:grid;place-items:center;text-align:center;padding:10vh 6vw}
.end p{font-size:clamp(1.4rem,3.6vw,2.4rem);font-weight:300;max-width:24ch;line-height:1.22;
 margin:0 0 1.6em}
.end a{font-family:"Archivo Narrow",sans-serif;font-size:12px;letter-spacing:.28em;
 text-transform:uppercase;border-bottom:1px solid;padding-bottom:4px;text-decoration:none}
@media(prefers-reduced-motion:no-preference){
 .stop>*{animation:rise linear both;animation-timeline:view();animation-range:entry 4% cover 32%}
 @keyframes rise{from{opacity:0;transform:translateY(34px)}to{opacity:1;transform:none}}
}
@media(max-width:860px){.stop{grid-template-columns:minmax(0,1fr);gap:32px;padding:9vh 7vw;
 min-height:auto}.stop:nth-child(even) .art{order:0}}
"""
    b = ['<section class="intro"><p>There are one hundred and fifty-five. '
         "Let me show you seven.</p>"
         "<small>a docent's route · about nine minutes</small></section>"]
    for slug, said in DOCENT:
        w = get(slug)
        d = [x for x in [w["medium"], dims(w), str(w["year"] or "")] if x]
        b.append(
            '<section class="stop">'
            f'<div class="art"><img src="{wide(w)}" alt="{alt(w)}" loading="lazy"></div>'
            f'<div><p class="said">{esc(said)}</p>'
            f'<p class="his">{esc(blurb(w, 260))}</p>'
            f'<div class="tomb"><b>{esc(w["title"])}</b><br>{esc(" · ".join(d))}</div></div>'
            "</section>"
        )
    b.append(
        '<section class="end"><p>That is the tour. The other hundred and forty-eight '
        "are catalogued, measured and photographed — go and get lost in them.</p>"
        '<a href="#">archive.kyleparkercunningham.com</a></section>'
    )
    return lib.write("38-docent.html", "The Docent", css, "".join(b), fonts=FONTS_MAP)


# ---------------------------------------------------------- 39 field station


def sheet_39():
    css = """
:root{--paper:#eceadf;--grid:#d6d3c4;--ink:#1a1c19;--orange:#d1571f;--blue:#2d5d7c;
 --green:#4a6b45;--dim:#78776a}
body{background:var(--paper);color:var(--ink);
 font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;font-size:13.5px;
 background-image:linear-gradient(var(--grid) 1px,transparent 1px),
  linear-gradient(90deg,var(--grid) 1px,transparent 1px);
 background-size:26px 26px;background-position:-1px -1px}
.stn{max-width:1240px;margin:0 auto;padding:0 20px 80px}
.bar{display:flex;flex-wrap:wrap;gap:6px 26px;align-items:baseline;
 border-bottom:2.5px solid var(--ink);padding:26px 0 10px;position:sticky;top:0;
 background:var(--paper);z-index:5}
.bar .id{font-weight:700;letter-spacing:.2em}
.bar span{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
.bar .live{color:var(--orange)}
.bar .live::before{content:"●";margin-right:5px}
h1{font-family:"Archivo Narrow","Helvetica Neue",sans-serif;font-size:clamp(2.4rem,7vw,4.6rem);
 font-weight:700;letter-spacing:-.03em;line-height:.94;margin:34px 0 6px;text-transform:uppercase}
.deck{font-family:"Newsreader",Georgia,serif;font-size:1.24rem;line-height:1.55;max-width:58ch;
 color:#3a3b34;margin:0 0 30px}
.panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:14px;
 align-items:start}
.panel{border:1.5px solid var(--ink);background:#f6f5ee;padding:14px 15px 16px;position:relative}
.panel h2{font-size:10px;letter-spacing:.26em;text-transform:uppercase;margin:0 0 12px;
 color:var(--dim);font-weight:400}
.big{font-family:"Archivo Narrow",sans-serif;font-size:2.6rem;font-weight:700;line-height:1;
 letter-spacing:-.02em}
.big small{font-size:.9rem;font-weight:400;color:var(--dim);letter-spacing:.08em}
.rows{line-height:1.95;font-size:12px}
.rows div{display:flex;justify-content:space-between;gap:14px;border-bottom:1px dotted #c9c7b8}
.rows b{font-weight:400}
.rows i{font-style:normal;color:var(--dim)}
.dial{display:block;width:100%;height:auto;margin:2px 0 6px}
.sect{margin-top:34px}
.sect>h2{font-family:"Archivo Narrow",sans-serif;font-size:11px;letter-spacing:.3em;
 text-transform:uppercase;border-bottom:1.5px solid var(--ink);padding-bottom:6px;
 margin:0 0 14px;display:flex;justify-content:space-between;color:var(--ink)}
.sect>h2 em{font-style:normal;color:var(--dim)}
.specimens{display:grid;grid-template-columns:repeat(auto-fill,minmax(122px,1fr));gap:12px}
.spec{text-decoration:none;color:inherit;display:block}
.spec img{width:100%;aspect-ratio:1;object-fit:cover;border:1px solid var(--ink)}
.spec .tag{font-size:9.5px;letter-spacing:.06em;line-height:1.4;margin-top:5px;color:#3a3b34}
.spec .tag b{display:block;color:var(--orange);font-weight:400;letter-spacing:.12em}
.transects{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.tr{border-left:3px solid var(--blue);padding:2px 0 2px 12px}
.tr b{font-family:"Archivo Narrow",sans-serif;font-size:1.05rem;letter-spacing:.02em;
 display:block;text-transform:uppercase}
.tr span{font-size:11.5px;color:var(--dim);line-height:1.55;display:block;margin-top:3px}
.log{font-size:12.5px;line-height:1.9;max-width:76ch}
.log div{display:grid;grid-template-columns:88px 1fr;gap:14px;padding:5px 0;
 border-bottom:1px dotted #c9c7b8}
.log time{color:var(--orange)}
footer{margin-top:44px;border-top:2.5px solid var(--ink);padding-top:12px;font-size:11px;
 letter-spacing:.14em;text-transform:uppercase;color:var(--dim);display:flex;flex-wrap:wrap;
 gap:8px 28px;justify-content:space-between}
@media(max-width:560px){.log div{grid-template-columns:1fr}.bar{position:static}}
"""
    seasons = [
        ("XIII", "Summer 2026", "Everything That Can Be Carried", "live",
         "Wyoming · Montana · Colorado", "the studio loses its walls"),
        ("XII", "Spring 2026", "The Ground Thaws Slowly", "retired",
         "Truth or Consequences, NM", "the press comes back online"),
        ("XI", "Winter 2025", "Long Nights, Small Plates", "retired",
         "Truth or Consequences, NM", "drypoint season"),
    ]
    recent = lib.with_image([w for w in lib.WORKS if w["year"] and w["year"] >= 2023])[:12]
    atmos = tagged("the memory of atmosphere")

    # A year ring, and every number in it is real: each work is plotted at
    # the angle of its own measured dominant hue and the radius of its year,
    # 2009 at the centre, 2026 at the rim. Read outward and you watch the
    # palette rotate — the early work clustered in earth, the recent work
    # swinging into blue.
    ring = ['<svg class="dial" viewBox="0 0 240 240" role="img" '
            'aria-label="every catalogued work plotted by hue around the circle '
            'and by year outward from the centre">']
    for r, lab in ((34, "2012"), (58, "2016"), (82, "2020"), (104, "2024")):
        ring.append(f'<circle cx="120" cy="120" r="{r}" fill="none" stroke="#d6d3c4"/>')
        ring.append(f'<text x="123" y="{120-r+9}" font-size="7.5" fill="#a5a396" '
                    f'font-family="monospace">{lab}</text>')
    for deg, name in ((0, "red"), (60, "yellow"), (120, "green"),
                      (180, "cyan"), (240, "blue"), (300, "magenta")):
        a = math.radians(deg - 90)
        x, y = 120 + math.cos(a) * 116, 120 + math.sin(a) * 116
        anchor = "middle" if deg in (0, 180) else ("start" if deg < 180 else "end")
        ring.append(f'<text x="{x:.1f}" y="{y+3:.1f}" font-size="7.5" fill="#78776a" '
                    f'text-anchor="{anchor}" font-family="monospace">{name}</text>')
        x2, y2 = 120 + math.cos(a) * 108, 120 + math.sin(a) * 108
        ring.append(f'<line x1="120" y1="120" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="#e4e2d6"/>')
    for w in lib.WORKS:
        if not w["year"]:
            continue
        a = math.radians(w["img"]["hue"] - 90)
        r = 12 + (w["year"] - 2009) / 17 * 94
        col = {"Painting": "#d1571f", "Printmaking": "#2d5d7c"}.get(w["discipline"], "#4a6b45")
        op = ".85" if w["img"]["chroma"] > 0.06 else ".3"
        ring.append(
            f'<circle cx="{120+math.cos(a)*r:.1f}" cy="{120+math.sin(a)*r:.1f}" r="2.3" '
            f'fill="{col}" opacity="{op}"/>'
        )
    ring.append('<circle cx="120" cy="120" r="4" fill="#1a1c19"/>')
    ring.append("</svg>")

    b = ['<div class="stn">',
         '<div class="bar"><span class="id">STATION KPC-01</span>'
         '<span class="live">SEASON XIII ACTIVE</span>'
         "<span>lat 33.128 lon −107.253 · elev 1382 m</span>"
         "<span>catalogue 155 · archive linked</span></div>",
         "<h1>Field Station</h1>",
         '<p class="deck">The seasons idea, taken seriously: not a magazine issue but a '
         "research station's status board. What the studio is doing right now, where it is "
         "standing, what came back from the field this week, and which transects are open "
         "for anyone who wants to walk one.</p>",
         '<div class="panels">']

    b.append(
        '<div class="panel"><h2>Current season</h2>'
        '<div class="big">XIII<small> / summer</small></div>'
        '<div class="rows" style="margin-top:10px">'
        "<div><b>Everything That Can Be Carried</b></div>"
        "<div><b>opened</b><i>21 June 2026</i></div>"
        "<div><b>closes</b><i>equinox</i></div>"
        "<div><b>filed under</b><i>survival notes</i></div></div></div>"
    )
    b.append(
        '<div class="panel"><h2>Conditions at the station</h2>'
        '<div class="rows"><div><b>position</b><i>mobile · satellite</i></div>'
        "<div><b>press</b><i>packed</i></div><div><b>bindery</b><i>operational</i></div>"
        "<div><b>easel</b><i>morning light only</i></div>"
        "<div><b>water</b><i>hauled</i></div></div>"
        '<div style="margin-top:12px;font-family:Newsreader,Georgia,serif;font-size:13px;'
        'line-height:1.5;color:#3a3b34">“Can the whole operation be <i>carried</i> — made '
        "small enough, and durable enough, to keep making real, physical things from "
        "wherever the work happens to be?”</div></div>"
    )
    b.append(
        '<div class="panel"><h2>Hue by year</h2>' + "".join(ring) +
        '<div class="rows"><div><b style="color:#d1571f">● painting</b><i>93</i></div>'
        '<div><b style="color:#2d5d7c">● printmaking</b><i>46</i></div>'
        '<div><b style="color:#4a6b45">● other</b><i>16</i></div></div>'
        '<div style="font-size:10.5px;color:#78776a;line-height:1.5;margin-top:8px">'
        'angle = measured dominant hue · radius = year · faint = near-neutral</div></div>'
    )
    b.append(
        '<div class="panel"><h2>Collected this season</h2>'
        '<div class="big">200<small> small watercolours</small></div>'
        '<div class="rows" style="margin-top:10px"><div><b>painted in the field</b><i>each unique</i></div>'
        "<div><b>his</b><i>100</i></div><div><b>hers</b><i>100</i></div>"
        "<div><b>first release</b><i>solstice</i></div></div></div>"
    )
    b.append("</div>")

    b.append(
        '<section class="sect"><h2>Open transects <em>walk one end to end</em></h2>'
        '<div class="transects">'
        + "".join(
            f'<div class="tr"><b>{esc(r["name"])}</b><span>{esc(r["sub"])} · '
            f'{len(r["slugs"])} stations</span></div>'
            for r in ROUTES
        )
        + "</div></section>"
    )

    b.append(
        '<section class="sect"><h2>Recent specimens <em>2023 onward</em></h2>'
        '<div class="specimens">'
        + "".join(
            f'<a class="spec" href="#{esc(w["slug"])}"><img src="{thumb(w)}" alt="{alt(w)}" '
            f'loading="lazy"><span class="tag"><b>{w["year"]}</b>{esc(w["title"])}</span></a>'
            for w in recent
        )
        + "</div></section>"
    )

    b.append(
        '<section class="sect"><h2>Standing investigation <em>the memory of atmosphere · '
        f'{len(atmos)} works</em></h2><div class="specimens">'
        + "".join(
            f'<a class="spec" href="#{esc(w["slug"])}"><img src="{thumb(w)}" alt="{alt(w)}" '
            f'loading="lazy"><span class="tag"><b>{w["year"]}</b>{esc(w["title"])}</span></a>'
            for w in atmos[:12]
        )
        + "</div></section>"
    )

    b.append(
        '<section class="sect"><h2>Station log</h2><div class="log">'
        "<div><time>21 JUN</time><span>Solstice. The season opens; the first of the 200 go up.</span></div>"
        "<div><time>10 MAR</time><span>The Periodic — production notes. Newsprint stock confirmed, "
        "four pages, one colour.</span></div>"
        "<div><time>15 FEB</time><span>Print specs and image prep. Standardised the ladder at "
        "480 / 960 / 1600.</span></div>"
        "<div><time>28 JAN</time><span>Artist newspaper distributed. Twelve towns, none of them "
        "with a gallery.</span></div>"
        "</div></section>"
    )

    b.append(
        "<footer><span>records → archive.kyleparkercunningham.com</span>"
        "<span>station established 2009</span><span>Truth or Consequences · New Mexico</span>"
        "</footer></div>"
    )
    return lib.write("39-field-station.html", "Field Station — Season XIII",
                     css, "".join(b), fonts=FONTS_MAP)


# ------------------------------------------------------------ 40 the long walk


def sheet_40():
    css = """
:root{--ink:#141210}
body{background:#0c0b0a;color:#efe9dd;font-family:"Archivo Narrow",Helvetica,sans-serif;
 overflow-y:auto}
.sky{display:none}
.head{position:fixed;top:0;left:0;right:0;z-index:9;display:flex;justify-content:space-between;
 align-items:baseline;padding:16px 22px;font-size:11px;letter-spacing:.26em;
 text-transform:uppercase;color:#a99e8c;
 background:linear-gradient(180deg,rgba(12,11,10,.92),rgba(12,11,10,0))}
.head b{color:#efe9dd;font-weight:600}
.walk{position:relative;z-index:1;display:flex;align-items:flex-end;gap:0;height:100svh;
 overflow-x:auto;overflow-y:hidden;scroll-snap-type:x proximity;padding:0 0 92px;
 scrollbar-width:thin;scrollbar-color:#4a443c #0c0b0a;
 background-attachment:local;background-repeat:no-repeat;
 background-image:linear-gradient(90deg,#0d1420 0%,#1d2a38 7%,#4a5560 14%,#8d8574 21%,
  #c9a77e 27%,#e0c39a 33%,#d9cbb3 41%,#b9bfc2 50%,#8fa2b0 58%,#6d7d90 66%,
  #7c6a63 73%,#a86f4c 79%,#6d4432 85%,#2e2a2c 92%,#0d1018 100%)}
.title h1,.title p{text-shadow:0 2px 24px rgba(8,10,14,.55)}
.title{flex:0 0 auto;width:min(88vw,660px);padding:0 6vw 4vh;align-self:center;
 scroll-snap-align:center}
.title h1{font-family:"Newsreader",Georgia,serif;font-weight:300;
 font-size:clamp(2.6rem,7.4vw,5.4rem);line-height:.98;letter-spacing:-.025em;margin:0 0 .34em}
.title p{font-family:"Newsreader",Georgia,serif;font-size:1.1rem;line-height:1.62;color:#c8bfb0;
 max-width:44ch;margin:0 0 1.4em}
.title small{font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:#8b8072}
.mile{flex:0 0 auto;align-self:stretch;display:flex;flex-direction:column;justify-content:flex-end;
 padding:0 30px 0 22px;border-left:1px solid rgba(239,233,221,.18);scroll-snap-align:start}
.mile b{font-family:"Newsreader",Georgia,serif;font-size:clamp(2.2rem,5vw,3.6rem);font-weight:300;
 line-height:1;color:#efe9dd;opacity:.5}
.mile span{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#8b8072;
 margin-bottom:6px}
.w{flex:0 0 auto;position:relative;margin:0 14px 0 0;scroll-snap-align:center}
.w img{height:100%;width:auto;display:block;box-shadow:0 30px 70px -40px #000}
.w figcaption{position:absolute;left:0;bottom:-70px;width:210px;font-size:10px;line-height:1.5;
 letter-spacing:.08em;text-transform:uppercase;color:#a99e8c}
.w figcaption b{display:block;color:#efe9dd;font-size:11px;letter-spacing:.1em}
.end{flex:0 0 auto;width:min(84vw,520px);align-self:center;padding:0 6vw;scroll-snap-align:center}
.end p{font-family:"Newsreader",Georgia,serif;font-size:1.4rem;line-height:1.4;font-weight:300;
 color:#efe9dd}
.end a{display:inline-block;margin-top:1.4em;font-size:11px;letter-spacing:.28em;
 text-transform:uppercase;color:#c8bfb0;text-decoration:none;border-bottom:1px solid #6b6255;
 padding-bottom:4px}
.hint{position:fixed;bottom:6px;left:0;right:0;text-align:center;font-size:10px;
 letter-spacing:.3em;text-transform:uppercase;color:#6b6255;z-index:9;pointer-events:none}
@media(max-width:700px){.walk{padding-bottom:80px}.w figcaption{width:150px;bottom:-62px}}
"""
    ws = [w for w in sorted(lib.WORKS, key=lambda x: (x["year"] or 0, x["title"])) if w["year"]]
    heights = {"Painting": 0.62, "Printmaking": 0.44, "Installation": 0.5,
               "Other": 0.4, "Sculpture": 0.46}

    b = ['<div class="head"><span><b>The Long Walk</b> · fifteen years, end to end</span>'
         "<span>scroll sideways · 155 works</span></div>",
         '<div class="walk">',
         '<div class="title"><h1>Everything, in the order it happened.</h1>'
         "<p>No grid, no filters, no page two. The whole catalogued oeuvre laid out along a "
         "single line and walked from left to right — 2009 at your back, 2024 somewhere ahead. "
         "Height is discipline; the year posts are the only signage.</p>"
         "<small>begin →</small></div>"]

    cur = None
    for w in ws:
        if w["year"] != cur:
            cur = w["year"]
            b.append(f'<div class="mile"><span>year</span><b>{cur}</b></div>')
        h = heights.get(w["discipline"], 0.45)
        wid = h * w["img"]["ratio"]
        b.append(
            f'<figure class="w" style="height:{h*100:.0f}%">'
            f'<img src="{wide(w)}" alt="{alt(w)}" loading="lazy" '
            f'style="aspect-ratio:{w["img"]["ratio"]:.3f}">'
            f'<figcaption><b>{esc(w["title"])}</b>{esc(w["medium"] or w["discipline"])}</figcaption>'
            f"</figure>"
        )

    b.append(
        '<div class="end"><p>You have just walked past everything he has made and kept. '
        "It took about four minutes.</p>"
        '<a href="#">now go slowly → archive.kyleparkercunningham.com</a></div>'
    )
    b.append('</div><div class="hint">shift + scroll, or swipe</div>')
    return lib.write("40-the-long-walk.html", "The Long Walk", css, "".join(b), fonts=FONTS_MAP)


def main():
    for fn in (sheet_36, sheet_37, sheet_38, sheet_39, sheet_40):
        print(fn())


if __name__ == "__main__":
    import sheets

    for s in sheets.SHEETS:
        lib.register(*s)
    main()
