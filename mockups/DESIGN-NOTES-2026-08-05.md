# Five directions — 5 August 2026

Mockups **31–35**. Each direction is two linked pages: a homepage and one
real work page from the Oeuvre. Every page is a single self-contained HTML
file; all imagery is real work pulled from `content/`; all prose is real —
the artist's own words, edition copy, project statements, log entries. No
placeholder text anywhere.

A fixed switcher sits in the bottom-right of every mockup so you can jump
between directions and between each direction's two pages.

| # | Direction | Home | Work page shown |
|---|-----------|------|-----------------|
| 31 | The Ledger | `31-the-ledger-home.html` | *the mother bear*, 2021 |
| 32 | The Specimen | `32-the-specimen-home.html` | *Cyclum Lunarem*, 2017 |
| 33 | The Index | `33-the-index-home.html` | *the river in the sky*, 2024 |
| 34 | The Wall | `34-the-wall-home.html` | *The Black Fire*, 2022 |
| 35 | The Reel | `35-the-reel-home.html` | *Once Creatures Existed*, 2022 |

All ten hold at 1440px and at 390px. Nothing scrolls horizontally at
either width, and every page was checked in a real browser at both.

---

## 31 — The Ledger

*Evolution of what exists.*

**Thesis.** The current design is already right: a masthead, a living
edition on the front, a catalogue underneath, a colophon at the foot. What
it lacks is discipline. This direction changes no ideas and no colours — it
imposes one measure for prose, one rail for marginalia, one real ledger for
the archive, and a vertical rhythm that doesn't guess. Same palette
(`#f7f4ef` / `#1e1a16` / `#1f3f5b`), same three faces (Literata, IBM Plex
Sans, Inconsolata), same spine.

**What changed, concretely.**

- The edition's numeral, title, deck and lead plate resolve into one
  *standfirst* block instead of floating separately (mockup 29 had the
  numeral hanging with nothing to hold it).
- Prose is locked to a 62ch measure with a **marginalia rail** at
  ≥940px carrying datelines, log links and studio notes. Below that the
  rail folds into a bordered aside above the paragraph it annotates,
  rather than vanishing.
- The two-column "recent works" list from 29 becomes an actual **ledger
  table** — number, work, discipline, medium, year — that restacks into
  labelled rows on phone instead of squeezing five columns into 390px.
- The work page's tombstone stops being a run-on sentence and becomes a
  four-cell record strip; the story keeps its measure with the particulars
  (discipline, year, subjects, place, how to cite) sticky in the rail.

**Optimises for.** Continuity. Kyle can ship this without re-teaching
anyone the site, and every existing template maps onto it one-to-one.

**Gives up.** Surprise. Nobody will describe this as a new site — it is
the same site, executed better. If the goal is to make people look twice,
this is not the one.

**Draws from.** 29 (edition lead + expanded footer + big typographic
menu), 30 (compact masthead, crumb, ledger-lite table), 04 *working index*,
02 *catalogue raisonné*. It is essentially 29 + 30 unified and tightened.

---

## 32 — The Specimen

*The site as a printed object.*

**Thesis.** Kyle runs a press. Agile Meteor Press binds books, prints
covers and sets *The Periodic*; the summer's conceptual engine is two
hand-bound first editions. A website for that practice shouldn't merely
look "editorial" — it should be *set*. So this one is: a nameplate with
rules over it, a dateline bar carrying volume and season, justified
multi-column text with column rules and a jump line, plates numbered inside
gatherings, a real **type specimen** panel, a contents page in place of a
nav bar, an imprint, and a folio at the foot of every page. The
navigation is a table of contents with page numbers, because in a book
that's what navigation is.

**Look.** Uncoated newsprint (`#e9e3d6`) with a paper tooth rendered in
CSS, a second run in vermillion (`#b0301b`), Bodoni Moda for display, EB
Garamond for text, Inconsolata for slugs and folios. Every image sits in a
ruled frame; the work page opens with a full plate and a **tissue-guard
caption** under it.

