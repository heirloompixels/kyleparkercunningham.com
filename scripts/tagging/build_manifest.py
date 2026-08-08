#!/usr/bin/env python3
"""Render docs/tagging-proposal.md from tags.jsonl + the content tree.

The manifest is generated, never hand-edited: every count in it is computed at
build time, so re-running after a vocabulary change or a batch of new tag rows
keeps the prose honest. Edit the narrative sections here, the vocabulary in
vocabulary.py, and the per-work tags in tags.jsonl.

Usage:  python3 scripts/tagging/build_manifest.py
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from works import ROOT, load_joined                      # noqa: E402
from vocabulary import DROP, MEDIUM_DUP, PLACE_PARENT    # noqa: E402

OUT = ROOT / "docs" / "tagging-proposal.md"

# Axes are a presentation device, not a constraint on the vocabulary — a tag not
# listed here still works, it just shows up under "Unsorted long tail".
AXES = [
 ("Series & bodies of work", [
  "animist solarpunk", "post-collapse", "the memory of atmosphere", "geometric anatomy",
  "ephemera series", "cyclum lunarem", "meaning is use", "language game",
  "atmospheric whales", "field theory", "manifesto image", "approximate completion",
  "harmonics", "series", "recurring motif", "cross-medium motif", "companion piece",
  "survey", "exhibition", "installation view", "archive"]),
 ("Subject — creatures", [
  "creature", "bird", "whale", "bear", "elephant", "owl", "bee", "bison", "rhino",
  "butterfly", "megafauna", "sandhill crane", "crocodilian", "turtle", "puma", "robot",
  "ghost", "narwhal", "octopus", "giraffe", "ant", "dragonfly", "worm", "monarch",
  "flicker", "crane", "saber tooth", "insect", "animal portrait", "anthropomorphism",
  "upright animal", "grazing", "shell", "feather", "bird feet", "stalked eyes", "pet",
  "human and animal", "spider silk", "teeth", "tusk", "larvae", "pollen"]),
 ("Subject — plants, land & sky", [
  "tree", "cloud", "sky", "desert", "juniper", "alligator juniper", "conifer",
  "landscape", "lightning", "geology", "moon", "garden", "seed", "corn", "cactus",
  "weather", "water cycle", "plankton", "cell", "bonsai", "blue corn", "growth",
  "flower", "mushroom", "sun", "lunar cycle", "rain", "wildfire", "drought", "harvest",
  "food", "agriculture", "ancient tree", "rainbow", "twilight", "autumn", "seasons",
  "solstice", "equinox", "monsoon", "shade", "shadow", "ice", "arctic", "ocean",
  "great plains", "wind", "dust", "carrot", "beet", "pumpkin", "vines", "tendrils",
  "leaf motif", "organic form", "sand mandala", "night", "horizon"]),
 ("Subject — human & body", [
  "figure", "portrait", "face", "anatomy", "head", "hand", "skull", "crowd", "profile",
  "mask", "eyes", "gaze", "ribcage", "family", "jeannie", "self portrait",
  "commissioned portrait", "double portrait", "curled figure", "intimacy", "row",
  "brain", "arm", "lungs", "halo", "mind", "consciousness", "identity", "concealment",
  "memento mori", "white hair", "glasses", "beanie", "flannel", "trousers", "suspenders",
  "costume", "masquerade", "mountain clothes", "long neck", "dot eyes", "silhouette",
  "rider", "chain of hands", "holding hands", "daydream", "buddha", "binoculars",
  "diver", "psychological"]),
 ("Subject — objects, tools & technology", [
  "still life", "machine", "space helmet", "glass jar", "tool", "tether",
  "breathing apparatus", "satellite dish", "spacecraft", "technology", "coffee",
  "domestic object", "origami", "airship", "antenna", "network", "rocket", "coracle",
  "flight", "vessel", "specimen", "analog", "energy", "communication", "sound",
  "clovis point", "flying saucer", "teardrop trailer", "invented technology",
  "space exploration", "kite", "scissors", "beer can", "rocks glass", "olympus",
  "tecate", "boombox", "gas mask", "exploded view", "diagram", "botanical plate", "web",
  "tower", "cruciform", "bubbles", "glassblowing", "handmade craft", "zigzag", "wreath",
  "dodecahedron", "crystal", "molecule", "physics", "sacred geometry", "fibonacci",
  "mathematics"]),
 ("Themes & concerns", [
  "humor", "deep time", "salvage", "time", "memory", "absurdism", "awe", "mutual aid",
  "extinction", "tenderness", "climate grief", "grief", "balance", "future", "survival",
  "attention", "patience", "solitude", "wildness", "everyday ritual", "mundane",
  "interdependence", "adaptation", "climate change", "transplant", "de-extinction",
  "intelligence of nature", "anthropocentrism", "ecology", "fable", "domesticity",
  "companionship", "community", "joy", "play", "aging", "ancestors", "lineage",
  "being seen", "fragility and force", "irony", "myth", "cyclic time", "preservation",
  "first contact", "migration", "surreal", "folk-modern", "poem", "zen", "meditation",
  "buddhism", "philosophy", "wittgenstein", "artificial intelligence",
  "human and machine", "paleoindian", "pleistocene", "poaching", "satao", "drones",
  "pesticide", "pollination", "life cycle", "fertility", "interspecies negotiation",
  "sacred ground", "ritual observation", "folk song", "folk vernacular",
  "indigenous visual vocabulary", "rock art", "petroglyph", "dia de los muertos",
  "refusal", "no deletion", "public rewriting", "version history", "collaborative text",
  "revision as succession", "duck rabbit", "abduction", "submersion", "stampede",
  "buffalo jump", "departure", "vacation", "calendar", "atmospheric light",
  "concentric eye", "music", "witness", "theft", "paradox", "order and chaos"]),
 ("Form, composition & surface", [
  "abstraction", "line work", "geometry", "gestural", "pattern", "triangle",
  "small format", "concentric", "minimal", "grid", "circle", "thick impasto", "faceted",
  "spiral", "scatter", "hard edge", "high chroma", "flat ground", "framed",
  "crosshatching", "contour line", "large format", "plate tone", "polyptych",
  "square format", "symmetry", "tessellation", "close crop", "centered composition",
  "vertical format", "panoramic format", "narrow format", "sphere", "enso",
  "negative space", "dense black", "grisaille", "scumbled ground", "raw linen ground",
  "gesso ground", "stripes", "gradient", "color field", "white on white", "stippling",
  "chiaroscuro", "realism", "black and white", "scraped surface", "perspective",
  "looking up", "frontal composition", "segmentation", "radial", "progression",
  "cluster", "square", "rectangle", "salon hang", "linear hang", "branching form",
  "hourglass", "pale palette", "pastel", "flesh tones", "warm palette", "light",
  "accumulation", "arrows", "hand lettering"]),
 ("Palette", [
  "orange", "blue", "green", "white", "yellow", "red", "gray", "pink", "teal", "gold",
  "ochre", "purple", "turquoise", "black", "coral", "cream", "navy", "lavender", "mauve",
  "rust", "violet", "terracotta", "olive", "peach", "plum", "magenta", "amber", "salmon",
  "aqua", "tan", "periwinkle", "beige", "rose", "brown"]),
 ("Place — general", [
  "new mexico", "montana", "india", "amsterdam", "desert", "great plains", "ocean",
  "place"]),
 ("Place — deep", [
  "truth or consequences", "desert archaic", "gila", "gila wilderness",
  "aldo leopold wilderness", "black range", "nogal canyon", "adobe canyon", "las cruces",
  "tres piedras", "taos", "rio grande", "bosque del apache", "rio grande rift",
  "chihuahuan desert", "grand enchantment trail", "absaroka mountains",
  "little belt mountains", "dharamshala", "continental divide", "creek", "canyon",
  "mountains"]),
 ("Life & practice", [
  "private collection", "sold", "on loan", "hand-colored", "hand-torn paper",
  "found wood", "reworked painting", "slow painting", "site-specific", "assemblage",
  "edition variants", "open edition", "artist proof", "gold leaf", "chine-colle",
  "direct carving", "work in progress", "plein air", "photograph", "studio journal",
  "studio", "mixed media", "works on paper", "process", "biography", "pandemic",
  "lightning strike", "hiking", "camping", "thru-hiking", "early work", "road life",
  "hunting", "foraging", "animal encounter", "devotion", "repetition"]),
]
AXES = [(name, list(dict.fromkeys(tags))) for name, tags in AXES]

GROUPS = [
 ("Paintings", "painting"),
 ("Prints", "printmaking"),
 ("Installations", "installation"),
 ("Other", "other"),
 ("Sculpture", "sculpture"),
 ("Exhibitions", "exhibitions"),
]

works, untagged, orphaned = load_joined()
C = collections.Counter(t for w in works for t in w["canon"])
RAW = collections.Counter(t for w in works for t in w["tags"])
INSTANCES = sum(C.values())
AVG = INSTANCES / len(works)
SINGLES = sum(1 for n in C.values() if n == 1)
SPINE = sum(1 for n in C.values() if n >= 10)
IMAGED = [w for w in works if w["images"]]
PALETTE_N = sum(1 for t in dict(AXES)["Palette"] if t in C)

L = []
w = L.append


def n(tag):
    return C.get(tag, 0)


w(f"""# Tagging the oeuvre — analysis and proposed manifest

