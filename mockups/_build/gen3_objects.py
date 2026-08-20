#!/usr/bin/env python3
"""Sheets 48–55 — the site as a physical object.

Kyle runs a press and a bindery. These eight ask what happens if the
website stops pretending to be a website and admits to being a thing:
a drawer, a roll of film, a length of cloth, a plate, a specimen sheet,
a folded broadsheet, a cabinet, a terminal.
"""

import math
from collections import Counter, defaultdict

import lib
from lib import (alt, blurb, by_hue, dims, esc, get, grid_svg, many, sentence,
                 tagged, thumb, wide)


# -------------------------------------------------------- 48 card catalogue

def sheet_48():
    css = """
:root{--wood:#4a2f1d;--card:#f0e7d2;--card2:#e7dcc3;--ink:#2b2317;--red:#9c2b1f;
 --type:#3a3025}
body{background:#33200f;color:var(--ink);font-family:"Xanh Mono",Courier,monospace;
 background-image:repeating-linear-gradient(90deg,rgba(0,0,0,.16) 0 2px,
  transparent 2px 7px),linear-gradient(180deg,#3d2513,#26160a)}
.case{max-width:1180px;margin:0 auto;padding:56px 20px 90px}
.brass{background:linear-gradient(180deg,#c8a24e,#8d6c26);color:#241a08;
 padding:8px 16px;display:inline-block;font-size:11px;letter-spacing:.32em;
 text-transform:uppercase;border:1px solid #6a5019;box-shadow:0 2px 0 rgba(0,0,0,.4)}
h1{font-family:"Xanh Mono",monospace;color:#efe3c8;font-weight:400;
 font-size:clamp(2rem,5.6vw,3.4rem);margin:.5em 0 .2em;letter-spacing:-.01em}
.hint{color:#b09a72;font-size:12.5px;line-height:1.7;max-width:60ch;margin:0 0 34px}
.hint b{color:#efe3c8;font-weight:400}
.drawer{background:var(--card2);border:1px solid #2b1c0d;padding:22px 18px 30px;
 box-shadow:inset 0 24px 40px -30px rgba(0,0,0,.8),0 18px 40px -20px rgba(0,0,0,.7);
 position:relative}
.drawer::after{content:"";position:absolute;left:8px;right:8px;bottom:9px;height:5px;
 background:linear-gradient(180deg,#8d6c26,#5c4416);border-radius:3px}
.tabs{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:18px}
.tab{background:var(--card);padding:4px 12px;font-size:11px;
 letter-spacing:.14em;text-transform:uppercase;color:var(--type);
 border:1px solid #bfae8b;border-bottom:none;text-decoration:none}
.tab:hover{background:#fff8e8}
.tab.on{background:var(--red);color:#f6ecd6;border-color:var(--red)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));gap:16px}
.card{background:var(--card);border:1px solid #c7b590;padding:14px 15px 12px;
 position:relative;box-shadow:2px 3px 0 rgba(0,0,0,.14);
 background-image:repeating-linear-gradient(180deg,transparent 0 21px,
  rgba(120,90,50,.14) 21px 22px);min-height:212px;display:flex;flex-direction:column}
.card:nth-child(3n){transform:rotate(-.35deg)}
.card:nth-child(4n){transform:rotate(.28deg)}
.card::after{content:"";position:absolute;left:50%;bottom:7px;width:11px;height:11px;
 border:1.5px solid #b09a72;border-radius:50%;transform:translateX(-50%)}
.no{font-size:10.5px;letter-spacing:.2em;color:var(--red);text-transform:uppercase}
.ttl{font-size:1.02rem;line-height:1.25;margin:6px 0 2px;color:var(--ink)}
.ttl i{font-style:italic}
.by{font-size:11.5px;color:#6b5c44;margin-bottom:9px}
.fields{font-size:11px;line-height:1.85;color:var(--type);flex:1}
.fields b{font-weight:400;color:#8a7756;display:inline-block;width:66px}
.trace{margin-top:8px;border-top:1px dashed #c2b087;padding-top:6px;font-size:10px;
 letter-spacing:.1em;color:#8a7756;text-transform:uppercase}
.thumbchip{position:absolute;right:12px;top:12px;width:44px;height:44px;
 border:1px solid #c2b087;object-fit:cover;filter:sepia(.24) contrast(.95)}
.seealso{color:var(--red)}
.guide{grid-column:1/-1;background:#d9c9a4;border:1px solid #b09a72;padding:10px 16px;
 font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:#4a3a20;
 box-shadow:2px 3px 0 rgba(0,0,0,.14)}
.foot{color:#b09a72;font-size:11px;letter-spacing:.14em;text-transform:uppercase;
 margin-top:26px;display:flex;flex-wrap:wrap;gap:8px 26px;justify-content:space-between}
@media(max-width:520px){.cards{grid-template-columns:minmax(0,1fr)}}
"""
    groups = [
        ("A–C", ["above-the-clouds", "arm-fauna", "bottled-lightning", "cyclum-lunarem"]),
        ("D–L", ["docile", "elephant-mask", "the-black-fire", "low-angle-sun-rays"]),
        ("M–R", ["me-own-juniper", "the-mother-bear", "pet-walk", "rhino-radar"]),
        ("S–Z", ["solar-ascension", "the-river-in-the-sky", "transplanter",
                 "there-once-was-ice-here"]),
    ]
    b = ['<div class="case">',
         '<div class="brass">Oeuvre · drawer 3 of 12</div>',
         "<h1>Card catalogue</h1>",
         '<p class="hint">The archive is a database and behaves like one. Before databases '
         "this is what an archive was: a rod through the bottom of a stack of cards, one card "
         "per object, typed once and never reformatted. Every field on these cards is real and "
         "comes straight from the record. <b>The point is that a card is finite</b> — it can "
         "hold about forty words, so somebody has to decide which forty.</p>",
         '<div class="drawer"><div class="tabs">'
         '<a class="tab on" href="#">Oeuvre</a><a class="tab" href="#">Projects</a>'
         '<a class="tab" href="#">Exhibitions</a><a class="tab" href="#">Editions</a>'
         '<a class="tab" href="#">Cinema</a><a class="tab" href="#">Subject</a></div>',
         '<div class="cards">']

    n = 0
    for label, slugs in groups:
        b.append(f'<div class="guide">{esc(label)}</div>')
        for slug in slugs:
            w = get(slug)
            n += 1
            mats = ", ".join((w["materials"] + w["techniques"])[:3]) or "—"
            subj = ", ".join(w["tags"][:4]) or "—"
            rel = w["related"][0] if w["related"] else None
            see = (f'<div class="trace seealso">see also: {esc(rel["title"])}, {rel["year"]}</div>'
                   if rel else '<div class="trace">see also: —</div>')
            b.append(
                f'<div class="card">'
                f'<img class="thumbchip" src="{thumb(w)}" alt="{alt(w)}" loading="lazy">'
                f'<div class="no">KPC {w["year"]}·{n:03d}</div>'
                f'<div class="ttl"><i>{esc(w["title"])}</i></div>'
                f'<div class="by">Cunningham, Kyle Parker, 1983–</div>'
                f'<div class="fields">'
                f'<div><b>Date</b>{w["year"] or "n.d."}</div>'
                f'<div><b>Medium</b>{esc(w["medium"] or "—")}</div>'
                f'<div><b>Dimens.</b>{esc(dims(w) or "not recorded")}</div>'
                f'<div><b>Class</b>{esc(w["discipline"])} · {esc(mats)}</div>'
                f'<div><b>Subject</b>{esc(subj)}</div>'
                f"</div>{see}</div>"
            )
    b.append("</div></div>")
    b.append(
        '<div class="foot"><span>Drawer 3 · 16 of 155 cards shown</span>'
        "<span>Full records → archive.kyleparkercunningham.com</span>"
        "<span>Typed once. Not reformatted.</span></div></div>"
    )
    return lib.write("48-card-catalogue.html", "Card Catalogue", css, "".join(b))


