# `rules/detail/doc/` — Hugo docs-site build pipeline

See the repo-root `AGENTS.md` first for general Bazel/Starlark gotchas (Starlark has no
recursion, `declare_directory` root creation, repository-rule refetch behavior) — those
apply here too and aren't repeated below.

Builds the whole Hugo docs site (`projects/docs`, `doc_publish` target `docs`) out of a
tree of `doc_section` targets nested under a `doc_publish`. Key rules:

- **`doc_section`** (`doc_section.bzl`) — metadata only, no build actions. Returns a
  `DocSectionInfo` provider (name/index/srcs/data/md_files). Requires a `slug` attr
  (lowercase/digits/hyphens, unique among sibling srcs) that becomes the section's URL path
  segment — this is what makes URLs clean instead of being derived from Bazel label paths.
  Nothing outside this docs subsystem ever consumes a `doc_section` directly — it only ever
  appears nested inside a parent's `srcs`.
- **`doc_site_build`** (`doc_site_build.bzl`, used inside `doc_publish`) — the *only* rule
  that runs actions, of which it runs three: one pass walks the entire nested
  `doc_section` tree (iterative worklist, see `_doc_common.bzl`'s
  `build_content_manifest`) into a JSON manifest that `utils/formatter.py` consumes in a
  single invocation to place every file at its final nested destination; one
  `markdownlint-cli` action lints every markdown file in the tree in a single invocation
  (not per-section); and one writes `config.yaml`. Output groups: `config`, `content`,
  `static`, `lint` — these names are load-bearing, since `doc_publish` selects them by
  string and a typo yields a silently empty `filegroup` (see the note below).
- **`doc_publish`** (`doc_publish.bzl`) — thin macro: wires a `doc_site_build` +
  `hugo_theme` + `hugo_site` + `hugo_serve` together. Doesn't do any formatting/copying
  itself.
- Content lives in each project's `docs/` subtree as nested `doc_section` BUILD targets;
  data files (images etc.) go in a sibling `data/` dir with its own `filegroup`, wired via
  the `doc_section`'s `data` attr.

## Markdown link handling

Docs are authored against the **source** layout: a link is written relative to the file
being edited, which is what VS Code generates when you drag one doc onto another. The site
is assembled into a different layout driven by each `doc_section`'s `slug`, so
`formatter.py` resolves every relative link against its own file's source directory and
rewrites it to the target's final site URL. This covers any file type — other markdown
pages, images, PDFs — and leaves anything carrying a URI scheme, a leading `/`, or a bare
`#` alone.

Two constraints make the whole tree get processed in one formatter invocation:

- **A leaf page's URL segment comes from its own H1**, via front-matter `slug` (a
  documented no-op for `_index.md` branch bundles, but *not* for leaf pages). Starlark
  can't read file contents, so the Bazel rule supplies only the section URL prefix and the
  formatter fills in the leaf segment — which means resolving a cross-section link
  requires having already read the page being linked to.
- **`slugify` must agree with Hugo's urlize.** Hugo normalises whatever lands in
  front-matter `slug`, so the formatter emits an already-urlized value and uses that same
  value in its link map; the map is then correct by construction rather than by guessing at
  Hugo's normalisation of titles like `If $x^2>0$, then $x>0$`. `formatter_test.py` pins
  this against URLs the site actually serves.

Emitted URLs are root-relative; `relativeURLs: true` in `data/config.yaml` turns them into
correctly-depth-adjusted relative URLs at render time and leaves external URLs untouched.

Two gotchas worth knowing:

- **A relative link that resolves to nothing fails the build**, listing each `file:line`.
  That is deliberate — the previous regex silently rewrote broken links into plausible
  404s. If a link legitimately points outside the doc tree, use an absolute URL.
- **Hugo renders `.html` in a content directory as a page, not a resource**, so
  `data/target.html` is reachable at `target/`, not `target.html` (see `content_asset_url`).
  This is the same quirk behind the `security.allowContent` note below.

Two forms are deliberately *not* handled, because neither appears in the tree and both
would need markdown state the scanner doesn't otherwise track: **4-space indented code
blocks** (fenced blocks, including inside blockquotes, are handled) and **reference-style
links** (`[a]: ./foo.md`). An indented literal like `    [x](./foo.md)` would be rewritten
or fail the build rather than staying literal — use a fence.

Raw HTML (`<img src="...">`) is also not rewritten; only markdown links are. There are two
such tags: `projects/networking/gopher/crawler/docs/index.md` (its image has never existed
in the repo) and `projects/qr/docs/docs.md`, which is not in the doc tree at all since
`projects/qr/docs/` has no BUILD file. If `qr` is ever wired in, its `src="data/qr_code.png"`
will 404 — assets are flattened out of `data/` into the section directory.

## Fixed: stale `hugo_site` output

This was long recorded here as an unresolved `rules_hugo` caching bug — `docs_site.build`
reporting up-to-date and serving old HTML after content changed. It was not upstream.
`doc_site_build` published its content TreeArtifact under an output group named `files`
while `doc_publish` asked for one named `content`; Bazel returns an *empty* `filegroup` for
an output group that doesn't exist, so `hugo_site` had **no dependency edge on the content
at all** and could never be invalidated by it. Hugo still read the directory off the
filesystem, which is why the site looked populated but arbitrarily stale.

Renaming the group to `content` fixed it; a content edit now propagates to rendered HTML
with no manual intervention. Diagnosing this class of problem is one command — an output
group that yields nothing is the tell:

```
bazel cquery //projects/docs:docs_site.prepare.content --output=files
```

## `security.allowContent` (Hugo config)

Hugo's default is a deny-only list (`['! ^text/html$', '! ^text/org$']`), meaning "allow
everything except these." Adding *any* positive/non-negated entry flips the whole list into
strict allow-list mode and silently breaks markdown parsing too. To loosen it, only ever
add/remove negated entries — see `data/config.yaml`.

## Verifying doc changes

1. `bazel build //projects/docs:docs_site.prepare` — check `bazel-bin/projects/docs/content/...`
   directly for the expected content (don't just trust "build succeeded").
2. `bazel build //projects/docs:docs_site.build` — the rendered HTML lands under
   `bazel-bin/projects/docs/docs_site.build/...` and now tracks content changes properly
   (see the output-group note above).
3. `bazel run //projects/docs:docs_site.serve` for a live server; if it fails with a
   permission error on `public/`, a stale read-only `public/` dir was probably left by an
   earlier `bazel build docs_site.build` — `chmod -R u+w` + `rm -rf` it and retry.
4. `bazel test //rules/detail/doc/utils:formatter_test` covers link rewriting directly and
   is far faster than rendering the site.

## Mermaid diagrams

The theme bundles Mermaid 11.17.2 (`static/mermaid.min.js` in the hugo-book repo).
`mermaid.parse` in a Node + jsdom harness catches syntax errors but not layout mistakes,
so look at the rendered page as well (serve `bazel-bin/projects/docs/docs_site.build`
with `python3 -m http.server`). One mistake that parses fine but renders wrong: in a
`gantt` with `dateFormat X`, a task written `: 1, 2` reads `1` as the task id, and
`: a2, 1, 2` still ignores the numeric start, so every bar starts at 0. Use
`after <id>` with durations (`: a2, after a1, 1s`) instead, plus `tickInterval 1second`
to avoid duplicated axis labels.