*Generated by `scripts/tagging/build_manifest.py`. Do not edit this file by hand —
edit the narrative in that script, the vocabulary in `scripts/tagging/vocabulary.py`,
or the per-work tags in `scripts/tagging/tags.jsonl`, then re-run it.*

*First pass drafted by Claude, August 2026; revised after Kyle's answers to the open
questions. Expect to revise it repeatedly — the works are being backfilled with more
text and more images over time, and the vocabulary is meant to move with them.*

---

## What this is

Every work in `content/oeuvre/` read end to end — the front matter, the body prose,
the alt text on every image, and the main image of each work looked at directly — and
a set of proposed tags derived from all of it together. {len(works)} entries:
{len(IMAGED)} works with images, plus the *Meaning Is Use* essays and the project
landing page they hang off.

The goal was not to tag each work in isolation but to find the vocabulary the oeuvre
already has. So the method was: tag liberally and specifically first ({sum(RAW.values()):,}
raw tag instances, {len(RAW):,} distinct terms), then look at what recurred, collapse
the synonyms and the over-granular variants, and see what constellation was left
standing.

**What was left standing: {len(C)} distinct tags, {INSTANCES:,} instances, averaging
{AVG:.1f} tags per work.** {SPINE} tags carry ten or more works each — that {SPINE} is
the actual spine.

