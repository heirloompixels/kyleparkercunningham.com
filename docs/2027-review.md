# The 2027 review

*Written 2026-10-07, at the start of the showcase split. Kyle: "the
archive/oeuvre is really what the site is now, just statically produced. I want
to seperate this out — where the archive is the archive, has everything. and
then the main site is the showcase of what is happening now and the best of the
past."*

This is the whole list of what has to happen, from a full review of the site
and the archive on the same day. Two audits ran: a technical one (fresh builds
on Zola 0.22.1 and 0.23.6, a crawl of the build, the live site, screenshots at
390 and 1440 px), and a content and data one (every section, every
`author = "claude"` page, the site's catalogue against the archive's public
API, the films in cine). Every finding below was verified; the ones marked
*ask* need a fact only Kyle has.

The designs for the new showcase are in `mockups/2027/` (ten sketches, see
its index page). This file is the work around them.

---

## 1. Needs Kyle, now

In order of what it costs to leave.

1. **Prices and buyer names were public on GitHub. — Purged 2026-10-07.**
   Kyle: "clear this out however we need to but keep the site live." Every
   branch was rewritten and force-pushed, with the site live throughout:
   the price spreadsheet (at both of its historical paths), the four
   `metadata_audit*.csv` files, `mockups/_build/raw/`, and a collector's name
   on the Three Blue Corn page and its 18 feeds. A scan of every blob found
   none left. **Still to do, by Kyle:** GitHub keeps the old commits reachable
   by their IDs and through the closed PRs #1–4 until GitHub Support removes
   them (support.github.com, "Remove sensitive data"; the old main tip was
   `f769cd6`). The pre-purge history is in a bundle at
   `~/kpc-site-private-backup/` on granite, with the spreadsheet beside it,
   readable only by Kyle; the oeuvre database already holds its rows. The
   archive's own Three Blue Corn page still names the collector — a one-field
   edit to its `body_md` that wants Kyle's go-ahead. `scripts/backfill_from_csv.py`
   now has no input; it was already exhausted.
2. **HTTPS is not enforced.** `http://kyleparkercunningham.com/` answers 200
   with no redirect; the Pages setting is off. `docs/seo-and-cutover.md` says it
   is on, and is wrong. One command fixes it:
   `gh api -X PUT repos/heirloompixels/kyleparkercunningham.com/pages -F https_enforced=true`.
3. **Machine prose is live under your name.** 90 pages are marked
   `author = "claude"` (80 works, 10 others) and nothing on the page says so;
   about 41 are in your first person. The worst is
   `content/oeuvre/painting/2022/ken/`, where a model tells how Ken's wife
   died, as you. The same drafts were imported into the archive with no
   authorship, so `archive.kyleparkercunningham.com/works/ken` carries it too.
   Foundation D3 already decided the rule; this is applying it: take the prose
   off both surfaces, keep the facts, keep the drafts in the record as drafts.
   Say the word and it is a mechanical job.
4. **Prices on the archive.** `/works/storm-castle-bluffs` shows "available ·
   81.00 USD", and the public API returns `price_cents` and a checkout URL. It
   is a live Shopify listing, so it may be intended — but "no prices on any
   public surface" says otherwise. Also, The 200's collection numbers (31, 55,
   81) *are* the prices, by design; the API serves them. Decide whether a
   listed work may show its price.
5. **The front page is still summer.** Season XIII says "Lives June —
   September 2026", has no cover, and ships its own working notes ("PLATE
   SLOT", "HOW TO ADD TO THIS EDITION") in the homepage HTML and the RSS feed.
   Its line about the 200 going on sale at the solstice is in the wrong tense.
   Either an autumn edition, or this is the moment the new showcase replaces
   editions as the front page (§ 4).
6. **Which films go public.** cine has 86 films and 158 shorts, none
   published. The site's cinema is eight clips from 2016–18, three of them on
   the Intentionally Confusing YouTube channel, which goes when that site
   shuts. cine `docs/sharing.md` says posting is your decision.
7. **Facts only you know** (*ask*):
   - Tomorrow is dated 2019 on both surfaces; the Vimeo upload and cine say 2018.
   - Two "Tomorrow" records — one work shown twice?
   - airlift / air-lift, dayhike / day-hike: reprints, or new plates?
   - The bio says you co-create Desert Archaic; `/links/` says it closed.
   - "Taos & Truth or Consequences" — is that still where you live and work?
   - The installation caption says December 2019; the file is named 2021.
   - The Blue Corn and Crystal Hammer film pages give media that don't match
     their works (drypoint print 2022 for a 2016 film; canvas vs linen).
   - Evening Clouds is public on the archive while marked in progress.
   - Log posts of Jan–Mar 2026, the Periodic and TorC project pages: yours,
     or unlabelled drafts? They read like the drafts.