# --------------------------------------------------------- 49 contact sheet

def sheet_49():
    css = """
:root{--black:#0a0a0a;--film:#1a1a1a;--edge:#c9a227;--grease:#e8541f;--ink:#e8e4dc}
body{background:var(--black);color:var(--ink);font-family:"IBM Plex Mono",monospace;
 font-size:13px}
.wrap{max-width:1240px;margin:0 auto;padding:0 22px 90px}
header{padding:56px 0 22px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,300px);
 gap:30px;align-items:end;border-bottom:1px solid #262626}
h1{font-family:"Archivo Narrow",sans-serif;font-weight:700;text-transform:uppercase;
 font-size:clamp(2.2rem,6.6vw,4.4rem);letter-spacing:-.02em;line-height:.94;margin:0}
.sub{color:#8d8880;font-size:11px;letter-spacing:.3em;text-transform:uppercase;
 margin-bottom:14px}
.slate{border:1px solid #333;padding:12px 14px;font-size:11px;line-height:1.95}
.slate div{display:flex;justify-content:space-between;gap:14px;border-bottom:1px dotted #2e2e2e}
.slate b{font-weight:400;color:#8d8880}
.roll{margin-top:30px}
.rollhead{display:flex;justify-content:space-between;font-size:10px;letter-spacing:.28em;
 text-transform:uppercase;color:var(--edge);padding:6px 0}
.strip{background:var(--film);border-top:1px solid #2a2a2a;border-bottom:1px solid #2a2a2a;
 display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:0;position:relative;
 padding:16px 0}
.strip::before,.strip::after{content:"";position:absolute;left:0;right:0;height:16px;
 background-image:radial-gradient(circle at 8px 8px,#0a0a0a 3.4px,transparent 3.5px);
 background-size:17px 16px}
.strip::before{top:0}.strip::after{bottom:0}
.fr{position:relative;padding:5px 6px;text-decoration:none;color:inherit;display:block}
.fr img{width:100%;aspect-ratio:1;object-fit:cover;display:block;filter:contrast(1.03)}
.fr .n{font-size:9.5px;color:var(--edge);letter-spacing:.14em;margin-top:4px}
.fr .t{font-size:9.5px;color:#9a958c;line-height:1.35;margin-top:1px;
 display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.fr.sel::after{content:"";position:absolute;inset:2px;border:2.5px solid var(--grease);
 border-radius:52% 48% 49% 51%/50% 52% 48% 50%;pointer-events:none;opacity:.92}
.fr.kill::after{content:"";position:absolute;inset:6px;pointer-events:none;
 background:linear-gradient(to bottom right,transparent calc(50% - 1.6px),var(--grease)
  calc(50% - 1.6px),var(--grease) calc(50% + 1.6px),transparent calc(50% + 1.6px)),
  linear-gradient(to bottom left,transparent calc(50% - 1.6px),var(--grease)
  calc(50% - 1.6px),var(--grease) calc(50% + 1.6px),transparent calc(50% + 1.6px))}
.fr.crop .cr{position:absolute;left:22%;top:10%;right:12%;bottom:34%;
 border:2px solid var(--grease);pointer-events:none}
.note{color:#8d8880;line-height:1.8;max-width:64ch;margin:26px 0 0;font-size:12.5px}
.note b{color:var(--ink);font-weight:400}
.legend{display:flex;flex-wrap:wrap;gap:12px 30px;margin-top:22px;font-size:10.5px;
 letter-spacing:.2em;text-transform:uppercase;color:#8d8880;border-top:1px solid #262626;
 padding-top:14px}
.legend i{color:var(--grease);font-style:normal}
@media(max-width:760px){header{grid-template-columns:minmax(0,1fr)}}
"""
    rolls = [
        ("ROLL 12", "2018", "the year something opened", 2018),
        ("ROLL 15", "2021", "solarpunk at full strength", 2021),
        ("ROLL 18", "2024", "the memory of atmosphere", 2024),
    ]
    b = ['<div class="wrap"><header><div>',
         '<div class="sub">Kyle Parker Cunningham · proof sheets · not for reproduction</div>',
         "<h1>Contact sheet</h1></div>",
         '<div class="slate"><div><b>Subject</b><span>the oeuvre</span></div>'
         "<div><b>Rolls</b><span>3 of 16</span></div>"
         "<div><b>Frames</b><span>67</span></div>"
         "<div><b>Marked</b><span>grease pencil</span></div>"
         "<div><b>Editor</b><span>KPC</span></div></div></header>"]

    b.append(
        '<p class="note">A contact sheet is the least flattering way to show work and the '
        "most honest: everything at the same size, in the order it was shot, including the "
        "frames that did not come off. <b>The marks are the argument.</b> A circle means "
        "print it. A cross means no. A rectangle means the painting is in there somewhere "
        "but not at that crop.</p>"
    )

    for name, year, cap, yr in rolls:
        ws = [w for w in lib.WORKS if w["year"] == yr]
        ws.sort(key=lambda w: w["title"].lower())
        frames = []
        for i, w in enumerate(ws, 1):
            # Selects are the works the catalogue itself flags: those that got
            # revisited in another year, or carry a whole body of work's tag.
            cls = ""
            if w["related"]:
                cls = " sel"
            elif w["img"]["sat"] < 0.12 and w["discipline"] == "Printmaking":
                cls = " kill"
            elif "the memory of atmosphere" in w["tags"]:
                cls = " crop"
            crop = '<span class="cr"></span>' if "crop" in cls else ""
            frames.append(
                f'<a class="fr{cls}" href="#{esc(w["slug"])}">'
                f'<img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">{crop}'
                f'<div class="n">{i}A</div><div class="t">{esc(w["title"])}</div></a>'
            )
        b.append(
            f'<section class="roll"><div class="rollhead"><span>{esc(name)} · '
            f"KODAK TRI-X 400 · {esc(year)}</span><span>{esc(cap)} · {len(ws)} frames</span>"
            f'</div><div class="strip">{"".join(frames)}</div></section>'
        )

    b.append(
        '<div class="legend"><span><i>◯</i> printed — the work was returned to in a later year</span>'
        "<span><i>✗</i> not this one</span>"
        "<span><i>▭</i> crop — part of a standing investigation</span>"
        "<span>marks derived from the catalogue's own relations, not from taste</span></div>"
    )
    b.append("</div>")
    return lib.write("49-contact-sheet.html", "Contact Sheet", css, "".join(b))