---

## The shape of it

A few things became obvious only once all {len(works)} were laid side by side, and they
should probably drive how the tags get used on the site:

**1. There is one enormous body of work that has never been named on the site.**
{n('animist solarpunk')} works belong to what you call, in the *Arm Fauna* (2014) text,
"an anamistic solarpunk future" — animals using the detritus of collapsed human
civilization to survive. Elephant with a rocket, rhino with a satellite dish, sandhill
cranes stripping a spacecraft, polar bears blowing glass bubbles, robot bison hunted
for their chips, whales and octopuses towing trees to new homes, an ant in a space
helmet winching a mushroom. It runs 2014 → 2023, across painting *and* printmaking,
and it is the single largest coherent thing in the oeuvre.
`animist solarpunk` ({n('animist solarpunk')}) and `post-collapse` ({n('post-collapse')})
are its two tags.

**2. The lightning strike of September 2023 is a hinge, and the work knows it.**
*Harmonics* and *First Contact* (2023) come immediately after; the whole 2024 sky
body follows. And it is foreshadowed: *120 Volts* (2018) is a figure plugged into a
wall outlet by his own hair, which you gloss as "five years before the sky demonstrated
the high-voltage version on me personally." `lightning strike` ({n('lightning strike')})
marks the biographical event; `the memory of atmosphere` ({n('the memory of atmosphere')})
marks the body of work.

