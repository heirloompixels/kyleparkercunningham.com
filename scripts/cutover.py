#!/usr/bin/env python3
"""Move kyleparkercunningham.com and www from GitHub Pages to the kpc-site Worker.

    scripts/cutover.py           save the GitHub Pages records, delete them, deploy with the domains
    scripts/cutover.py --undo    detach the Worker's domains and put the saved records back
    scripts/cutover.py --check   exit 1 while GitHub Pages' records still hold the names

docs/hosting.md § cutover is the why. The four apex A records and the www CNAME
that point at GitHub Pages are written to docs/cutover-github-pages-records.json
before they are deleted, so --undo can put back exactly what was there. Nothing
else in the zone is touched: mail, Mailgun, the Search Console and tzprofiles
records, the archive, daybook, reception and media all stay as they are.
"""
import json, os, subprocess, sys, time, urllib.error, urllib.request

ACCOUNT = "0170b714b0ee025091fed8a088f7a65a"
ZONE = "eeaaf1265b97b78a7c7a3962077062fa"
HOSTS = ["kyleparkercunningham.com", "www.kyleparkercunningham.com"]
WORKER = "kpc-site"
STAGED = "https://kpc-site.torc.workers.dev"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVED = os.path.join(ROOT, "docs", "cutover-github-pages-records.json")
UA = "kpc-site-cutover/1 (+https://kyleparkercunningham.com)"


def token():
    # Read the token from the file rather than the environment, and never print it.
    for line in open(os.path.expanduser("~/.config/cloudflare/torc.env")):
        key, _, value = line.strip().partition("=")
        if key == "CLOUDFLARE_API_TOKEN":
            return value.strip().strip('"').strip("'")
    sys.exit("no CLOUDFLARE_API_TOKEN in ~/.config/cloudflare/torc.env")


def cf(method, path, body=None):
    req = urllib.request.Request(
        "https://api.cloudflare.com/client/v4" + path,
        method=method,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + token(), "Content-Type": "application/json", "User-Agent": UA},
    )
    try:
        with urllib.request.urlopen(req) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        d = json.load(e)
    if not d.get("success"):
        sys.exit(f"{method} {path} failed: {d.get('errors')}")
    return d["result"]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def get(url):
    """Status, Server header and Location of one request, never following a redirect."""
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        r = opener.open(req, timeout=20)
    except urllib.error.HTTPError as e:
        r = e
    return r.status if hasattr(r, "status") else r.code, r.headers.get("Server", ""), r.headers.get("Location", "")


def pages_records():
    found = []
    for host in HOSTS:
        for r in cf("GET", f"/zones/{ZONE}/dns_records?name={host}&per_page=100"):
            if r["type"] in ("A", "AAAA", "CNAME"):
                found.append({k: r[k] for k in ("id", "type", "name", "content", "ttl", "proxied")})
    return found


def cut_over():
    status, _, _ = get(STAGED + "/")
    redirect = get(STAGED + "/oeuvre/other/2022/abduction/")
    if status != 200 or redirect[0] != 301 or "archive.kyleparkercunningham.com/works/abduction" not in redirect[2]:
        sys.exit(f"the staged Worker is not right ({status}, {redirect}); deploy it first: scripts/deploy-worker.sh")

    records = pages_records()
    if not records:
        sys.exit("no A/AAAA/CNAME records on the apex or www: already cut over? Nothing done.")
    if any(r["type"] != "CNAME" and not r["content"].startswith("185.199.") for r in records) or any(
        r["type"] == "CNAME" and r["content"] != "heirloompixels.github.io" for r in records
    ):
        sys.exit(f"these are not the GitHub Pages records this script expects; nothing done:\n{json.dumps(records, indent=2)}")

    with open(SAVED, "w") as f:
        json.dump(records, f, indent=2)
        f.write("\n")
    print(f"saved {len(records)} records to {os.path.relpath(SAVED, ROOT)}")

    for r in records:
        cf("DELETE", f"/zones/{ZONE}/dns_records/{r['id']}")
        print(f"deleted {r['type']} {r['name']} {r['content']}")

    print("deploying with the custom domains (scripts/deploy-worker.sh)")
    if subprocess.call([os.path.join(ROOT, "scripts", "deploy-worker.sh")], cwd=ROOT) != 0:
        sys.exit("the deploy failed; the GitHub Pages records are deleted. Run scripts/cutover.py --undo to put them back.")

    # Resolvers may hold the old GitHub Pages addresses for up to five minutes,
    # and the certificate takes a moment, so wait for Cloudflare to answer.
    for host in HOSTS:
        for _ in range(40):
            try:
                status, server, _ = get(f"https://{host}/")
            except Exception as e:  # certificate not issued yet, connection reset
                status, server = 0, repr(e)[:60]
            if status in (200, 301) and server.lower() == "cloudflare":
                print(f"{host}: {status} from cloudflare")
                break
            time.sleep(15)
        else:
            print(f"{host}: not yet answering from cloudflare ({status} {server}); this resolver may still hold GitHub's address")
    print("next: docs/hosting.md § cutover, steps 4 to 6")


def undo():
    if not os.path.exists(SAVED):
        sys.exit(f"{os.path.relpath(SAVED, ROOT)} is missing; nothing to put back")
    for host in HOSTS:
        for d in cf("GET", f"/accounts/{ACCOUNT}/workers/domains?hostname={host}"):
            if d.get("service") == WORKER:
                cf("DELETE", f"/accounts/{ACCOUNT}/workers/domains/{d['id']}")
                print(f"detached {host} from {WORKER}")
    present = {(r["type"], r["name"], r["content"]) for r in pages_records()}
    for r in json.load(open(SAVED)):
        if (r["type"], r["name"], r["content"]) in present:
            continue
        cf("POST", f"/zones/{ZONE}/dns_records",
           {"type": r["type"], "name": r["name"], "content": r["content"], "ttl": r["ttl"], "proxied": r["proxied"]})
        print(f"restored {r['type']} {r['name']} {r['content']}")
    print("GitHub Pages serves the site again once resolvers catch up (up to five minutes).")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--undo"]:
        undo()
    elif args == ["--check"]:
        sys.exit(1 if pages_records() else 0)
    elif not args:
        cut_over()
    else:
        sys.exit(__doc__)