# -------------------------------------------------------------- 50 the loom

def sheet_50():
    css = """
:root{--linen:#ddd3c0;--warp:#c3b59c;--ink:#2a2419;--dim:#7b7160;--sel:#8c3a26}
body{background:var(--linen);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;
 background-image:repeating-linear-gradient(90deg,rgba(255,255,255,.34) 0 1px,transparent 1px 4px),
  repeating-linear-gradient(0deg,rgba(120,100,70,.09) 0 1px,transparent 1px 4px)}
.wrap{max-width:1280px;margin:0 auto;padding:0 22px 96px}
header{padding:64px 0 26px;max-width:60ch}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.36em;
 text-transform:uppercase;color:var(--dim)}
h1{font-family:"Cormorant Garamond",Georgia,serif;font-weight:400;
 font-size:clamp(2.8rem,8vw,5.4rem);line-height:.96;margin:.16em 0 .22em;letter-spacing:-.01em}
header p{line-height:1.68;color:#463f31;font-size:1.02rem}
header p b{font-weight:600}
.cloth{overflow-x:auto;padding-bottom:10px;scrollbar-width:thin}
table{border-collapse:collapse;min-width:940px;width:100%}
th,td{padding:0;border:0}
thead th{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.12em;
 color:var(--dim);font-weight:400;padding:0 0 8px;text-align:center;vertical-align:bottom}
tbody th{text-align:right;font-family:"Cormorant Garamond",Georgia,serif;font-size:1.05rem;
 font-weight:400;padding-right:14px;white-space:nowrap;width:1%;font-style:italic}
tbody th small{display:block;font-family:"IBM Plex Mono",monospace;font-size:9px;
 letter-spacing:.16em;text-transform:uppercase;color:var(--dim);font-style:normal}
td{height:34px;position:relative;border-right:1px solid rgba(255,255,255,.5)}
td .th{position:absolute;inset:3px 1px;border-radius:1px}
td a{position:absolute;inset:0;display:block}
td .tip{position:absolute;left:50%;bottom:calc(100% + 4px);transform:translateX(-50%);
 background:#2a2419;color:#f2ede2;font-size:10.5px;letter-spacing:.04em;padding:4px 8px;
 white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .15s;z-index:5}
td:hover .tip{opacity:1}
tbody tr:nth-child(odd) td{background:rgba(255,255,255,.16)}
.selv{margin-top:8px;display:flex;justify-content:space-between;
 font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--dim)}
.read{margin-top:52px;display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
 gap:30px;border-top:1px solid #c3b59c;padding-top:24px}
.read h2{font-family:"Cormorant Garamond",Georgia,serif;font-weight:400;font-size:1.4rem;
 margin:0 0 8px;font-style:italic}
.read p{margin:0;line-height:1.7;font-size:.95rem;color:#463f31}
"""
    motifs = [
        ("elephant", "elephant"), ("whale", "whale"), ("juniper", "juniper"),
        ("bison", "bison"), ("owl", "owl"), ("bee", "bee"),
        ("space helmet", "space helmet"), ("glass jar", "glass jar"),
        ("circle / ensō", "circle"), ("triangle", "triangle"),
        ("concentric", "concentric"), ("skull", "skull"),
        ("cloud", "cloud"), ("lightning", "lightning"),
        ("machine", "machine"), ("hand", "hand"),
        ("portrait", "portrait"), ("still life", "still life"),
        ("deep time", "deep time"), ("post-collapse", "post-collapse"),
    ]
    years = list(range(2009, 2025))

    b = ['<div class="wrap"><header>',
         '<div class="kick">Warp: sixteen years · Weft: twenty motifs</div>',
         "<h1>The loom</h1>",
         "<p>Several of these paintings are on <b>handwoven linen</b> — the ground is itself "
         "a grid of decisions. So set the oeuvre on a loom. The warp running across is time, "
         "one thread per year. The weft running down is subject, one thread per recurring "
         "motif. Where a thread is picked up, the cell carries the real colour of the work "
         "that picked it up. What you are looking for is not the dense parts. It is the "
         "threads that drop out for six years and come back.</p></header>",
         '<div class="cloth"><table><thead><tr><th></th>']
    for y in years:
        b.append(f"<th>{str(y)[2:]}</th>")
    b.append("</tr></thead><tbody>")

    for label, tag in motifs:
        ws = tagged(tag)
        by_y = defaultdict(list)
        for w in ws:
            if w["year"]:
                by_y[w["year"]].append(w)
        span = [y for y in years if by_y.get(y)]
        first, last = (min(span), max(span)) if span else (0, 0)
        b.append(f'<tr><th>{esc(label)}<small>{len(ws)} works · '
                 f'{first}–{last}</small></th>')
        for y in years:
            cell = by_y.get(y)
            if not cell:
                inside = ""
                if span and first < y < last:
                    # the thread is still on the loom, just not picked up
                    inside = ('<span class="th" style="background:none;inset:0;'
                              'border-top:1.5px dotted rgba(140,58,38,.55);'
                              'top:50%;height:0"></span>')
                b.append(f"<td>{inside}</td>")
                continue
            im = cell[0]["img"]
            col = f"hsl({im['hue']:.0f} {min(im['sat']*150,74):.0f}% {26+im['lig']*46:.0f}%)"
            if im["chroma"] <= 0.06:
                col = f"hsl(38 6% {24+im['lig']*50:.0f}%)"
            titles = ", ".join(w["title"] for w in cell[:3])
            b.append(
                f'<td><span class="th" style="background:{col}"></span>'
                f'<a href="#{esc(cell[0]["slug"])}" aria-label="{esc(titles)}"></a>'
                f'<span class="tip">{esc(titles)} · {y}</span></td>'
            )
        b.append("</tr>")
    b.append("</tbody></table></div>")
    b.append(
        '<div class="selv"><span>selvedge · 2009</span>'
        "<span>cell colour = the measured colour of the work</span>"
        "<span>2024 · selvedge</span></div>"
    )
    b.append(
        '<div class="read"><div><h2>How to read the cloth</h2>'
        "<p>A filled cell is a year the motif was picked up. The dotted red line between "
        "filled cells is the same thread still on the loom, waiting: the motif went "
        "underground and came back. <i>Juniper</i> does this across twelve years. So does "
        "<i>whale</i>, which starts as a painted animal and returns as a boat carrying a "
        "tree across an ocean.</p></div>"
        "<div><h2>What the density says</h2><p>The right-hand third of the cloth is much "
        "denser than the left, and that is not only productivity. It is a controlled "
        "vocabulary: 476 tags, applied consistently, only recently. Older work is "
        "under-described, so the loom under-reports it. A structure this legible is worth "
        "having and worth distrusting at the same time.</p></div>"
        "<div><h2>Where it goes</h2><p>Every cell is a link. Pull one thread and you get "
        "the run — every appearance of the whale, in order, which is sheet 61. The loom is "
        "the index; the atlas is the reading.</p></div></div></div>"
    )
    return lib.write("50-the-loom.html", "The Loom", css, "".join(b))


