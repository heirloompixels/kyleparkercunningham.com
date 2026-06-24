# Architecture

## Stack

- **Zola 0.22.1** static site generator (TOML front matter, Tera templates).
- **Sass** compiled by Zola (`compile_sass = true`); `sass/style.scss` is the
  single global stylesheet → `/style.css`.
- **GitHub Pages** deploy via GitHub Actions (`.github/workflows/main.yml`):
  on every push to `main` it runs `update_recently_edited.py` +
  `generate_site_index.py`, then `shalzz/zola-deploy-action` publishes the
  built `public/` to the `gh-pages` branch. `static/CNAME` sets the served
  domain.

## Directory layout

```
content/            Markdown content (front matter + body)
  _index.md         Homepage section (template = index.html)
  about/, colophon/, bio/, ... 21 generic text pages (template = page.html)
  oeuvre/<medium>/<year>/<slug>/index.md   the works archive
  editions/<slug>/index.md                 the living-homepage issues
  projects/, log/, notes/ (drafted)        sections
templates/          Tera templates (see table below)
sass/style.scss     the global stylesheet (only source of CSS truth)
static/             copied verbatim to the site root (favicons, CNAME,
                    robots.txt, editions.css, processed_images/)
scripts/            build/serve/edition/data helpers (see content-guide.md)
data/               build-time JSON: site_index.json, recently_edited
docs/               this documentation
mockups/            self-contained HTML design mockups (history; #29 → homepage,
                    #4 → oeuvre ledger, #5 → work page, #30 → inner chrome)
```

## Templates and what they render

| Template | Renders |
|----------|---------|
| `base.html` | The shell: `<head>` (SEO meta, OpenGraph, favicons, fonts, stylesheet) + default `site_header` (masthead) and `site_footer` (colophon) blocks |
| `index.html` | The homepage — the live edition inline + recent-work index + big type menu + expanded footer. Its own loud hero masthead (overrides `site_header`/`site_footer`). Layout from `mockups/29`. |
| `page.html` | Generic text pages (about, colophon, bio, …). Editorial body with drop-cap. |
| `section.html` | Generic section fallback (structural year indexes). Editorial doc-list. |
| `oeuvre/section.html` | `/oeuvre/` — the full "working index" ledger (all disciplines). Layout from `mockups/4`. |
| `oeuvre/discipline.html` | `/oeuvre/<medium>/` — discipline-scoped ledger with the active filter chip lit. |
| `oeuvre/single.html` | A single work page (breadcrumb, tombstone, drop-cap prose, prev/next). Layout from `mockups/5`. |
| `editions/section.html` | `/editions/` — the shelf of past issues + the live one. Loads `static/editions.css`. |
| `editions/single.html` | A single edition — immersive (own cover + internal colophon; suppresses site masthead AND footer). Includes `editions/issue.html`. |
| `editions/issue.html` | The shared partial that renders a full edition (cover, masthead, body, doors, colophon). |
| `projects/{section,single}.html`, `log/{section,single}.html` | Editorial section indexes + single pages. |
| `notes/{section,single}.html`, `taxonomy_{list,single}.html` | Notes + topics taxonomy. **Currently drafted** (not built). |
| `dashboard.html` | `/dashboard/` — studio dashboard (projects by status, production log, archive counts). Layout from `mockups/6`. |
| `manifest.html` | `/manifest/` — every page + who authored it (see content-guide.md). |
| `works_json.html` | Emits `/works.json` for the external "river" service (`river.kyleparkercunningham.com`). Driven by `content/works-index.md`. |
| `partials/masthead.html` | The compact running masthead (kicker + wordmark + mono nav). Reads optional `mast_active`. |
| `partials/colophon.html` | The expanded 4-column footer (Studio / Contact / Archive / This Page). Self-contained — computes catalogue counts + live edition. |
| `shortcodes/{plate,diptych,wallquote,marginalia,interlude,art_image}.html` | Editorial image/quote vocabulary used in edition + work bodies. |

## The design system

One visual language site-wide: the homepage is the loud version, every inner
page wears the same DNA at a quieter volume (see [decisions.md](decisions.md)).

**Tokens** (defined in `sass/style.scss` `:root`, mirrored in the homepage's
inline `--h29-*` vars):

- Colours: `--bg #f7f4ef`, `--bg-accent #efe9e1`, `--ink #1e1a16`,
  `--muted #6a6258`, `--accent #1f3f5b` (navy), `--line #e2dbd1`.
- Fonts: **Literata** (serif body/headings), **IBM Plex Sans** (labels/UI),
  **Inconsolata** (mono kickers/metadata). Loaded site-wide in `base.html`.
- Fluid type/space scale (Utopia-style `--step-*` / `--space-*` clamps).

**Chrome** (the shared furniture):

- `partials/masthead.html` — kicker bar (`Painting · Printmaking · Installation
  · Cinema` linked + `Est. 2003`), compact wordmark, mono uppercase nav. A page
  can set `mast_active` (`oeuvre`/`editions`/`projects`/`log`/`about`) to
  underline its nav item. Wired in via `base.html`'s default `site_header`;
  most templates also include it directly so they can set `mast_active`.
- `partials/colophon.html` — the 4-column footer, the `base.html` default
  `site_footer`.
- Key CSS classes: `.mast`, `.page-doc` (editorial body, drop-cap scoped here),
  `.foot`, `.ledger`/`.ledger-*` (oeuvre table), `.work-page` (single work),
  `.doc-list`/`.doc-deck` (index lists), `.h29-*` (homepage, inline in
  `index.html`), `.dash` (dashboard), `.manifest-*`/`.atag` (manifest).

**Width model:** `main` is capped at `var(--max)` (78ch); the masthead/footer
and the oeuvre ledger run wider (~1180–1240px). The ledger table escapes the
78ch column with a negative-margin trick — don't change `main`'s max-width
without re-checking `table.ledger`.

**Immersive pages** (homepage, individual editions) deliberately opt out of the
shared chrome: they blank `site_header`/`site_footer` and supply their own.
