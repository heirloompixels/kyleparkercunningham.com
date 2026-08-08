# Tag icons

Sourcing icons for the oeuvre tags — see [scripts/tagging/](../tagging/) for the tags
themselves and [docs/tagging-proposal.md](../../docs/tagging-proposal.md) for the vocabulary.

The premise: there are tens of thousands of good open-source icons already drawn, so the
first round is **selection, not illustration**. This directory downloads ten icon sets,
matches them against the tag vocabulary, and builds a sheet where every candidate is
inlined side by side so a choice can be made by eye. Custom drawing comes later, informed
by what the gaps turn out to be.

## Files

| file | what it is |
|---|---|
| `aliases.py` | **The data.** The alias table (tag → icon words), the axis grouping, the palette swatches, and the licence facts. Hand-authored; the only part that isn't re-derivable. |
| `fetch_sets.py` | `npm pack`s the ten sets into `.icon-sets/`, then re-reads every licence and flags drift against `aliases.SETS`. |
| `index_sets.py` | Indexes the sets into `.icon-sets/index.json` — name → SVG body, per style. |
| `match.py` | Tags × index → ranked candidates. Run bare for a coverage report, `--gaps` to list what matched nothing. |
| `build_mockup.py` | Builds `.icon-sets/tag-icons.html`, the picking sheet. |
| `picks.tsv` | Kyle's choices, once made: `tag⇥style⇥icon`. Absent until the first round comes back. |

`.icon-sets/` is gitignored — ~350 MB of downloaded sets plus a 32 MB index and a 2.4 MB
sheet, all reproducible in about a minute.

## The loop

```sh
python3 scripts/tag-icons/fetch_sets.py     # once, or after an upgrade
python3 scripts/tag-icons/index_sets.py     # after fetching
python3 scripts/tag-icons/match.py --gaps   # what matched, what didn't
python3 scripts/tag-icons/build_mockup.py   # -> .icon-sets/tag-icons.html
```

Then publish the sheet as an artifact to look at and pick from. **Copy picks** in the
sheet emits exactly the `picks.tsv` format; paste it into `scripts/tag-icons/picks.tsv`
and re-run `build_mockup.py` to have those choices pre-selected next round.

Improving a bad match is a line in `ALIASES` and a re-run — no need to re-fetch or
re-index.

## What the first round found

- **The line sets have almost no animals.** Lucide, Tabler, Feather and friends are UI
  vocabularies, so `whale` falls back to *fish*, `owl` to *bird*, `bison` to *cow*. Real
  animals come only from OpenMoji (line) and Material (flat). Since the oeuvre is
  animal-heavy, this is where custom drawing earns its keep first.
- **Colour tags shouldn't be icons.** All 34 matched nothing, which is the right answer —
  a colour is best drawn as itself. They render as swatches instead, from `PALETTE`.
- **211 tags have no candidate.** Mostly abstractions ("surreal", "mind") and surface
  descriptions ("scumbled ground") that may never want an icon — plus a few, like
  `clovis point` and `alligator juniper`, that are the real case for commissioning.

## Licences

Read from each package's own `package.json` by `fetch_sets.py`, which fails loudly if a
recorded licence stops matching. Nine of the ten are permissive and need only a credit:
Lucide (ISC); Tabler, Phosphor, Feather, Heroicons, Iconoir, Bootstrap (MIT); Remix and
Material Design (Apache-2.0, which also wants the NOTICE preserved).

**OpenMoji is CC-BY-SA-4.0** — attribution *and* share-alike. Untouched icons with a
colophon credit are fine; anything *adapted* from it must be released under the same
licence. It is also the only source with a bear, an owl and a narwhal, so it fills exactly
the gaps the UI sets leave. The recommendation on the sheet: use it to decide what an icon
should be, then redraw, rather than building a custom set on a share-alike foundation.

Whatever ships needs a credit line in the colophon naming the sets actually used.
