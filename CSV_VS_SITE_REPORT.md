# CSV vs. Site — paintings coverage audit

Generated 2026-05-19 by comparing [Kyle Oeuvre/Oeuvre-Table 1.csv](Kyle%20Oeuvre/Oeuvre-Table%201.csv) (exported from Kyle Oeuvre.numbers) against `content/oeuvre/`.

## Headline numbers

| | Count |
|---|---|
| Rows in CSV (all paintings) | **179** |
| Painting pages on site | **93** |
| CSV entries matched to a painting page | **58** |
| **CSV paintings missing from site (any discipline)** | **118** |
| CSV paintings already on site under a different discipline | **6** |
| Site paintings with no CSV entry | **39** (mostly 2023–2024 — CSV pre-dates them) |

## Caveats — read first

1. **The CSV is paintings-only.** It contains no printmaking, sculpture, installation, or cinema entries. So the print pages on the site (47 of them) are not represented in this audit.
2. **CSV is frozen around early 2024.** The Numbers file was last saved Jan 2024. That's why ~25 site paintings from 2024 have no CSV match — they were made after the spreadsheet.
3. **Granularity differs.** The CSV sometimes lists components separately while the site bundles them. Example: CSV has three rows for `Enso (1 of 3)`, `(2 of 3)`, `(3 of 3)` plus a `Three Cycles (Triptych)` summary — all four show as "missing" but the site has a single [`/oeuvre/painting/2015/enso/`](content/oeuvre/painting/2015/enso/) page covering them. There are similar cases.
4. **Typos in CSV affect matching.** `Coffee Caraffe` (CSV) vs `Coffee Carafe` (site), `Crystalized`, `Oragami`, `burd`, `Acrylica`, etc. — preserved as written in the spreadsheet.
5. **Reworks / cross-media.** Some CSV paintings exist on site as a *print* version (Butterfly Conundrum, Airlift, Lunar Lander, etc.) — the paintings are still missing their own pages.

---

## 6 CSV paintings that exist on site only as a print/other

These works have a print or "other" page on the site, but not a painting page. These are good candidates for cross-linking (like we just did for Butterfly Conundrum):

| CSV painting | Year | Existing site page (other discipline) |
|---|---|---|
| Lunar Lander | 2014 | `printmaking/2021/lunar-lander` |
| Airlift | 2015 | `printmaking/2021/airlift` |
| Skull | 2015 | `printmaking/2022/skull` |
| Blue Corn | 2016 | `printmaking/2022/blue-corn` |
| Blue Corn | 2016 (2nd entry) | `printmaking/2022/blue-corn` |
| Continuation | 2022 | `other/2022/continuation` |

---

## 118 CSV paintings missing from the site

Grouped by year. Format: `Title [Medium] — Size`

### 2002 (1)
- Circle Triangle Square (Study) [Acrylic & Latex on Canvas] — 24 x 10

### 2003 (1)
- Telephone [Oil on Canvas]

### 2004 (2)
- Two weird heads with red background [Oil on Canvas]
- Abstract shape thick impasto [Oil on Canvas]

### 2007 (1)
- Shell Woman [Watercolor on Paper]

### 2008 (2)
- Space Shot [Oil on Linen] — 16x20
- Tai Chi [Watercolor on Paper]

### 2009 (3)
- burd [Oil on Linen]
- Tent [Oil on Linen] — 16x20
- Tex [Oil on Panel]

### 2010 (3)
- Jars (Red) [Oil on Gesso Paper]
- Pool [Oil on Linen]
- Three Jars [Oil on Gesso Paper]

### 2011 (3)
- Indian Creek [Oil on Panel]
- Willow Tree [Oil on Linen]
- Yucca [Oil on Panel] — 12 x 14

### 2012 (9)
- Bison [Oil and Ink on Panel]
- Butterfly Circles [Oil on Panel]
- Field Theory (yellow & green) [Oil on Gesso Panel] — 14.5x11.75
- Millett [Oil on Panel] — 5x7
- Millett [Oil on Linen] — 13x21
- Portrait Circle Field [Oil on Panel]
- Robot [Oil on Gesso Panel] — 12x12
- Transitions [Oil on Panel]
- Zinnias [Oil on Gesso Panel] — 11.75 x 7.5

### 2013 (14)
- Bowl with Handle [Oil on Panel] — 8x8
- Bowl without Handle [Oil on Panel] — 8x8
- Disc [Oil on Linen]
- Dzogchen [Oil on Panel] — 9x12
- Enigma [Oil on Linen]
- Enso Pink and Turquoise [Oil on Panel]
- Exhale (man on red) [Oil on Gesso Panel] — 7x12
- Flying Cripply Yogi [Oil and ink on Gesso Panel] — 12x12
- Mask [Oil on Linen]
- Oil Cans (Two) [Oil on Linen]
- Pink Sunset [Oil on Panel]
- Sequence (Yellow) [Oil on Panel]
- Turtle Medicine [Oil on Panel] — 12x24
- Archaic Daydream [Oil on Linen] — 55 by 34 inches

