#!/usr/bin/env python3
"""Write public/_redirects: the catalogue's URLs on this site, sent to the archive.

The archive at archive.kyleparkercunningham.com is the catalogue of record, and
this site stops keeping a second copy of it (foundation D5; docs/2027-review.md
§ 3). Every work page, every alias that points at one, the oeuvre's index pages
and the tag pages answer 301 to the matching archive page, so links and search
results that know the old addresses land on the record instead of a stale copy.

Run after `zola build`. It reads the content tree's front matter and the
archive's public API, and never a hand-kept list: a work added to both surfaces
gets its redirect on the next build. It also takes every redirected address out
of public/sitemap.xml, since a sitemap should list only pages that answer 200.

    python3 scripts/redirects.py            # live API
    python3 scripts/redirects.py --archive-json works.json   # offline, a saved copy
    python3 scripts/redirects.py --report   # also print every non-exact match

What is left alone, on purpose:
- B-sides & Rarities (/oeuvre/exhibitions/…) and the Meaning Is Use essays
  (/oeuvre/philosophy/…) exist only here; they stay until the archive can hold
  exhibitions and writing.
- A work the archive does not have publicly keeps its page here.
- A tag the archive does not use keeps its page here.

Rules are explicit, one per address (Workers static assets allow 2,000 static
and 100 dynamic, and redirects win over a matching asset). Only the trailing-
slash form Zola serves is listed; a request without the slash gets the asset
handler's 307 to it first, then this 301.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zola_paths import CONTENT, ROOT, is_rendered, permalink_for, slugify, split_frontmatter  # noqa: E402

ARCHIVE = "https://archive.kyleparkercunningham.com"
API = ARCHIVE + "/api/v1/works?per_page=100&page={}"
# Cloudflare's Browser Integrity Check refuses Python's default user agent.
UA = "kpc-site-redirects/1 (+https://kyleparkercunningham.com)"
PUBLIC = ROOT / "public"
STATIC_LIMIT = 2000

# Sections of the oeuvre that hold things the archive has no place for yet.
KEEP_SECTIONS = {"exhibitions", "philosophy"}
WORK_RE = re.compile(r"^/oeuvre/([^/]+)/(\d{4})/([^/]+)/$")


def archive_works(saved: str | None) -> list[dict]:
    if saved:
        return json.loads(Path(saved).read_text())
    works, page = [], 1
    while True:
        req = urllib.request.Request(API.format(page), headers={"User-Agent": UA})
        data = json.load(urllib.request.urlopen(req, timeout=30))
        works += data["works"]
        if len(works) >= data["total"] or not data["works"]:
            return works
        page += 1


class _NoFollow(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def forwarded(slug: str) -> str | None:
    """The archive's current slug for one it has renamed, from its own forward.

    The archive answers a renamed work's old address with a 301 to the new one
    (its prints spec, § names), so a site page whose slug the archive no
    longer uses is sent straight to where the work is now, not through a
    second hop.
    """
    req = urllib.request.Request(f"{ARCHIVE}/works/{urllib.parse.quote(slug)}", method="HEAD",
                                 headers={"User-Agent": UA})
    try:
        urllib.request.build_opener(_NoFollow).open(req, timeout=20)
        return None
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location", "") if e.code in (301, 308) else ""
    # The archive answers with a path; accept a full URL too.
    m = re.match(r"(?:" + re.escape(ARCHIVE) + r")?/works/([^/?#]+)$", loc)
    return urllib.parse.unquote(m.group(1)) if m else None


def norm_title(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--archive-json", help="read the archive's works from a saved API dump")
    ap.add_argument("--report", action="store_true", help="print every non-exact mapping")
    args = ap.parse_args()

    if not (PUBLIC / "index.html").exists():
        sys.exit("public/ has no build; run `zola build` first")

    works = archive_works(args.archive_json)
    by_slug = {w["slug"]: w for w in works}
    by_title: dict[tuple[str, int | None], list[dict]] = {}
    for w in works:
        by_title.setdefault((norm_title(w["title"]), w["date"]["year"]), []).append(w)
    archive_terms: dict[str, set[str]] = {}
    archive_years: set[tuple[str, int]] = set()  # (category, year) pairs that hold a work
    for w in works:
        for kind, terms in w["terms"].items():
            archive_terms.setdefault(kind, set()).update(t["slug"] for t in terms)
        for t in w["terms"].get("category", []):
            archive_years.add((t["slug"], w["date"]["year"]))

    rules: list[tuple[str, str, str]] = []  # (source, target, class)
    notes: list[str] = []
    kept: list[str] = []

    def add(src: str, dst: str, cls: str) -> None:
        if not src.startswith("/") or src.rstrip("/") == "":
            return
        # An alias may name an address another, living page now answers at;
        # a redirect there would take that page down, so it is reported instead.
        page = PUBLIC / src.strip("/") / "index.html"
        if (cls.endswith("alias") and page.exists()
                and 'http-equiv="refresh"' not in page.read_text(encoding="utf-8", errors="ignore")):
            kept.append(f"{src} — an alias, but a live page answers there; not redirected")
            return
        rules.append((src, dst, cls))

    # 1. Work pages, and every alias that points at one.
    for path in sorted(CONTENT.glob("oeuvre/**/*.md")):
        rel = path.relative_to(CONTENT)
        fm, _ = split_frontmatter(path)
        if not is_rendered(rel, fm) or rel.name == "_index.md":
            continue
        url = permalink_for(rel, fm)
        m = WORK_RE.match(url)
        if not m or m.group(1) in KEEP_SECTIONS:
            continue
        slug, year = m.group(3), int(m.group(2))
        hit, how = by_slug.get(slug), "slug"
        if hit is None and not args.archive_json:
            new = forwarded(slug)
            if new is not None and new in by_slug:
                hit, how = by_slug[new], "forward"
        if hit is None:
            cands = by_title.get((norm_title(str(fm.get("title", ""))), year), [])
            if len(cands) == 1:
                hit, how = cands[0], "title+year"
        if hit is None:
            kept.append(f"{url} — no public archive work matches '{fm.get('title')}' ({year})")
            continue
        target = f"{ARCHIVE}/works/{hit['slug']}"
        if how != "slug":
            notes.append(f"{url} → {target} (by {how}: '{fm.get('title')}' = '{hit['title']}')")
        add(url, target, "work")
        for alias in fm.get("aliases", []) or []:
            a = "/" + str(alias).strip("/") + "/"
            if a != url:
                add(a, target, "work alias")

    # 2. The oeuvre's index pages: the whole catalogue, each medium, each year.
    for path in sorted(CONTENT.glob("oeuvre/**/_index.md")):
        rel = path.relative_to(CONTENT)
        fm, _ = split_frontmatter(path)
        url = permalink_for(rel, fm)
        parts = [p for p in url.strip("/").split("/")][1:]  # after "oeuvre"
        if parts and parts[0] in KEEP_SECTIONS:
            continue
        query: dict[str, str] = {}
        if parts and parts[0] in archive_terms.get("category", set()):
            query["category"] = parts[0]
        elif parts:
            kept.append(f"{url} — the archive has no category '{parts[0]}'")
            continue
        if len(parts) > 1 and parts[1].isdigit():
            # Where the two surfaces date a work differently the archive's
            # year page can be empty; the whole medium beats an empty page.
            if (query.get("category"), int(parts[1])) in archive_years:
                query["year"] = parts[1]
            else:
                notes.append(f"{url} → medium only: the archive has no {query.get('category')} in {parts[1]}")
        if not query:
            query["sort"] = "-year"  # the site's oeuvre index reads newest year first
        target = f"{ARCHIVE}/works?{urllib.parse.urlencode(query)}"
        add(url, target, "index")
        for alias in fm.get("aliases", []) or []:
            a = "/" + str(alias).strip("/") + "/"
            if a != url:
                add(a, target, "index alias")

    # 3. Tag pages, where the archive uses the same tag.
    tags_dir = PUBLIC / "tags"
    archive_tags = archive_terms.get("tag", set())
    if tags_dir.is_dir():
        add("/tags/", f"{ARCHIVE}/works", "tag")
        for d in sorted(p for p in tags_dir.iterdir() if p.is_dir()):
            if d.name in archive_tags:
                add(f"/tags/{d.name}/", f"{ARCHIVE}/works?tag={d.name}", "tag")
            else:
                kept.append(f"/tags/{d.name}/ — the archive has no tag '{d.name}'")

    # One rule per source; a later duplicate would never fire.
    seen: dict[str, str] = {}
    out: list[tuple[str, str, str]] = []
    for src, dst, cls in rules:
        if src in seen:
            if seen[src] != dst:
                notes.append(f"{src} claimed twice: {seen[src]} and {dst}; first kept")
            continue
        seen[src] = dst
        out.append((src, dst, cls))
    if len(out) > STATIC_LIMIT:
        sys.exit(f"{len(out)} rules is over the {STATIC_LIMIT} static redirect limit")
    too_long = [s for s, d, _ in out if len(f"{s} {d} 301") > 1000]
    if too_long:
        sys.exit(f"rules over 1,000 characters: {too_long}")

    lines = [
        "# Generated by scripts/redirects.py — do not edit by hand.",
        "# The catalogue lives at the archive; these addresses answer 301 there.",
    ]
    lines += [f"{src} {dst} 301" for src, dst, _ in out]
    (PUBLIC / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # The sitemap lists only pages that answer 200.
    sm = PUBLIC / "sitemap.xml"
    gone = {"https://kyleparkercunningham.com" + s for s in seen}
    text = sm.read_text(encoding="utf-8")
    blocks = re.findall(r"\s*<url>.*?</url>", text, flags=re.S)
    def answers(loc: str) -> bool:
        # Zola lists an empty taxonomy (/topics/) it never renders; drop those too.
        path = loc.removeprefix("https://kyleparkercunningham.com").strip("/")
        return loc not in gone and (PUBLIC / path / "index.html").exists() if path else True
    kept_blocks = [b for b in blocks if answers(re.search(r"<loc>(.*?)</loc>", b).group(1))]
    head, tail = text.split("<url>", 1)[0].rstrip(), "\n</urlset>\n"
    sm.write_text(head + "".join(kept_blocks) + tail, encoding="utf-8")

    counts: dict[str, int] = {}
    for _, _, cls in out:
        counts[cls] = counts.get(cls, 0) + 1
    print(f"_redirects: {len(out)} rules " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    print(f"sitemap.xml: {len(blocks)} → {len(kept_blocks)} urls")
    print(f"left on the site: {len(kept)}")
    if args.report:
        for n in notes:
            print("  ~ " + n)
        for k in kept:
            print("  = " + k)
    return 0


if __name__ == "__main__":
    sys.exit(main())
