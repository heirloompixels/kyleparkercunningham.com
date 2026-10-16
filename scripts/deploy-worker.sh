#!/usr/bin/env bash
# Build the site and deploy it to the kpc-site Worker (docs/hosting.md).
#
#   scripts/deploy-worker.sh            build, write the redirects, deploy
#   scripts/deploy-worker.sh --dry-run  build and write, but only show the upload
#
# Zola must be 0.22.1: 0.23 rewrote the template engine and these templates
# predate it (TODO.md § 2). Credentials come from ~/.config/cloudflare/torc.env.
set -euo pipefail
cd "$(dirname "$0")/.."

ZOLA="${ZOLA:-zola}"
case "$("$ZOLA" --version)" in
  "zola 0.22.1") ;;
  *) echo "need zola 0.22.1, found: $("$ZOLA" --version) (set ZOLA=/path/to/zola)" >&2; exit 1 ;;
esac

# The generators CI runs before every build. Their output is not committed, so
# the tracked copies are put back afterwards and a deploy leaves the tree clean.
keep="$(mktemp -d)"
cp data/recently_edited.json data/site_index.json "$keep/"
trap 'cp "$keep"/*.json data/; rm -rf "$keep"' EXIT
python3 scripts/update_recently_edited.py
python3 scripts/generate_site_index.py
"$ZOLA" build
python3 scripts/redirects.py
python3 scripts/finalize_links.py

# wrangler.jsonc names the domains, so a real deploy attaches them. Before the
# cutover, GitHub Pages' records still hold those names; stop rather than fail
# halfway. A dry run never attaches anything.
case " $* " in
  *" --dry-run "*) ;;
  *) python3 scripts/cutover.py --check || {
       echo "GitHub Pages still holds kyleparkercunningham.com: cut over first (scripts/cutover.py)" >&2; exit 1; } ;;
esac

set -a; . "$HOME/.config/cloudflare/torc.env"; set +a
WRANGLER="${WRANGLER:-npx --yes wrangler@4}"
$WRANGLER deploy "$@"