# ------------------------------------------------------------- 51 the press

def sheet_51():
    css = """
:root{--ink:#111;--paper:#f7f4ec;--rag:#efe9dc;--red:#a32b1c;--dim:#7a746a}
body{background:var(--paper);color:var(--ink);font-family:"Archivo Narrow",sans-serif;
 font-size:16px}
.reg{position:fixed;pointer-events:none;z-index:8;width:22px;height:22px;opacity:.5}
.reg::before,.reg::after{content:"";position:absolute;background:var(--ink)}
.reg::before{left:50%;top:0;bottom:0;width:1px}
.reg::after{top:50%;left:0;right:0;height:1px}
.reg.tl{left:14px;top:14px}.reg.tr{right:14px;top:14px}
.wrap{max-width:1120px;margin:0 auto;padding:0 26px 100px}
header{padding:74px 0 20px;border-bottom:4px solid var(--ink)}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.34em;
 text-transform:uppercase;color:var(--dim)}
h1{font-weight:700;text-transform:uppercase;font-size:clamp(2.8rem,9vw,6.2rem);
 letter-spacing:-.035em;line-height:.86;margin:.1em 0 .16em}
.lede{font-family:"Newsreader",Georgia,serif;font-size:1.2rem;line-height:1.6;max-width:60ch;
 color:#2e2b26;margin:0 0 8px}
h2{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.3em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:58px 0 14px;
 border-bottom:1px solid #d8d1c3;padding-bottom:7px;display:flex;justify-content:space-between}
.states{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:18px}
.state{position:relative}
.state .plate{background:var(--rag);border:1px solid #ddd5c5;padding:12px;
 box-shadow:0 8px 20px -18px rgba(0,0,0,.6)}
.state img{width:100%;aspect-ratio:4/5;object-fit:contain;display:block;
 background:#fff;padding:4px}
.state .lab{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--dim);margin-top:9px;line-height:1.6}
.state .lab b{display:block;color:var(--ink);font-size:11.5px}
.state .lab i{color:var(--red);font-style:normal}
.wear{height:4px;background:linear-gradient(90deg,var(--ink),#c9c2b4);margin-top:8px}
.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px;
 align-items:start}
.pair figure{margin:0}
.pair img{width:100%;height:auto;border:1px solid #ddd5c5;background:#fff}
.pair figcaption{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--dim);margin-top:9px;line-height:1.55}
.pair figcaption b{display:block;font-family:"Archivo Narrow",sans-serif;font-size:1.05rem;
 letter-spacing:.01em;color:var(--ink);text-transform:none}
.arrow{display:grid;place-items:center;font-size:1.6rem;color:var(--red)}
p.body{font-family:"Newsreader",Georgia,serif;line-height:1.66;max-width:62ch;color:#2e2b26}
.spec{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;
 border:2px solid var(--ink);margin-top:18px}
.spec div{padding:12px 14px;border-right:1px solid #d8d1c3}
.spec div:last-child{border-right:0}
.spec dt{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--dim)}
.spec dd{margin:3px 0 0;font-size:1.35rem;font-weight:700;letter-spacing:-.01em}
.spec dd small{font-size:.6rem;font-weight:400;color:var(--dim);letter-spacing:.14em;
 text-transform:uppercase}
@media(max-width:640px){.spec div{border-right:0;border-bottom:1px solid #d8d1c3}}
"""
    # Works the catalogue records as crossing media: painting → plate, or back.
    cross = tagged("cross-medium motif")
    pairs = []
    seen = set()
    for w in cross:
        for r in w["related"]:
            other = lib.BY_SLUG.get(r["slug"])
            if not other:
                continue
            key = tuple(sorted([w["slug"], other["slug"]]))
            if key in seen:
                continue
            seen.add(key)
            a, c = sorted([w, other], key=lambda x: x["year"] or 0)
            if a["discipline"] != c["discipline"]:
                pairs.append((a, c))

    b = ['<div class="reg tl"></div><div class="reg tr"></div><div class="wrap"><header>',
         '<div class="kick">Agile Meteor Press · intaglio · drypoint · chine-collé</div>',
         "<h1>Plate,<br>state, proof.</h1>",
         '<p class="lede">Forty-nine works in the catalogue are intaglio, forty-five of them '
         "drypoint. Drypoint is the one printmaking process that destroys itself as it works: "
         "the burr that holds the ink is soft metal, and every pass through the press flattens "
         "it. An edition of drypoints is not a set of copies. It is a decline.</p></header>"]

    demo = get("butterfly-conundrum")
    b.append(
        f"<h2><span>States of one plate</span><span><i>{esc(demo['title'])}</i>, "
        f"{demo['year']} · drypoint on hand-torn paper</span></h2>"
        '<div class="states">'
    )
    for i, (roman, note, filt, wear) in enumerate([
        ("I", "trial proof · full burr", "contrast(1.12) saturate(.2)", 100),
        ("II", "second state · line opened", "contrast(1.04) saturate(.55)", 74),
        ("III", "hand-coloured · watercolour", "none", 48),
        ("IV", "late pull · burr gone", "contrast(.86) brightness(1.08) saturate(.8)", 18),
    ], 1):
        b.append(
            f'<div class="state"><div class="plate">'
            f'<img src="{thumb(demo)}" alt="{alt(demo)}" loading="lazy" '
            f'style="filter:{filt}">'
            f'<div class="wear" style="width:{wear}%"></div>'
            f'<div class="lab"><b>State {roman}</b>{esc(note)}<br>'
            f'<i>burr remaining ≈ {wear}%</i></div></div></div>'
        )
    b.append("</div>")
    b.append(
        '<p class="body" style="margin-top:18px">The four frames above are a demonstration, '
        "not four photographed proofs — the archive stores one image for this work. But it "
        "does store <i>edition variants</i> as a tag on nine works, which is the studio saying "
        "out loud that no two pulls are the same. A site built on this idea would show the "
        "states, and a collector would know which pull they own.</p>"
    )

    b.append(
        f"<h2><span>Across the press bed</span><span>{len(pairs)} motifs that changed medium</span></h2>"
        '<p class="body">The catalogue records twenty-eight pairs of related works. Some of '
        "them are the same image in two materials, years apart: a painting scratched back into "
        "copper, or a plate that became a canvas. This is the part of the practice the "
        "catalogue is best at and the old site showed least.</p>"
    )
    for a, c in pairs[:4]:
        b.append(
            f'<div class="pair" style="margin-top:26px">'
            f'<figure><img src="{wide(a)}" alt="{alt(a)}" loading="lazy">'
            f'<figcaption><b>{esc(a["title"])}</b>{a["year"]} · {esc(a["medium"] or a["discipline"])}'
            f"</figcaption></figure>"
            f'<figure><img src="{wide(c)}" alt="{alt(c)}" loading="lazy">'
            f'<figcaption><b>{esc(c["title"])}</b>{c["year"]} · {esc(c["medium"] or c["discipline"])}'
            f' · {abs((c["year"] or 0)-(a["year"] or 0))} years later</figcaption></figure></div>'
        )

    b.append(
        "<h2><span>The shop</span><span>as recorded</span></h2>"
        '<dl class="spec">'
        "<div><dt>Intaglio works</dt><dd>49</dd></div>"
        "<div><dt>Drypoint</dt><dd>45</dd></div>"
        "<div><dt>Hand-coloured</dt><dd>32<small> of them</small></dd></div>"
        "<div><dt>Chine-collé</dt><dd>1</dd></div>"
        "<div><dt>Rives BFK</dt><dd>5<small> recorded</small></dd></div>"
        "<div><dt>Hand-torn</dt><dd>21<small> sheets</small></dd></div></dl>"
    )
    b.append("</div>")
    return lib.write("51-the-press.html", "Plate, State, Proof", css, "".join(b))


