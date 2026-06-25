# Decision log & open items

## Decisions (the "why")

**The homepage is a work, not a landing page.** Kyle rejected conventional
portfolio grids. The front page is a seasonally-composed magazine *edition* that
retires whole to a permanent archive when its season ends, told as editorial.
Cadence: seasonally, with projects interspersed. → the Editions system
([editions.md](editions.md)).

**One design language, two volumes.** Rather than a separate look per section,
the homepage's editorial chrome (kicker, wordmark masthead, mono nav, 4-column
colophon) was promoted to every inner page at a quieter scale. Homepage and
individual editions stay "loud" and immersive; everything else is the quiet
variant. Built incrementally, section by section, then promoted to `base.html`
as the default. Prototype: `mockups/30`.

**Approved mockups → roles.** `mockups/4` → the `/oeuvre/` ledger ("the working
index"). `mockups/5` → the single work page (editorial, drop-cap, tombstone).
`mockups/6` → `/dashboard/`. `mockups/29` → the edition-led homepage.

**Oeuvre is medium-first.** Works live at `/oeuvre/<medium>/<year>/<slug>/`. The
old site was year-first (`/oeuvre/<year>/<medium>/<slug>`); all old URLs are
preserved via aliases ([seo-and-cutover.md](seo-and-cutover.md)). The external
archive drive was also planned around a medium-first hierarchy.

**Authorship is by prose, stored in front matter.** The `/manifest/` page marks
who wrote the *visible words* (`extra.author`: kyle/claude/structure), not who
touched the file. Transcribing Kyle's catalogue data still counts as Kyle's.

**Aliases over a redirect map.** GitHub Pages has no server-side 301s, so Zola
`aliases` (meta-refresh/JS) are used for all legacy-URL preservation. Google
honors them.

**Taxonomies trimmed to `topics`.** `categories`/`years`/`medium` were declared
in config but never populated (works use plain `category`/`year` fields and
`extra.medium`), so they only produced empty pages. Removed.

**Placeholder content is drafted, not deleted.** The whole `notes/` section was
scaffold ("Example: Bookbinding"). Drafted (all files) to hide from production
while keeping the structure for real notes later. Same for the `2026-summer`
edition (Kyle's WIP).

**Gallery representation (June 2026):** Truth or Consequences Contemporary
(torc.art), Truth or Consequences NM, and Sun and Dust (sunanddust.gallery),
Santa Fe NM. The old `desertarchaic.com` (former gallery name) is defunct and
was removed from the About page.

## Bugs found & fixed (don't reintroduce)

- **The stale-CSS bug.** A committed `static/style.css` shadowed the Sass output
  (Zola copies `static/` over compiled CSS), silently discarding every
  `sass/style.scss` edit. Deleted it. **Never commit a compiled `static/style.css`.**
- **Image centering.** Global `figure img { display:block; width:100% }` ignored
  the figure's `text-align:center`. Fixed with explicit `margin:auto` on
  `.ed-plate img` and the work-page image.
- **`processed_images` churn.** `zola build` prunes orphaned resized variants
  from `static/processed_images/` every run. Don't "restore" them thinking it's
  data loss — commit the pruned, self-consistent state.
- **Domain flip outage.** Flipping `CNAME` to the apex before DNS was repointed
  took the site offline. Order matters — see the cutover runbook.
- **Tera arithmetic.** `{% set x = a + (b | length) %}` fails to parse; assign
  each `| length` to its own variable first, then sum.
- **Front-matter editing.** When scripting alias inserts, parse the front matter
  line-by-line; a greedy regex glued the closing `+++` onto the aliases line.

## Open items / next up

- [x] **Apex DNS cutover** — **done June 2026.** Live at
  `https://kyleparkercunningham.com`; remaining housekeeping (Enforce HTTPS,
  Search Console resubmit, retire the droplet) is in
  [seo-and-cutover.md](seo-and-cutover.md).
- [ ] **External archive drive reorganization** — discussed, not implemented:
  a definitive medium-first `works/<medium>/<year>/<work>/` hierarchy, with
  ~2048px web masters committed to the repo and originals kept on the drive.
- [ ] **Notes** — write real notes, then un-draft (`draft = true` on all
  `content/notes/**`).
- [ ] **Work pages** — grow the terse stubs into image-rich, prose-heavy
  documents (ongoing direction).
- [ ] **Dead-code** — `partials/navigation.html` etc. were removed; if any old
  `static/processed_images` legacy files prove unreferenced long-term they could
  be dropped, but they're harmless.
