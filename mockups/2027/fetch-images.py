#!/usr/bin/env python3
"""Rebuild works.js and img/ for the 2027 sketchbook from the archive's public API.

The images are not committed (about 20 MB). Run this from mockups/2027/ to view
the sketches locally: python3 fetch-images.py && python3 -m http.server
Facts only: descriptions are left out, because about half of them were drafted
by a model and only Kyle's words go on the site.
"""
import json, os, subprocess, urllib.request, concurrent.futures as cf

API = "https://archive.kyleparkercunningham.com/api/v1/works?per_page=100&page={}"
BEST = set(open("best.txt").read().split())

works, page = [], 1
while True:
    data = json.load(urllib.request.urlopen(API.format(page)))
    works += data["works"]
    if len(works) >= data["total"]:
        break
    page += 1

os.makedirs("img", exist_ok=True)
out, jobs = [], []
for x in works:
    pi = x.get("primary_image")
    if not pi:
        continue
    s, d, t = x["slug"], x.get("dimensions") or {}, x["terms"]
    out.append(dict(
        slug=s, title=x["title"], year=x["date"]["year"], date=x["date"]["display"],
        medium=x["medium"], h=d.get("height_mm"), w=d.get("width_mm"),
        tags=[k["name"] for k in t.get("tag", [])], cat=[k["name"] for k in t.get("category", [])],
        series=[k["name"] for k in t.get("series", [])],
        coll=[(k["name"], k["number"]) for k in t.get("collection", [])],
        status=x["status"], iw=pi["width"], ih=pi["height"], hex=pi.get("dominant_color"),
        pal=[p["hex"] for p in (pi.get("palette") or [])], alt=pi.get("alt"), best=s in BEST))
    jobs.append((pi["thumb_url"], f"img/{s}-480.jpg"))
    if s in BEST:
        ladder = sorted(pi["srcset"], key=lambda v: v["width"])
        big = [v for v in ladder if v["width"] >= 960] or ladder[-1:]
        jobs.append((big[0]["url"], f"img/{s}-960.jpg"))

def get(job):
    url, path = job
    if not os.path.exists(path):
        subprocess.run(["curl", "-sf", "-o", path, url], check=False)

with cf.ThreadPoolExecutor(12) as ex:
    list(ex.map(get, jobs))

with open("works.js", "w") as f:
    f.write("window.IMG_BASE = window.IMG_BASE || 'img/';\n")
    f.write("window.WORKS = " + json.dumps(out, ensure_ascii=False) + ";\n")
    f.write("window.img = (w, size) => window.IMG_BASE + w.slug + '-' + (size === 960 && w.best ? 960 : 480) + '.jpg';\n")
print(len(out), "works,", len(jobs), "images")
