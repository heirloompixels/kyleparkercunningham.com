#!/usr/bin/env python3
"""The controlled vocabulary for oeuvre tags: synonym merges, cuts, and the
place hierarchy. Every other script in this directory imports `canon()` from here.

The raw tagging pass (scripts/tagging/tags.jsonl) is deliberately over-specific —
it records what a work actually is, in whatever words fit. This module is where
that becomes a vocabulary: near-synonyms collapse, forty variants of "pale gray
ground" become `gray`, and a specific place drags its general place along with it.

Editing this file re-canonicalises every work at once. That is the point: renaming
a tag across the whole oeuvre is a one-line change here plus a re-run of
build_manifest.py / apply_tags.py. Never hand-edit canonical tags into a work page.

Rules, in the order canon() applies them:
  1. MEDIUM_DUP  — dropped; already carried by `category` / `[extra] medium`
  2. DROP        — dropped; vague abstractions that don't help anyone find a work
  3. COLOUR_ALIAS— "<colour> ground/sky/palette/accent" folds to the bare colour
  4. MERGE       — near-synonyms fold to one canonical term (followed transitively)
  5. PLACE_PARENT— a specific place also emits the general place(s) above it

See docs/tagging-proposal.md for the reasoning and the resulting constellation.
"""
from __future__ import annotations

# --- 3. palette -------------------------------------------------------------
# Surface behaviour (thick impasto, scumbled ground, grisaille) is a different
# kind of fact and stays out of here — it lives in MERGE under "process / form".
COLOUR_ALIAS = {
    "gray ground": "gray", "gray white": "gray", "gray palette": "gray",
    "gray blue": "gray", "pale gray ground": "gray", "gray sky": "gray",
    "white and gray": "gray", "monochrome ground": "gray",
    "gray green ground": "green", "pale green": "green", "yellow green": "green",
    "yellow green ground": "green", "olive green": "olive",
    "pale blue": "blue", "blue palette": "blue", "deep blue": "blue",
    "sky blue": "blue", "slate blue": "blue", "cerulean": "blue",
    "blue violet": "violet", "blue and gold": "gold",
    "pale yellow ground": "yellow", "yellow ground": "yellow", "yellow accent": "yellow",
    "gold horizon": "gold", "gold ground": "gold", "golden": "gold",
    "orange red": "orange", "orange accent": "orange", "orange ground": "orange",
    "orange sky": "orange", "burnt orange": "orange",
    "coral sky": "coral", "rust red": "rust",
    "red earth": "red", "red line": "red", "red outline": "red", "crimson": "red",
    "pink ground": "pink", "pink arc": "pink", "pink sky": "pink",
    "lavender ground": "lavender", "aqua ground": "aqua", "tan ground": "tan",
    "beige ground": "beige", "cream ground": "cream", "warm ground": "cream",
    "dark ground": "black", "black ground": "black", "white ground": "white",
    "turquoise accent": "turquoise",
    "pastel ground": "pastel",
}

