#!/usr/bin/env python3
"""Sheets 63–69 — experiments, and one synthesis.

The last six take a real risk each; 69 spends everything the sketchbook
learned inside the site's existing design language, so there is a version
of this that Kyle could ship without re-teaching anybody the site.
"""

import math
from collections import Counter, defaultdict

import lib
from lib import (alt, blurb, by_hue, dims, esc, get, many, revisits, sentence,
                 tagged, thumb, wide)


# ------------------------------------------------------------- 63 the score

def sheet_63():
    css = """
:root{--paper:#fcfbf7;--ink:#14130f;--dim:#8d887c;--rule:#1a1815;--red:#9c2b1c}
body{background:var(--paper);color:var(--ink);font-family:"Playfair Display",Georgia,serif;
 font-size:17px}
.wrap{max-width:1320px;margin:0 auto;padding:0 22px 100px}
header{padding:60px 0 20px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,320px);
 gap:34px;align-items:end;border-bottom:1px solid var(--rule)}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.34em;
 text-transform:uppercase;color:var(--dim)}
h1{font-weight:400;font-size:clamp(2.6rem,8vw,5.4rem);line-height:.92;margin:.14em 0 0;
 letter-spacing:-.02em}
h1 em{font-style:italic}
header p{margin:0;line-height:1.62;color:#3a3730;font-size:.98rem}
.score{margin-top:34px;overflow-x:auto;padding-bottom:16px;scrollbar-width:thin}
.sys{min-width:1080px}
.part{display:grid;grid-template-columns:132px minmax(0,1fr);gap:0 18px;align-items:center;
 margin-bottom:22px}
.pname{text-align:right;font-style:italic;font-size:1.12rem;line-height:1.15}
.pname small{display:block;font-family:"IBM Plex Mono",monospace;font-size:8.5px;
 letter-spacing:.2em;text-transform:uppercase;color:var(--dim);font-style:normal;
 margin-top:3px}
.stave{position:relative;height:96px}
.stave .l{position:absolute;left:0;right:0;height:1px;background:#2a2823;opacity:.5}
.note{position:absolute;transform:translate(-50%,-50%);border-radius:50%;
 border:1.2px solid rgba(0,0,0,.55);cursor:pointer}
.note::after{content:attr(data-t) " " attr(data-y);position:absolute;left:50%;bottom:calc(100% + 6px);
 transform:translateX(-50%);background:#14130f;color:#fcfbf7;font-family:"IBM Plex Mono",monospace;
 font-size:9.5px;letter-spacing:.06em;padding:3px 7px;white-space:nowrap;opacity:0;
 pointer-events:none;transition:opacity .15s;z-index:9}
.note:hover::after{opacity:1}
.bars{display:grid;grid-template-columns:132px minmax(0,1fr);gap:0 18px;margin-top:6px}
.barline{display:flex;position:relative;height:22px;border-top:1px solid var(--rule)}
.barline span{flex:1;font-family:"IBM Plex Mono",monospace;font-size:9.5px;
 letter-spacing:.14em;color:var(--dim);border-left:1px solid #ccc7b9;padding-left:5px;
 padding-top:4px}
.marks{display:grid;grid-template-columns:132px minmax(0,1fr);gap:0 18px;margin:0 0 8px}
.marks div{position:relative;height:20px}
.marks i{position:absolute;transform:translateX(-50%);font-style:italic;font-size:1rem;
 color:var(--red);white-space:nowrap}
.key{margin-top:44px;border-top:1px solid var(--rule);padding-top:22px;display:grid;
 grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:26px}
.key h3{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.24em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:0 0 8px}
.key p{margin:0;line-height:1.66;font-size:.94rem;color:#3a3730}
@media(max-width:820px){header{grid-template-columns:minmax(0,1fr)}}
"""
    years = list(range(2009, 2025))
    parts = [
        ("Painting", "oil, mostly on linen", "Painting"),
        ("Printmaking", "intaglio, drypoint", "Printmaking"),
        ("Installation", "floor and wall", "Installation"),
        ("Other", "sculpture, assemblage", None),
    ]
    marks = [
        (2012, "sotto voce"), (2015, "poco a poco"), (2018, "ff"),
        (2019, "meno mosso"), (2021, "ff sempre"), (2024, "cantabile"),
    ]

    def x_for(year):
        return (year - 2009 + 0.5) / len(years) * 100

    b = ['<div class="wrap"><header><div>',
         '<div class="kick">One system · four parts · sixteen bars</div>',
         "<h1>The <em>Score</em></h1></div>",
         "<p>Bar lines are years. Each note is a work: its height on the stave is the work's "
         "measured lightness, its size is its real physical area, its colour is its own "
         "dominant hue. Four parts, one per discipline, because that is how you see two "
         "instruments come in together.</p></header>",
         '<div class="score"><div class="sys">']

    b.append('<div class="marks"><div></div><div>')
    for y, m in marks:
        b.append(f'<i style="left:{x_for(y):.2f}%">{esc(m)}</i>')
    b.append("</div></div>")

    for name, sub, disc in parts:
        if disc:
            ws = [w for w in lib.WORKS if w["discipline"] == disc and w["year"]]
        else:
            ws = [w for w in lib.WORKS
                  if w["discipline"] not in ("Painting", "Printmaking", "Installation")
                  and w["year"]]
        lines = "".join(
            f'<span class="l" style="top:{t}%"></span>' for t in (12, 31, 50, 69, 88)
        )
        notes = []
        # Works from the same year share an x, so a busy year piles into one
        # column. Spread them across the bar the way a score spreads a run of
        # semiquavers — the bar still means the year, but you can see the notes.
        per_bar = defaultdict(list)
        for w in ws:
            per_bar[w["year"]].append(w)
        bar_w = 100 / len(years)
        for year, group in per_bar.items():
            group.sort(key=lambda w: -w["img"]["lig"])
            n = len(group)
            for j, w in enumerate(group):
                im = w["img"]
                spread = 0 if n == 1 else (j / (n - 1) - 0.5) * bar_w * 0.74
                x = x_for(year) + spread
                y = 92 - im["lig"] * 84
                area = (w["h_mm"] or 300) * (w["w_mm"] or 300)
                r = max(4.5, min(math.sqrt(area) / 38, 18))
                col = f"hsl({im['hue']:.0f} {min(im['sat']*150,72):.0f}% {30+im['lig']*42:.0f}%)"
                if im["chroma"] <= 0.06:
                    col = f"hsl(40 5% {26+im['lig']*46:.0f}%)"
                # A note with no recorded measurements is drawn hollow, the way a
                # minim is hollow: present, but not filled in.
                if w["h_mm"]:
                    fill = f"background:{col}"
                else:
                    fill = f"background:transparent;border-color:{col};border-width:2.2px"
                notes.append(
                    f'<a class="note" href="#{esc(w["slug"])}" data-t="{esc(w["title"])}" '
                    f'data-y="· {year}" style="left:{x:.2f}%;top:{y:.1f}%;width:{r*2:.0f}px;'
                    f'height:{r*2:.0f}px;{fill}"></a>'
                )
        b.append(
            f'<div class="part"><div class="pname">{esc(name)}<small>{esc(sub)}</small></div>'
            f'<div class="stave">{lines}{"".join(notes)}</div></div>'
        )

    b.append('<div class="bars"><div></div><div class="barline">')
    for y in years:
        b.append(f"<span>{str(y)[2:]}</span>")
    b.append("</div></div></div></div>")

    b.append(
        '<div class="key"><div><h3>Pitch</h3><p>High on the stave is a light work; low is a '
        "dark one. It is the same measurement the elevation profiles in sheet 36 use, and it "
        "is the only property every work in the catalogue has.</p></div>"
        "<div><h3>Duration and dynamics</h3><p>Notehead size is real physical area. A work "
        "with no recorded measurements is drawn hollow, the way a minim is hollow: present, "
        "but not filled in. Sixty of them, and you can see exactly where in the piece the "
        "archive stops knowing.</p></div>"
        "<div><h3>What it shows</h3><p>2018 and 2021 are the tutti passages. Printmaking "
        "sits low and dark almost throughout — black ink on white rag reads as a bass line. "
        "The 2024 painting run is the highest, lightest phrase in the piece.</p></div>"
        "<div><h3>What it isn't</h3><p>Music. The Italian markings are editorial and they "
        "are the only thing on this page that isn't measured. They stay because a score "
        "without them is a spreadsheet.</p></div></div></div>"
    )
    return lib.write("63-the-score.html", "The Score", css, "".join(b))


