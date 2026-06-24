# Editions — the living homepage

The homepage is not a fixed landing page. It is the **current edition**: a
seasonally-composed magazine "issue" built around whatever the studio is
actually doing. When the season turns, that issue **retires, unchanged, to a
permanent address** under `/editions/`, and a new one takes the front page.
Projects can be interspersed between seasons.

- The front page (`index.html`) renders whichever edition is `status = "live"`.
- `/editions/` is the shelf: the live issue + every retired one.
- Each edition has a permanent home at `/editions/<slug>/`.

## Content model

`content/editions/<slug>/index.md`, front matter `[extra]`:

| Field | Meaning |
|-------|---------|
| `kind` | `"season"` or `"project"` |
| `numeral` | Roman numeral (auto-assigned by `edition.sh new`) |
| `status` | `"staging"` → `"live"` → `"retired"` |
| `lifespan` | e.g. `"Lives March — June 2026"` (tense flips to "lived" on retire) |
| `cover`, `cover_alt`, `cover_tag` | Cover image + alt + small label |
| `deck` | One-line italic standfirst |
| `dateline` | Place/line under the deck |
| `ornament` | A glyph (e.g. `❦`) used as a section divider |
| `sign_off` | Closing line in the colophon |
| `author` | `kyle` / `claude` (for the manifest) |

The body uses the editorial shortcode vocabulary: `plate`, `diptych`,
`wallquote`, `marginalia`, `interlude`. See an existing edition's `index.md`
(e.g. `content/editions/2026-spring/index.md`) for usage. Drop an `edition.css`
next to the `index.md` for per-edition art direction (auto-loaded).

## Workflow — `scripts/edition.sh`

```
./scripts/edition.sh new <slug> "<Title>" [season|project]
        # scaffolds content/editions/<slug>/index.md as draft + staging,
        # auto-assigns the next Roman numeral.

./scripts/edition.sh serve
        # regenerates data + `zola serve --drafts` so you can build the
        # staged edition in real time (preview at /editions/<slug>/).

./scripts/edition.sh list
        # lists editions with their status.

./scripts/edition.sh promote <slug>
        # retires the currently-live edition (flips status → retired, stamps
        # the date, flips the lifespan tense) and promotes <slug>:
        # removes draft, sets status = "live", stamps the published date.
```

## Staging model

- A staged edition is `draft = true` + `status = "staging"` → **invisible in
  production**, visible with `zola serve --drafts` (i.e. `edition.sh serve`).
- `promote` is the single command that swaps the front page. Only one edition
  should be `live` at a time.
- Retired editions keep their exact markup and URL forever — that's the point.

**Current state:** `2026-spring` ("The Memory of Atmosphere", Season XII) is
live. `2026-summer` exists as a draft Kyle is writing.
