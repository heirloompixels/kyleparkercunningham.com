# Hosting: a Worker on the TorC account

*Written 2026-10-15. Staged, not cut over: the site is still served by GitHub
Pages until the DNS swap below, which waits for Kyle.*

## Why it moved

The archive at archive.kyleparkercunningham.com is the catalogue of record, and
this site stops keeping a second copy of it (foundation D5,
`docs/2027-review.md` § 3). Its catalogue addresses have to go to the archive,
and an address that has moved should say so with a **301**: search engines then
carry a page's standing to its new home and drop the old one.

GitHub Pages cannot answer 301. Zola's aliases are pages that refresh
themselves, which search engines treat as a weaker hint, and there is no way to
send a whole page, rather than an alias of it, anywhere else. A Cloudflare
Worker serving the same build can: `public/_redirects` is read by the platform
and wins over any file at the same address. Kyle chose this on 2026-10-15
("Worker in TorC, real 301s") over proxying GitHub Pages through Cloudflare,
which risks the Pages certificate renewing, and over keeping the refresh pages.

It is also where the showcase will live (foundation D7): the next front page is
a Worker reading the archive's API, and this one moves there first so that the
cutover is a deploy, not a migration.

## What is served

- **The Zola build**, unchanged, as static assets (`wrangler.jsonc`). Zola's
  addresses end in a slash; `html_handling = auto-trailing-slash` sends a
  request without one to it (307), and `404.html` answers anything missing.
- **`public/_redirects`**, written by `scripts/redirects.py` from the content
  tree and the archive's public API after every build, never by hand. On
  2026-10-15 it held 1,006 rules: 156 work pages and 294 of their aliases to
  `/works/<slug>`, 38 oeuvre index pages and 41 of their aliases to the
  matching `/works?category=…&year=…`, and 477 tag pages to `/works?tag=…`.
  Every target was fetched and answered 200. The platform allows 2,000 static
  rules, and the script refuses to write more.
- **What stays here**: B-sides & Rarities and the Meaning Is Use essays (the
  archive has no exhibitions or writing yet), `/oeuvre/book-binding/` (no such
  category there), and 14 tags the archive does not use. The script prints the
  list with `--report`.
- **`sitemap.xml`** with every redirected address taken out, and Zola's empty
  `/topics/`: 68 addresses, each answering 200.

## Build and deploy

```bash
scripts/deploy-worker.sh             # build, write the redirects, deploy
scripts/deploy-worker.sh --dry-run   # everything but the upload
```

Zola must be **0.22.1** (`ZOLA=/path/to/zola` if `zola` is another version);
0.23 breaks the templates (`TODO.md` § 2). Wrangler comes from npm
(`WRANGLER=` overrides it) and the credentials from
`~/.config/cloudflare/torc.env`. The script runs CI's two data generators first
and puts their tracked output back afterwards. Zola itself deletes unused
images from `static/processed_images/` as it builds; those deletions are the
build's, not changes to commit.

The Worker is `kpc-site`, on the TorC account
(`0170b714b0ee025091fed8a088f7a65a`), staged at
<https://kpc-site.torc.workers.dev>. **The preview borrows the live site's CSS
and fonts**: `base_url` is absolute, so every page links its stylesheets at
kyleparkercunningham.com. Judge layout only after the cutover.

## Cutover — waits for Kyle

The site deploys on merge today and keeps draft PRs; it keeps them after the
move, because a deploy is still a change to the live site.

1. Merge the PRs this branch sits on (#7, then #8) and this one, and deploy
   from main with `scripts/deploy-worker.sh`.
2. In the `kyleparkercunningham.com` zone, delete the four apex A records
   (185.199.108–111.153) and the `www` CNAME to `heirloompixels.github.io`.
   Leave the MX, SPF, Mailgun, `tzprofiles` and Google verification records
   alone.
3. Uncomment the two `custom_domain` routes in `wrangler.jsonc` and deploy;
   Cloudflare creates the records and the certificate.
4. Check: `https://kyleparkercunningham.com/` and `www` answer 200 from
   Cloudflare (`server: cloudflare`), http answers 301 to https, a sample of
   `_redirects` answers 301 to the archive, and a real Chrome look at the home
   page, a project page and a redirected work.
5. Retire `.github/workflows/main.yml` (the gh-pages build), then turn GitHub
   Pages off for the repo, so two hosts never claim the domain.
6. In Search Console (domain property `sc-domain:kyleparkercunningham.com`,
   verified 2026-10-15 by a DNS TXT record), resubmit
   `https://kyleparkercunningham.com/sitemap.xml` and watch Pages → "Page with
   redirect" fill with the old catalogue addresses over the following weeks.

To undo before step 5, put the A records and the CNAME back and remove the
custom domains; GitHub Pages is still building.
