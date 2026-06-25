# SEO & the apex-domain cutover

## Current domain state

**Cut over to the apex in June 2026.** The site is live at
**`https://kyleparkercunningham.com`** — GitHub Pages, apex A records
`185.199.108–111.153`, `static/CNAME` + `config.toml` base_url both on the apex,
HTTPS enforced. `brain.kyleparkercunningham.com` was the pre-launch dev URL and
now canonicalizes to the apex; its DNS record can be removed whenever. The old
Ghost site (DigitalOcean droplet `164.90.135.135`) is no longer referenced and
can be retired.

> **Hard-won lesson (kept for the record):** the cutover is a DNS operation, not
> a code change. Flipping `CNAME`/`base_url` to the apex *before* DNS pointed at
> GitHub Pages took the site offline (Pages 404'd `brain.` and redirected to an
> apex it didn't serve). Order matters: repoint DNS first, verify with `dig`,
> *then* flip the config.

### If you ever need to move domains again

1. Point the target domain's DNS at GitHub Pages (A records
   `185.199.108–111.153`, optional AAAA `2606:50c0:8000–8003::153`).
2. Verify: `dig +short <domain>` shows those IPs.
3. Set `static/CNAME` + `config.toml` `base_url` to the new domain; push.
4. GitHub → Settings → Pages: confirm custom domain + Enforce HTTPS.
5. Resubmit the sitemap in Search Console.

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

## Post-launch follow-ups

Done at cutover (June 2026): apex DNS repointed to GitHub Pages, `CNAME` +
`base_url` flipped to the apex, deploy verified live (homepage, work pages,
legacy redirects, RSS, sitemap, HTTPS cert all 200/valid).

Remaining housekeeping (low-priority, Kyle's side):

- [ ] GitHub → Settings → Pages: confirm custom domain + **Enforce HTTPS** is on.
- [ ] Google Search Console: resubmit `https://kyleparkercunningham.com/sitemap.xml`
      (same apex domain → the internal redirects carry link equity; no
      Change-of-Address needed).
- [ ] Retire the old DigitalOcean droplet (`164.90.135.135`) — nothing points
      at it anymore.
- [ ] Optionally remove the `brain.kyleparkercunningham.com` DNS record (it now
      just canonicalizes to the apex).

## Known false positive

`zola check` (with external links) flags `sunanddust.gallery` as broken — it
returns 403 to automated requests (bot protection) but is a live site. Safe to
ignore.