**Optimises for.** Reading, and identity. It says *a person who makes
physical things made this* before you have read a word. It also gives the
long prose pages (bio, artist statement, the Meaning Is Use essays) a home
that actually flatters them.

**Gives up.** Speed of scanning, and a certain kind of contemporary-art
neutrality. Justified columns are lovely at 1440px and a compromise at
390px — they unjustify below 600px and drop to a single column, which is
correct but does mean the phone experience is a different creature from the
desktop one. Also: a four-column newspaper grid is a commitment. Adding a
new content type later means finding it a place in the book.

**Draws from.** 09 *season issue*, 12 *colophon*, 17 *nameplate issue*,
18 *the issue*, 21 *cover plate*. It takes the direction those were
circling and stops hedging.

---

## 33 — The Index

*The site as an archive you query.*

**Thesis.** `SPEC.md` states the core value plainly: "comprehensive,
precise, searchable records per work, built to last decades." This
direction takes that literally and makes the finding aid the front door.
There is **no hero image**. The first things on the homepage are a query
box and the facet counts: discipline (93 painting / 47 printmaking / 8
installation…), year, medium, status, and *has* — photograph, prose,
dimensions, in a project, reworked. Below them, a dense results table with
40px thumbnails and monospace record IDs.

The facets toggle for real (checkbox + label, zero JavaScript). The
curated-threads idea from `TODO.md` §4 appears here as **saved queries** —
"Animals wearing the future", "Painted, then scribed", "Returned to, years
later" — which is a thread *and* an executable filter.

The work page is a **record**: image pane on one side, the complete
universal schema on the other, including the fields that are empty, marked
`unrecorded` rather than hidden. At the bottom, the record exactly as it is
stored on disk, with a short note on why that matters for a fifty-year
archive.

**Optimises for.** Collectors, researchers, and Kyle's own retrieval. It
is the only one of the five that answers "do you have anything from 2018 in
drypoint that's still available" in one screen. It also makes the archive's
gaps visible — the completeness bars say out loud that 12 of 160 records
carry a collection status — which turns `TODO.md`'s unfinished metadata
into a feature instead of an embarrassment.

**Gives up.** Warmth, and the paintings' scale. Thumbnails are 40px. A
first-time visitor meets a table, not a picture — which is a real risk for
an artist's site and the strongest argument against this direction. It also
writes a cheque the build has to cash: honest facet counts mean the
metadata backfill in `TODO.md` §2 stops being optional.

**Draws from.** 15 *system archive*, 04 *working index*, 30's ledger
table. Nothing else in `mockups/` has gone this far toward instrumentation.

---

## 34 — The Wall

*The site as one continuous hang.*

**Thesis.** He is a painter. Put people in front of the paintings and get
out of the way. The homepage is one uninterrupted vertical run of work —
no cards, no grid, no borders, no shadows, no index — and **every word on
the page is marginalia**: it lives in a narrow left rail, small, sticky at
the height of the thing it refers to, and never interrupts the images.
Pure white, `Instrument Serif` for the few large words, `Inter` at 0.7rem
for everything else, no accent colour at all.

Scale does the editing. Works are hung at 100%, 82%, 60%, 42% or 30% of
the column and pushed left or right, so the wall has rhythm instead of
uniformity; the *Once Creatures Existed* panorama breaks the full viewport
width. Two "breaths" — a single line of the artist's prose alone on the
wall — pace the run. The navigation is four words in a near-invisible
sticky signage bar, plus "doors in the far wall" at the end.

The work page is not an article. It is a closer stop on the same wall: the
painting takes the room, and Kyle's account of it *stays* marginalia,
stepping down the rail beside the works that stand next to it. You never
stop looking.

**Optimises for.** The work, and mood. This is the direction that reads as
a serious contemporary painter's site to someone who arrives from
Instagram. It is also the most restful of the five.

**Gives up.** Nearly everything else. There is no way to find a specific
work, no year, no discipline, no search — those all live behind four small
links. The long prose (bio, statement, philosophy essays) has no natural
home in this system and would need a second, quieter page type. And a
marginalia rail means text is set small by design; that is a legibility
choice Kyle should look at on his own screen before committing.

