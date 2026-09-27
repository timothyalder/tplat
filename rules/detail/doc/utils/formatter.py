"""Assembles the Hugo content tree from a build manifest.

Markdown here is authored against the *source* layout - a link is written
relative to the file being edited, which is what VS Code generates when you
drag one doc onto another. The site is assembled into a different layout, one
driven by each doc_section's `slug`, so a source-relative link would point at
nothing once the tree is rearranged. Every relative link is therefore resolved
against its own file's source directory and rewritten to the target's final
site URL.

Rewriting runs over the whole tree in one invocation because a link's target
URL can depend on a file this tool has not otherwise been asked to look at: a
leaf page's URL segment comes from its own H1, so resolving a cross-section
link means having already read the page being linked to.

Emitted URLs are root-relative. Hugo's `relativeURLs: true` (see
`rules/detail/doc/data/config.yaml`) turns them into correctly-depth-adjusted
relative URLs in the rendered HTML, and leaves external URLs alone.
"""

import argparse
import json
import os
import posixpath
import re
import shutil
import sys
from urllib.parse import quote, unquote

# A fence opens with at least three backticks or tildes, indented at most three
# spaces. Nothing inside a fenced block is a link, including the parenthesised
# node labels that Mermaid diagrams are full of.
_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")

# Fences are routinely nested inside blockquotes, where ">" would otherwise
# stop _FENCE from matching and leave the block's contents treated as prose.
_QUOTE = re.compile(r"^(?:\s{0,3}>\s?)+")

# "https:", "mailto:", "tel:" - anything already carrying a URI scheme is
# somebody else's address and is passed through untouched.
_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:")

_FRAGMENT = re.compile(r"^([^#?]*)([#?].*)?$")


def slugify(title):
    """Reduce a title to the URL segment Hugo will publish it under.

    Hugo urlizes whatever lands in front-matter `slug`. Confining the result to
    [a-z0-9-], with no leading or trailing hyphen, lands inside the alphabet
    Hugo's own sanitiser is the identity on - so urlize(slugify(t)) equals
    slugify(t) and the link map matches the published URLs by construction,
    rather than by guessing at Hugo's handling of titles like
    "If $x^2>0$, then $x>0$".

    The reduction is lossier than Hugo's ("C++" becomes "c"), and can empty out
    entirely, which the caller rejects.
    """
    slug = title.strip().lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return re.sub(r"-+", "-", slug).strip("-")


def _code_spans(line):
    """Index pairs covering each inline code span in `line`.

    A span opens on a run of N backticks and closes on the next run of exactly
    N, matching CommonMark closely enough that `` `[a](b.md)` `` stays literal.
    """
    spans = []
    i, n = 0, len(line)
    while i < n:
        if line[i] != "`":
            i += 1
            continue
        j = i
        while j < n and line[j] == "`":
            j += 1
        ticks = j - i
        k, closed = j, False
        while k < n:
            if line[k] != "`":
                k += 1
                continue
            m = k
            while m < n and line[m] == "`":
                m += 1
            if m - k == ticks:
                spans.append((i, m))
                i, closed = m, True
                break
            k = m
        if not closed:
            i = j
    return spans


def _parse_destination(line, start):
    """Destination of an inline link whose "(" sits just before `start`.

    Returns (dest, dest_start, dest_end, resume), or None when this is not a
    well-formed destination. `resume` is where the rest of the link continues,
    which for an angle-bracketed destination is past its closing ">".
    Parenthesis depth is tracked so the scan stops at its own closing paren
    instead of running on into later text.
    """
    n = len(line)
    i = start
    while i < n and line[i] in " \t":
        i += 1
    if i >= n:
        return None
    if line[i] == "<":
        end = line.find(">", i + 1)
        if end == -1:
            return None
        return line[i + 1:end], i + 1, end, end + 1
    j, depth = i, 0
    while j < n:
        c = line[j]
        if c in " \t":
            break
        if c == "(":
            depth += 1
        elif c == ")":
            if depth == 0:
                break
            depth -= 1
        j += 1
    if j == i:
        return None
    return line[i:j], i, j, j


def _closes(line, pos):
    """Whether a link's ")" follows at `pos`, allowing an optional title."""
    n = len(line)
    i = pos
    while i < n and line[i] in " \t":
        i += 1
    if i < n and line[i] in "\"'":
        i = line.find(line[i], i + 1)
        if i == -1:
            return False
        i += 1
        while i < n and line[i] in " \t":
            i += 1
    return i < n and line[i] == ")"


