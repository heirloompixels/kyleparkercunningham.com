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

- [x] **Promote the 2026-summer edition** [build] — done; Season XIII is the
  front page, Spring XII retired to the shelf with a past-tense lifespan.
  (Also fixed a latent build break: an unescaped `plate` shortcode inside the
  edition's HTML working-notes comment.)
- [ ] **Give the summer edition a cover** [voice] — `cover` / `cover_alt` are
  empty. One photographed work from the road is enough. Same for the empty
  `PLATE SLOT` in the body: drop in the first photographed painting of The 200.
- [x] **Write the Agile Meteor Press project page** [voice; build scaffolds] —
  scaffolded from the verified bookbinding/letterpress interviews (Sewn Boards,
  the two first editions, the Vandercook 325G shop, the field kit), marked
  `author = "claude"`. **Kyle: make it yours** — especially the first-person
  "book is meant to be carried" register, which is quoted rather than lived.
- [x] **Write the Survival Notes project statement** [voice; build scaffolds] —
  scaffolded from the season's own words, marked `author = "claude"`, status
  flipped to *ongoing*. **Kyle: make it yours** — it's the conceptual spine
  of the summer and deserves first-person voice.
- [x] **Wire the field log to /log/** [build] — done. The solstice entry is
  now a real log post; the homepage surfaces the three latest log entries
  under the edition's field-log note while a season is live. Post from the
  road to `/log/` and the front page updates itself.

## 2. Fixes & migration debt

- [x] **Add og:image / summary_large_image cards** [build] — done. Each page
  unfurls with its own first co-located photo (resized to 1200px at build
  time); the fallback painting is set in `config.toml` (`og_default_image`).
- [x] **Fold orphaned artwork pages into the Oeuvre** [build] — done. Four of
  the five were Ghost-era duplicates of works already catalogued; their URLs
  now redirect to the canonical pages and their unique prose (Sunflowers
  versions, Crystal Tooth Whale edition details) was merged in. Rainfall —
  the one true orphan — lives at `/oeuvre/installation/2015/rainfall/`.
- [x] **Audit internal links** [build] — a full scan of the built site found
  zero broken internal links; `/works/animism/` turned out to be a legacy
  alias redirecting to `/oeuvre/`, not a 404.
- [ ] **Write the animism topic page** [voice] — the About page lists
  *animism: acknowledging animals have intelligence and souls* but the link
  just redirects to the oeuvre index. It deserves the real page the About
  list promises.
- [x] **De-Ghost the prose pages** [build] — done. Bio and artist statement
  are clean markdown with the words unchanged; cinema became per-film pages
  (see below).
- [ ] **Fill in collector metadata** [voice] — ~148 of 156 works have no
  `status` (available / sold / collection). The CSV backfill is already
  exhausted (`scripts/backfill_from_csv.py` reports all 48 matchable rows
  complete), so the remaining statuses are knowledge only Kyle has. The
  work-page tombstone and the oeuvre ledger both render status the moment
  it's added to a work's `[extra]`. Also: 45 post-2023 works have no CSV row
  at all — add them to the spreadsheet, and consider folding the CSV's
  `Remarks` column into page prose (the dry run prints the list).
- [x] **Clean the repo root** [build] — done; everything now lives in
  `docs/archive/`, and `backfill_from_csv.py` points at the new CSV location.

## 3. New features

- [x] **Catalogue index** [build] — already existed: `/oeuvre/` is a full
  ledger of every work grouped by year with thumbnail, discipline, medium,
  and status columns. (`works-index.md` turned out to be the machine-readable
  JSON bridge for the river service, not a stub.) What makes the ledger look
  unfinished is the *unrecorded* status on most rows — see the collector
  metadata item above.
- [x] **"Where to see the work" page** [build scaffolds; voice reviews] —
  scaffolded at `/collect/` (marked `author = "claude"`): representation, the
  shop, and how to ask about a work. Every oeuvre work page now has an
  *enquire* mailto with the title prefilled, and Collect sits in both
  footers. **Kyle: review the wording.**
- [x] **Per-film cinema pages** [build] — done: eight film pages with
  format/location metadata and privacy-respecting embeds (youtube-nocookie /
  vimeo dnt), and `/cinema/` is the filmography. Year and duration fields
  render when added — Kyle can fill those in per film.

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
- [ ] **Retire Season XII with the first coda** [voice] — Spring 2026 is now
  retired (Summer was promoted 2026-07-06); write its postscript while it's
  fresh.

---

*List compiled July 2026 from a full-site review; maintained by hand.*
