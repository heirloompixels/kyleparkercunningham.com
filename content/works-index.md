+++
# The river bridge. Publishes a machine-readable index of the oeuvre to
# /works.json, which the river service (river.kyleparkercunningham.com) syncs
# into its catalog mirror by slug. See templates/works_json.html.
#
# This page is data, not a document: `path` pins the output URL and the template
# emits raw JSON, so it never uses base.html.
path = "works.json"
template = "works_json.html"
render = true
+++
