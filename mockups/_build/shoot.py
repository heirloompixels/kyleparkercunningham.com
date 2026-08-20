#!/usr/bin/env python3
"""Screenshot mockups at desktop and phone width, and report console errors,
horizontal overflow, and any image that failed to load.

    python3 mockups/_build/shoot.py 36 37 40
    python3 mockups/_build/shoot.py all
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
MOCKUPS = ROOT / "mockups"
SHOTS = Path("/tmp/claude-0/-home-user-kyleparkercunningham-com/"
             "0ec09b2e-cbdc-5487-8b1f-950701dea235/scratchpad/shots")
BROWSER = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


def files(args):
    if not args or args == ["all"]:
        return sorted(p for p in MOCKUPS.glob("[3-9][0-9]-*.html"))
    out = []
    for a in args:
        out += sorted(MOCKUPS.glob(f"{a}-*.html"))
    return out


def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    targets = files(sys.argv[1:])
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=BROWSER)
        for f in targets:
            for label, w, h, full in (("desk", 1440, 900, True), ("phone", 390, 844, False)):
                page = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
                errs, bad = [], []
                page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e: errs.append(str(e)))
                page.on("requestfailed", lambda r: bad.append(r.url.split("/")[-1]))
                page.goto(f"file://{f}", wait_until="load")
                page.wait_for_timeout(700)
                # force lazy images in view for the full-page shot
                if full:
                    page.evaluate(
                        "async()=>{for(const i of document.images){i.loading='eager';}"
                        "window.scrollTo(0,document.body.scrollHeight);"
                        "await new Promise(r=>setTimeout(r,900));window.scrollTo(0,0);"
                        "await new Promise(r=>setTimeout(r,400));}"
                    )
                info = page.evaluate(
                    "()=>({ow:document.documentElement.scrollWidth,"
                    "iw:window.innerWidth,"
                    "h:document.documentElement.scrollHeight,"
                    "broken:[...document.images].filter(i=>i.complete&&i.naturalWidth===0)"
                    ".map(i=>i.getAttribute('src')).slice(0,5)})"
                )
                out = SHOTS / f"{f.stem}-{label}.png"
                try:
                    page.screenshot(path=str(out), full_page=full and info["h"] < 24000)
                except Exception as e:  # very tall pages
                    page.screenshot(path=str(out))
                flags = []
                if info["ow"] > info["iw"] + 2:
                    flags.append(f"OVERFLOW-X {info['ow']}>{info['iw']}")
                if info["broken"]:
                    flags.append(f"BROKEN IMG {info['broken']}")
                if errs:
                    flags.append(f"CONSOLE {errs[:2]}")
                if bad:
                    flags.append(f"404 {sorted(set(bad))[:4]}")
                print(f"{f.name:34} {label:5} {info['h']:>6}px  {' | '.join(flags) or 'ok'}")
                page.close()
        br.close()
    print("shots →", SHOTS)


if __name__ == "__main__":
    main()