8. **Opening the archive to AI crawlers** (foundation D13). The archive's
   `robots.txt` refuses nine AI crawlers and sends `ai-train=no`; the main site
   allows everything and is the one carrying the drafts — the reverse of what
   you want. Flip the archive for your instance only, *after* item 3.

## 2. Fix now (mechanical)

Nothing here needs a decision. Grouped by where the fix lands.

**Site, broken**
- Five dead links on `/manifest/` and `/dashboard/` (dated log URLs, and
  `/works-index/` which is really `/works.json/`): the generators build
  addresses from file paths. 31 of 278 addresses in
  `data/recently_edited.json` don't exist.
- `/links/` links `/now`, a 404.
- `content/materials/index.md`: an href with a leading space.
- 34 blank year pages (`/oeuvre/painting/2024/` and so on) and `/painting/`,
  each with an empty title, all in the sitemap. `render = false`, and an alias
  for `/painting/`.
- All 190 RSS items say `<author>Unknown</author>`: a top-level `author` in
  `config.toml`.
- `/works.json` redirects to `/works.json/`, served as HTML and listed in the
  sitemap.

**Site, wrong**
- `/privacy/` says "We track you in no way at all" while every page loads
  Google Fonts and the films embed Vimeo and YouTube. Self-host the fonts or
  change the sentence.
- 739 of 744 pages share one meta description.
- No structured data anywhere: no `VisualArtwork`, no `Person`. Foundation § 4
  point 3 wants it on every work.
- Resized PNGs stay PNG: Paper Neck Giraffes is 8.7 MB on a phone, Butterfly
  Conundrum 7.5 MB. `format="auto"` in `shortcodes/art_image.html`.
- 212 MB of unused originals are deployed and downloadable.
- The catalogue download serves the 13.4 MB PDF; a 7.9 MB web version sits
  unlinked beside it.
- 2,316 linked thumbnails have empty alt, so their links have no name; the
  Rainfall page has 18 images with none.
- The main image on every work page is lazy-loaded.
- Fonts are render-blocking, about 300 KB a page.
- Headings jump from h1 to h5 in the footer; no skip link.
- "Recently edited" sorts by file time, meaningless in CI; works that share a
  date reorder between builds.
- The colophon says "No JavaScript". `SPEC.md` § 6 still says so on main
  (the 2027-pass branch strikes it but was never merged), and calls this site
  "the definitive lifelong archive".
- `README.md` is still the Ghost-migration readme (`kpc-site/`, Netlify).
- Intentionally Confusing links in `about`, `chronos` ("2021 – Present"),
  `collect`, `contact-2` and `links`.
- `projects/tomorrow`: "Project overview coming soon." `/oeuvre/book-binding/`
  shows "0 works". 26 placeholder notes, `/notes/` a 404.
- No film has a year or a duration; Vimeo has both.
- Spelling, with file and line, in the content audit: "print makes",
  "agua-lungs", "it's own" ×2, "experiemnting", "sterate", "guache", "leary",
  "lily's", "anamistic", "survivie", "sub teranian", "burried",
  "unprecidented", "Mycellium", "Diabond", "created by wholly by".

**Build and CI**
- Zola 0.23 breaks 13 templates exactly as `TODO.md` predicts (6 `ending_with`,
  21 `concat`, 17 `filter`, 5 `slice`, 10 `.N`). Only worth doing if the site
  stays on Zola (§ 4).
- `actions/checkout@v4` runs on deprecated Node 20, and `ubuntu-latest`
  moves to Ubuntu 26 on 2026-10-19. The deploy action is pinned by tag, not
  SHA, and pull requests are never built.
- The git pack is 554 MB, including an 86.8 MB PDF that survives only in
  history and 1,098 committed resized images. Folds into the history rewrite
  in § 1 item 1 if that happens.

**Archive (atelier/oeuvre)**
- Machine drafts unattributed (§ 1 item 3).
- 24 public works print the same text twice (`description` equals `body_md`).
- Duplicates to merge: coffee-carafe / coffee-caraffe, spring / spring-window,
  michael / michael-donlan, cyclum-lunarem / its summer-2016 row, five rows
  for the Enso triptych, rhino-radar / rhino-radar-arm-fauna, and CSV pairs
  (four-oil-cans / oil-cans-four, orange-diamond / diamond-orange,
  two-oil-cans / oil-cans-two, three-red-apples, venus, millett). Two junk rows:
  `checkpoint-2026-08-08t04-55-09-293z` and `untitled-4` "Test".
- Slugs that disagree with their titles: path-though, tubed-pachydeerm,
  gardner, mycellium, untitled-begins ("Combinations and Re-Entry"), shawn,
  untitled-1 to 7. Each rename needs a redirect row.
