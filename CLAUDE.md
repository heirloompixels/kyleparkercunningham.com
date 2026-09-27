# CLAUDE.md

Read `README.md` first — it is this repo's own manual for the site as it is
built today. This file holds the brief for the work now under way, and the
cross-repo session rule.

## The 2027 pass

*Set by Kyle on 2026-09-27, ahead of a marketing push built on the films.*

**The foundation stays.** The works, the written descriptions, the editions
and the thirteen seasons are the first time one of Kyle's sites was actually
filled rather than scaffolded — `brain/themes/the-website-as-artwork.md`
counts eight sites in fifteen years that failed the other way. Nothing here
is rebuilt from scratch, and no new domain is the answer to anything.

**The work is enrichment.** Every work carried until its data is complete,
and then shown to the world as well as it can be. Complete means five layers,
not one:

1. **Record** — what the catalogue holds: medium, size, date, place,
   pigments, provenance, typed relations to other works.
2. **Voice** — what Kyle has said about the work, on camera, transcribed.
3. **Evidence** — footage of the making.
4. **Context** — what the brain knows: themes, people, places, series.
5. **World** — where and when it was made, and what else was true that day.

**The stack is open.** This site is open ground (root `CLAUDE.md` § two houses
and the open ground). The July rules — static only, typography first, no
JavaScript (`SPEC.md` § 6) — are withdrawn: in Kyle's words they came "from a
different place and time." Any technology is fair game: client code, a
framework, a Worker, search, video, a public endpoint for agents, a native app
alongside. Write down why a choice was made in `docs/`, so the next session
inherits a reason. Anything with a live layer or client code gets a real
browser smoke before it is called done.

### Where the material lives

The site draws on stores it does not own, and enrichment goes into the store
that owns the fact, not into a copy here.

| Layer | Authority | Reach it by |
|---|---|---|
| Record | the oeuvre — `atelier/oeuvre`, live at archive.kyleparkercunningham.com | the `kpc_oeuvre` MCP tools (`stats` gives the gaps as queues) |
| Voice | daybook `library/transcripts/`, and the talking sessions to come | daybook's `CLAUDE.md` |
| Evidence | daybook's clip library; cine's films and shorts | `daybook/`, `cine/NOTES.md` |
| Context | `brain/` — **`visibility: public` notes only** | `brain/MAP.md` |
| World | `lab/weather`, keyed by place and date | its `docs/sources.md` |

`content/oeuvre/` in this repo is a copy of catalogue data made in July,
before the archive existed. Which of the two a page should read from, and how
the copy is retired or kept in step, is an open question for this pass — do
not enrich both by hand.

### Lines that hold

- **No prices.** Valuations and private notes are in the oeuvre and are
  nobody's business but Kyle's. No public surface shows them.
- **Brain notes marked `private` or `restricted` never reach the site.**
- **Voice is Kyle's.** Writing in his voice is drafted by him; a scaffold is
  marked `author = "claude"` per the Manifest's attribution rules (`TODO.md`
  says how). Whether a model may speak in its own voice on the site, clearly
  labelled, is **not yet decided** — until it is, the site shows only what
  Kyle has written or said.

## Sessions end with a PR

A branch is not a deliverable. Before ending any session — web or local:

- Push the work. A `claude/*` branch push opens a draft PR by itself
  (`.github/workflows/claude-branch-pr.yml`); for any other branch, open
  the PR yourself. If the work was committed straight to main, push main.
- Say in the handoff where the work now lives: the PR number, or the main
  push.
- Merged branches delete themselves on GitHub; do not resurrect one.

The PR list is the inbox. Work that ends a session without a PR or a
pushed main strands invisibly.