# ------------------------------------------------------------------ 64 tide

def sheet_64():
    css = """
:root{--deep:#06131a;--mid:#0d2733;--surf:#dfe9e6;--ink:#e7efec;--dim:#6d8a8c}
body{background:var(--deep);color:var(--ink);font-family:"Cormorant Garamond",Georgia,serif;
 font-size:18px}
.surface{min-height:100svh;display:grid;place-items:center;text-align:center;padding:10vh 7vw;
 background:linear-gradient(180deg,#dfe9e6 0%,#93b3b4 42%,#2c5560 78%,#06131a 100%);
 color:#0d2733}
.surface h1{font-weight:300;font-size:clamp(3rem,11vw,7.4rem);line-height:.92;margin:0 0 .3em;
 letter-spacing:-.02em}
.surface p{max-width:40ch;margin:0 auto;line-height:1.66;font-size:1.1rem;color:#123642}
.surface small{display:block;margin-top:3em;font-family:"IBM Plex Mono",monospace;font-size:10px;
 letter-spacing:.36em;text-transform:uppercase;color:#3c6470}
.col{position:relative}
.band{min-height:86svh;display:grid;place-items:center;padding:8vh 6vw;position:relative}
.band figure{margin:0;max-width:min(760px,86vw);position:relative}
.band img{width:100%;height:auto;display:block}
.band figcaption{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--dim);margin-top:14px;display:flex;flex-wrap:wrap;
 gap:5px 22px;justify-content:space-between}
.band figcaption b{color:var(--ink);font-family:"Cormorant Garamond",serif;font-size:1.2rem;
 letter-spacing:0;text-transform:none;font-weight:400}
.depth{position:absolute;left:22px;top:50%;transform:translateY(-50%);
 font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.2em;color:#2f4a52;
 writing-mode:vertical-rl}
.say{min-height:60svh;display:grid;place-items:center;padding:8vh 8vw;text-align:center}
.say p{max-width:24ch;font-size:clamp(1.5rem,4.4vw,3rem);line-height:1.2;font-weight:300;
 margin:0;color:#9fc3c0;font-style:italic}
.floor{min-height:80svh;display:grid;place-items:center;text-align:center;padding:10vh 7vw;
 background:linear-gradient(180deg,#06131a,#02080b)}
.floor p{max-width:38ch;color:#587a7c;line-height:1.7;margin:0 auto}
.floor a{display:inline-block;margin-top:2.4em;font-family:"IBM Plex Mono",monospace;
 font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:#9fc3c0;
 text-decoration:none;border-bottom:1px solid #2f4a52;padding-bottom:5px}
@media(prefers-reduced-motion:no-preference){
 .band figure{animation:rise linear both;animation-timeline:view();
  animation-range:entry 0% exit 100%}
 @keyframes rise{
  0%{opacity:0;transform:translateY(70px) scale(.965);filter:blur(7px) saturate(.5)}
  32%{opacity:1;transform:none;filter:blur(0) saturate(1)}
  68%{opacity:1;transform:none;filter:blur(0) saturate(1)}
  100%{opacity:0;transform:translateY(-70px) scale(.965);filter:blur(7px) saturate(.5)}}
 .say p{animation:swell linear both;animation-timeline:view();animation-range:entry 10% exit 90%}
 @keyframes swell{0%{opacity:0}40%,60%{opacity:1}100%{opacity:0}}
}
"""
    seq = ["there-once-was-ice-here", "submerged", "deep-sea", "transplanter",
           "tugboat-whale-sequoia", "crystal-tooth-whale", "narwhal",
           "orbits-plankton-dreaming-of-a-sedimentary-afterlife", "molecule"]
    breaths = [
        "Whatever is in the jar is a thing he thinks is running out.",
        "Whales fly before they swim.",
        "Plankton dreaming of a sedimentary afterlife.",
    ]
    b = ['<section class="surface"><div><h1>Tide</h1>'
         "<p>Nine works that live in water, or wish they did. They surface as you come to "
         "them and go under again as you leave. Nothing is lost — it is only below you.</p>"
         "<small>scroll · about three minutes · motion respects your settings</small>"
         "</div></section>",
         '<div class="col">']
    for i, slug in enumerate(seq):
        w = get(slug)
        b.append(
            f'<section class="band"><span class="depth">−{(i+1)*11} m</span>'
            f'<figure><img src="{wide(w)}" alt="{alt(w)}" loading="lazy">'
            f'<figcaption><b>{esc(w["title"])}</b><span>{w["year"]}</span>'
            f'<span>{esc(w["medium"] or w["discipline"])}</span></figcaption></figure></section>'
        )
        if i in (2, 5, 7):
            b.append(f'<section class="say"><p>{esc(breaths[(i//3) % 3])}</p></section>')
    b.append("</div>")
    b.append(
        '<section class="floor"><div><p>The bottom. One hundred and forty-six more works are '
        "up there in the light, catalogued, measured, and considerably easier to find.</p>"
        '<a href="#">archive.kyleparkercunningham.com</a></div></section>'
    )
    return lib.write("64-tide.html", "Tide", css, "".join(b))


