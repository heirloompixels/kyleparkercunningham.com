# SEO & the apex-domain cutover

## Current domain state

- **New site (this repo)** → GitHub Pages → served at
  **`brain.kyleparkercunningham.com`** (`static/CNAME`, `config.toml` base_url).
- **Apex `kyleparkercunningham.com`** → A record `164.90.135.135`, a
  **DigitalOcean droplet running Kyle's old Ghost site** (confusingly, same
  title "The art of Kyle Parker Cunningham").

The goal is to move the new site onto the apex. **This is a DNS operation, not
a code change.** Flipping `CNAME`/`base_url` to the apex *before* DNS points at
GitHub Pages takes the new site offline (GitHub Pages 404s `brain.` and
redirects to an apex it doesn't serve). This was tried and reverted — do it in
the right order.

## SEO head (in `base.html`)

The live site has: per-page `<title>`, meta `description`, `author`, `robots`,
**canonical** (`current_url`), **OpenGraph** + `twitter:card`, favicons +
`site.webmanifest`. `static/robots.txt` points at the sitemap. Zola generates
`sitemap.xml` automatically (canonical pages only — alias redirects are not in
the sitemap). The homepage `og:title` uses the site title (the root
`_index.md` title was set to the full name for this).

## RSS feed

`generate_feeds = true` + `feed_filenames = ["rss.xml"]` in `config.toml`
produce a site-wide feed at **`/rss.xml`** (Zola's built-in template), newest
first — it mirrors the old Ghost site where each work was a post. Autodiscovery
`<link rel="alternate" type="application/rss+xml">` is in `base.html`, and the
footer Contact column links it. The old Ghost feed lived at `/rss/`; readers on
that URL will need to re-point (it wasn't in the sitemap). To scope the feed to
just the Log later, move `generate_feeds` to `content/log/_index.md` instead.

## Legacy-URL redirects (the important part)

The old Ghost site exposed **218 URLs** (sitemap: 18 pages, 156 posts, 2
authors, 42 tags). The new site has a **different URL structure**, so 201 would
have 404'd. Every one now redirects via Zola `aliases`:

| Old pattern | Count | Redirects to |
|-------------|-------|--------------|
| `/oeuvre/`**`YEAR/MEDIUM`**`/slug` (year-first) | 156 | the new **`/oeuvre/MEDIUM/YEAR/slug`** page (151 auto-matched; 5 live as top-level pages: espress-machine, rainfall, future-capcitor, sun, crystal-tooth-whale-intaglio) |
| `/printmaking`, `/works/{painting,printmaking,installation,sculpture,exhibitions}` | 6 | the matching `/oeuvre/<medium>/` section |
| `/works/the-memory-of-atmosphere`, `/works/tomorrow` | 2 | their `/projects/` pages |
| `/author/kyle`, `/author/ghost-user` | 2 | `/about/` |
| `/works/<tag>` and `/works/<year>` (Ghost archives, no equivalent) | ~35 | `/oeuvre/` |

Notes:
- The aliases were added by mapping each old URL to its **real** new page
  (slugs aren't always 1:1 — e.g. old `espress-machine` → new `espresso-machine`).
- Redirects are meta-refresh/JS (GitHub Pages can't do server 301s). Google
  honors them.
- They currently target `brain.` URLs; at cutover they auto-retarget to the
  apex (generated from `base_url`).

**To re-audit parity** (after any restructuring): build, then for each old path
check `public/<path>/index.html` exists. The old sitemap URL list was captured
during the migration; regenerate from `https://kyleparkercunningham.com/sitemap*.xml`
if needed.

## The cutover runbook

Do in order:

1. **Repoint apex DNS:** remove the `164.90.135.135` A record; add GitHub Pages
   A records `185.199.108.153`, `.109.153`, `.110.153`, `.111.153`. Optionally
   add a `www` CNAME → `heirloompixels.github.io`.
2. Wait for propagation; confirm `dig +short kyleparkercunningham.com` shows the
   `185.199.x` IPs.
3. **Flip the config:** set `static/CNAME` → `kyleparkercunningham.com` and
   `config.toml` `base_url` → `https://kyleparkercunningham.com` (there's an
   inline note in `config.toml`). Push.
4. In **GitHub → Settings → Pages**: confirm custom domain =
   `kyleparkercunningham.com` and enable **Enforce HTTPS** (wait for the cert).
5. In **Google Search Console**: resubmit the sitemap. Same apex domain, so the
   internal redirects carry the link equity — no Change-of-Address needed.
6. Retire the DigitalOcean droplet.

## Known false positive

`zola check` (with external links) flags `sunanddust.gallery` as broken — it
returns 403 to automated requests (bot protection) but is a live site. Safe to
ignore.
