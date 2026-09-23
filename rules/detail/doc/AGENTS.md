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
  that runs actions. One pass walks the entire nested `doc_section` tree (iterative
  worklist, see `_doc_common.bzl`'s `build_content_script`) copying/transforming every
  markdown file straight to its final nested destination in one content-assembly action,
  and one separate `markdownlint-cli` action lints every markdown file in the tree in a
  single invocation (not per-section). Output groups: `config`, `files`, `static`, `lint`.
- **`doc_publish`** (`doc_publish.bzl`) — thin macro: wires a `doc_site_build` +
  `hugo_theme` + `hugo_site` + `hugo_serve` together. Doesn't do any formatting/copying
  itself.
- Content lives in each project's `docs/` subtree as nested `doc_section` BUILD targets;
  data files (images etc.) go in a sibling `data/` dir with its own `filegroup`, wired via
  the `doc_section`'s `data` attr.

## Known unresolved bug: stale `hugo_site` output

**`hugo_site` (from the vendored `rules_hugo`, see `toolchains/hugo/`) doesn't reliably
pick up changes to its `content` input** when that input is a `declare_directory`
TreeArtifact passed through a `filegroup(output_group=...)` indirection (see
`hugo_inputs`/`copy_to_dir` in `hugo/internal/hugo_site.bzl` — a generated, non-source
TreeArtifact is passed straight through as an action input rather than copied per-file).

Reproduced concretely: rebuilding `//projects/docs:docs_site.prepare` correctly updated
`bazel-bin/projects/docs/content/.../foo.md` (mtime bumped, new content confirmed by
reading the file), but a subsequent `bazel build //projects/docs:docs_site.build` reported
fully up-to-date (zero actions run, empty `--explain=...` log) and its rendered HTML output
still had the *old* mtime and old content.

**Do not trust `docs_site.build`/`docs_site.serve` output as reflecting the latest source
changes just because the build reported success.** Verify by comparing mtimes/content
directly: `bazel-bin/projects/docs/content/**` (should be fresh after `docs_site.prepare`)
vs. `bazel-bin/projects/docs/docs_site.build/**` (may be stale). If stale, force a rebuild
(e.g. touch a file `hugo_site` depends on, or `bazel clean` the affected outputs) rather
than assuming a green build means fresh output. Root cause not yet fixed or worked around
upstream — worth revisiting if it keeps costing verification time.

## `security.allowContent` (Hugo config)

Hugo's default is a deny-only list (`['! ^text/html$', '! ^text/org$']`), meaning "allow
everything except these." Adding *any* positive/non-negated entry flips the whole list into
strict allow-list mode and silently breaks markdown parsing too. To loosen it, only ever
add/remove negated entries — see `data/config.yaml`.

## Verifying doc changes

1. `bazel build //projects/docs:docs_site.prepare` — check `bazel-bin/projects/docs/content/...`
   directly for the expected content (don't just trust "build succeeded").
2. `bazel build //projects/docs:docs_site.build` — then re-check the final HTML under
   `bazel-bin/projects/docs/docs_site.build/...` for staleness given the bug above.
3. `bazel run //projects/docs:docs_site.serve` for a live server; if it fails with a
   permission error on `public/`, a stale read-only `public/` dir was probably left by an
   earlier `bazel build docs_site.build` — `chmod -R u+w` + `rm -rf` it and retry.
