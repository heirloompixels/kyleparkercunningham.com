# Content guide

## Adding a work

Works live at `content/oeuvre/<medium>/<year>/<slug>/index.md`, with the work's
image(s) as sibling files (Zola "assets"). The URL is **medium-first**:
`/oeuvre/<medium>/<year>/<slug>/`.

Front matter:

```toml
+++
title = "Butterfly Conundrum"
date = 2015-01-01          # drives sort + the year shown
year = 2015
category = "painting"      # plain field (not a taxonomy)
aliases = ["/oeuvre/painting/2015/butterfly-conundrum/", "/butterfly-conundrum/"]

[extra]
medium = "Oil on Gesso Panel"
dimensions = "5.75 x 11.75 inches"
status = "Private Collection"      # shows as a status dot in the ledger
# year_started = 2014              # optional: renders a "YYYY — YYYY" range
# year_reworked = 2020             # optional: "· reworked YYYY"
+++
Body prose. The first image asset becomes the ledger thumbnail.
```

The ledger (`/oeuvre/` and `/oeuvre/<medium>/`) is generated from these files —
no list to maintain. The `[extra]` medium/dimensions/status were backfilled
from Kyle's CSV via `scripts/backfill_from_csv.py` (conservative: dry-run by
default, `--apply` to write, never overwrites existing values).

> **Direction:** work pages are growing from terse one-image stubs into
> image-rich, prose-heavy documents. Use the `plate` / `diptych` shortcodes.

## Adding a generic page

`content/<slug>/index.md` with `template = "page.html"`. Optional `[extra]`:
`label` (the small mono kicker above the title) and `mast_active` (underline a
nav item). Gets the editorial body + drop-cap automatically.

## Aliases (redirects)

Zola `aliases = [...]` in front matter generate redirect pages (meta-refresh +
JS — the right tool for GitHub Pages, which has no server-side 301s). This is
how every legacy URL is preserved — see [seo-and-cutover.md](seo-and-cutover.md).
Always trailing-slashed, e.g. `"/old-path/"`.

## Drafts

`draft = true` excludes a page from production (`zola build`); visible with
`zola serve --drafts`. **Drafting a section's `_index.md` cascades** — Zola
drops the whole subtree and any taxonomy it fed. But `generate_site_index.py`
(the manifest) skips drafts **per file**, so if you draft a section, also draft
its child pages, or the manifest will list pages that 404.

Currently drafted: the entire `notes/` section (placeholder scaffold) and the
`2026-summer` edition.

## Authorship / the manifest

`/manifest/` lists every page and who wrote the **prose** (not who touched the
file). Stored as `extra.author`:

- `kyle` (default) — Kyle wrote the words.
- `claude` — the AI assistant wrote the prose.
- `structure` — derived, for prose-less generated index pages.

`scripts/generate_site_index.py` walks `content/`, reads `extra.author`, and
writes `data/site_index.json` (consumed by `manifest.html`). It runs in
`build.sh`, `serve.sh`, `edition.sh serve`, and CI. Regenerate it after content
changes that affect the page list.

## The works.json bridge

`content/works-index.md` + `templates/works_json.html` emit `/works.json` (156
records: slug, title, medium, dim, year, image, order) for the external "river"
service. Image URLs use `base_url`, so they follow the domain automatically.
Don't break this when restructuring oeuvre.

## Data scripts (`scripts/`)

- `build.sh` / `serve.sh` — regenerate data (`update_recently_edited.py` +
  `generate_site_index.py`) then `zola build` / `serve`. Prefer these over bare
  `zola` so the manifest + recently-edited data stay current.
- `update_recently_edited.py` — refreshes the recently-edited list (used by the
  dashboard) from git history.
- `generate_site_index.py` — the manifest data (see above).
- `backfill_from_csv.py` — one-off CSV → front-matter metadata backfill.
- `edition.sh` — the editions workflow (see [editions.md](editions.md)).

## Images / `static/processed_images`

`resize_image()` in templates produces responsive variants. **`zola build`
itself prunes orphaned entries** from `static/processed_images/` every run — if
you see ~100 files "deleted" after a build, that's Zola removing stale variants,
not a bug. Commit the pruned state. Source images live on Kyle's external drive
(the definitive archive); the site commits ~2048px web masters.
