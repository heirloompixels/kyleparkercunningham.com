# Site TODO

A working list from the July 2026 site review. Items are ordered by impact
within each section. Checked items are done; strike nothing — when an item is
finished, check it and note the commit.

Two kinds of work are mixed here, marked accordingly:

- **[build]** — mechanical/structural; Claude can do these.
- **[voice]** — writing in Kyle's voice; drafted by Kyle (Claude may scaffold,
  marked `author = "claude"` per the [Manifest](/manifest/) attribution rules).

---

## 1. Make the site current

- [ ] **Promote the 2026-summer edition** [build] — it is July and Season XII
  (Spring) is still live; "Everything That Can Be Carried" sits in staging.
  `./scripts/edition.sh promote 2026-summer`. The living homepage only works
  if the season is actually alive.
- [ ] **Give the summer edition a cover** [voice] — `cover` / `cover_alt` are
  empty. One photographed work from the road is enough. Same for the empty
  `PLATE SLOT` in the body: drop in the first photographed painting of The 200.
- [ ] **Write the Survival Notes project statement** [voice; build scaffolds] —
  `/projects/survival-notes-from-the-near-future/` is the conceptual spine of
  the whole summer and currently reads "This project is currently in
  progress." It is the most-linked stub on the site.
- [ ] **Wire the field log to /log/** [build] — the edition keeps an inline
  field log *and* there's a Log section. Write once: post to `/log/`, have the
  live edition surface the latest entries automatically.

## 2. Fixes & migration debt

- [ ] **Add og:image / summary_large_image cards** [build] — an art site whose
  links unfurl with no image. Per-page image from the work's own photos, with
  a site-wide fallback.
- [ ] **Fold orphaned artwork pages into the Oeuvre** [build] — root-level
  pages that are really artworks (`espress-machine`, `crystal-tooth-whale-intaglio`,
  `future-capcitor`, `rainfall`, `sun`, …). Move each into
  `content/oeuvre/<discipline>/<year>/<slug>/` with aliases so no URL breaks.
- [x] **Audit internal links** [build] — a full scan of the built site found
  zero broken internal links; `/works/animism/` turned out to be a legacy
  alias redirecting to `/oeuvre/`, not a 404.
- [ ] **Write the animism topic page** [voice] — the About page lists
  *animism: acknowledging animals have intelligence and souls* but the link
  just redirects to the oeuvre index. It deserves the real page the About
  list promises.
- [ ] **De-Ghost the prose pages** [build] — `bio`, `artist-statement`, and
  `cinema` are raw Ghost HTML blobs pasted into markdown. Convert to clean
  markdown with words unchanged; make cinema embeds responsive instead of
  200 px wide.
- [ ] **Fill in collector metadata** [voice] — ~148 of 156 works have no
  `status` (available / sold / collection). The CSV backfill is already
  exhausted (`scripts/backfill_from_csv.py` reports all 48 matchable rows
  complete), so the remaining statuses are knowledge only Kyle has. The
  work-page tombstone and the oeuvre ledger both render status the moment
  it's added to a work's `[extra]`. Also: 45 post-2023 works have no CSV row
  at all — add them to the spreadsheet, and consider folding the CSV's
  `Remarks` column into page prose (the dry run prints the list).
- [ ] **Clean the repo root** [build] — move migration-era audit files
  (`metadata_audit*.csv`, `*_REPORT.md`, `BACKFILL_CANDIDATES.md`,
  `external_images_report.txt`, `Kyle Oeuvre/`) into `docs/archive/`.

## 3. New features

- [x] **Catalogue index** [build] — already existed: `/oeuvre/` is a full
  ledger of every work grouped by year with thumbnail, discipline, medium,
  and status columns. (`works-index.md` turned out to be the machine-readable
  JSON bridge for the river service, not a stub.) What makes the ledger look
  unfinished is the *unrecorded* status on most rows — see the collector
  metadata item above.
- [ ] **"Where to see the work" page** [build scaffolds; voice reviews] —
  gallery representation (Truth or Consequences Contemporary; Sun and Dust),
  what's available now, the shop, and a per-work *Enquire* mailto link with
  the work's title prefilled. Right now buying interest has no path except
  finding an email address on the About page.
- [ ] **Per-film cinema pages** [build] — each film gets
  `content/cinema/<slug>/` with duration/format/year metadata and a
  full-width embed, per the SPEC's cinema schema. The cinema index becomes a
  filmography.

## 4. Telling the story better

- [ ] **Rebuild About as one first-person narrative** [voice] — the raw
  material (Montana, the monastery *and* the cattle ranches, the rural/urban
  bridge) is scattered across nine third-person topic pages behind an
  alphabetized link list. One page, one voice — "I paint the life I live" is
  the opening line; keep that register throughout. Topic pages survive as
  deep links from within the prose.
- [ ] **Curated threads through the oeuvre** [voice; build makes the template] —
  the artist statement already names the series: animals with solarpunk
  apparatus, still lifes as lineage, hyperreal self-portraits, abstraction as
  encoded memory. Each becomes a guided walk: 6–10 works in sequence with
  connective prose. Chronology archives the work; threads interpret it.
- [ ] **Edition codas** [voice] — when a season retires, it gets a short
  "what actually happened" postscript before shelving. The editions archive
  then reads as a serialized autobiography, not a stack of old front pages.
- [ ] **Retire Season XII with the first coda** [voice] — Spring 2026 retires
  when Summer is promoted; write its postscript while it's fresh.

---

*List compiled July 2026 from a full-site review; maintained by hand.*
