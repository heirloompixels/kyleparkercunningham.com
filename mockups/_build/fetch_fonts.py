#!/usr/bin/env python3
"""Pull the sketchbook's typefaces down into assets/fonts.

Self-hosting rather than linking Google keeps every mockup working with
no network at all — which matters, because a mockup that has to phone
home is not a mockup you can hand to somebody on a plane.

Latin subsets only. Run once.

    python3 mockups/_build/fetch_fonts.py
"""

import re
import subprocess
from pathlib import Path

FONTS = Path(__file__).resolve().parents[1] / "assets" / "fonts"

# family spec → local basename
FAMILIES = [
    ("Newsreader:ital,opsz,wght@0,6..72,200..700;1,6..72,200..600", "newsreader"),
    ("Archivo+Narrow:ital,wght@0,400..700;1,400..600", "archivo-narrow"),
    ("Instrument+Serif:ital@0;1", "instrument-serif"),
    ("IBM+Plex+Mono:ital,wght@0,300;0,400;0,500;0,600;1,400", "plex-mono"),
    ("IBM+Plex+Sans:ital,wght@0,300..700;1,400", "plex-sans"),
    ("Literata:ital,opsz,wght@0,7..72,300..700;1,7..72,300..500", "literata"),
    ("Bodoni+Moda:ital,opsz,wght@0,6..96,400..800;1,6..96,400..600", "bodoni-moda"),
    ("EB+Garamond:ital,wght@0,400..700;1,400..600", "eb-garamond"),
    ("Space+Grotesk:wght@300..700", "space-grotesk"),
    ("Space+Mono:ital,wght@0,400;0,700;1,400", "space-mono"),
    ("Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,300..700", "inter"),
    ("Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..700", "fraunces"),
    ("Cormorant+Garamond:ital,wght@0,300..700;1,300..600", "cormorant-garamond"),
    ("Syne:wght@400..800", "syne"),
    ("Bebas+Neue", "bebas-neue"),
    ("Xanh+Mono:ital@0;1", "xanh-mono"),
    ("Redaction:wght@300..700", "redaction"),
    ("Playfair+Display:ital,wght@0,400..900;1,400..700", "playfair-display"),
    ("Inconsolata:wght@200..900", "inconsolata"),
    ("IBM+Plex+Serif:ital,wght@0,300;0,400;0,500;1,300;1,400", "plex-serif"),
]

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0 Safari/537.36")


def curl(url, binary=False):
    r = subprocess.run(
        ["curl", "-sS", "-A", UA, "-L", url],
        capture_output=True, check=False,
    )
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def main():
    FONTS.mkdir(parents=True, exist_ok=True)
    css_out = ["/* Sketchbook typefaces, self-hosted. Latin subsets, woff2. */"]
    for spec, base in FAMILIES:
        url = f"https://fonts.googleapis.com/css2?family={spec}&display=swap"
        css = curl(url)
        if not css or "@font-face" not in css:
            print(f"  !! {base}: no css")
            continue
        blocks = re.findall(r"/\*\s*([\w\[\]-]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S)
        if not blocks:
            blocks = [("latin", m) for m in re.findall(r"@font-face\s*\{.*?\}", css, re.S)]
        kept = 0
        for label, block in blocks:
            if label not in ("latin", "latin-ext"):
                continue
            m = re.search(r"url\((https://[^)]+\.woff2)\)", block)
            if not m:
                continue
            src = m.group(1)
            style = "italic" if "font-style: italic" in block else "normal"
            fname = f"{base}-{label}-{style}.woff2"
            dest = FONTS / fname
            if not dest.exists():
                data = curl(src, binary=True)
                if not data or len(data) < 500:
                    print(f"  !! {fname}: download failed")
                    continue
                dest.write_bytes(data)
            block = block.replace(m.group(0), f"url({fname}) format('woff2')")
            block = re.sub(r"\s+", " ", block).strip()
            css_out.append(block)
            kept += 1
        size = sum(f.stat().st_size for f in FONTS.glob(f"{base}-*.woff2"))
        print(f"  {base:20} {kept} faces  {size/1024:.0f} KB")

    (FONTS / "fonts.css").write_text("\n".join(css_out) + "\n")
    total = sum(f.stat().st_size for f in FONTS.glob("*.woff2"))
    print(f"total {total/1_048_576:.2f} MB in {FONTS}")


if __name__ == "__main__":
    main()