# ------------------------------------------------------------- 52 herbarium

def sheet_52():
    css = """
:root{--sheet:#f6f2e6;--board:#cfc4a8;--ink:#2c2718;--label:#faf7ee;--hand:#3b4a6b;
 --dim:#7d7460}
body{background:#b8ab8c;color:var(--ink);font-family:"EB Garamond",Georgia,serif;
 font-size:17px;
 background-image:repeating-linear-gradient(45deg,rgba(0,0,0,.03) 0 2px,transparent 2px 5px)}
.wrap{max-width:1180px;margin:0 auto;padding:52px 20px 90px}
.masthead{background:var(--sheet);border:1px solid #a89a78;padding:32px 30px;
 box-shadow:0 14px 34px -22px rgba(0,0,0,.6);margin-bottom:26px}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.34em;
 text-transform:uppercase;color:var(--dim)}
h1{font-family:"Cormorant Garamond",Georgia,serif;font-weight:300;
 font-size:clamp(2.4rem,7vw,4.6rem);line-height:1;margin:.16em 0 .2em;letter-spacing:-.01em}
.masthead p{max-width:62ch;line-height:1.62;margin:0;color:#3d3728}
.sheets{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px}
.spec{background:var(--sheet);border:1px solid #a89a78;padding:16px 16px 14px;
 box-shadow:0 12px 28px -22px rgba(0,0,0,.7);display:flex;flex-direction:column}
.mount{position:relative;background:#fffdf7;border:1px solid #ddd3ba;padding:14px;
 flex:1;display:grid;place-items:center;min-height:190px}
.mount img{max-width:100%;max-height:230px;width:auto;height:auto;
 filter:sepia(.06) saturate(.94)}
.tape{position:absolute;width:44px;height:15px;background:rgba(214,198,160,.72);
 border:1px solid rgba(160,145,110,.5);transform:rotate(-4deg)}
.tape.a{left:-6px;top:22px}.tape.b{right:-6px;bottom:26px;transform:rotate(5deg)}
.label{background:var(--label);border:1px solid #cfc4a8;margin-top:12px;padding:10px 12px;
 font-family:"IBM Plex Mono",monospace;font-size:10.5px;line-height:1.85;color:#4a4433}
.label .top{display:flex;justify-content:space-between;font-size:9px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--dim);border-bottom:1px solid #ddd3ba;
 padding-bottom:5px;margin-bottom:6px}
.label .sci{font-family:"Cormorant Garamond",Georgia,serif;font-size:1.3rem;font-style:italic;
 color:var(--ink);line-height:1.15;display:block;margin-bottom:2px}
.label .det{color:var(--hand);font-family:"EB Garamond",serif;font-size:14px;font-style:italic;
 line-height:1.4;display:block;margin-top:6px;border-top:1px dotted #ddd3ba;padding-top:6px}
.label b{font-weight:400;color:#8b8168;display:inline-block;width:58px}
.colophon{background:var(--sheet);border:1px solid #a89a78;padding:24px 26px;margin-top:26px;
 box-shadow:0 12px 28px -22px rgba(0,0,0,.6)}
.colophon h2{font-family:"Cormorant Garamond",Georgia,serif;font-weight:400;font-size:1.5rem;
 margin:0 0 8px}
.colophon p{max-width:66ch;line-height:1.64;margin:0 0 10px;color:#3d3728}
"""
    # Every specimen is a real record; the "scientific" binomial is built from
    # the work's own two strongest tags, and the sheet says so.
    picks = ["me-own-juniper", "parasitic-pollen-eaters", "prickly-pear", "sunflowers",
             "origami-beetroot", "bottled-oxygen", "alligator-juniper-nogal",
             "three-blue-corn", "pruning", "docile", "in-the-pines", "molecule"]
    b = ['<div class="wrap"><div class="masthead">',
         '<div class="kick">Herbarium of the Near Future · sheets 1–12 · Truth or Consequences</div>',
         "<h1>Pressed, mounted,<br>determined.</h1>",
         "<p>A herbarium sheet carries a specimen and a label, and the label is the science: "
         "who collected it, where, when, and what they decided it was. The archive already "
         "holds every one of those fields for every work. This is what they look like when "
         "the record is treated as a determination rather than a caption — and when somebody "
         "is willing to be wrong in ink.</p></div>",
         '<div class="sheets">']

    for i, slug in enumerate(picks, 1):
        w = get(slug)
        tags = [t for t in w["tags"] if t not in {"private collection", "sold"}]
        genus = (tags[0] if tags else w["discipline"]).replace(" ", "-")
        species = (tags[1] if len(tags) > 1 else w["discipline"]).replace(" ", "-")
        b.append(
            f'<article class="spec"><div class="mount">'
            f'<span class="tape a"></span><span class="tape b"></span>'
            f'<img src="{wide(w)}" alt="{alt(w)}" loading="lazy"></div>'
            f'<div class="label"><div class="top"><span>Sheet {i:03d}</span>'
            f'<span>KPC HERB.</span></div>'
            f'<span class="sci">{esc(genus)} {esc(species)}</span>'
            f'<div><b>Coll.</b>K. P. Cunningham</div>'
            f'<div><b>Date</b>{w["year"] or "n.d."}</div>'
            f'<div><b>Loc.</b>{esc(w["place"] or "New Mexico / Montana")}</div>'
            f'<div><b>Subst.</b>{esc(w["medium"] or "—")}</div>'
            f'<div><b>Meas.</b>{esc(dims(w) or "not taken")}</div>'
            f'<span class="det">{esc(sentence(w, 130))}</span></div></article>'
        )
    b.append("</div>")
    b.append(
        '<div class="colophon"><h2>A note on the determinations</h2>'
        "<p>The binomials are not real. They are assembled from each work's own two "
        "strongest catalogue tags — <i>juniper deep-time</i>, <i>bee mutual-aid</i> — "
        "and they are here to make a point about what a controlled vocabulary already is. "
        "476 terms, applied consistently across 155 works, <b>is</b> a taxonomy. It has "
        "genera and it has species and it has a lot of arguments buried in it.</p>"
        "<p>The italic line at the foot of each label is the artist's own determination, "
        "quoted from the record. On a real herbarium sheet that line is signed, dated, and "
        "sometimes crossed out sixty years later by somebody who disagrees. The archive "
        "should probably let that happen too.</p></div></div>"
    )
    return lib.write("52-herbarium.html", "Herbarium", css, "".join(b))