# ------------------------------------------------------------- 65 the window

def sheet_65():
    n = 8
    picks = ["above-the-clouds", "the-black-fire", "cyclum-lunarem", "the-mother-bear",
             "solar-ascension", "low-angle-sun-rays", "me-own-juniper", "docile"]
    dur = 8 * 26  # 26 seconds a work; a window is not a slideshow

    keyframes = []
    for i in range(n):
        start = i * 100 / n
        step = 100 / n
        keyframes.append(
            f"@keyframes w{i}{{"
            f"0%,{max(start - 2.2, 0):.2f}%{{opacity:0}}"
            f"{start + 1.6:.2f}%,{start + step - 1.6:.2f}%{{opacity:1}}"
            f"{min(start + step + 2.2, 100):.2f}%,100%{{opacity:0}}}}"
        )
    fades = "".join(keyframes)
    panes = "".join(
        f".p{i}{{animation:w{i} {dur}s linear infinite}}" for i in range(n)
    )

    css = """
:root{--room:#0f0f0e;--ink:#efece4;--dim:#84806f}
body{background:var(--room);color:var(--ink);font-family:"Instrument Serif",Georgia,serif;
 height:100svh;overflow:hidden}
.room{position:fixed;inset:0;display:grid;place-items:center;padding:min(6vh,54px) min(6vw,64px)}
.frame{position:relative;width:100%;height:100%;display:grid;place-items:center}
.pane{position:absolute;inset:0;display:grid;place-items:center;opacity:0}
.pane img{max-width:100%;max-height:100%;width:auto;height:auto;
 box-shadow:0 60px 130px -70px rgba(0,0,0,.95)}
.cap{position:fixed;left:min(6vw,64px);bottom:min(4vh,34px);right:min(6vw,64px);
 display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:6px 26px;
 pointer-events:none}
.cap .slot{position:relative;height:1.5em;flex:1;min-width:0}
.cap .t{position:absolute;left:0;bottom:0;white-space:nowrap;opacity:0;font-size:1.5rem;
 letter-spacing:-.01em}
.cap .m{position:absolute;right:0;bottom:.25em;white-space:nowrap;opacity:0;
 font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.22em;
 text-transform:uppercase;color:var(--dim)}
.hdr{position:fixed;left:min(6vw,64px);top:min(4vh,30px);font-family:"IBM Plex Mono",monospace;
 font-size:10px;letter-spacing:.34em;text-transform:uppercase;color:var(--dim)}
.about{position:fixed;right:min(6vw,64px);top:min(4vh,30px);max-width:26ch;
 font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:11px;line-height:1.7;
 color:var(--dim);text-align:right}
@media(prefers-reduced-motion:reduce){.pane,.cap .t,.cap .m{animation:none!important}
 .p0,.cap .t.c0,.cap .m.c0{opacity:1}}
@media(max-width:700px){.about{display:none}.cap .t{font-size:1.1rem}}
"""
    css += fades + panes
    css += "".join(
        f".cap .t.c{i},.cap .m.c{i}{{animation:w{i} {dur}s linear infinite}}" for i in range(n)
    )

    b = ['<div class="room"><div class="frame">']
    for i, slug in enumerate(picks):
        w = get(slug)
        b.append(
            f'<div class="pane p{i}"><img src="{wide(w)}" alt="{alt(w)}"></div>'
        )
    b.append("</div></div>")
    b.append('<div class="hdr">The Window · Kyle Parker Cunningham</div>')
    b.append(
        '<div class="about">One work at a time, changing every twenty-six seconds. '
        "No grid, no menu, nothing to click. It is a window, and a window does not have "
        "a table of contents.</div>"
    )
    b.append('<div class="cap"><div class="slot">')
    for i, slug in enumerate(picks):
        w = get(slug)
        b.append(f'<span class="t c{i}">{esc(w["title"])}</span>')
    b.append('</div><div class="slot">')
    for i, slug in enumerate(picks):
        w = get(slug)
        d = " · ".join(x for x in [str(w["year"]), w["medium"], dims(w)] if x)
        b.append(f'<span class="m c{i}">{esc(d)}</span>')
    b.append("</div></div>")
    return lib.write("65-the-window.html", "The Window", css, "".join(b))


# -------------------------------------------------------- 66 correspondence