**3. Motifs cross media constantly, and that crossing is itself worth indexing.**
{n('cross-medium motif')} works are a second take on an image made in another medium —
*Butterfly Conundrum* painted 2015 / printed 2021, *Crystal Tooth Whale* painted 2018 /
printed 2023, *Rocket Propelled Clovis Point* painted 2020 / printed 2022 (where a
turtle takes over the delivery), *Three Blue Corn* / *Blue Corn*,
*Tugboat Whale Sequoia* / *Gardener*, *Expansion*, *Skull*, *Elephant Mask*,
*Field Theory*. `cross-medium motif` makes that visible as a structure rather than a
coincidence.

**4. Three alligator junipers, three moons, three coffee vessels, six pines, seven
ghosts, seven figures, six creatures.** The work counts things and returns to them.
`recurring motif` ({n('recurring motif')}) and the specific subject tags
(`alligator juniper` {n('alligator juniper')}, `lunar cycle` {n('lunar cycle')},
`coffee` {n('coffee')}) both earn their place.

**5. The abstract work and the animal work are not separate practices — they share a
formal vocabulary.** `concentric` ({n('concentric')}), `circle` ({n('circle')}),
`spiral` ({n('spiral')}), `triangle` ({n('triangle')}), `grid` ({n('grid')}),
`repetition` ({n('repetition')}) run from *Enso* (2015) through *Cadence*,
*Transition*, *Approximate Completion*, the 2024 orbit paintings, and out into
*Cyclum Lunarem*'s gold-leaf moon grid and *Balance*'s scattered paper triangles. The
geometry is the throughline.

**6. Portraiture is the quiet third practice.** {n('portrait')} portraits, and the good
ones carry their occasion in the text: Ken had just told you Kathy died; Nana's face is
"a map and I painted every road"; Mika's first huckleberry. `portrait` ({n('portrait')}),
`commissioned portrait` ({n('commissioned portrait')}), `realism` ({n('realism')}).

---

## Conventions the tagging follows

**Medium is not duplicated in tags.** `oil on linen`, `drypoint`, `intaglio`,
`acrylic` and friends already live in `[extra] medium` and would be dead weight
repeated as tags. What *is* tagged is practice that the medium string doesn't
capture: `hand-colored` ({n('hand-colored')}), `hand-torn paper` ({n('hand-torn paper')}),
`found wood` ({n('found wood')}), `gold leaf` ({n('gold leaf')}),
`open edition` ({n('open edition')}), `chine-collé`, `direct carving`,
`reworked painting` ({n('reworked painting')}), `slow painting` ({n('slow painting')}),
`plein air`.

**Category and year are not duplicated either** — `category` and `year` are already
front matter, so no `painting` / `2021` tags.

**Colour is tagged, but flattened.** The raw pass produced `pale gray ground`,
`gray white`, `gray palette`, `warm ground`, `tan ground`, `beige ground` and about
forty other near-identical variants. All fold to a plain palette term (`gray`, `cream`,
`ochre`). Surface behaviour stays separate and is a different kind of fact:
`thick impasto` ({n('thick impasto')}), `scumbled ground`, `scraped surface`,
`grisaille`, `white on white`, `raw linen ground`.

**Provenance is tagged.** `private collection` ({n('private collection')}),
`sold` ({n('sold')}), `on loan` ({n('on loan')}) — see the open item below on whether
this duplicates `[extra] status`.

**{SINGLES} tags are used exactly once.** Most are concrete subject nouns — `narwhal`,
`buddha`, `giraffe`, `pumpkin`, `boombox`, `dodecahedron` — and those are precisely
what makes a subject index worth having, so they stay. The vague one-offs
("existence", "convergence", "transformation", "duality", "wholeness") were cut; the
full cut list is in Appendix C.

---

## Settled

**1. The taxonomy is `tags`, not `topics`.** `topics` stays with the notes section;
`tags` gets declared alongside it in `config.toml`:
""")

w("""
```toml
taxonomies = [
  {name = "topics", feed = true},
  {name = "tags", feed = true},
]
```
""")

w(f"""
**2. `animist solarpunk` is an internal tag for now.** It groups the
{n('animist solarpunk')} works without appearing as a label on the front end. The name
is yours — from the *Arm Fauna* text of 2014 — but it can stay behind the curtain until
you want to say it out loud.