# -------------------------------------------------------------- 53 the fold

def sheet_53():
    css = """
:root{--news:#e9e4d6;--ink:#1a1814;--red:#a8321f;--dim:#6f6959;--fold:#cdc5b0}
body{background:#8f8874;color:var(--ink);font-family:"Bodoni Moda",Georgia,serif;
 font-size:16px}
.desk{max-width:1240px;margin:0 auto;padding:40px 16px 90px}
.broadsheet{background:var(--news);box-shadow:0 26px 60px -34px rgba(0,0,0,.8);
 position:relative;
 background-image:radial-gradient(circle at 20% 10%,rgba(0,0,0,.035),transparent 60%),
  radial-gradient(circle at 80% 70%,rgba(0,0,0,.03),transparent 55%)}
.nameplate{border-bottom:5px double var(--ink);padding:34px 30px 16px;text-align:center}
.nameplate .over{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.4em;
 text-transform:uppercase;color:var(--dim)}
.nameplate h1{font-weight:500;font-size:clamp(2.4rem,8.4vw,5.6rem);line-height:.94;
 margin:.1em 0 .12em;letter-spacing:-.02em}
.nameplate .under{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.28em;
 text-transform:uppercase;color:var(--dim);display:flex;flex-wrap:wrap;gap:6px 26px;
 justify-content:center;border-top:1px solid var(--ink);padding-top:9px;margin-top:12px}
.panels{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0}
.panel{border-right:1px dashed var(--fold);padding:24px 22px 30px;position:relative}
.panel:last-child{border-right:0}
.panel::before{content:attr(data-fold);position:absolute;top:8px;right:10px;
 font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.24em;color:#a49c86;
 text-transform:uppercase}
details{border-top:1px solid var(--ink);padding:10px 0}
details:last-of-type{border-bottom:1px solid var(--ink)}
summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;
 align-items:baseline;gap:12px}
summary::-webkit-details-marker{display:none}
summary h2{font-weight:500;font-size:1.4rem;margin:0;line-height:1.1;letter-spacing:-.01em}
summary .cue{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--red);white-space:nowrap}
details[open] summary .cue::after{content:" ▲"}
summary .cue::after{content:" ▼"}
.inner{padding-top:12px}
.inner p{font-size:.95rem;line-height:1.6;margin:0 0 10px;color:#2c2823}
.inner img{width:100%;height:auto;margin:0 0 8px;filter:grayscale(.18) contrast(1.04)}
.cap{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--dim);line-height:1.5;margin:0 0 14px}
.lead{font-size:1.06rem;line-height:1.55;margin:0 0 14px}
.lead::first-letter{float:left;font-size:3.4em;line-height:.82;padding:.06em .08em 0 0;
 font-weight:600}
.rule{border:0;border-top:1px solid var(--ink);margin:16px 0}
.strip{display:flex;gap:5px;flex-wrap:wrap;margin-top:8px}
.strip img{width:52px;height:52px;object-fit:cover;margin:0}
.folded{background:var(--news);border-top:1px dashed var(--fold);padding:16px 22px;
 font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.22em;
 text-transform:uppercase;color:var(--dim);display:flex;flex-wrap:wrap;gap:8px 26px;
 justify-content:space-between}
@media(max-width:860px){.panels{grid-template-columns:minmax(0,1fr)}
 .panel{border-right:0;border-bottom:1px dashed var(--fold)}}
"""
    def strip(slugs):
        return '<div class="strip">' + "".join(
            f'<img src="{thumb(get(s))}" alt="{alt(get(s))}" loading="lazy">'
            for s in slugs if s in lib.BY_SLUG
        ) + "</div>"

    panels = [
        ("Fold 1 · front", [
            ("What the studio is doing", "open",
             '<p class="lead">This season the studio has no walls. Through the summer Jeannie '
             "and I are working out of a vehicle across Wyoming, Montana, and Colorado — "
             "climbing and painting in the mornings, swimming the heat off at midday, "
             "documenting in the evenings, all of it running on a satellite signal and a "
             "battery.</p>"
             '<p class="cap">Season XIII · Everything That Can Be Carried · opens at solstice</p>'),
            ("The 200", "",
             "<p>Two hundred small watercolours — half his, half hers — painted in the field "
             "and each one unique. The first iteration of a larger idea, made entirely on the "
             "move.</p>" + strip(["absolute-potential", "evening-clouds"])),
            ("Where to start", "",
             "<p>If you have four minutes: the long walk. If you have nine: the docent's "
             "route. If you came to find one specific object, you want the archive, and it "
             "is one click away and much better at that than this is.</p>"),
        ]),
        ("Fold 2 · centre", [
            ("The near future, and its gear", "open",
             "<p>Animals in breathing apparatus, machines grazing, mutual aid by airship. "
             "Twenty-eight works across ten years, arguing that what is coming is neither "
             "utopia nor collapse but a great deal of improvised equipment.</p>"
             + strip(["bonsai-giant-sequoia", "paper-neck-giraffes", "there-once-was-ice-here",
                      "rhino-radar", "space-owl", "transplanter"])),
            ("Weather, without ground", "",
             "<p>The newest sustained body of work. Lightning kept in a jar; water vapour "
             "solved as algebra; the sky with the landscape removed from underneath it.</p>"
             + strip(["bottled-lightning", "the-algebra-of-water-vapor", "towers",
                      "the-river-in-the-sky"])),
            ("One tree, twelve years", "",
             "<p>He walks to the same alligator junipers and draws them again. Each time the "
             "drawing gets slower.</p>"
             + strip(["me-own-juniper", "alligator-juniper", "alligator-juniper-nogal"])),
        ]),
        ("Fold 3 · back", [
            ("From the bindery", "open",
             "<p>Two hand-bound first editions this season; <i>The Periodic</i> set on "
             "newsprint, four pages, one colour; twelve towns on the distribution list, none "
             "of them with a gallery.</p>"),
            ("The colophon", "",
             "<p>Set in Bodoni Moda and IBM Plex Mono. Printed here as a broadsheet because a "
             "broadsheet folds: you get the front panel first and open the rest only if you "
             "want it. A website can do that and almost never does.</p>"),
            ("Correspondence", "",
             "<p>Truth or Consequences, New Mexico. Letters answered slowly and in order.</p>"),
        ]),
    ]

    b = ['<div class="desk"><div class="broadsheet">',
         '<div class="nameplate"><div class="over">Agile Meteor Press · '
         "issued at the solstice · one sheet, three folds</div>",
         "<h1>The Broadsheet</h1>",
         '<div class="under"><span>Kyle Parker Cunningham</span><span>Season XIII</span>'
         "<span>Summer 2026</span><span>Free to take</span></div></div>",
         '<div class="panels">']

    for fold, items in panels:
        b.append(f'<div class="panel" data-fold="{esc(fold)}">')
        for title, state, body in items:
            b.append(
                f"<details{' open' if state else ''}><summary><h2>{esc(title)}</h2>"
                f'<span class="cue">unfold</span></summary>'
                f'<div class="inner">{body}</div></details>'
            )
        b.append("</div>")
    b.append("</div>")
    b.append(
        '<div class="folded"><span>Fold along the dashed rules</span>'
        "<span>Everything closed fits one screen</span>"
        "<span>archive.kyleparkercunningham.com</span></div>"
    )
    b.append("</div></div>")
    return lib.write("53-the-fold.html", "The Broadsheet", css, "".join(b))