def sheet_66():
    css = """
:root{--paper:#fdfcf7;--ink:#22201b;--dim:#8b8578;--blue:#2c3f6b;--rule:#ded8ca}
body{background:#b6ae9c;color:var(--ink);font-family:"Xanh Mono",Courier,monospace;
 font-size:15px;line-height:1.72;
 background-image:repeating-linear-gradient(45deg,rgba(0,0,0,.025) 0 3px,transparent 3px 7px)}
.desk{max-width:1080px;margin:0 auto;padding:44px 16px 90px;display:grid;
 grid-template-columns:minmax(0,1fr) minmax(0,260px);gap:26px;align-items:start}
.letter{background:var(--paper);padding:clamp(28px,5vw,62px);
 box-shadow:0 24px 60px -34px rgba(0,0,0,.7);position:relative}
.letter::before{content:"";position:absolute;left:0;right:0;top:0;height:6px;
 background:repeating-linear-gradient(90deg,#a83c2c 0 12px,#2c3f6b 12px 24px,
  transparent 24px 34px)}
.head{border-bottom:1px solid var(--rule);padding-bottom:16px;margin-bottom:26px;
 display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px 24px;align-items:flex-end}
.head h1{font-family:"Bodoni Moda",Georgia,serif;font-weight:400;font-size:1.9rem;margin:0;
 letter-spacing:-.01em;line-height:1.05}
.head .adr{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);
 text-align:right;line-height:1.9}
.date{color:var(--dim);font-size:12.5px;letter-spacing:.1em;margin-bottom:22px}
.letter p{margin:0 0 1.15em;max-width:66ch}
.letter p.sal{margin-bottom:1.6em}
.letter em{font-style:italic}
.letter b{font-weight:400;border-bottom:1px solid var(--blue);color:var(--blue)}
.encl{border:1px solid var(--rule);padding:14px 16px;margin:1.8em 0;background:#f7f4ea}
.encl h2{font-size:10.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--dim);
 margin:0 0 12px;font-weight:400}
.encl .row{display:flex;gap:12px;align-items:flex-start;margin-bottom:12px}
.encl img{width:82px;height:82px;object-fit:cover;border:1px solid var(--rule);flex:0 0 auto;
 transform:rotate(-1.2deg);box-shadow:2px 3px 0 rgba(0,0,0,.08)}
.encl .row:nth-child(odd) img{transform:rotate(1deg)}
.encl .txt{font-size:12.5px;line-height:1.62;color:#3a362e}
.encl .txt b{border:0;color:var(--ink);font-weight:400;display:block;
 font-family:"Bodoni Moda",Georgia,serif;font-size:1.05rem}
.sig{margin-top:2.4em;font-family:"Bodoni Moda",Georgia,serif;font-size:1.6rem;
 font-style:italic;color:var(--blue);line-height:1}
.ps{margin-top:2em;border-top:1px solid var(--rule);padding-top:14px;font-size:13px;
 color:#3a362e}
aside{position:sticky;top:26px}
.stamp{background:var(--paper);padding:16px;box-shadow:0 16px 40px -28px rgba(0,0,0,.7);
 text-align:center}
.stamp .sq{border:2px dashed #a83c2c;padding:14px 10px;color:#a83c2c}
.stamp .sq b{display:block;font-family:"Bodoni Moda",serif;font-size:1.5rem;font-weight:400}
.stamp .sq span{font-size:9px;letter-spacing:.22em;text-transform:uppercase}
.stamp p{font-size:10.5px;line-height:1.7;color:var(--dim);margin:12px 0 0;
 letter-spacing:.06em;text-align:left}
@media(max-width:820px){.desk{grid-template-columns:minmax(0,1fr)}aside{position:static}}
"""
    encl = ["the-mother-bear", "bottled-lightning", "me-own-juniper"]
    b = ['<div class="desk"><div class="letter">',
         '<div class="head"><h1>Kyle Parker Cunningham</h1>'
         '<div class="adr">Truth or Consequences<br>New Mexico<br>on the Rio Grande</div></div>',
         '<div class="date">17 August 2026 — somewhere with a satellite signal</div>',
         '<p class="sal">Dear whoever has arrived,</p>',
         "<p>You have found the front of a website, which is a strange thing to find, so let "
         "me tell you what is here and what isn't. Everything I have made and kept — one "
         "hundred and fifty-five objects, with their measurements, their materials, where "
         "they are now and who has them — lives at "
         "<b>archive.kyleparkercunningham.com</b>. That is the real catalogue and it is "
         "better than this page at every factual question you might have.</p>",
         "<p>What is here is me telling you where to look. That is all a front page can "
         "honestly be once the catalogue exists, and I would rather write you a letter than "
         "build you a grid.</p>",
         "<p>This summer the studio has no walls. Jeannie and I are working out of a vehicle "
         "across Wyoming, Montana and Colorado — climbing and painting in the mornings, "
         "swimming the heat off at midday, documenting in the evenings, all of it running on "
         "a satellite signal and a battery. The question underneath it is practical: can the "
         "whole operation be <em>carried</em>?</p>",
         '<div class="encl"><h2>Enclosed, three things</h2>']
    for slug in encl:
        w = get(slug)
        b.append(
            f'<div class="row"><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">'
            f'<div class="txt"><b>{esc(w["title"])}, {w["year"]}</b>'
            f"{esc(sentence(w, 190))}</div></div>"
        )
    b.append("</div>")
    b.append(
        "<p>I have been struck by lightning. I mention it because you will meet a painting "
        "of a jar with lightning in it, and because five years before it happened I made a "
        "print of a man plugged into a wall socket by his own hair. I do not have a theory "
        "about that.</p>"
        "<p>If you want the short way in: there is a route through the junipers that takes "
        "twelve years and six pictures, and a route through the weather that takes two. If "
        "you want the long way, start in 2009 and walk sideways.</p>"
        "<p>Write back if you like. Letters are answered slowly and in order.</p>"
        '<div class="sig">Kyle</div>'
        '<div class="ps"><b style="border:0;color:inherit">P.S.</b> There are two years in '
        "the catalogue with nothing in them at all. I have stopped being embarrassed about "
        "that and started thinking it is the most honest part of the record.</div>"
    )
    b.append("</div>")
    b.append(
        '<aside><div class="stamp"><div class="sq"><b>XIII</b>'
        "<span>season · summer 2026</span></div>"
        "<p>Posted from the road.<br>Contents: one letter, three enclosures, "
        "one forwarding address.<br><br>Return to sender if the studio has moved, "
        "which it has.</p></div></aside></div>"
    )
    return lib.write("66-correspondence.html", "Correspondence", css, "".join(b))


# ---------------------------------------------------------- 67 constellations