### 2014 (12 — Coffee Caraffe = Coffee Carafe on site (typo); Lunar Lander exists as print)
- Coffee Caraffe [Oil on Panel] *(possible typo match: site has [`Coffee Carafe`](content/oeuvre/painting/2014/coffee-carafe/) — verify and dedupe)*
- Drip Coffee Maker [Oil on Panel]
- Field Theory (Pink Lines) [Oil on Linen] — 8x13
- Honey Bees #2 [Oil on Handwoven Linen]
- Honey Bubble [Oil on Handwoven Linen] — 6.5x11.75
- Lunarem (january 16–18th 2014) [Oil on Goldleaf on Panel] — 3x3
- Mario Incandenza [Oil on Handwoven Linen] — 10x16.5
- Oil Cans (Three, Yellow) [Oil on Handwoven Linen]
- Opalite [Oil on Handwoven Linen] — 5.5x6.5
- Orange Squares [Oil on Panel]
- Satao [Oil on Handwoven Linen]
- The Rain Shaker [Oil on Handwoven Linen] — 5.75x6.75
- Three Red Pears [Oil on Panel]

### 2015 (12 — note triptych granularity and Airlift→print)
- 3 Pears [Oil on Handwoven Linen] — 5.5x7
- Digital Nomads [Oil on Linen] — 13x21
- *Triptych group:* Enso (1 of 3), Enso (2 of 3), Enso (3 of 3), Three Cycles (Triptych) — *all four likely covered by existing single [`enso`](content/oeuvre/painting/2015/enso/) page; consider expanding or accepting as-is*
- Expanding [Oil on Panel]
- Field Theory (red) [Oil on Linen] — 13x21
- Lavender Rose [Oil on Gesso Panel] — 11.75x11.75
- Lunarem (9.22.15–9.25.15) [Oil on Goldleaf on Panel] — 3x3
- Scarf Wrapped Hair [Oil on Panel]
- Spheres [Oil on Gesso Panel] — 12x16.5
- Three Red Apples [Oil on Panel] — 8x8 *(duplicate entry in CSV)*
- Three Red Apples [Oil on Panel] *(duplicate entry in CSV)*
- Two Oil Cans [Oil on Linen] — 8.75 x 6.75
- Venus [Oil on Linen]
- Venus Wave [Oil on Linen]

### 2016 (20 — Blue Corn ×2 exist as print)
- Crystalized Bison [Acrylic and Spraypaint on Diabond, Oil]
- Cyclum Lunarem (summer 2016) [Oil on Goldleaf on Panel] — variable
- Diamondback [Oil on Gesso Panel] — 12x18
- Field Theory (orange) [Oil on Panel] — 13x13
- Gray Expansion [Oil on Panel]
- Hive [Oil on Panel] — 8x13
- Lucretia [Oil on Gesso Panel] — 12x20.5
- Oil Cans (Four) [Oil on Diabond]
- Oil Cans Golden [Oil on Panel]
- Oil Cans Kalashnikov [Oil on Panel]
- Oragami [Oil on Panel]
- Skull Study [Oil on Panel] — 8 7/8 x 11 3/4
- Spherical Expansion [Oil on Diabond]
- The Crystal Hammer [Oil on Linen]
- Transcendent [Oil on Diabond] — 11x14
- Triangle Hair [Oil on Diabond]
- Two Faces Intertwined [Oil on Linen] — 16x20
- Two Tipis [Oil on Diabond] — 5.5x5.5
- Vessel [Oil on Diabond]
- Woven Matter [Oil on Panel]

### 2017 (6)
- Diamond (orange) [Oil on Diabond] — 12x12
- Four Oil Cans [Oil on Diabond] — 6x9.5
- Oil Cans (yellow) [Oil on Gesso Panel] — 8x13
- Orange Diamond [Oil on Diabond]
- Pairs [Oil on Diabond] — 16x20
- Venus [Oil on Linen] — 13x21

### 2018 (9)
- 5.56 Nato [Oil on Linen] — 5x7
- Eleven PM [Oil on Linen] — 11x14
- Oil Cans (burnt sienna) [Oil on Linen] — 5x7
- Raven [Oil on Linen] — 11x14
- Teardrop (Yellow) [Oil on Linen] — 5x7
- Ten PM [Oil on Diabond] — 11.5x11.5
- The Last Rhino (Northern White) [Oil on Gesso Panel] — 8x13
- Collecting Time [Oil on Canvas] — 27 x 27
- Two Squash [Oil on Linen] — 11 x 14

### 2019 (2)
- Isolated Geography [Oil on Linen] — 11 x 14
- Intermittent Resolution [Oil on Linen] — 12 x 16

### 2020 (1)
- Airborn Pollen Eaters [Oil on Handloom Linen] — 6 5/8 x 11 3/4, 19 fringe, 31 overall