# ---------------------------------------------------------- 54 wunderkammer

def sheet_54():
    css = """
:root{--wood:#2e2018;--shelf:#4b3626;--wall:#171009;--gold:#b18f4c;--ink:#ece2cf;
 --z:1}
@media(max-width:760px){:root{--z:.62}}
@media(max-width:430px){:root{--z:.46}}
body{background:var(--wall);color:var(--ink);font-family:"Cormorant Garamond",Georgia,serif;
 font-size:17px}
.cab{max-width:1320px;margin:0 auto;padding:44px 18px 90px}
.hd{text-align:center;padding:26px 0 30px}
.hd .kick{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.4em;
 text-transform:uppercase;color:var(--gold)}
h1{font-weight:300;font-size:clamp(2.6rem,8vw,5.4rem);line-height:1;margin:.14em 0 .2em;
 letter-spacing:-.01em}
.hd p{max-width:56ch;margin:0 auto;color:#b7ab93;line-height:1.6;font-size:1.02rem}
.case{background:linear-gradient(180deg,#3a291d,#251a12);border:12px solid var(--wood);
 overflow:hidden;
 box-shadow:0 0 0 2px #14100b,inset 0 0 90px rgba(0,0,0,.9),0 40px 80px -40px #000;
 padding:0 14px 14px}
.shelf{border-bottom:12px solid var(--shelf);
 box-shadow:0 6px 12px -6px rgba(0,0,0,.9);display:flex;flex-wrap:wrap;
 align-items:flex-end;justify-content:center;gap:12px 14px;padding:26px 10px 10px;
 min-height:120px}
.shelf:last-child{border-bottom:0}
.ob{position:relative;display:block;text-decoration:none;color:inherit}
.ob img{display:block;border:3px solid #0d0906;
 box-shadow:0 0 0 1px var(--gold),0 14px 22px -14px #000}
.ob .cap{position:absolute;left:50%;top:calc(100% + 5px);transform:translateX(-50%);
 font-family:"IBM Plex Mono",monospace;font-size:8.5px;letter-spacing:.1em;color:#d8caa9;
 white-space:nowrap;opacity:0;transition:opacity .2s;pointer-events:none;
 background:#0d0906;padding:3px 7px;z-index:4;color:#d8caa9}
.ob:hover .cap{opacity:1}
.ob:hover img{box-shadow:0 0 0 1px #e0bd72,0 0 26px rgba(224,189,114,.35)}
.plaque{text-align:center;font-family:"IBM Plex Mono",monospace;font-size:9.5px;
 letter-spacing:.28em;text-transform:uppercase;color:var(--gold);padding:14px 0 4px}
.key{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:26px;
 margin-top:44px;border-top:1px solid #3a2b1e;padding-top:22px}
.key h2{font-weight:400;font-size:1.3rem;margin:0 0 6px;font-style:italic}
.key p{margin:0;color:#b7ab93;line-height:1.66;font-size:.96rem}
"""
    shelves = [
        ("Fauna, augmented", tagged("animist solarpunk")[:14]),
        ("Weather & the upper air", tagged("cloud", "lightning", "sky")[:14]),
        ("Geometry, repeated", tagged("circle", "triangle", "concentric")[:14]),
        ("Persons", tagged("portrait", "face")[:12]),
        ("The mundane, raised", tagged("still life", "domestic object")[:12]),
        ("Deep time", tagged("deep time", "megafauna", "extinction")[:12]),
    ]
    b = ['<div class="cab"><div class="hd">',
         '<div class="kick">Cabinet · one case · six shelves · everything at once</div>',
         "<h1>Wunderkammer</h1>",
         "<p>Before museums separated art from natural history from curiosities, a collection "
         "was one dense wall and you did the sorting yourself. Scale here is real: each object "
         "is sized by its actual measurements where the archive has them, so the small "
         "drypoints sit like specimens beside paintings the size of a door.</p></div>",
         '<div class="case">']
    for name, ws in shelves:
        b.append(f'<div class="plaque">{esc(name)}</div><div class="shelf">')
        for w in ws:
            if w["h_mm"]:
                h = max(min(w["h_mm"] * 0.13, 130), 34)
            else:
                h = 62
            wd = h * w["img"]["ratio"]
            b.append(
                f'<a class="ob" href="#{esc(w["slug"])}">'
                f'<img src="{thumb(w)}" alt="{alt(w)}" loading="lazy" '
                f'style="height:calc(var(--z) * {h:.0f}px);'
                f'width:calc(var(--z) * {wd:.0f}px);object-fit:cover">'
                f'<span class="cap">{esc(w["title"])} · {w["year"]}</span></a>'
            )
        b.append("</div>")
    b.append("</div>")
    b.append(
        '<div class="key"><div><h2>Why one wall</h2>'
        "<p>A grid tells you every work matters equally, which is a lie every gallery site "
        "tells. A dense hang tells you they don't, and lets you find that out with your "
        "eyes.</p></div>"
        "<div><h2>Sorted by kind, not date</h2><p>The six shelves are drawn from the "
        "catalogue's own tags. A work can only stand on one shelf here, which forced some "
        "decisions the archive is right not to force.</p></div>"
        "<div><h2>The cost</h2><p>Nothing is legible at this size and nothing is meant to "
        "be. This is the view that makes you point at something, and pointing is the whole "
        "job of a front page.</p></div></div></div>"
    )
    return lib.write("54-wunderkammer.html", "Wunderkammer", css, "".join(b))