def _resolve(dest, ref, urls, errors, lineno):
    """Site URL for `dest` as written in the file `ref`, or None to leave it."""
    if not dest or dest[0] in "#/" or _SCHEME.match(dest):
        return None
    path, suffix = _FRAGMENT.match(dest).groups()
    if not path:
        return None
    target = posixpath.normpath(
        posixpath.join(posixpath.dirname(ref), unquote(path))
    )
    url = urls.get(target)
    if url is None:
        errors.append((ref, lineno, dest, target))
        return None
    return url + (suffix or "")


def _rewrite_line(line, lineno, ref, urls, errors):
    spans = _code_spans(line)
    edits = []
    at = line.find("](")
    while at != -1:
        if not any(s <= at < e for s, e in spans):
            parsed = _parse_destination(line, at + 2)
            if parsed and _closes(line, parsed[3]):
                dest, start, end, _ = parsed
                url = _resolve(dest, ref, urls, errors, lineno)
                if url is not None:
                    edits.append((start, end, url))
        at = line.find("](", at + 2)
    for start, end, url in reversed(edits):
        line = line[:start] + url + line[end:]
    return line


def rewrite_links(text, ref, urls, errors):
    out, fence = [], None
    for lineno, line in enumerate(text.split("\n"), 1):
        marker = _FENCE.match(_QUOTE.sub("", line))
        if fence is not None:
            if (
                marker
                and marker.group(1)[0] == fence[0]
                and len(marker.group(1)) >= len(fence)
                and not marker.group(2).strip()
            ):
                fence = None
            out.append(line)
        elif marker:
            fence = marker.group(1)
            out.append(line)
        else:
            out.append(_rewrite_line(line, lineno, ref, urls, errors))
    return "\n".join(out)


def build(manifest):
    for root in manifest["roots"]:
        os.makedirs(root, exist_ok=True)

    pages, assets = manifest["pages"], manifest["assets"]

    # A leaf page's URL segment comes from its own H1, so every page is read
    # and slugged before any link is resolved against it.
    for page in pages:
        with open(page["src"], encoding="utf-8") as handle:
            lines = handle.readlines()
        if not lines:
            sys.exit("ERROR: {} is empty.".format(page["src"]))
        page["text"] = "\n".join(line.rstrip() for line in lines)
        page["title"] = lines[0].strip().lstrip("#").strip()
        page["slug"] = slugify(page["title"])
        if page["index"]:
            page["url"] = page["url_dir"]
        else:
            if not page["slug"]:
                sys.exit(
                    "ERROR: {} has the heading {!r}, which leaves nothing usable "
                    "as a URL segment.".format(page["src"], page["title"])
                )
            page["url"] = page["url_dir"] + page["slug"] + "/"

    urls = {}
    published = {}
    for entry in pages + assets:
        url = quote(entry["url"], safe="/")
        if url in published:
            sys.exit(
                "ERROR: {} and {} both publish to {} - one would silently "
                "overwrite the other.".format(published[url], entry["ref"], url)
            )
        published[url] = entry["ref"]
        urls[entry["ref"]] = url

    errors = []
    for page in pages:
        body = rewrite_links(page["text"], page["ref"], urls, errors)
        front = "\n".join(
            [
                "---",
                "title: {}".format(page["title"]),
                "type: docs",
                "weight: {}".format(page["weight"]),
                "slug: {}".format(page["slug"]),
                "bookCollapseSection: true",
                "---",
                "",
            ]
        ) if page["front"] else ""
        os.makedirs(os.path.dirname(page["dest"]), exist_ok=True)
        with open(page["dest"], "w", encoding="utf-8") as handle:
            # Per-line rstrip drops the source's final newline; put it back so
            # a verbatim page round-trips byte for byte.
            handle.write(front + body + "\n")

    if errors:
        for ref, lineno, dest, target in errors:
            print(
                "{}:{}: unresolvable link '{}' (looked for '{}')".format(
                    ref, lineno, dest, target
                ),
                file=sys.stderr,
            )
        sys.exit(
            "ERROR: {} markdown link(s) point outside the doc tree. Relative "
            "links must target a file reachable from doc_publish - add it to a "
            "doc_section's srcs or data, or use an absolute URL.".format(len(errors))
        )

    for asset in assets:
        os.makedirs(os.path.dirname(asset["dest"]), exist_ok=True)
        shutil.copyfile(asset["src"], asset["dest"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hugo Doc Formatter")
    parser.add_argument("manifest", help="JSON manifest of pages and assets")
    args = parser.parse_args()

    with open(args.manifest, encoding="utf-8") as handle:
        build(json.load(handle))