def sheet_67():
    css = """
:root{--sky:#05070f;--ink:#e6ecf5;--dim:#5d6b85;--gold:#d8c48a}
body{background:var(--sky);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;
 background-image:radial-gradient(ellipse at 30% 0%,#101a33 0%,transparent 58%),
  radial-gradient(ellipse at 80% 90%,#0d1626 0%,transparent 55%)}
.wrap{max-width:1240px;margin:0 auto;padding:0 22px 90px}
header{padding:60px 0 18px;max-width:58ch}
.kick{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.38em;
 text-transform:uppercase;color:var(--gold)}
h1{font-family:"Cormorant Garamond",Georgia,serif;font-weight:300;
 font-size:clamp(2.8rem,8.4vw,5.6rem);line-height:.95;margin:.14em 0 .22em;letter-spacing:-.01em}
header p{color:#9aa8bf;line-height:1.7;margin:0;font-size:1rem}
header p b{color:var(--ink);font-weight:500}
.chart{margin-top:26px;border:1px solid #16203a;background:rgba(6,10,20,.55)}
.chart svg{display:block;width:100%;height:auto}
.star{cursor:pointer}
.star circle{transition:r .2s ease}
.star:hover circle{r:6}
.star text{opacity:0;transition:opacity .18s;font-family:"IBM Plex Mono",monospace;
 font-size:7px;letter-spacing:.1em;fill:#e6ecf5}
.star:hover text{opacity:1}
.legend{display:flex;flex-wrap:wrap;gap:10px 30px;margin-top:14px;
 font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.22em;
 text-transform:uppercase;color:var(--dim)}
.asters{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:24px;
 margin-top:52px;border-top:1px solid #16203a;padding-top:26px}
.ast h2{font-family:"Cormorant Garamond",Georgia,serif;font-weight:400;font-size:1.5rem;
 margin:0 0 4px;color:var(--gold)}
.ast .n{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.2em;
 text-transform:uppercase;color:var(--dim);margin-bottom:10px}
.ast p{margin:0 0 10px;color:#9aa8bf;line-height:1.66;font-size:.92rem}
.ast .row{display:flex;gap:4px;flex-wrap:wrap}
.ast img{width:44px;height:44px;object-fit:cover;opacity:.82}
.ast img:hover{opacity:1}
"""
    ASTERISMS = [
        ("The Gear", "animist solarpunk", "#7fd4c1",
         "The largest constellation in the sky and the one everything else is navigated by."),
        ("The Weather", "the memory of atmosphere", "#8fb6e8",
         "New, and tight: every star in it was made within two years of the others, low in the north."),
        ("The Ring", "circle", "#e8c98f",
         "Faint but never absent — visible in every year since 2015."),
        ("Deep Time", "deep time", "#c9a0d8",
         "Old light. The stars in it are the oldest things he paints."),
        ("The Jar", "glass jar", "#8fe0a8",
         "A small, recent, anxious cluster."),
        ("The Ridge", "new mexico", "#e89a8f",
         "The ground constellation. Everything that names the place he lives."),
    ]
    W, H = 1180, 660
    pos = {}
    for w in lib.WORKS:
        if not w["year"]:
            continue
        # right ascension = year, declination = measured lightness; magnitude = area
        x = 44 + (w["year"] - 2009) / 15 * (W - 88)
        y = H - 40 - w["img"]["lig"] * (H - 96)
        # spread works sharing a year so they don't stack into a line
        jitter = (hash(w["slug"]) % 1000) / 1000
        x += (jitter - 0.5) * 44
        y += ((hash(w["slug"] + "y") % 1000) / 1000 - 0.5) * 26
        pos[w["slug"]] = (x, y)

    svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="every work plotted by year '
           'and measured lightness, with tag constellations drawn between them">']
    for gy in range(0, 6):
        y = 40 + gy * (H - 80) / 5
        svg.append(f'<line x1="34" y1="{y:.0f}" x2="{W-34}" y2="{y:.0f}" '
                   f'stroke="#131d33" stroke-width=".7"/>')
    for yr in range(2009, 2025, 3):
        x = 44 + (yr - 2009) / 15 * (W - 88)
        svg.append(f'<line x1="{x:.0f}" y1="30" x2="{x:.0f}" y2="{H-30}" '
                   f'stroke="#131d33" stroke-width=".7"/>')
        svg.append(f'<text x="{x:.0f}" y="{H-12}" font-size="9" fill="#5d6b85" '
                   f'text-anchor="middle" font-family="monospace">{yr}</text>')

    # asterism lines first, so the stars sit on top
    for name, tag, colour, note in ASTERISMS:
        ws = sorted([w for w in tagged(tag) if w["slug"] in pos],
                    key=lambda w: pos[w["slug"]][0])
        if len(ws) < 2:
            continue
        pts = " ".join(f"{pos[w['slug']][0]:.1f},{pos[w['slug']][1]:.1f}" for w in ws)
        svg.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" '
                   f'stroke-width="1" opacity=".38"/>')

    for w in lib.WORKS:
        if w["slug"] not in pos:
            continue
        x, y = pos[w["slug"]]
        area = (w["h_mm"] or 260) * (w["w_mm"] or 260)
        r = max(1.4, min(math.sqrt(area) / 150, 4.4))
        im = w["img"]
        col = (f"hsl({im['hue']:.0f} {min(im['sat']*120,55):.0f}% {66+im['lig']*22:.0f}%)"
               if im["chroma"] > 0.06 else "#dfe6f2")
        svg.append(
            f'<g class="star"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" '
            f'opacity=".92"/><title>{esc(w["title"])} · {w["year"]}</title>'
            f'<text x="{x+7:.1f}" y="{y+3:.1f}">{esc(w["title"])}</text></g>'
        )
    svg.append("</svg>")

    b = ['<div class="wrap"><header>',
         '<div class="kick">Star chart · 155 bodies · epoch 2009–2024</div>',
         "<h1>Constellations</h1>",
         "<p>A tag is not a filing category. It is a line somebody drew between things that "
         "are nowhere near each other. <b>That is exactly what a constellation is</b> — "
         "unrelated stars at wildly different distances, joined because a person on the "
         "ground needed a way to find them again. Here the sky is real: right ascension is "
         "the year a work was made, declination is its measured lightness, and magnitude is "
         "its physical size. The lines are the tags.</p></header>",
         f'<div class="chart">{"".join(svg)}</div>',
         '<div class="legend"><span>x = year</span><span>y = measured lightness</span>'
         "<span>size = physical area</span><span>colour = dominant hue</span>"
         "<span>hover a star for its name</span></div>",
         '<div class="asters">']
    for name, tag, colour, note in ASTERISMS:
        ws = [w for w in tagged(tag) if w["slug"] in pos]
        b.append(
            f'<div class="ast"><h2 style="color:{colour}">{esc(name)}</h2>'
            f'<div class="n">{len(ws)} stars · {esc(tag)}</div><p>{esc(note)}</p>'
            f'<div class="row">'
            + "".join(f'<img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">' for w in ws[:8])
            + "</div></div>"
        )
    b.append("</div></div>")
    return lib.write("67-constellations.html", "Constellations", css, "".join(b))


# ------------------------------------------------------------- 68 the sieve