# --------------------------------------------------------------- 55 terminal

RAMP = " .:-=+*#%@$"


def ascii_grid(w, cols=34):
    """Render a work as text, sampled from its own derived thumbnail.

    A terminal cell is roughly twice as tall as it is wide, so the sample
    grid is squashed vertically to keep the work's real proportions.
    """
    from PIL import Image

    src = lib.MOCKUPS / "assets" / "t" / f"{w['slug']}.webp"
    rows_n = max(6, round(cols / w["img"]["ratio"] / 2.05))
    im = Image.open(src).convert("L").resize((cols, rows_n), Image.LANCZOS)
    px = list(im.getdata())
    lo, hi = min(px), max(px)
    span = max(hi - lo, 1)
    out = []
    for y in range(rows_n):
        line = []
        for x in range(cols):
            v = (px[y * cols + x] - lo) / span          # stretch to full range
            line.append(RAMP[max(0, min(len(RAMP) - 1, int((1 - v) * (len(RAMP) - 1))))])
        out.append("".join(line))
    return "\n".join(out)


def sheet_55():
    css = """
:root{--bg:#0b0e0b;--fg:#b8e986;--dim:#5f7a4a;--hot:#e8c547}
body{background:var(--bg);color:var(--fg);font-family:"IBM Plex Mono",monospace;
 font-size:13px;line-height:1.5;text-shadow:0 0 6px rgba(184,233,134,.28)}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:99;
 background:repeating-linear-gradient(0deg,rgba(0,0,0,.22) 0 1px,transparent 1px 3px)}
.term{max-width:960px;margin:0 auto;padding:34px 18px 90px;white-space:pre-wrap}
.term a{color:var(--hot);text-decoration:none;border-bottom:1px dotted var(--dim)}
.term a:hover{background:var(--hot);color:#0b0e0b;border-color:var(--hot)}
.b{color:#dcf7b8}
.d{color:var(--dim)}
.cursor{display:inline-block;width:8px;height:15px;background:var(--fg);
 vertical-align:-2px;animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
@media(prefers-reduced-motion:reduce){.cursor{animation:none}}
pre{margin:0;font-size:9px;line-height:.92;letter-spacing:0;color:#9ccf6b;
 font-family:"IBM Plex Mono",monospace;overflow:hidden}
.two{display:grid;grid-template-columns:auto minmax(0,1fr);gap:0 26px;align-items:start}
@media(max-width:620px){.two{grid-template-columns:minmax(0,1fr)}pre{font-size:7px}}
hr{border:0;border-top:1px solid #24331c;margin:18px 0}
"""
    picks = ["the-mother-bear", "cyclum-lunarem", "bottled-lightning", "me-own-juniper"]
    counts = Counter(w["discipline"] for w in lib.WORKS)

    def esc_t(s):
        return esc(s)

    b = ['<div class="term">']
    b.append(
        '<span class="d">KPC-OEUVRE 2.1 · serial console · 9600 8N1\n'
        "connected to archive.kyleparkercunningham.com\n"
        "155 records resident · 476 terms · type HELP\n</span><hr>"
    )
    b.append(
        '<span class="b">&gt; STATS</span>\n\n'
        f"  records ......... {len(lib.WORKS)}\n"
        f"  painting ........ {counts.get('Painting',0)}\n"
        f"  printmaking ..... {counts.get('Printmaking',0)}\n"
        f"  installation .... {counts.get('Installation',0)}\n"
        f"  other ........... {counts.get('Other',0)+counts.get('Sculpture',0)}\n"
        "  span ............ 2009–2024 (2 fallow years)\n"
        "  measured ........ 95 / 155\n\n"
    )
    b.append(
        '<span class="b">&gt; ROUTES</span>\n\n'
        '  1  <a href="36-trailhead.html">the juniper trail</a> ......... 6 works, 12 years\n'
        '  2  <a href="37-field-guide.html">survival notes</a> ........... 28 works\n'
        '  3  <a href="46-weather-log.html">memory of atmosphere</a> ..... 12 works\n'
        '  4  <a href="60-the-return.html">what he came back to</a> ..... 28 pairs\n'
        '  5  <a href="47-fallow.html">the years with nothing</a> ... 2 rows\n\n'
    )
    b.append('<span class="b">&gt; SHOW --ascii</span>\n\n')
    for slug in picks:
        w = get(slug)
        b.append(
            '<div class="two"><pre>' + ascii_grid(w) + "</pre><div>"
            f'<span class="b">{esc_t(w["title"].upper())}</span>\n'
            f'<span class="d">{w["year"]} · {esc_t(w["medium"] or w["discipline"])}'
            f'{" · " + esc_t(dims(w)) if dims(w) else ""}</span>\n\n'
            f"{esc_t(blurb(w, 240))}\n\n"
            f'<a href="#{esc(w["slug"])}">open record →</a>\n</div></div>\n\n'
        )
    b.append("<hr>")
    b.append(
        '<span class="b">&gt; WHY</span>\n\n'
        "  Because the whole catalogue is 40 KB of text and 155 pictures.\n"
        "  This page is the 40 KB. It loads on one bar of signal in a canyon,\n"
        "  it can be read aloud by a screen reader without losing anything,\n"
        "  and it will still open in 2075.\n\n"
        "  The pictures are the other site's job. This one is the finding aid,\n"
        "  and a finding aid does not need to be beautiful to be beautiful.\n\n"
        '  <span class="d">(the plates above are sampled from each work\'s own\n'
        "   photograph at 34 columns, contrast-stretched, and mapped to an\n"
        "   eleven-step density ramp. no image files are loaded.)</span>\n\n"
    )
    b.append('<span class="b">&gt; </span><span class="cursor"></span></div>')
    return lib.write("55-terminal.html", "KPC-OEUVRE · console", css, "".join(b))


def main():
    for fn in (sheet_48, sheet_49, sheet_50, sheet_51, sheet_52, sheet_53,
               sheet_54, sheet_55):
        print(fn())


if __name__ == "__main__":
    import sheets

    for s in sheets.SHEETS:
        lib.register(*s)
    main()