- Title and medium typos: Stormcastlle, Airborn, Crystalized, Caraffe,
  Oragami, "LInen" ×5, "Acylic", "Acrylica", "Diabond" ×13, "OIL ON". There are
  51 distinct medium strings for perhaps fifteen media.
- The native 2026 works have `alt=""` and no tags.
- No collections index, no about page; "Recently added" is import order.

## 3. The split

**The archive has everything. The site shows now and the best.** Today it is
nearly the reverse: the site is a second catalogue (160 works, images in git)
and the archive holds only works and two collections.

**What the archive has to gain before it can be "everything":**
films (86 now, and the old eight), exhibitions (the schema has
`oeuvre_exhibitions`; B-sides & Rarities is one), the editions and the log,
writing (the Meaning Is Use essays, signed by Claude), the 137 private works
reviewed and the duplicates merged, inventory numbers (0 of 296 — foundation
D1), places (149 of 159 public works have none), and a collections index and
an about page. Whether films and writing live *in* the oeuvre or in a sibling
store is foundation D6; the archive's front door should show all of them
either way.

**Where each part of today's site goes:**

| Today | Goes to |
|---|---|
| Front page (editions) | **Showcase** — replaced by the new design; retired editions move to the archive as a record |
| `oeuvre/` (160 works, 44 indexes) | **Archive.** Already there, facts identical on all 156 shared works. The copy retires (D5); its 218 aliases become redirects to archive pages |
| `projects/` | **Showcase** for the live ones (the 1000, the Periodic, Survival Notes, Agile Meteor Press, TorC); **archive** for finished ones (Memory of Atmosphere becomes the Atmospheric Balance collection) |
| `cinema/` | **Showcase**, rebuilt from cine; the 2016–18 clips go to the archive |
| `log/` | **Showcase** if it is fed (nothing since 06-21); otherwise retire |
| `about/` + bio, statement, abstraction, chronos, portraiture, installations, materials, paper | **Showcase**: one first-person About in your words. The rest **archive** |
| `collect/`, `press-kit/` | **Showcase**, rewritten by you (both are drafts) |
| `privacy-2/` | **Showcase** footer, made true |
| `manifest`, `dashboard`, `colophon`, `learning`, `links`, `contact-2`, `notes/`, `painting/`, `works-index` | **Retire or redirect** |
| `oeuvre/exhibitions/…/b-sides-rarities`, `oeuvre/philosophy/…` | **Archive** |

**Only on the site, so carry it over before retiring the copy:** B-sides &
Rarities, the three Meaning Is Use essays, the frontmatter that records which
80 works are drafts (foundation D8 needs it to attribute the archive's
copies). **Only in the archive:** the three 2026 watercolours, Atmospheric
Balance (eight works), 14 private 2026 works, and 22 more *sold* statuses than
the site knows.

## 4. Building the showcase

1. **Pick the direction.** The ten sketches in `mockups/2027/` are deliberately
   far apart. The likely answer is one spine plus two or three of the others
   as rooms (§ the sketchbook index says which combine).
2. **Decide the stack** (foundation D7). The recommendation stands: a Worker
   on the TorC account reading the archive API at request time, behind a cache.
   Moving is a DNS change, not a migration. Several sketches need client code
   (WebGL, WebAudio, canvas); none needs a framework. Write the reason down in
   `docs/` when it is chosen.
3. **Decide the ending** (D9): what a visitor does last. Every sketch ends at
   the archive and most offer one email relationship; where that list lives is
   the open question.
4. **Read works from the archive, never copy them.** The showcase chooses
   (featured, rank, collections — the archive has `featured` and
   `featured_rank`, both empty); the archive holds.
5. **Films need a public home** before any sketch with video is real: Stream
   or HLS from R2 (D7). Today nothing is public; reception's media is public
   only while Instagram fetches it.
6. **Your words.** The showcase is short, so it needs only a few: an opening,
   an About, a line per room. The talking sessions and the transcripts are the
   supply. Lines you typed to Claude in private (several sketches quote one
   from 2026-09-27) need your OK before they appear anywhere.
7. **Then cut over.** The kpc site goes back to the draft-PR rule the moment it
   deploys on merge (machinery `CLAUDE.md`); redirect every old URL; enforce
   HTTPS; structured data on every page; `llms.txt`; open the crawlers (§ 1
   item 8).

## 5. Already decided, for reference

From `daybook/docs/explorations/2026-09-27-the-foundation.md`: the foundation
stays; the stack is open; no prices; private brain notes never reach the site;
your words are yours and a machine's are signed by Owl (D3); every work gets a
record at the start (D2, the record half); the site stops being a copy of the
catalogue (D5, recommended, not yet decided).