def sheet_68():
    disciplines = sorted({w["discipline"] for w in lib.WORKS})
    decades = [("2009-2014", 2009, 2014), ("2015-2019", 2015, 2019),
               ("2020-2024", 2020, 2024)]
    hues = [("warm", lambda w: w["img"]["chroma"] > .06 and (w["img"]["hue"] < 70 or w["img"]["hue"] > 330)),
            ("green", lambda w: w["img"]["chroma"] > .06 and 70 <= w["img"]["hue"] < 165),
            ("cool", lambda w: w["img"]["chroma"] > .06 and 165 <= w["img"]["hue"] <= 330),
            ("neutral", lambda w: w["img"]["chroma"] <= .06)]
    sizes = [("held", lambda w: w["h_mm"] and max(w["h_mm"], w["w_mm"]) < 300),
             ("reach", lambda w: w["h_mm"] and 300 <= max(w["h_mm"], w["w_mm"]) < 600),
             ("wall", lambda w: w["h_mm"] and max(w["h_mm"], w["w_mm"]) >= 600),
             ("unmeasured", lambda w: not w["h_mm"])]

    groups = [
        ("disc", "Discipline", [(d.lower().replace(" ", "-"), d,
                                 sum(1 for w in lib.WORKS if w["discipline"] == d))
                                for d in disciplines]),
        ("dec", "When", [(k.replace("-", "_"), k,
                          sum(1 for w in lib.WORKS if w["year"] and lo <= w["year"] <= hi))
                         for k, lo, hi in decades]),
        ("hue", "Colour", [(k, k, sum(1 for w in lib.WORKS if f(w))) for k, f in hues]),
        ("size", "Size", [(k, k, sum(1 for w in lib.WORKS if f(w))) for k, f in sizes]),
    ]

    rules = []
    for gid, _, opts in groups:
        for key, _, _ in opts:
            rules.append(f"body:has(#{gid}-{key}:checked) .w:not(.{gid}-{key}){{display:none}}")

    css = """
:root{--bg:#101012;--panel:#17171a;--ink:#f0eee9;--dim:#85817a;--hot:#e2543a;--line:#26262a}
body{background:var(--bg);color:var(--ink);font-family:"Space Grotesk",system-ui,sans-serif;
 font-size:15px}
.wrap{max-width:1400px;margin:0 auto;padding:0 22px 90px}
header{padding:54px 0 22px;max-width:60ch}
.kick{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:.34em;
 text-transform:uppercase;color:var(--hot)}
h1{font-weight:700;font-size:clamp(2.6rem,8vw,5.4rem);line-height:.9;margin:.12em 0 .22em;
 letter-spacing:-.045em}
header p{color:#a5a099;line-height:1.66;margin:0}
header p b{color:var(--ink);font-weight:500}
.rig{display:grid;grid-template-columns:minmax(0,250px) minmax(0,1fr);gap:26px;
 margin-top:34px;align-items:start}
.panel{background:var(--panel);border:1px solid var(--line);padding:16px 16px 18px;
 position:sticky;top:16px}
.grp{border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:14px}
.grp:last-of-type{border-bottom:0;margin-bottom:0}
.grp h2{font-family:"Space Mono",monospace;font-size:9.5px;letter-spacing:.26em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:0 0 9px}
.grp label{display:flex;justify-content:space-between;align-items:baseline;gap:10px;
 padding:4px 7px;cursor:pointer;font-size:13px;border-radius:2px}
.grp label:hover{background:#202024}
.grp label span{font-family:"Space Mono",monospace;font-size:10.5px;color:var(--dim)}
.grp input{position:absolute;opacity:0;pointer-events:none}
.grp input:checked+label{background:var(--hot);color:#141210}
.grp input:checked+label span{color:rgba(20,18,16,.72)}
.reset{display:block;text-align:center;margin-top:14px;font-family:"Space Mono",monospace;
 font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--dim);
 border:1px solid var(--line);padding:8px;cursor:pointer;border-radius:2px}
.reset:hover{border-color:var(--hot);color:var(--hot)}
.results{min-width:0}
.bar{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 22px;
 font-family:"Space Mono",monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;
 color:var(--dim);border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(124px,1fr));gap:12px}
.w{text-decoration:none;color:inherit;display:block}
.w img{width:100%;aspect-ratio:1;object-fit:cover;background:#1c1c20}
.w b{display:block;font-size:11.5px;font-weight:500;margin-top:6px;line-height:1.3}
.w span{display:block;font-family:"Space Mono",monospace;font-size:9.5px;color:var(--dim);
 margin-top:2px;letter-spacing:.08em}
.empty{display:none;color:var(--dim);padding:40px 0;font-family:"Space Mono",monospace;
 font-size:12px}
.results:not(:has(.w:not([style*="none"]))) .empty{display:block}
.note{margin-top:34px;border-top:1px solid var(--line);padding-top:18px;
 display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px}
.note h3{font-family:"Space Mono",monospace;font-size:9.5px;letter-spacing:.24em;
 text-transform:uppercase;color:var(--dim);font-weight:400;margin:0 0 7px}
.note p{margin:0;color:#a5a099;line-height:1.7;font-size:.92rem}
.note code{font-family:"Space Mono",monospace;font-size:11px;color:var(--hot)}
@media(max-width:820px){.rig{grid-template-columns:minmax(0,1fr)}.panel{position:static}}
"""
    css += "\n".join(rules)

    def classes(w):
        cl = [f"disc-{w['discipline'].lower().replace(' ', '-')}"]
        for k, lo, hi in decades:
            if w["year"] and lo <= w["year"] <= hi:
                cl.append("dec-" + k.replace("-", "_"))
        for k, f in hues:
            if f(w):
                cl.append("hue-" + k)
        for k, f in sizes:
            if f(w):
                cl.append("size-" + k)
        return " ".join(cl)

    b = ['<div class="wrap"><header>',
         '<div class="kick">Zero javascript · four facets · 155 works</div>',
         "<h1>The Sieve</h1>",
         "<p>The archive has a search box; it should. What a front page can offer instead is "
         "<b>sifting</b> — grabbing the whole catalogue and shaking it until something falls "
         "through. Every control below is a radio input and a CSS <code>:has()</code> rule. "
         "It filters for real, it works with the browser back button off and the network "
         "gone, and it will still work in twenty years.</p></header>",
         '<div class="rig"><form class="panel">']

    for gid, label, opts in groups:
        b.append(f'<div class="grp"><h2>{esc(label)}</h2>')
        b.append(f'<input type="radio" name="{gid}" id="{gid}-all" checked>'
                 f'<label for="{gid}-all">any<span>{len(lib.WORKS)}</span></label>')
        for key, name, count in opts:
            b.append(
                f'<input type="radio" name="{gid}" id="{gid}-{key}">'
                f'<label for="{gid}-{key}">{esc(name)}<span>{count}</span></label>'
            )
        b.append("</div>")
    b.append('<label class="reset" for="disc-all">clear discipline</label></form>')

    b.append(
        '<div class="results"><div class="bar"><span>the whole catalogue, sifted</span>'
        "<span>counts are totals per facet</span></div>"
        '<div class="grid">'
    )
    for w in by_hue(lib.WORKS):
        b.append(
            f'<a class="w {classes(w)}" href="#{esc(w["slug"])}">'
            f'<img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">'
            f'<b>{esc(w["title"])}</b><span>{w["year"]} · {esc(w["discipline"].lower())}</span></a>'
        )
    b.append('</div><div class="empty">Nothing passes all four. Loosen one.</div></div></div>')

    b.append(
        '<div class="note"><div><h3>How it works</h3><p>Each facet is one radio group with an '
        "“any” default. One generated rule per option: "
        "<code>body:has(#hue-cool:checked) .w:not(.hue-cool){display:none}</code>. Four "
        "groups compose as AND for free, because each rule only ever hides.</p></div>"
        "<div><h3>Why radios and not checkboxes</h3><p>Honesty. Multi-select needs OR inside "
        "a group, and pure CSS can only express that by enumerating every subset. Radios give "
        "you a correct, tiny, permanent filter; checkboxes would need a line of JavaScript "
        "and I would rather show you the version that never breaks.</p></div>"
        "<div><h3>Where it hands off</h3><p>Four facets is a sieve, not a query language. "
        "The moment you want <i>drypoint, 2018, still available, under 300mm</i>, that is "
        "the archive's job, and it is one link away.</p></div>"
        "<div><h3>The honest gap</h3><p>The counts are totals per facet, computed at build "
        "time — they do not update as you sift, because a static page can't count what it "
        "just hid. Live counts are the one thing here worth spending JavaScript on.</p></div>"
        "</div></div>"
    )
    return lib.write("68-the-sieve.html", "The Sieve", css, "".join(b))