### 2022 (6 — Continuation exists as "other")
- Jeannie and Horse Skull [Oil on Panel] — 16 x 20
- Past Capacitor [Acrylic and Latex on Canvas] — 21 x 21
- Skeleton Vessel Balanced [Oil on Linen] — 21 x 34
- We are already living in the future nightmare we've been promised. [Oil on Linen] — 20 x 30
- Remembered Conglomerate of the Past [Oil on Panel (ACM)] — 24 x 20
- Josh [Oil on Diabond Panel] — 16 x 20

### Year unknown (5)
- India Works
- I am becoming all that I am
- Being with flower
- Golden Pears [Oil on Gesso Paper]
- Teardrop (Green) [Oil] — 5x7

---

## 39 site paintings with no CSV entry (mostly recent)

The CSV pre-dates 2024 and is incomplete for 2021–2023. Listed for reference — most just need adding to the spreadsheet, not the site.

| Year | Title | Path |
|---|---|---|
| 2014 | Coffee Carafe | `content/oeuvre/painting/2014/coffee-carafe/` *(probably = CSV "Coffee Caraffe")* |
| 2014 | espresso machine | `content/oeuvre/painting/2014/espresso-machine/` |
| 2018 | A. Muscaria | `content/oeuvre/painting/2018/a-muscaria/` |
| 2018 | Airdrop | `content/oeuvre/painting/2018/airdrop/` |
| 2018 | Flicker Rhino | `content/oeuvre/painting/2018/flicker-rhino/` |
| 2018 | Hands | `content/oeuvre/painting/2018/hands/` |
| 2018 | Narwhal | `content/oeuvre/painting/2018/narwhal/` |
| 2018 | Octobat | `content/oeuvre/painting/2018/octobat/` |
| 2019 | Monsoon Bird | `content/oeuvre/painting/2019/monsoon-bird/` |
| 2019 | Self Portrait | `content/oeuvre/painting/2019/self-portrait/` |
| 2020 | Nana | `content/oeuvre/painting/2020/nana/` |
| 2021 | rhino radar | `content/oeuvre/painting/2021/rhino-radar/` |
| 2021 | the berry picker | `content/oeuvre/painting/2021/the-berry-picker/` |
| 2021 | the mother bear | `content/oeuvre/painting/2021/the-mother-bear/` |
| 2021 | transplanter | `content/oeuvre/painting/2021/transplanter/` |
| 2023 | Autumnal Twilight | `content/oeuvre/painting/2023/autumnal-twilight/` |
| 2023 | Calavera Del Caballo | `content/oeuvre/painting/2023/calavera-del-caballo/` |
| 2023 | First Contact | `content/oeuvre/painting/2023/first-contact/` |
| 2023 | Geometric Anatomy | `content/oeuvre/painting/2023/geometric-anatomy/` |
| 2023 | Harmonics | `content/oeuvre/painting/2023/harmonics/` |
| 2024 | above the clouds | `content/oeuvre/painting/2024/above-the-clouds/` |
| 2024 | alpenglow at mineral creek with the adults after the babies have gone to sleep | `content/oeuvre/painting/2024/alpenglow-at-mineral-creek-with-the-adults-after-the-babies-have-gone-to-sleep/` |
| 2024 | bottled lightning | `content/oeuvre/painting/2024/bottled-lightning/` |
| 2024 | does math control nature? | `content/oeuvre/painting/2024/does-math-control-nature/` |
| 2024 | equilateral equilibrium | `content/oeuvre/painting/2024/equilateral-equilibrium/` |
| 2024 | felt and lived | `content/oeuvre/painting/2024/felt-and-lived/` |
| 2024 | low angle sun rays | `content/oeuvre/painting/2024/low-angle-sun-rays/` |
| 2024 | orbits (plankton dreaming of a sedimentary afterlife) | `content/oeuvre/painting/2024/orbits-plankton-dreaming-of-a-sedimentary-afterlife/` |
| 2024 | out there, on the horizon, a solitary cloud | `content/oeuvre/painting/2024/out-there-on-the-horizon-a-solitary-cloud/` |
| 2024 | pollen and larvae | `content/oeuvre/painting/2024/pollen-and-larvae/` |
| 2024 | separate, yet delicate, representations of existence | `content/oeuvre/painting/2024/separate-yet-delicate-representations-of-existence/` |
| 2024 | symbologies intertwine electronically | `content/oeuvre/painting/2024/symbologies-intertwine-electronically/` |
| 2024 | the algebra of water vapor | `content/oeuvre/painting/2024/the-algebra-of-water-vapor/` |
| 2024 | the atmosphere's electric finger | `content/oeuvre/painting/2024/the-atmospheres-electric-finger/` |
| 2024 | the river in the sky | `content/oeuvre/painting/2024/the-river-in-the-sky/` |
| 2024 | towers | `content/oeuvre/painting/2024/towers/` |
| 2024 | triangular circles | `content/oeuvre/painting/2024/triangular-circles/` |
| 2024 | twenty-one years | `content/oeuvre/painting/2024/twenty-one-years/` |
| 2024 | two squared | `content/oeuvre/painting/2024/two-squared/` |
