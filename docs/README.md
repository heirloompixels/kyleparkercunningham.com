# Project notes

Working documentation for **kyleparkercunningham.com** — a Zola static site that
is the permanent archive of Kyle Parker Cunningham's art (painting, printmaking,
installation, sculpture, cinema), plus a living, seasonally-composed homepage.

Start here, then dive into the file you need:

| Doc | What's in it |
|-----|--------------|
| [architecture.md](architecture.md) | Tech stack, directory layout, every template and what it renders, the design system (chrome, tokens, fonts) |
| [editions.md](editions.md) | The "living homepage" Editions system and the staging → live → retired workflow |
| [content-guide.md](content-guide.md) | How to add a work / page / edition, front-matter conventions, drafts, authorship/manifest |
| [seo-and-cutover.md](seo-and-cutover.md) | SEO setup, the legacy-URL redirect aliases, and the apex-domain cutover runbook |
| [decisions.md](decisions.md) | Why things are the way they are — the decision log and the open items |

## 30-second orientation

- **Generator:** Zola 0.22.1. **Hosting:** GitHub Pages (`gh-pages` branch) via
  GitHub Actions. **Repo:** `heirloompixels/kyleparkercunningham.com`.
- **Live URL:** `https://kyleparkercunningham.com` (apex). The site cut over
  from the old Ghost site to this Zola build on the apex in June 2026;
  `brain.kyleparkercunningham.com` was the pre-launch dev URL and now
  canonicalizes to the apex. See [seo-and-cutover.md](seo-and-cutover.md).
- **Stylesheet source of truth:** `sass/style.scss` (compiled by Zola). The
  homepage and editions carry extra scoped CSS inline in their templates.
- **Run locally:** `./scripts/serve.sh` (regenerates data, then `zola serve`).
  **Build:** `./scripts/build.sh`. **Check links:** `zola check`.

## Conventions for working in this repo

- Branch off `main`; the deploy fires on every push to `main`.
- After content/template changes, run `zola build` and `zola check` before
  pushing. Verify visually with a headless screenshot when layout changes.
- Never commit a compiled `static/style.css` — it shadows the Sass output
  (see [decisions.md](decisions.md), "the stale-CSS bug").