**3. The palette axis stays.** All {PALETTE_N} colour tags in use. It is a real index
of your colour, and it costs nothing to carry.

**4. Place is dual — general *and* deep.** Every work that names a specific place
carries both, so the ledger can be browsed either way. A work made at Nogal Canyon
carries `nogal canyon` *and* `new mexico`; the Black Fire painting carries
`aldo leopold wilderness` → `gila` → `new mexico`; the Absaroka bear carries
`absaroka mountains` *and* `montana`. The general tag is generated from the deep one by
`PLACE_PARENT` in `vocabulary.py`, so tagging a work with its actual place is enough —
the parent follows automatically, transitively, at build time.

The hierarchy as it stands:

| deep | rolls up to |
|---|---|
""")
_children = collections.defaultdict(list)
for child, parents in PLACE_PARENT.items():
    key = parents if isinstance(parents, str) else " + ".join(parents)
    _children[key].append(child)
for parent in sorted(_children):
    w(f"| {', '.join(sorted(_children[parent]))} | {parent} |\n")

w(f"""
`new mexico` reaches {n('new mexico')} works under this rule and
`truth or consequences` {n('truth or consequences')}. Adding a level later — a
`southwest` above the states, say — is one line in `PLACE_PARENT`.

**5. This document is a first pass, not a verdict.** The works are going to be
backfilled with more prose and more images, and the tagging will be revised alongside
them for a long while. Nothing here is load-bearing: tags can be renamed in bulk from
`vocabulary.py`, axes split or collapsed in `build_manifest.py`, and the whole thing
re-run over richer text whenever a batch of work pages gets deepened. See
`scripts/tagging/README.md` for the loop.

---

## Still worth deciding, when you get to it

- **Provenance tags.** `private collection` ({n('private collection')}),
  `sold` ({n('sold')}), `on loan` ({n('on loan')}) partly duplicate `[extra] status`.
  Harmless, but redundant if the ledger already surfaces it.
- **The thin works.** *Abduction*, *Mycellium*, *Continuation*, *Prophets*, both
  *Tomorrow* installations and *Solstice* have almost no text; their tags lean entirely
  on the image and are correspondingly shallow. Good candidates for the first round of
  backfill — the tags will get better on their own once the prose exists.

---

## How these would be applied

Flat lowercase phrases in a `[taxonomies]` block, written by
`scripts/tagging/apply_tags.py`:
""")

w('''
```toml
+++
title = "the mother bear"
date = 2021-11-13
category = "painting"
year = 2021

[taxonomies]
tags = [
  "bear", "animal encounter", "wildness", "climate grief", "drought",
  "absaroka mountains", "montana",          # deep place, then general
  "hiking", "thick impasto", "gestural", "ochre", "white", "large format",
]

[extra]
medium = "Oil, Oil Stick, Acrylic and Latex on Canvas"
dimensions = "51 1/2 x 32 inches"
+++
```

---
''')

# ---------------------------------------------------------------- vocabulary
w(f"\n## The constellation\n\n{len(AXES)} axes. Counts are how many of the "
  f"{len(works)} entries carry the tag.\n")
placed = set()
for name, tags in AXES:
    placed.update(tags)
    present = sorted(((t, C[t]) for t in tags if C.get(t)), key=lambda x: (-x[1], x[0]))
    if not present:
        continue
    w(f"\n### {name}  *({len(present)} tags)*\n")
    w(" · ".join(f"**{t}** {c}" if c >= 10 else f"{t} {c}" for t, c in present) + "\n")

unplaced = sorted(t for t in C if t not in placed)
if unplaced:
    w(f"\n### Unsorted long tail  *({len(unplaced)} tags)*\n\n")
    w("Tags in use that no axis claims — either genuinely miscellaneous, or a sign an\n"
      "axis list in `build_manifest.py` needs updating.\n\n")
    w(" · ".join(f"{t} {C[t]}" for t in unplaced) + "\n")

# ------------------------------------------------------------------ manifest
w(f"""
---