# --- 4. synonyms ------------------------------------------------------------
MERGE = {
    "ochre ground": "ochre", "pale ground": "pale palette", "sea": "ocean",
    "deep sea": "ocean", "surface": "ocean", "bubble": "bubbles",
    "prose poem": "poem", "thought": "mind", "expansion": "mind",
    "distance": "solitude", "tunnel": "perspective", "text": "hand lettering",
    "backpack": "hiking", "hat": "costume", "towing": "transplant",
    # --- near-synonyms ------------------------------------------------------
    "linework": "line work", "single line": "contour line", "outline": "contour line",
    "outlined form": "contour line", "hand-drawn line": "line work", "line": "line work",
    "buffalo": "bison", "sperm whale": "whale", "mountain lion": "puma", "big cat": "puma",
    "maize": "corn", "clouds": "cloud", "animals": "creature", "animal": "creature",
    "creatures": "creature", "invented creature": "creature", "magical creature": "creature",
    "hands": "hand", "faces": "face", "eye": "eyes", "ribs": "ribcage", "bone": "anatomy",
    "skeleton": "anatomy", "dissection": "anatomy", "cross-section": "anatomy",
    "architecture of the body": "anatomy", "tortoise": "turtle", "songbird": "bird",
    "honeybee": "bee", "pollinator": "bee", "crocodile": "crocodilian",
    "reptile": "crocodilian", "grizzly": "bear", "polar bear": "bear", "mammoth": "megafauna",
    "elder tree": "ancient tree", "portrait of a tree": "tree", "canopy": "tree", "bark": "tree",
    "roots": "tree", "leaves": "tree", "forest": "tree", "pine": "conifer", "sequoia": "conifer",
    "giant sequoia": "conifer", "cottonwood": "tree", "seedling": "seed", "sprout": "seed",
    "seed head": "seed", "root vegetable": "garden", "beetroot": "beet",
    "wildflower": "flower", "sunflower": "flower", "barrel cactus": "cactus", "saguaro": "cactus",
    "prickly pear": "cactus", "amanita muscaria": "mushroom", "fungi": "mushroom",
    "mycelium": "mushroom", "desert flora": "desert",
    "cumulus": "cloud", "water vapor": "cloud", "atmospheric river": "cloud", "thermals": "sky",
    "atmosphere": "sky", "storm": "lightning", "overtone": "harmonics", "phases": "lunar cycle",
    "celestial": "moon", "sunlight": "sun", "sunset": "twilight",
    "alpenglow": "twilight", "fire": "wildfire", "melting": "climate change",
    "water scarcity": "drought", "scarcity": "drought", "heat": "drought",
    "mountain": "mountains", "valley": "mountains", "volcano": "mountains", "altitude": "mountains",
    "cliff": "canyon", "arroyo": "canyon", "mesa": "canyon", "rock": "geology", "strata": "geology",
    "sediment": "geology", "stone": "geology", "erosion": "geology", "plains": "great plains",
    # --- figures ------------------------------------------------------------
    "standing figures": "figure", "attenuated figure": "figure", "hooded figure": "figure",
    "curled figure": "figure", "fetal position": "curled figure", "nude": "figure",
    "two figures": "figure", "four figures": "figure", "six figures": "figure",
    "seven figures": "figure", "group": "crowd", "procession": "crowd",
    "likeness": "portrait", "portrait practice": "portrait", "mother and child": "family",
    "child": "family", "elder": "family", "partner": "jeannie", "widower": "grief",
    "calavera": "skull", "horse skull": "skull",
    # --- objects / technology -----------------------------------------------
    "mason jar": "glass jar", "canning jar": "glass jar", "bell jar": "glass jar",
    "glass dome": "glass jar", "glass globe": "glass jar", "glass sphere": "glass jar",
    "drinking glass": "rocks glass", "mug": "vessel", "carafe": "vessel",
    "espresso machine": "coffee", "aeropress": "coffee", "loppers": "scissors",
    "weapon": "tool", "sledgehammer": "tool", "projectile point": "clovis point",
    "lunar lander": "spacecraft", "geodesic dome": "spacecraft",
    "zeppelin": "airship", "hot air balloon": "airship",
    "parachute": "flight", "airlift": "flight", "airdrop": "flight", "descent": "flight",
    "lifting": "flight", "radar": "satellite dish", "radio": "satellite dish",
    "broadcast": "communication", "speaker": "sound", "amplifier": "sound",
    "vacuum tube": "analog", "typewriter": "analog",
    "node": "network", "circuit": "network", "wireframe": "network",
    "capacitor": "energy", "electricity": "energy", "wall outlet": "energy", "cord": "energy",
    "space suit": "space helmet", "glass helmet": "space helmet", "diving helmet": "space helmet",
    "respirator": "breathing apparatus", "oxygen tank": "breathing apparatus",
    "hazmat suit": "breathing apparatus", "oxygen": "breathing apparatus",
    "astronaut": "space exploration", "space": "space exploration", "spaceport": "space exploration",
    "ufo": "flying saucer", "camper": "teardrop trailer", "vehicle": "teardrop trailer",
    "boat": "coracle", "winch": "machine", "pulley": "machine", "harness": "machine",
    "prosthetic": "machine", "string": "tether", "thread": "tether", "leash": "tether",
    "pin": "specimen", "paper crane": "origami", "fold": "origami",
    "hive": "bee", "swarm": "bee",
    # --- themes -------------------------------------------------------------
    "loss": "grief", "elegy": "grief", "dread": "grief", "hope and dread": "grief",
    "death": "memento mori",
    "fear and awe": "awe", "wonder": "awe", "sublime": "awe", "reverence": "awe",
    "gratitude": "awe", "wilderness": "wildness", "nature": "ecology",
    "interconnection": "interdependence", "cooperation": "mutual aid", "rescue": "mutual aid",
    "provision": "mutual aid", "protection": "mutual aid", "assisted migration": "transplant",
    "rewilding": "de-extinction", "endurance": "survival",
    "scavenging": "salvage", "recycling": "salvage", "silicon chips": "salvage",
    "recycled libraries": "salvage", "cargo cult": "salvage",
    "evolution": "adaptation", "indigenous technology": "agriculture", "staple food": "food",
    "gardening": "garden", "pruning": "garden", "compost": "garden",
    "home": "domesticity", "kitchen": "domesticity",
    "ritual": "everyday ritual", "sacrament": "everyday ritual", "altar": "devotion",
    "object portrait": "still life", "warmth": "tenderness", "gentleness": "tenderness",
    "touch": "intimacy", "embrace": "intimacy", "friendship": "companionship",
    "whimsy": "humor", "mischief": "play", "mythology": "myth", "creation myth": "myth",
    "ancient cycles": "cyclic time", "non-linear time": "cyclic time",
    "childhood memory": "memory", "continuity": "lineage", "generational knowledge": "lineage",
    "youth": "biography", "anniversary": "biography",
    "exposure": "being seen", "watching": "gaze", "observation": "gaze", "looking": "gaze",
    "surveillance": "gaze", "awareness": "gaze", "listening": "gaze",
    "self": "identity", "disguise": "concealment", "equilibrium": "balance",
    "seriality": "repetition", "rhythm": "repetition", "variation": "repetition",
    "stillness": "patience", "slowness": "patience", "waiting": "patience",
    "quiet": "solitude", "loneliness": "solitude", "isolation": "solitude",
    "anonymity": "solitude", "modesty": "solitude",
    "conservation": "preservation", "containment": "preservation",
    "collection": "specimen", "entomology": "specimen", "microscopy": "specimen",
    "algebra": "mathematics", "golden ratio": "fibonacci",
    "atom": "physics", "matter and antimatter": "physics",
    "order": "order and chaos", "monastery": "zen", "platonic solid": "sacred geometry",
    "icon": "sacred ground",
    "philosophical investigations": "wittgenstein", "use": "wittgenstein",
    "public practice": "wittgenstein",
    "machine meaning": "artificial intelligence",
    "large language models": "artificial intelligence",
    "stochastic parrots": "artificial intelligence",
    "interpretability": "artificial intelligence",
    "global workspace": "artificial intelligence", "grounding": "artificial intelligence",
    "anthropic": "artificial intelligence",
    "authored by claude": "human and machine", "collaboration": "human and machine",
    "post-human": "post-collapse",
    # --- process / form -----------------------------------------------------
    "scrubbed surface": "scumbled ground", "palette knife": "scraped surface",
    "raw surface": "gestural", "fast painting": "gestural", "expressionism": "gestural",
    "gesture": "gestural", "gestural ground": "gestural", "hand mark": "gestural",
    "stroke as unit": "gestural", "drips": "gestural", "monochrome": "grisaille",
    "hand-colored variant": "hand-colored", "black and white with color": "hand-colored",
    "unique impression": "open edition", "small edition": "edition variants",
    "handmade paper": "hand-torn paper", "brown paper": "hand-torn paper",
    "cream paper": "hand-torn paper",
    "found object": "found wood", "found panel": "found wood", "raw wood": "found wood",
    "weathered wood": "found wood", "exposed wood grain": "found wood",
    "distressed paint": "found wood", "stacked boards": "assemblage",
    "revision": "reworked painting", "nine years": "slow painting",
    "in progress": "work in progress", "unfinished": "work in progress",
    "plein air sketch": "plein air", "mural study": "cross-medium motif",
    "series origin": "series", "serial work": "series",
    "woven ground": "raw linen ground", "textile ground": "raw linen ground",
    "carving": "direct carving", "tool marks": "direct carving",
    "dimensions variable": "site-specific",
    "log book": "studio journal", "studio practice": "studio",
    # --- composition --------------------------------------------------------
    "two by two": "grid", "lattice": "grid",
    "nested form": "concentric", "rings": "concentric", "tree rings": "concentric",
    "orbit": "concentric", "segmented arc": "concentric",
    "coil": "spiral", "accordion": "segmentation",
    "radial composition": "radial", "radiating lines": "radial", "rays": "radial",
    "fan": "radial", "wedge": "radial",
    "scatter composition": "scatter", "all-over composition": "scatter",
    "dense hang": "salon hang", "frieze hang": "linear hang", "horizontal drift": "linear hang",
    "panorama": "panoramic format", "large plate": "large format", "monumental": "large format",
    "miniature": "small format", "off-center composition": "centered composition",
    "mirror symmetry": "symmetry", "emptiness": "negative space", "reduction": "minimal",
    "horizon line": "horizon", "upward view": "looking up",
    "faceted form": "faceted", "faceted landscape": "faceted", "faceted sky": "faceted",
    "faceted ground": "faceted", "cubist": "faceted", "block form": "faceted",
    "subdivision": "tessellation",
    "flat color": "flat ground", "flat field": "flat ground", "color bands": "gradient",
    "striped form": "stripes", "diamond": "pattern", "hexagon": "pattern",
    "pyramid": "triangle", "spire": "triangle", "oval": "circle", "egg": "circle",
    "three panels": "polyptych", "triptych": "polyptych", "diptych": "polyptych",
    "pair": "polyptych", "fifteen paintings": "polyptych", "twenty three paintings": "polyptych",
    "framed works": "framed", "white frames": "framed", "gold frame": "framed",
    "pine frame": "framed", "walnut frame": "framed",
    "white wall": "installation view", "gallery": "installation view",
    "studio archive": "archive", "scale contrast": "scale",
    # --- place / biography --------------------------------------------------
    "rio grande bosque": "rio grande", "southwest": "new mexico",
    "american west": "road life", "nomadism": "road life", "travel": "road life",
    "alpine climbing": "hiking", "day hike": "hiking",
    "sleeping outside": "camping", "glassing ridgelines": "hunting",
    "huckleberry": "foraging", "berries": "foraging",
    "friends": "companionship", "grandfather": "family", "inherited object": "family",
    "musician": "portrait", "michael": "portrait", "nana": "portrait",
    "conversation": "portrait", "commission": "commissioned portrait",
    "dada ball": "community", "fundraiser": "community",
    "premonition": "lightning strike",
    "happiness": "joy", "celebration": "joy", "laughter": "joy",
}

