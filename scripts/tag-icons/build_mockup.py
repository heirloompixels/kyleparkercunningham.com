#!/usr/bin/env python3
"""Build the icon-picking sheet: every candidate icon, inlined, choosable.

Design tokens are lifted from sass/style.scss so the sheet reads as the site it is
for — warm off-white ground, warm near-black ink, deep slate accent, zero radius.
Everything is inline: no CDN, no webfont, no external request.

If scripts/tag-icons/picks.tsv exists, its choices are pre-selected in the sheet, so
a second round starts from where the last one finished.

Output goes to .icon-sets/tag-icons.html (gitignored — it's ~2.4 MB of inline SVG).

Usage:  python3 scripts/tag-icons/build_mockup.py
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts" / "tagging"))

from aliases import AXIS, AXIS_ORDER, PALETTE, SET_LABEL, SETS   # noqa: E402
from match import candidates, tag_counts                          # noqa: E402

OUT = ROOT / ".icon-sets" / "tag-icons.html"
PICKS = HERE / "picks.tsv"
MAX_OPTIONS = 12
HEX_BLACK = re.compile(r'(stroke|fill)="#(?:000|000000)"', re.I)


def svg(opt, px=30):
    body, mode, vb = opt["body"], opt["mode"], opt["viewBox"]
    if opt["set"] == "openmoji-black":
        body = HEX_BLACK.sub(r'\1="currentColor"', body)
        attrs = 'fill="currentColor"'
    elif opt["set"] == "openmoji-color":
        attrs = ""
    elif mode == "stroke":
        attrs = ('fill="none" stroke="currentColor" stroke-width="1.75" '
                 'stroke-linecap="round" stroke-linejoin="round"')
    else:
        attrs = 'fill="currentColor"'
    return (f'<svg viewBox="{vb}" width="{px}" height="{px}" {attrs} '
            f'aria-hidden="true" focusable="false">{body}</svg>')


def load_picks():
    if not PICKS.exists():
        return {}
    out = {}
    for line in PICKS.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("\t") if p.strip()]
        if len(parts) >= 3:
            out[parts[0]] = {"set": parts[1], "name": parts[2]}
    return out


counts = tag_counts()
picks = load_picks()

rows, total_opts = [], 0
for tag, n in counts.most_common():
    if tag in PALETTE or tag not in AXIS:
        continue
    opts = candidates(tag)[:MAX_OPTIONS]
    if not opts:
        continue
    rows.append((tag, n, AXIS[tag], opts))
    total_opts += len(opts)
rows.sort(key=lambda r: (AXIS_ORDER.index(r[2]), -r[1], r[0]))

covered = {r[0] for r in rows} | set(PALETTE)
gaps = sorted(((n, t) for t, n in counts.items() if t not in covered), reverse=True)
styles_used = sorted({o["set"] for _, _, _, opts in rows for o in opts})

P = []
w = P.append

w(f"""<title>Tag icons — options to pick from</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{
  --bg:#f7f4ef; --panel:#efe9e1; --ink:#1e1a16; --muted:#6a6258;
  --line:#e2dbd1; --accent:#1f3f5b; --accent-ink:#f7f4ef;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --sans:ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}}
@media (prefers-color-scheme:dark) {{
  :root {{ --bg:#17140f; --panel:#1f1b16; --ink:#f0ebe3; --muted:#9a9083;
           --line:#332c24; --accent:#7ba7cd; --accent-ink:#12100c; }}
}}
:root[data-theme="dark"] {{ --bg:#17140f; --panel:#1f1b16; --ink:#f0ebe3; --muted:#9a9083;
  --line:#332c24; --accent:#7ba7cd; --accent-ink:#12100c; }}
:root[data-theme="light"] {{ --bg:#f7f4ef; --panel:#efe9e1; --ink:#1e1a16; --muted:#6a6258;
  --line:#e2dbd1; --accent:#1f3f5b; --accent-ink:#f7f4ef; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:var(--sans);
  font-size:15px; line-height:1.5; -webkit-font-smoothing:antialiased; }}
.wrap {{ max-width:1180px; margin:0 auto; padding:0 20px 140px; }}
h1 {{ font-family:var(--serif); font-weight:600; font-size:clamp(1.7rem,1.2rem+2vw,2.5rem);
  margin:0; letter-spacing:-.01em; text-wrap:balance; }}
h2 {{ font-family:var(--serif); font-weight:600; font-size:1.35rem; margin:0; }}
.lede {{ color:var(--muted); max-width:62ch; margin:.7rem 0 0; }}
header.top {{ padding:52px 0 26px; border-bottom:1px solid var(--line); }}
.eyebrow {{ font-family:var(--mono); font-size:.68rem; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted); margin:0 0 .9rem; }}
.stats {{ display:flex; flex-wrap:wrap; gap:0 26px; margin-top:20px;
  font-family:var(--mono); font-size:.74rem; letter-spacing:.04em; color:var(--muted);
  font-variant-numeric:tabular-nums; }}
.stats b {{ color:var(--ink); font-weight:600; }}
.bar {{ position:sticky; top:0; z-index:20; background:var(--bg);
  border-bottom:1px solid var(--line); padding:11px 0; margin-bottom:8px;
  display:flex; flex-wrap:wrap; gap:8px; align-items:center; }}
.bar .grp {{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; }}
.lbl {{ font-family:var(--mono); font-size:.64rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--muted); margin-right:2px; }}
button.f {{ font:inherit; font-size:.78rem; padding:4px 10px; background:transparent;
  color:var(--muted); border:1px solid var(--line); border-radius:0; cursor:pointer; }}
button.f:hover {{ color:var(--ink); border-color:var(--muted); }}
button.f[aria-pressed="true"] {{ background:var(--accent); color:var(--accent-ink);
  border-color:var(--accent); }}
button.f:focus-visible, .opt:focus-visible {{ outline:2px solid var(--accent);
  outline-offset:2px; }}
.axis {{ font-family:var(--mono); font-size:.68rem; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted); padding:34px 0 10px;
  border-bottom:1px solid var(--line); }}
.row {{ display:grid; grid-template-columns:172px 1fr; gap:18px; padding:14px 0;
  border-bottom:1px solid var(--line); align-items:start; }}
@media (max-width:720px) {{ .row {{ grid-template-columns:1fr; gap:8px; }} }}
.tagname {{ font-family:var(--serif); font-size:1.02rem; line-height:1.25;
  position:sticky; top:66px; }}
.tagmeta {{ font-family:var(--mono); font-size:.66rem; letter-spacing:.07em;
  color:var(--muted); margin-top:3px; font-variant-numeric:tabular-nums; }}
.opts {{ display:flex; flex-wrap:wrap; gap:5px; }}
.opt {{ width:70px; padding:9px 3px 5px; background:transparent; border:1px solid transparent;
  border-radius:0; cursor:pointer; display:flex; flex-direction:column; align-items:center;
  gap:6px; color:var(--ink); font:inherit; }}
.opt:hover {{ background:var(--panel); border-color:var(--line); }}
.opt[aria-pressed="true"] {{ border-color:var(--accent); background:var(--panel);
  box-shadow:inset 0 -3px 0 var(--accent); }}
.opt .src {{ font-family:var(--mono); font-size:.55rem; letter-spacing:.05em;
  color:var(--muted); text-align:center; line-height:1.25; word-break:break-word; }}
.opt[aria-pressed="true"] .src {{ color:var(--accent); }}
.swatches {{ display:flex; flex-wrap:wrap; gap:14px; margin-top:18px; }}
.sw {{ width:78px; text-align:center; }}
.sw i {{ display:block; width:100%; height:44px; border:1px solid var(--line); }}
.sw span {{ font-family:var(--mono); font-size:.6rem; color:var(--muted);
  display:block; margin-top:5px; letter-spacing:.04em; }}
section.block {{ padding:38px 0 0; }}
.note {{ background:var(--panel); border-left:2px solid var(--accent); padding:14px 18px;
  margin:18px 0 0; max-width:70ch; }}
.note p {{ margin:0 0 .6rem; }} .note p:last-child {{ margin:0; }}
table.lic {{ border-collapse:collapse; width:100%; margin-top:16px; font-size:.82rem; }}
table.lic th, table.lic td {{ text-align:left; padding:7px 10px 7px 0;
  border-bottom:1px solid var(--line); }}
table.lic th {{ font-family:var(--mono); font-size:.64rem; letter-spacing:.13em;
  text-transform:uppercase; color:var(--muted); font-weight:400; }}
table.lic td.n {{ font-family:var(--mono); font-size:.76rem;
  font-variant-numeric:tabular-nums; color:var(--muted); }}
.gaps {{ display:flex; flex-wrap:wrap; gap:5px; margin-top:14px; }}
.gaps span {{ font-family:var(--mono); font-size:.7rem; color:var(--muted);
  border:1px solid var(--line); padding:2px 7px; }}
.dock {{ position:fixed; left:0; right:0; bottom:0; z-index:30; background:var(--panel);
  border-top:1px solid var(--line); padding:11px 20px; display:flex; gap:14px;
  align-items:center; justify-content:center; flex-wrap:wrap; }}
.dock .count {{ font-family:var(--mono); font-size:.76rem; color:var(--muted);
  font-variant-numeric:tabular-nums; }}
.dock .count b {{ color:var(--ink); }}
button.act {{ font:inherit; font-size:.8rem; padding:6px 14px; border-radius:0;
  border:1px solid var(--accent); background:var(--accent); color:var(--accent-ink);
  cursor:pointer; }}
button.act.ghost {{ background:transparent; color:var(--ink); border-color:var(--line); }}
button.act:hover {{ filter:brightness(1.08); }}
.hidden {{ display:none !important; }}
@media (prefers-reduced-motion:reduce) {{ * {{ transition:none !important; }} }}
</style>

<div class="wrap">
<header class="top">
  <p class="eyebrow">Oeuvre tags · icon sourcing</p>
  <h1>Pick the icons</h1>
  <p class="lede">Every candidate below is an open-source icon, matched by hand to a tag
  and inlined here at its real size. Click one per tag to choose it; your picks are kept
  in this browser. When you're done, <b>Copy picks</b> hands back a list I can act on.</p>
  <div class="stats">
    <span><b>{len(rows)}</b> tags</span>
    <span><b>{total_opts:,}</b> options</span>
    <span><b>{len(styles_used)}</b> styles</span>
    <span><b>{len(gaps)}</b> tags with no candidate</span>
    {f'<span><b>{len(picks)}</b> already picked</span>' if picks else ''}
  </div>
</header>

<div class="bar">
  <span class="lbl">Style</span>
  <div class="grp" id="styleFilters">
    <button class="f" data-style="all" aria-pressed="true">All</button>
    <button class="f" data-style="line" aria-pressed="false">Line only</button>
    <button class="f" data-style="flat" aria-pressed="false">Flat only</button>
    <button class="f" data-style="emoji" aria-pressed="false">Emoji only</button>
  </div>
  <span class="lbl" style="margin-left:14px">Size</span>
  <div class="grp" id="sizeFilters">
    <button class="f" data-size="30" aria-pressed="true">30</button>
    <button class="f" data-size="22" aria-pressed="false">22</button>
    <button class="f" data-size="44" aria-pressed="false">44</button>
  </div>
  <div class="grp" style="margin-left:auto">
    <button class="f" id="themeBtn" aria-pressed="false">Dark</button>
    <button class="f" id="onlyPicked" aria-pressed="false">Show picked only</button>
  </div>
</div>
""")

cur_axis = None
for tag, count, axis, opts in rows:
    if axis != cur_axis:
        cur_axis = axis
        w(f'<div class="axis">{html.escape(axis)}</div>\n')
    w(f'<div class="row" data-tag="{html.escape(tag)}">'
      f'<div><div class="tagname">{html.escape(tag)}</div>'
      f'<div class="tagmeta">{count} work{"" if count == 1 else "s"}</div></div>'
      f'<div class="opts">')
    for o in opts:
        style = ("emoji" if o["set"].startswith("openmoji")
                 else "flat" if o["style"] == "flat" else "line")
        label = SET_LABEL.get(o["set"], o["set"])
        w(f'<button class="opt" data-style="{style}" data-set="{o["set"]}" '
          f'data-name="{html.escape(o["name"])}" aria-pressed="false" '
          f'title="{html.escape(label)} · {html.escape(o["name"])}">'
          f'<span class="ic">{svg(o)}</span>'
          f'<span class="src">{html.escape(label)}</span></button>')
    w('</div></div>\n')

w('<section class="block"><h2>Colour tags want swatches, not icons</h2>')
w(f'<p class="lede">{len(PALETTE)} of the tags are colours. No icon set has a candidate '
  'for them, and none should — a colour is best drawn as itself. These are the palette '
  'tags as flat chips, sampled from the works they appear on.</p><div class="swatches">')
for name, hexv in PALETTE.items():
    if name in counts:
        w(f'<div class="sw"><i style="background:{hexv}"></i>'
          f'<span>{html.escape(name)} {counts[name]}</span></div>')
w('</div></section>')

w(f'<section class="block"><h2>No candidate yet — {len(gaps)} tags</h2>'
  '<p class="lede">Nothing in the indexed sets matched these. Most are abstractions '
  '("surreal", "mind") or surface descriptions ("scumbled ground") that may simply never '
  'want an icon. A handful — the specific junipers, the clovis point — are the real case '
  'for commissioning custom drawings later.</p><div class="gaps">')
for n, t in gaps[:90]:
    w(f'<span>{html.escape(t)} <b>{n}</b></span>')
w('</div></section>')

w('<section class="block"><h2>Where these come from</h2>'
  '<p class="lede">Every set is open source; licences are read from each package by '
  '<code>fetch_sets.py</code>, which flags drift rather than trusting this table. Nine are '
  'permissive and need nothing but a credit line. OpenMoji is the exception.</p>'
  '<table class="lic"><thead><tr><th>Set</th><th>Licence</th><th>Obligation</th>'
  '</tr></thead><tbody>')
for _pkg, (label, licence, obligation) in SETS.items():
    w(f'<tr><td>{html.escape(label)}</td><td>{html.escape(licence)}</td>'
      f'<td>{html.escape(obligation)}</td></tr>')
w('</tbody></table>')
w('<div class="note"><p><b>The OpenMoji question.</b> It is the only set here with real '
  'strings: CC-BY-SA-4.0 wants attribution <em>and</em> share-alike, which means any icon '
  'you adapt from it has to be released under the same licence. That is fine for a credit '
  'in the colophon and untouched icons; it is a poor foundation if these become the basis '
  'of your own drawn set later. It is also the only source with a bear, an owl and a '
  'narwhal — so it fills exactly the gaps the UI sets leave.</p>'
  '<p>My read: use it to decide what an icon <em>should be</em>, then redraw. '
  'Everything else here can ship as-is with a line in the colophon.</p></div></section>')

seed = ("{" + ",".join(
    f'{html.escape(k)!r}:{{"set":"{v["set"]}","name":{v["name"]!r}}}'.replace("'", '"')
    for k, v in picks.items()) + "}") if picks else "{}"

w(f"""
</div>
<div class="dock">
  <span class="count"><b id="nPicked">0</b> of <span id="nTags">0</span> tags picked</span>
  <button class="act" id="copyBtn">Copy picks</button>
  <button class="act ghost" id="clearBtn">Clear</button>
</div>
<script>
(function(){{
  var KEY='kpc-tag-icons-v1';
  var SEED={seed};
  var picks={{}}; try{{picks=JSON.parse(localStorage.getItem(KEY)||'null')||SEED;}}catch(e){{picks=SEED;}}
  var rows=[].slice.call(document.querySelectorAll('.row'));
  document.getElementById('nTags').textContent=rows.length;

  function persist(){{ try{{localStorage.setItem(KEY,JSON.stringify(picks));}}catch(e){{}} }}
  function tally(){{ document.getElementById('nPicked').textContent=Object.keys(picks).length; }}

  rows.forEach(function(row){{
    var tag=row.dataset.tag;
    row.querySelectorAll('.opt').forEach(function(btn){{
      if(picks[tag] && picks[tag].set===btn.dataset.set && picks[tag].name===btn.dataset.name){{
        btn.setAttribute('aria-pressed','true');
      }}
      btn.addEventListener('click',function(){{
        var on=btn.getAttribute('aria-pressed')==='true';
        row.querySelectorAll('.opt').forEach(function(b){{b.setAttribute('aria-pressed','false');}});
        if(on){{ delete picks[tag]; }}
        else {{ btn.setAttribute('aria-pressed','true');
               picks[tag]={{set:btn.dataset.set,name:btn.dataset.name}}; }}
        persist(); tally(); applyPicked();
      }});
    }});
  }});
  tally();

  var styleMode='all';
  document.getElementById('styleFilters').addEventListener('click',function(e){{
    var b=e.target.closest('button'); if(!b) return;
    styleMode=b.dataset.style;
    this.querySelectorAll('button').forEach(function(x){{
      x.setAttribute('aria-pressed', String(x===b)); }});
    document.querySelectorAll('.opt').forEach(function(o){{
      o.classList.toggle('hidden', styleMode!=='all' && o.dataset.style!==styleMode); }});
  }});

  document.getElementById('sizeFilters').addEventListener('click',function(e){{
    var b=e.target.closest('button'); if(!b) return;
    var px=b.dataset.size;
    this.querySelectorAll('button').forEach(function(x){{
      x.setAttribute('aria-pressed', String(x===b)); }});
    document.querySelectorAll('.opt svg').forEach(function(s){{
      s.setAttribute('width',px); s.setAttribute('height',px); }});
    document.querySelectorAll('.opt').forEach(function(o){{
      o.style.width=(Math.max(70, (+px)+34))+'px'; }});
  }});

  var onlyPicked=false;
  function applyPicked(){{
    rows.forEach(function(r){{
      r.classList.toggle('hidden', onlyPicked && !picks[r.dataset.tag]);
      if(onlyPicked){{
        r.querySelectorAll('.opt').forEach(function(o){{
          o.classList.toggle('hidden', o.getAttribute('aria-pressed')!=='true'); }});
      }} else {{
        r.querySelectorAll('.opt').forEach(function(o){{
          o.classList.toggle('hidden', styleMode!=='all' && o.dataset.style!==styleMode); }});
      }}
    }});
  }}
  document.getElementById('onlyPicked').addEventListener('click',function(){{
    onlyPicked=!onlyPicked; this.setAttribute('aria-pressed',String(onlyPicked));
    this.textContent = onlyPicked ? 'Show all' : 'Show picked only';
    applyPicked();
  }});

  document.getElementById('themeBtn').addEventListener('click',function(){{
    var dark=document.documentElement.getAttribute('data-theme')==='dark';
    document.documentElement.setAttribute('data-theme', dark?'light':'dark');
    this.setAttribute('aria-pressed',String(!dark));
    this.textContent = dark ? 'Dark' : 'Light';
  }});

  document.getElementById('clearBtn').addEventListener('click',function(){{
    if(!confirm('Clear every pick?')) return;
    picks={{}}; persist(); tally();
    document.querySelectorAll('.opt').forEach(function(o){{o.setAttribute('aria-pressed','false');}});
    applyPicked();
  }});

  document.getElementById('copyBtn').addEventListener('click',function(){{
    var keys=Object.keys(picks).sort();
    var btn=this;
    if(!keys.length){{ btn.textContent='Nothing picked yet';
      setTimeout(function(){{btn.textContent='Copy picks';}},1600); return; }}
    var out=keys.map(function(k){{ return k+'\\t'+picks[k].set+'\\t'+picks[k].name; }}).join('\\n');
    var txt='# scripts/tag-icons/picks.tsv — tag\\tset\\ticon ('+keys.length+')\\n'+out+'\\n';
    navigator.clipboard.writeText(txt).then(function(){{
      btn.textContent='Copied '+keys.length; setTimeout(function(){{btn.textContent='Copy picks';}},1600);
    }},function(){{
      var ta=document.createElement('textarea'); ta.value=txt; document.body.appendChild(ta);
      ta.select(); document.execCommand('copy'); ta.remove();
      btn.textContent='Copied '+keys.length; setTimeout(function(){{btn.textContent='Copy picks';}},1600);
    }});
  }});
}})();
</script>
""")

OUT.parent.mkdir(exist_ok=True)
OUT.write_text("".join(P), encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)}  ({OUT.stat().st_size / 1048576:.2f} MB)")
print(f"  {len(rows)} tags · {total_opts:,} options · {len(styles_used)} styles · "
      f"{len(gaps)} gaps" + (f" · {len(picks)} pre-picked" if picks else ""))
