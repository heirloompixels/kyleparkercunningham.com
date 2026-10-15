"""Shared helpers for the build-time data scripts: front matter, Zola's real
permalinks, and last-edited dates from git.

Both generators used to build URLs straight from file paths, which is wrong
wherever Zola does something else: a page named `2026-01-28-foo` is served at
`/foo/` (Zola strips a leading date), and `slug` / `path` in front matter
override the name. Those mismatches were the dead links on /manifest/ and
/dashboard/. This module follows Zola 0.22's rules for the cases this site uses.
"""
from __future__ import annotations

import re
import subprocess
import tomllib
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

FRONTMATTER_RE = re.compile(r"^\+\+\+\s*$")
# Zola takes a leading date off a page's file or folder name for its slug.
DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?)?[_-]")


def split_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not FRONTMATTER_RE.match(lines[0]):
        return {}, text
    for i in range(1, len(lines)):
        if FRONTMATTER_RE.match(lines[i]):
            raw = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1:])
            try:
                return tomllib.loads(raw), body
            except tomllib.TOMLDecodeError:
                return {}, body
    return {}, text


def slugify(name: str) -> str:
    """Zola's default `slugify.paths = "on"`: ASCII, lowercase, dashes."""
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s


def is_rendered(rel: Path, fm: dict) -> bool:
    """False for drafts and for anything marked render = false."""
    return fm.get("draft") is not True and fm.get("render", True) is not False


def permalink_for(rel: Path, fm: dict) -> str:
    """The URL Zola serves a content file at, relative to the site root."""
    if fm.get("path"):
        return "/" + str(fm["path"]).strip("/") + "/"
    if rel.name == "_index.md":
        parent = rel.parent
        return "/" if parent == Path(".") else "/" + "/".join(slugify(p) for p in parent.parts) + "/"
    if rel.name == "index.md":
        section_parts, name = rel.parent.parent.parts, rel.parent.name
    else:
        section_parts, name = rel.parent.parts, rel.stem
    if fm.get("slug"):
        leaf = slugify(str(fm["slug"]))
    else:
        leaf = slugify(DATE_PREFIX_RE.sub("", name))
    parts = [slugify(p) for p in section_parts] + [leaf]
    return "/" + "/".join(p for p in parts if p) + "/"


def title_for(rel: Path, fm: dict) -> str:
    if fm.get("title"):
        return str(fm["title"])
    if rel.name == "_index.md" and rel.parent == Path("."):
        return "Home"
    return rel.parent.name.replace("-", " ").replace("_", " ").title()


_GIT_DATES: dict[str, str] | None = None


def _git_dates() -> dict[str, str]:
    """One pass over the log: each path's most recent commit time."""
    global _GIT_DATES
    if _GIT_DATES is None:
        _GIT_DATES = {}
        try:
            out = subprocess.run(
                ["git", "log", "--format=@%cI", "--name-only", "--", "content"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
        except (OSError, subprocess.CalledProcessError):
            out = ""
        when = ""
        for line in out.splitlines():
            if line.startswith("@"):
                when = line[1:]
            elif line and line not in _GIT_DATES:
                _GIT_DATES[line] = when
    return _GIT_DATES


def git_updated(path: Path) -> str:
    """ISO time of the last commit touching `path`; the file's mtime if git has
    no record (uncommitted work). File mtimes alone are meaningless in CI, where
    every file is as old as the checkout, so CI must fetch full history."""
    when = _git_dates().get(path.relative_to(ROOT).as_posix())
    if when:
        return datetime.fromisoformat(when).astimezone(timezone.utc).isoformat()
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