# --- 1. already carried by front matter -------------------------------------
# `category` and `[extra] medium` hold these; repeating them as tags is dead weight.
MEDIUM_DUP = {
    "painting", "printmaking", "installation", "sculpture", "writing", "essay", "project",
    "oil on linen", "oil on panel", "oil on canvas", "oil", "acrylic", "latex", "oil stick",
    "paint marker", "canvas", "acm panel", "dibond", "gesso panel", "baltic birch",
    "rives bfk", "handwoven linen", "japanese ink", "spray paint", "marble",
    "colorado marble", "gouache", "watercolor", "drypoint", "intaglio", "website",
    "2026",
}

# --- 2. cuts ----------------------------------------------------------------
# Abstractions that describe a work without helping anyone find it. If one of
# these turns out to be a concept worth browsing by, move it out of here.
DROP = {
    "abstraction and realism", "air", "apocalypse", "architecture", "ascension",
    "authorship", "biomorphic", "birth", "conformity", "connectivity", "constraint",
    "convergence", "correction", "curiosity", "daily practice", "daily reality",
    "darkness", "dependency", "deployment", "digital", "division", "doubt", "dream",
    "duality", "dwelling", "emotion", "epistemic humility", "epistemology", "existence",
    "experience", "finitude", "fog", "futility", "glow", "humanness", "impermanence",
    "individuality", "infrastructure", "intuition", "inversion", "labor", "leisure",
    "longing", "luminosity", "making of", "mystery", "news", "night version",
    "nonconformity", "ongoing", "partnership", "path", "permanence", "pilgrimage",
    "potential", "protest", "reckoning", "recombination", "return", "scale",
    "social awkwardness", "spring", "study", "summer", "symbol", "symbolism",
    "transformation", "village", "vulnerability", "wariness", "weathered", "wholeness",
    "winter",
}

