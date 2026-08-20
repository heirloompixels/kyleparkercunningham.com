# Sketchbook — new directions for kyleparkercunningham.com

Started 17 August 2026. Thirty-four sheets, numbered 36–69, continuing from
the existing `mockups/` run. Open `mockups/index.html` for the contact sheet;
every sheet also carries a switcher in its bottom-right corner.

---

## The premise everything here starts from

**archive.kyleparkercunningham.com now exists.** That changes what this site
is for, completely.

The archive is the catalogue raisonné: 295 works, 159 public, every record,
every measurement, provenance, condition, valuation, exhibition history, a
476-term controlled vocabulary. It answers *what exists*. It is a database
and it should look and behave like one.

Which means this site no longer has to be one — and the old brief ("a
definitive, lifelong, searchable archive of all works", `SPEC.md` §1) is now
being served twice. The interesting question is what the front-facing site
becomes once it is relieved of the duty to be comprehensive.

My answer, and the spine of all thirty-four sheets:

> **The archive holds the works. The site holds the routes through them.**

An archive without routes is a warehouse. Every sheet in here is an attempt
at a route — a reason to look at this next, and this after that. Some are
literal (marked trails, a docent, a dichotomous key). Some are structural
(hue, scale, lightfastness, the years he didn't work). Some are objects (a
card drawer, a contact sheet, a folded broadsheet). One is just a window.

Two consequences worth stating plainly:

1. **Completeness stops being a virtue here.** A sheet that shows 7 works
   well beats one that shows 155 badly. The 155 are one click away and always
   will be.
2. **The site can now be opinionated.** The archive must be neutral —
   catalogues are. This site can argue.

---

## The material I found

Before drawing anything I pulled the archive apart to see what it actually
holds, because the data *is* the design material here. Findings, in rough
order of usefulness:

| Found | Size | What it's good for |
|---|---|---|
| `dominant_hex` + `palette_json` on every image | 226/226 | sorting the oeuvre by colour; a chromatic index |
| Pigment table with **CI codes and Blue Wool lightfastness** | 54 pigments | which works will fade — see sheet 42 |
| `oeuvre_related` — motif returned to years later | 28 pairs | the strongest narrative structure in the archive |
| Real dimensions in mm | 95 works, 127mm → 1308mm | true-scale comparison; nobody knows how big these are |
| Controlled tag vocabulary | 476 tags | *animist solarpunk* (28), *the memory of atmosphere* (12), *deep time* (14) |
| `blurhash` + `pixel_grid_key` on every image | 226 | image-free browsing |
| Year distribution | 2010 and 2011 are **empty** | the fallow years — sheet 47 |

Two things I did not use and want to flag: **valuations** (108 rows) and
`private_note` are in the archive and are nobody's business but Kyle's — I
kept every price out of every sheet. And `created_place` is only filled on
eight works, all of them 2026 watercolours with no photograph yet, so the
map-shaped ideas I wanted to try (where each work was made; where each work
now lives) have nothing to stand on. **That is a metadata gap worth filling**
— it would unlock a genuinely good sheet.

I also computed things the archive doesn't store, locally from the pixels:
average hue/saturation/lightness per work, and a 6×6 average-colour grid.
Those drive sheets 41, 44, 45 and the elevation profiles in 36.

---

## Round one — sheets 36–40, the route idea taken literally

**36 Trailhead.** Routes as marked trails, with distance, grade, and an
elevation profile. **37 Field Guide.** A dichotomous key to the creatures —
*does it wear a breathing apparatus?* **38 The Docent.** One voice, seven
works, nine minutes. **39 Field Station.** The fieldwork/seasons idea rebuilt
as a research station's status board. **40 The Long Walk.** All 155 works on
one horizontal line, 2009 to 2024.

### What I learned

**Derived data is flat until you stretch it.** The first elevation profiles
in 36 were drawn from raw measured lightness and every route came out as the
same near-horizontal line, because lightness across the whole oeuvre lives in
a narrow band. Normalising each route to its own min and max turned them into
five distinctly-shaped ridgelines. The general rule: *global* scales flatten,
*local* scales reveal. Worth remembering for every data sheet after this.

**Decorative data reads as a lie.** Sheet 39's dial started as a scatter of
dots placed by `random()` — it looked like a chart, so it claimed to mean
something, and it meant nothing. I replaced it with angle = the work's real
measured hue, radius = its year. It is now both honest and better: you can
watch the palette rotate outward from earth tones into blue across fifteen
years. **Rule adopted: no ornament shaped like a chart.** If it looks like
data it has to be data.

**A background on a scroll container needs `background-attachment: local`.**
Sheet 40's sky was meant to run dawn→noon→dusk→night across the whole
fifteen-year walk. By default the gradient painted itself across the viewport
instead and just sat there. One property turns a static backdrop into a sky
you actually walk through. This is now the best thing on that sheet.

**Self-host the fonts.** I pulled all eighteen families into
`mockups/assets/fonts/`. A mockup that has to phone Google to look right is
not a mockup you can hand somebody on a plane, and half of what these sheets
are testing *is* the typography.

**Horizontal is underused.** 40 is the least conventional layout in the batch
and took the least code. Time is a line; we keep folding it into a grid for
no reason.

### What I'm carrying forward

- Routes want a **grade** — some indication of how much work looking will be.
  It made 36 feel generous rather than bossy.
- Field-guide voice ("note that the apparatus is always hand-made, never
  sleek") is the most natural register I've found for writing about this
  work. It's specific without being reverent.
- Every sheet should say what it *doesn't* do, and point at the archive for
  the rest. Confidence about scope reads better than pretending to be total.

---

## Round two — sheets 41–47, the archive's own data made visible

**41 Chromatic Index.** All 155 works ordered around the colour wheel.
**42 Fugitive.** Which pigments outlive the painter. **43 True Scale.** Every
measured work at its real size, on one wall, with a person in it. **44 Deep
Time.** The practice as a stratigraphic column. **45 The Quilt.** No
photographs — only the 6×6 colour grids. **46 Weather Log.** *The memory of
atmosphere* read as a meteorological record. **47 Fallow.** The years with
nothing in them.

### What I learned

**Fill the shape with its own colour; don't stack a palette in it.** 41's
spectrum band first drew each work as its five palette swatches stacked
vertically. 155 of those side by side is a barcode — no sweep, no order, and
the sort I'd spent effort on became invisible. Refilling each strip with the
work's single measured mean colour, and demoting the palette to a 16px footer,
turned it into an actual spectrum you can read left to right. **A sorted set
has to be able to show its sort at a glance or the sort was for nothing.**

**Vertical register is a promise you have to keep.** 44 was a three-column
grid: year / proportional bed / note. The bed heights are honest — one work,
one unit — so a year with 0 works is a 16px sliver, and its note is four
lines. Everything below drifted out of alignment. Fixed by splitting the
proportional column off as its own self-contained figure and letting the notes
run underneath at reading pace. **Don't mix a measured column and a written
column in the same rows.** One of them will lie.

**A scale factor wants to be a unitless variable.** 43 hangs everything at one
scale, and at 0.3 px/mm the largest painting is 392px — four pixels wider than
a phone. Hard-coding pixels meant either overflowing or lying about scale.
Making it `--s: .30` and sizing every work with `calc(var(--s) * 813px)` means
one media query rescales the entire wall and **every ratio stays exact.**

**The gaps are the best content in the catalogue.** 47 is the sheet I'd fight
for. 2010 and 2011 hold nothing, and an object-record has no way to say why —
so the page says that, at the same size as the years that have work in them.
It also catches its own mistake out loud: 2017 looks nearly empty at three
catalogue entries, and one of those is *Cyclum Lunarem*, which is 365 nights of
painting. **Counting works is a bad proxy for working, and every artist site
that draws an output bar chart is quietly making that mistake.**

**Label the simulation.** 42's fade frames are a CSS filter, not a
measurement — the archive knows which pigments are in the studio but not which
went into which work. Saying so in a box on the page made it stronger: it turns
an illustration into a specific, costed request for the one piece of metadata
that would make it real.

**Sheets that expose a metadata gap are more useful than sheets that hide
one.** 43 can only hang the 95 works that have been measured, and says the
other 60 are missing. 42 says what it can't yet forecast. That reads as
rigour, and it converts `TODO.md` from a chore list into an argument for
something you can already see the shape of.

### Carried forward

- Every derived number needs a one-line note on the page saying how it was
  derived. It costs 12 words and it's the difference between a chart and a
  claim.
- Dark ground (41, 45) suits the colour work; warm paper (44, 47) suits the
  time work. Not a house style — a per-sheet argument.
- 45 has **zero bytes of imagery** and is still legible as this specific
  practice. Worth remembering when the phone-in-a-canyon case comes up.

---

## Round three — sheets 48–55, the site as a physical object

**48 Card Catalogue.** A drawer of typed cards. **49 Contact Sheet.** The whole
roll, with grease-pencil marks. **50 The Loom.** Warp of years, weft of
motifs. **51 The Press.** Plate, state, proof, edition. **52 Herbarium.** Works
as pressed specimens with determination labels. **53 The Fold.** A broadsheet
that unfolds. **54 Wunderkammer.** One dense cabinet. **55 Terminal.** The
oeuvre over a serial line.

### What I learned

**The loom is the best structural finding in the whole sketchbook.** Twenty
motifs down, sixteen years across, each cell filled with the real colour of
the work that picked that thread up. It makes visible the one thing no other
view could: a motif drops out for six years and comes back. *Juniper* runs
2012 → 2016 → 2018 → 2020 → 2022. *Whale* starts in the air and returns as a
boat. My first version drew the dropped years as a faint red block and it read
as noise; drawing them as a **dotted line at the vertical centre of the row** —
the thread still on the loom, waiting — made the whole grid legible in one
pass. Small change, completely different page.

**The constraint is the content.** 48 works because a catalogue card holds
about forty words, so somebody has to choose which forty. 55 works because
it's text only. 49 works because a contact sheet shows the frames that didn't
come off. In each case the *limit* is what makes it say something — which the
infinite-scroll grid, by design, never does.

**Marks should come from the data, not from taste.** 49's grease-pencil
circles are not my opinion about which works are good. A circle means the
archive records that work being returned to in a later year; a cross means a
low-saturation print; a crop rectangle means it belongs to a standing
investigation. Deriving the editorial marks from the catalogue's own relations
means the page can be regenerated and stays true.

**A picture made of text needs enough characters.** 55's ASCII plates started
from the stored 6×6 colour grid and were unreadable — 12 characters wide is
not a picture. Re-sampling each work's own thumbnail at 34 columns, squashed
2:1 for terminal cell aspect and contrast-stretched per work, made *the mother
bear* recognisable in monospace. Then I had to go back and fix the footnote,
which still described the old method — **a derived-data note is a claim, and
it goes stale when you change the derivation.**

**A sizing multiplier beats a media query full of magic numbers.** 54's
cabinet hangs works at real relative scale; on a phone that pushed the page
sideways. One `--z` multiplier consumed by every `calc()` shrinks the whole
cabinet without touching a single ratio. Same trick as 43. This is now the
third time it's come up — it should just be the house pattern.

---

## Round four — sheets 56–69, time, lineage, experiment, synthesis

**56 Almanac.** The seasons idea, fully grown. **57 Lunarem.** Twenty-eight
works, one per phase. **58 The Day.** Dawn to dark. **59 Ephemeris.** The
archive as an astronomical table. **60 The Return.** The revisit pairs, side by
side. **61 Motif Atlas.** Every elephant, every ensō. **62 Genealogy.** Works
with descendants. **63 The Score.** The oeuvre as notation. **64 Tide.**
Surfacing and going under. **65 The Window.** One painting, all day.
**66 Correspondence.** A letter. **67 Constellations.** Tags as a night sky.
**68 The Sieve.** A working, JavaScript-free faceted filter.
**69 The Guide.** Everything learned, in the site's existing design language.

### What I learned

**Make the device reveal the work, not cover it.** 57's moons started as
opaque discs sitting on top of each painting — a nice icon that hid the thing
it was labelling. Inverting it so the disc is an *aperture*, with the work
visible only where the moon is lit, is the single best move in this round. At
new moon you get nothing; at full you get the whole crop; the works are
ordered by their own measured luminance, so no editorial hand places them.
**A decoration laid over the work is almost always an aperture drawn
backwards.**

**Almanac beats edition.** An edition is a magazine issue — it opens, runs,
retires. An almanac assumes you'll come back and tells you what to expect
before it happens. The practice already runs on solstices and equinoxes; 56
just shows the whole ring at once, so a visitor in February can see that
August is lightning and December is gold leaf. That is a reason to return
that a live-issue homepage structurally cannot give.

**Same x means a pile.** 63's noteheads all sit at their year, so a
twenty-five-work year became one unreadable column. Spreading them across
their own bar — the way a score spreads a run of semiquavers — keeps the bar
meaning the year and makes the chord readable. Then the hollow-notehead idea
(a work with no recorded measurements is drawn hollow, like a minim) turned
a missing-data problem into notation.

**`:has()` gives you a real filter with no JavaScript — if you use radios.**
68 filters 155 works across four facets and composes them as AND: 155 → 46
printmaking → 29 in the 2020s → 16 near-neutral → 6 held-size. Each rule is
just `body:has(#hue-cool:checked) .w:not(.hue-cool){display:none}`. Multi-select
would need OR *within* a group, which pure CSS can only express by enumerating
every subset — so radios, and say why on the page. The one thing genuinely
worth spending script on is **live counts**, because a static page can't count
what it just hid.

**Prose that hard-codes a number will disagree with the data eventually.**
61's copy said "nine works" for the space helmet while the plate counted eight
(nine are tagged; one has no photograph). Both were right and the page looked
wrong. Rule: **either the number comes from the data or the sentence doesn't
have a number in it.**

**A column of em-dashes reads as a bug unless the page explains it.** 69's
ledger shows "—" in the size column for every 2024 work, because none of them
are measured yet. One line underneath turns it from broken into a statement.

---

## Where I'd take this

If Kyle only reads one section, this one.

**The premise held up.** Thirty-four sheets in, I'm more convinced than at the
start: with the archive live, this site's job is *routes*, and the sheets that
commit hardest to that are the strongest. The sheets I would build:

1. **69 The Guide** as the actual homepage. It is the existing design language
   — same palette, same three faces — restructured around three routes, a live
   season, the return-pairs, and an explicit hand-off to the archive. Nobody
   has to re-learn the site, and it stops competing with the catalogue.
2. **50 The Loom** as the one big interactive page. It is the only view that
   shows the shape of the practice, it is genuinely novel, and every cell is
   already a link.
3. **60 The Return** and **61 Motif Atlas** as the route pages the Guide links
   to. Both are built entirely from `oeuvre_related` and the tag vocabulary —
   no new content required.
4. **56 Almanac** to replace the edition shelf, or sit above it.
5. **47 Fallow** as an About-adjacent page. It is the most honest page here and
   the only one that says something an artist site normally hides.

**Three sheets are worth keeping as one-offs**, not as system: 45 The Quilt
(loads on one bar of signal, zero image bytes), 55 Terminal (the 40 KB version
of the whole catalogue), 65 The Window (a screen for the studio wall).

**What the archive should add, in order of how much it would unlock:**

- **Per-work pigment links.** 42 Fugitive is currently a simulation. With
  `oeuvre_work_pigments` filled in, it becomes a real permanence forecast per
  work — something no other artist's site has, and something a collector would
  actually use.
- **Dimensions for the remaining 60.** 43 True Scale, 63 The Score and 54
  Wunderkammer all degrade gracefully but visibly without them.
- **Typed relations.** The schema supports `pendant / study / reworked /
  series`, and every one of the 28 relations is currently typed `other`. Typing
  them would make 62 Genealogy draw itself.
- **`created_place` / provenance coordinates.** Only 8 works carry a place, all
  of them 2026 watercolours with no photograph. Two of the best sheets I
  *couldn't* make were a map of where each work was made and a map of where
  each work now lives. That is the biggest single gap.

**One thing I'd resist.** Several of these sheets are gorgeous and would be
miserable to maintain — 35 The Reel from the last run, 64 Tide, 58 The Day.
Composing a season shouldn't mean art-directing a sequence four times a year,
forever. The seasons only survived thirteen issues because composing one is
writing, not designing. Keep that.

---

## Notes on the build

- `mockups/index.html` is the contact sheet — every sheet with a live preview,
  grouped by family. Not one of the thirty-four.
- `mockups/_build/` holds the machinery: `prepare.py` (joins the archive dump
  to the images in `content/` and computes the colour analysis),
  `fetch_fonts.py`, `lib.py`, `gen1`–`gen5`, `gen_index.py`, and `shoot.py`,
  which screenshots every sheet at 1440 and 390 and reports horizontal
  overflow, broken images and console errors. All 34 pass clean at both widths.
- **Fonts are now self-hosted for the whole `mockups/` directory**, not just
  the new sheets. The earlier 40 files linked Google Fonts and rendered in
  fallback faces offline; they now point at `assets/fonts/fonts.css`. Eighteen
  families, 2.85 MB, and nothing in the folder needs a network any more.
- Imagery: 155 works derived to WebP at 1280px and 420px, 23 MB total, from
  the originals already in `content/oeuvre/`.
- **No prices anywhere.** The archive holds 108 valuations and a private note
  per work; none of it appears on any sheet. A public route through the work
  does not need to know what anything sold for.
- One pre-existing bug turned up while sweeping: `30-inner-chrome.html` pushed
  19px sideways at 390px, because its ledger table had no `table-layout: fixed`.
  Fixed. Every file in `mockups/` now passes the sweep at 1440 and 390.
