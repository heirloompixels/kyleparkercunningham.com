# Oeuvre tagging

Tooling for the tag vocabulary described in [docs/tagging-proposal.md](../../docs/tagging-proposal.md).

The design premise: **works get tagged once, in their own words, and canonicalised
forever after.** `tags.jsonl` is the hand-authored record — what a work is, in whatever
terms fit it. `vocabulary.py` turns that into a controlled vocabulary. Renaming a tag
across the whole oeuvre is a one-line change in `vocabulary.py` plus a re-run; it is
never a find-and-replace across 160 content files.

## Files

| file | what it is |
|---|---|
| `tags.jsonl` | **The data.** One row per work: `{file, note, tags}`. Hand-authored, keyed by repo-relative path. This is the irreplaceable part. |
| `vocabulary.py` | Merge rules, cuts, and the place hierarchy. Exports `canon()`. |
| `works.py` | Reads `content/oeuvre/` into records; joins them to `tags.jsonl`. Run it bare for a status summary. |
| `build_manifest.py` | Renders `docs/tagging-proposal.md`. Every count in that document is computed here. |
| `apply_tags.py` | Writes `[taxonomies] tags` into front matter. Dry run by default. |
| `review_images.py` | Downscales each work's main image into `.tagging-review/` so the images can actually be looked at during a pass. |

## The loop

Check what's on disk versus what's tagged:

```sh
python3 scripts/tagging/works.py
```

It reports counts, and names any work page missing a `tags.jsonl` row (**untagged** —
new work) or any row whose page has gone (**orphaned** — renamed or deleted). Both are
warnings, not errors; the other scripts skip untagged pages and refuse to apply while
rows are orphaned.

Tagging a new or backfilled work:

1. `python3 scripts/tagging/review_images.py` — regenerate the review images.
2. Read the page: front matter, prose, alt text; look at its image in `.tagging-review/`.
3. Append a row to `tags.jsonl`. Tag liberally and specifically — 8–15 terms, in
   whatever words are true. Don't pre-canonicalise; that is what `vocabulary.py` is for.
   Do use the actual specific place; the general one is generated.
4. `python3 scripts/tagging/build_manifest.py` — regenerate the proposal doc and see
   where the new tags landed.
5. `python3 scripts/tagging/apply_tags.py` to preview, `--apply` to write.

Changing the vocabulary — a rename, a merge, a new place level — is step 4 and 5 only.

## Row format

```json
{"file": "content/oeuvre/painting/2021/the-mother-bear/index.md",
 "note": "A dark brown bear turned to face the viewer, built in thick oil-stick…",
 "tags": ["bear", "grizzly", "animal encounter", "montana", "absaroka mountains", "…"]}
```

`note` is prose for the manifest — what the work is, what its text says, what the image
shows. It is the reason the manifest is readable, and it is what makes a re-read cheap
a year from now.

## Before applying

`tags` must be declared in `config.toml`, or Zola ignores the block:

```toml
taxonomies = [
  {name = "topics", feed = true},
  {name = "tags", feed = true},
]
```

`topics` stays with the notes section; `tags` is the oeuvre's.

## Caveats

- `apply_tags.py` **overwrites** any `[taxonomies]` block it finds. Hand edits there
  will be lost — edit `tags.jsonl`.
- `works.py` parses front matter with regexes rather than a TOML parser, matching the
  house style of `generate_site_index.py`. It reads scalar keys only.
- **Zola takes `[taxonomies]` on pages only.** A section `_index.md` carrying one fails
  the build (`unknown field taxonomies`). Project-type works are sections, so a landing
  page listed in `PROJECT_INDEXES` is read for the manifest but never written to —
  `apply_tags.py` skips it and says so. If a project's tags need to be live, put them on
  one of its child pages.
- Tag pages render through `templates/tags/list.html` and `templates/tags/single.html`
  (the ledger, filtered). `templates/tags/list.html` holds a `hidden` list for tags that
  should group works without being advertised; their term pages still exist and work.