## The manifest

{len(works)} entries. Each gives what the front matter records, what the work's own text
says, what the main image actually shows, and the proposed tags.
""")


def entry(work):
    title = work["title"] or "(untitled)"
    w(f"\n#### {title} · {work['year'] or '—'}\n")
    w(f"`{work['file']}`  \n")
    meta = [x for x in (work["medium"], work["dimensions"], work["status"]) if x]
    count = len(work["images"])
    meta.append(f"{count} image" + ("s" if count != 1 else ""))
    w("*" + " · ".join(meta) + "*\n\n")
    w(work["note"] + "\n\n")
    w("**Tags** — " + " · ".join(f"`{t}`" for t in work["canon"]) + "\n")


for gname, category in GROUPS:
    items = sorted((x for x in works if x["category"] == category),
                   key=lambda x: (x["year"], x["title"].lower()))
    if not items:
        continue
    w(f"\n---\n\n### {gname}  *({len(items)})*\n")
    year = None
    for item in items:
        if item["year"] != year:
            year = item["year"]
            w(f"\n**{year}**\n")
        entry(item)

rest = [x for x in works if x["category"] not in {c for _, c in GROUPS}]
if rest:
    w(f"\n---\n\n### Meaning Is Use  *({len(rest)})*\n")
    w("\nA project rather than an object: a section landing page plus three essays.\n\n"
      "Zola accepts `[taxonomies]` on **pages only** — a section `_index.md` carrying one\n"
      "fails the build — so the landing page's row below is a record for this document,\n"
      "not something written to the file. Its project-level mechanics tags (public\n"
      "rewriting, version history, no deletion, collaborative text) were moved onto\n"
      "*Through the Same Forms as Everyone*, the making-of essay, which is where they\n"
      "actually describe the prose. `duck rabbit` names the landing page's cover image\n"
      "and had no essay to move to, so it lives here and nowhere else.\n")
    # Landing page first, then the essays in their front-matter `weight` order —
    # the same order the project template renders them in.
    rest.sort(key=lambda x: (not x["file"].endswith("_index.md"),
                             int(x["weight"] or 0), x["file"]))
    for item in rest:
        entry(item)

# ---------------------------------------------------------------- appendices
w("\n---\n\n## Appendix A — full canonical vocabulary by frequency\n\n")
w("| tag | works |\n|---|---|\n")
for t, c in sorted(C.items(), key=lambda x: (-x[1], x[0])):
    w(f"| {t} | {c} |\n")

merged = sorted(t for t in RAW if t not in C)
w(f"\n---\n\n## Appendix B — terms folded into others  *({len(merged)})*\n\n")
w("The raw pass produced these; each was merged into a canonical tag above, or dropped\n"
  "as a duplicate of an existing front-matter field. Listed so nothing is lost silently.\n\n")
w(", ".join(f"{t} ({RAW[t]})" for t in merged) + "\n")

w(f"\n---\n\n## Appendix C — terms cut outright  *({len(DROP)})*\n\n")
w("Abstractions that described the work without helping anyone find it. If any of these\n"
  "is actually a concept you want to index by, move it out of `DROP` in `vocabulary.py`.\n\n")
w(", ".join(sorted(DROP)) + "\n")

w(f"\n*Front-matter fields treated as already-carried and never repeated as tags: "
  f"{', '.join(sorted(MEDIUM_DUP))}.*\n")

OUT.write_text("".join(L), encoding="utf-8")

print(f"wrote {OUT.relative_to(ROOT)}")
print(f"  {len(works)} entries · {len(C)} tags · {INSTANCES:,} instances · {AVG:.1f} avg")
if untagged:
    print(f"  WARNING: {len(untagged)} work page(s) have no tags.jsonl row — not in the manifest:")
    for f in untagged:
        print("   ", f)
if orphaned:
    print(f"  WARNING: {len(orphaned)} tags.jsonl row(s) have no work page:")
    for f in orphaned:
        print("   ", f)