# -------------------------------------------------------------- 69 the guide

def sheet_69():
    css = """
:root{--bg:#f7f4ef;--bg2:#efe9e1;--ink:#1e1a16;--muted:#6a6258;--accent:#1f3f5b;
 --line:#e2dbd1}
body{background:var(--bg);color:var(--ink);font-family:"Literata",Georgia,serif;
 font-size:18px;line-height:1.7}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.mast{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;
 gap:10px 26px;padding:22px 0 14px;border-bottom:1px solid var(--line)}
.mast .name{font-size:1.06rem;letter-spacing:.01em}
.mast nav{display:flex;flex-wrap:wrap;gap:4px 20px;font-family:"IBM Plex Sans",system-ui,
 sans-serif;font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.mast nav a{text-decoration:none}
.mast nav a:hover{color:var(--accent)}
.hero{padding:64px 0 20px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,340px);
 gap:44px;align-items:end}
h1{font-weight:300;font-size:clamp(2.6rem,7.2vw,4.8rem);line-height:1;letter-spacing:-.022em;
 margin:0 0 .28em}
.hero p{margin:0;color:#3f382f;font-size:1.06rem}
.hero p b{font-weight:600}
.handoff{background:var(--bg2);border-left:3px solid var(--accent);padding:16px 18px;
 font-family:"IBM Plex Sans",sans-serif;font-size:.86rem;line-height:1.65;color:#4a4238}
.handoff b{display:block;font-family:"Literata",serif;font-size:1.06rem;color:var(--ink);
 font-weight:600;margin-bottom:5px}
.handoff a{color:var(--accent)}
h2{font-family:"IBM Plex Sans",sans-serif;font-size:.74rem;letter-spacing:.28em;
 text-transform:uppercase;color:var(--muted);font-weight:500;margin:66px 0 16px;
 padding-bottom:8px;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;
 justify-content:space-between;gap:6px 20px}
h2 em{font-style:normal;color:#948b7e}
.season{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:34px;
 align-items:start}
.season img{width:100%;height:auto;max-height:min(66vh,560px);object-fit:cover;
 object-position:center 38%}
.numeral{font-size:.74rem;letter-spacing:.28em;text-transform:uppercase;color:var(--accent);
 font-family:"IBM Plex Sans",sans-serif}
.season h3{font-weight:300;font-size:clamp(1.7rem,3.6vw,2.6rem);line-height:1.08;
 margin:.16em 0 .3em;letter-spacing:-.015em}
.season .deck{color:#3f382f;font-size:1rem}
.season .life{font-family:"IBM Plex Sans",sans-serif;font-size:.78rem;letter-spacing:.14em;
 text-transform:uppercase;color:var(--muted);border-top:1px solid var(--line);
 padding-top:10px;margin-top:16px}
.routes{display:grid;grid-template-columns:repeat(auto-fit,minmax(268px,1fr));gap:26px}
.route{text-decoration:none;color:inherit;display:block;border-top:2px solid var(--ink);
 padding-top:12px}
.route:hover h3{color:var(--accent)}
.route .strip{display:flex;gap:3px;margin-bottom:11px}
.route .strip img{flex:1;min-width:0;aspect-ratio:1;object-fit:cover}
.route h3{font-weight:400;font-size:1.32rem;margin:0 0 .2em;line-height:1.18}
.route .meta{font-family:"IBM Plex Sans",sans-serif;font-size:.74rem;letter-spacing:.14em;
 text-transform:uppercase;color:var(--muted)}
.route p{font-size:.94rem;line-height:1.6;color:#4a4238;margin:.6em 0 0}
.pairrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:30px}
.pr{display:grid;grid-template-columns:1fr auto 1fr;gap:12px;align-items:center}
.pr img{width:100%;aspect-ratio:1;object-fit:cover}
.pr .yrs{font-family:"IBM Plex Sans",sans-serif;font-size:.7rem;letter-spacing:.14em;
 text-transform:uppercase;color:var(--accent);writing-mode:vertical-rl;text-align:center}
.prcap{font-family:"IBM Plex Sans",sans-serif;font-size:.76rem;letter-spacing:.06em;
 color:var(--muted);margin-top:9px;line-height:1.55}
.prcap b{color:var(--ink);font-family:"Literata",serif;font-size:.95rem;font-weight:400;
 letter-spacing:0}
.spectrum{display:flex;height:76px;gap:1px;margin-bottom:10px}
.spectrum a{flex:1;min-width:0;display:block}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:34px}
.two p{margin:0 0 1em;font-size:1rem}
.ledger{width:100%;border-collapse:collapse;font-family:"IBM Plex Sans",sans-serif;
 font-size:.86rem}
.ledger th{text-align:left;font-weight:500;font-size:.68rem;letter-spacing:.2em;
 text-transform:uppercase;color:var(--muted);padding:0 12px 8px 0;
 border-bottom:1px solid var(--ink)}
.ledger td{padding:8px 12px 8px 0;border-bottom:1px solid var(--line);vertical-align:middle}
.ledger img{width:38px;height:38px;object-fit:cover}
.ledger .n{font-family:"Inconsolata","IBM Plex Mono",monospace;color:var(--muted);
 font-size:.8rem}
footer{margin-top:80px;border-top:1px solid var(--line);padding:26px 0 70px;
 display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:26px;
 font-family:"IBM Plex Sans",sans-serif;font-size:.82rem;color:var(--muted)}
footer h4{font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;margin:0 0 8px;
 color:var(--ink);font-weight:500}
footer a{display:block;text-decoration:none;line-height:2}
footer a:hover{color:var(--accent)}
@media(max-width:880px){.hero,.season{grid-template-columns:minmax(0,1fr);gap:26px}}
"""
    ROUTES = [
        ("The Juniper Trail", "6 works · 2012–2022 · a decade",
         "One tree, drawn again and again. The route to take if you want to understand "
         "patience as a subject rather than a virtue.",
         ["me-own-juniper", "alligator-juniper", "alligator-juniper-nogal", "transplanter"]),
        ("Survival Notes", "28 works · 2014–2023 · the long one",
         "Animals in breathing apparatus, machines grazing, mutual aid by airship. Neither "
         "utopia nor collapse — a lot of improvised gear.",
         ["bonsai-giant-sequoia", "paper-neck-giraffes", "rhino-radar", "there-once-was-ice-here"]),
        ("The Memory of Atmosphere", "12 works · 2023–2024 · newest",
         "Lightning kept in a jar, water vapour solved as algebra, the sky with the ground "
         "taken out from under it.",
         ["bottled-lightning", "the-algebra-of-water-vapor", "towers", "the-river-in-the-sky"]),
    ]
    season = get("bindery-at-dusk") if "bindery-at-dusk" in lib.BY_SLUG else get("absolute-potential") if "absolute-potential" in lib.BY_SLUG else get("out-there-on-the-horizon-a-solitary-cloud")
    pairs = revisits()[:2]
    recent = [w for w in lib.WORKS if w["year"] and w["year"] >= 2024][:8]

    b = ['<div class="wrap">',
         '<div class="mast"><span class="name">Kyle Parker Cunningham</span>'
         '<nav><a href="#">Season XIII</a><a href="#">Routes</a><a href="#">Cinema</a>'
         '<a href="#">Press</a><a href="#">About</a>'
         '<a href="#" style="color:#1f3f5b">The Archive ↗</a></nav></div>',
         '<div class="hero"><div><h1>Start anywhere.<br>I will tell you where it goes.</h1>'
         "<p>This is not the catalogue. <b>The catalogue is at "
         "archive.kyleparkercunningham.com</b> — every work, every measurement, every "
         "provenance line, and it is much better than this page at answering a question. "
         "This page is for the other thing: a small number of marked routes through fifteen "
         "years of work, and one season that is happening right now.</p></div>"
         '<div class="handoff"><b>Looking for something specific?</b>'
         "155 public records, 476 subject terms, full-text search, and every field the "
         'catalogue holds. <a href="#">Go straight to the archive →</a></div></div>']

    b.append(
        "<h2><span>The season</span><em>opens at the solstice, retires at the equinox</em></h2>"
        f'<div class="season"><img src="{wide(season)}" alt="{alt(season)}" loading="lazy">'
        '<div><div class="numeral">Season XIII · Summer 2026</div>'
        "<h3>Everything That<br>Can Be Carried</h3>"
        '<p class="deck">The studio loses its walls. A summer spent finding out whether the '
        "whole operation — paintings, a press, a bindery — can be carried, and keep working "
        "from anywhere. Filed under <i>Survival Notes from the Near Future</i>.</p>"
        '<div class="life">Lives June — September 2026 · on the road · '
        "Wyoming, Montana, Colorado</div></div></div>"
    )

    b.append('<h2><span>Three routes through the work</span><em>pick one · 5–15 minutes</em></h2>'
             '<div class="routes">')
    for name, meta, note, slugs in ROUTES:
        ws = many(*slugs)
        b.append(
            f'<a class="route" href="#"><div class="strip">'
            + "".join(f'<img src="{thumb(w)}" alt="{alt(w)}" loading="lazy">' for w in ws)
            + f'</div><h3>{esc(name)}</h3><div class="meta">{esc(meta)}</div>'
            f"<p>{esc(note)}</p></a>"
        )
    b.append("</div>")

    b.append(
        "<h2><span>What he came back to</span><em>28 pairs in the catalogue</em></h2>"
        '<div class="pairrow">'
    )
    for a, c, delta in pairs:
        b.append(
            f'<div><div class="pr"><img src="{thumb(a)}" alt="{alt(a)}" loading="lazy">'
            f'<span class="yrs">{delta} years</span>'
            f'<img src="{thumb(c)}" alt="{alt(c)}" loading="lazy"></div>'
            f'<div class="prcap"><b>{esc(a["title"])}</b>, {a["year"]} '
            f'{esc(a["discipline"].lower())} → <b>{esc(c["title"])}</b>, {c["year"]} '
            f'{esc(c["discipline"].lower())}</div></div>'
        )
    b.append("</div>")

    b.append(
        "<h2><span>The whole catalogue, by colour</span>"
        "<em>155 works · measured, not chosen</em></h2>"
        '<div class="spectrum">'
    )
    for w in by_hue(lib.WORKS):
        im = w["img"]
        col = (f"hsl({im['hue']:.0f} {min(im['sat']*140,66):.0f}% {28+im['lig']*46:.0f}%)"
               if im["chroma"] > 0.06 else f"hsl(38 5% {26+im['lig']*48:.0f}%)")
        b.append(f'<a href="#{esc(w["slug"])}" title="{alt(w)}" '
                 f'style="background:{col}"></a>')
    b.append("</div>")
    b.append(
        '<div class="two"><p>Ordered by the dominant hue measured off each photograph. It is '
        "the single cheapest thing the archive gives away and the most surprising: the "
        "practice is one continuous spectrum, heavy in ochre and teal, thin in violet.</p>"
        "<p>Every band is a link into the archive's own facets. The site suggests; the "
        "catalogue answers.</p></div>"
    )

    b.append(
        "<h2><span>Most recent</span><em>2024 · newest first</em></h2>"
        '<table class="ledger"><thead><tr><th></th><th>Work</th><th>Discipline</th>'
        "<th>Medium</th><th>Size</th></tr></thead><tbody>"
    )
    for i, w in enumerate(recent, 1):
        b.append(
            f'<tr><td><img src="{thumb(w)}" alt="{alt(w)}" loading="lazy"></td>'
            f'<td>{esc(w["title"])} <span class="n">{w["year"]}</span></td>'
            f'<td>{esc(w["discipline"])}</td><td>{esc(w["medium"] or "—")}</td>'
            f'<td class="n">{esc(dims(w) or "—")}</td></tr>'
        )
    b.append("</tbody></table>"
             '<p style="font-family:\'IBM Plex Sans\',sans-serif;font-size:.78rem;'
             'letter-spacing:.06em;color:#6a6258;margin:10px 0 0">— in the size column means not yet measured. Sixty of the hundred and fifty-five are still unmeasured, and the ledger says so rather than leaving the column out.</p>')

    b.append(
        '<footer><div><h4>Routes</h4><a href="#">The Juniper Trail</a>'
        '<a href="#">Survival Notes</a><a href="#">The Memory of Atmosphere</a>'
        '<a href="#">The Circle Route</a><a href="#">Truth or Consequences</a></div>'
        '<div><h4>The studio</h4><a href="#">Season XIII</a><a href="#">Past seasons</a>'
        '<a href="#">Field log</a><a href="#">Agile Meteor Press</a></div>'
        '<div><h4>About</h4><a href="#">Biography</a><a href="#">Statement</a>'
        '<a href="#">Press kit</a><a href="#">Contact</a></div>'
        '<div><h4>The archive</h4><a href="#">All 155 works ↗</a><a href="#">Search ↗</a>'
        '<a href="#">Subject terms ↗</a><a href="#">Colophon</a></div></footer></div>'
    )
    return lib.write("69-the-guide.html", "Kyle Parker Cunningham", css, "".join(b))


def main():
    for fn in (sheet_63, sheet_64, sheet_65, sheet_66, sheet_67, sheet_68, sheet_69):
        print(fn())


if __name__ == "__main__":
    import sheets

    for s in sheets.SHEETS:
        lib.register(*s)
    main()