# --- 5. place hierarchy -----------------------------------------------------
# Kyle, Aug 2026: place should be dual — general and deep. Tag a work with the
# actual place; the general one follows automatically. Values may be a string or
# a tuple when a place rolls up two ways (the Chihuahuan Desert is both a desert
# and in New Mexico). Chains resolve transitively: aldo leopold wilderness ->
# gila -> new mexico.
PLACE_PARENT = {
    "truth or consequences": "new mexico",
    "desert archaic": "truth or consequences",
    "las cruces": "new mexico",
    "tres piedras": "new mexico",
    "taos": "new mexico",
    "adobe canyon": "new mexico",
    "nogal canyon": "new mexico",
    "black range": "new mexico",
    "gila": "new mexico",
    "gila wilderness": "gila",
    "aldo leopold wilderness": "gila",
    "rio grande": "new mexico",
    "bosque del apache": "rio grande",
    "rio grande rift": "rio grande",
    "chihuahuan desert": ("desert", "new mexico"),
    "grand enchantment trail": "new mexico",
    "absaroka mountains": "montana",
    "little belt mountains": "montana",
    "dharamshala": "india",
}


def canon(tags):
    """Raw tags -> canonical tags, order preserved, duplicates removed."""
    out = []
    for tag in tags:
        t = tag.strip().lower()
        if t in MEDIUM_DUP or t in DROP:
            continue
        t = COLOUR_ALIAS.get(t, t)
        seen = set()
        while t in MERGE and MERGE[t] != t and t not in seen:
            seen.add(t)
            t = MERGE[t]
        if t not in out:
            out.append(t)
    # Walk each place up to the general place(s) above it. Appending while
    # iterating is intentional — it resolves chains in one pass.
    i = 0
    while i < len(out):
        parents = PLACE_PARENT.get(out[i], ())
        if isinstance(parents, str):
            parents = (parents,)
        for parent in parents:
            if parent not in out:
                out.append(parent)
        i += 1
    return out