**Draws from.** 14 *salon wall*, 03 *night gallery* (inverted to white),
16 *filmstrip*. It is the least like the current site of the four
non-evolutionary directions, and the easiest to underestimate on a
screenshot — it needs to be scrolled.

---

## 35 — The Reel

*The site as a film.* **This is the risky one.**

**Thesis.** Kyle makes films — eight of them are already on the site — and
the current edition system already thinks in scenes: cover, plate,
interlude, wall quote, colophon. So run the whole front page as a
projection. Full black. A title card. Letterboxed frames that snap one at a
time as you scroll (`scroll-snap`), each with a **slate** in the corner
giving title, medium, year and a timecode. Silent-film **intertitles**
carrying Kyle's own sentences, one line to a screen. A match cut putting
*Cadence* (2015) beside *Cyclum Lunarem* (2017) — the same repeated mark,
two years and one material apart. And **end credits that are the
navigation**: the oeuvre, cinema, projects and production, rolling in
columns under "END OF REEL XIII".

Film grain, a vignette, a slow drift on every image, and an entrance
animation keyed to the scroll via `animation-timeline: view()` — the same
modern CSS the live `editions.css` already uses for its cover. Set in Space
Grotesk and Space Mono. No JavaScript at all; snap points and view
timelines do the whole thing, and everything is disabled under
`prefers-reduced-motion`.

The work page is a short: head slate, the wide establishing shot, an
intertitle, a **shot list** of what was made in the same window, and
**production notes / call sheet** in place of a tombstone. The catalogue
data is all there — it is just wearing a call sheet.

**Optimises for.** Impact and memorability. Nobody forgets this site. It
also unifies the two halves of the practice — the films stop being a
subsection and become the grammar of the whole thing.

**Gives up.** A great deal, honestly.

- **Density.** One work per screen means eight works is a long scroll.
  This front page can carry maybe ten things; the current edition carries
  more.
- **Skimmability.** Snap scrolling takes control away from the reader.
  Some people hate that, and on a trackpad it can feel sticky. (I used
  `proximity` rather than `mandatory` snapping to soften it — it can be
  tightened if Kyle likes the effect.)
- **Text.** Black backgrounds are the worst possible home for the long
  essays. This direction almost certainly needs a light inner page type for
  About / the philosophy writing, which means the site would carry two
  visual systems.
- **Maintenance.** Composing a season means art-directing a sequence, not
  writing an edition. That is more work every quarter, forever.

It is included because the brief asked for one that takes a real risk, and
because the film practice genuinely justifies it — not as a hedge.

**Draws from.** 16 *filmstrip*, 03 *night gallery*, 07 *frontispiece*, and
the sticky-cover treatment in the live `static/editions.css`.

---

## Honest comparison

| | 31 Ledger | 32 Specimen | 33 Index | 34 Wall | 35 Reel |
|---|---|---|---|---|---|
| Best for | continuity | identity | retrieval | the work | impact |
| First thing you see | the season | a nameplate | a query box | a painting | a title card |
| Long prose | good | **best** | fine | poor | poor |
| Finding a work | good | fine | **best** | poor | poor |
| Effort to build | **low** | medium | medium–high | low | high |
| Effort each season | low | medium | low | low | **high** |
| Risk | none | some | some | some | **high** |

Two things worth saying plainly:

1. **31 and 34 are not mutually exclusive.** 34's continuous hang would
   work as the *edition* body inside 31's chrome. If Kyle likes both, that
   is a real hybrid, not a compromise.
2. **33 is a promise about metadata.** Its facet counts are honest today
   (12 of 160 works have a status), and the design shows that gap rather
   than hiding it — but choosing 33 means committing to the collector-metadata
   work in `TODO.md` §2. Choosing any of the others leaves that optional.

## Assets

Seven new images were flattened into `mockups/assets/` using the existing
`<section>__<path>__<file>` convention: the five summer-edition process
photographs and two further Cyclum Lunarem views. Every one is referenced
by at least one mockup, and every `src` across all ten files was verified
against disk. Nothing under `content/`, `templates/`, `sass/`, `static/` or
`config.toml` was touched.
