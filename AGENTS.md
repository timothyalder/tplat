# tplat repo notes for coding agents

Personal monorepo (see `README.md`), built entirely with Bazel + bzlmod (Bazel 9.0.2, see
`.bazelversion`). Per-language toolchains are pulled in via
`include("//toolchains/<lang>:<lang>.MODULE.bazel")` from the root `MODULE.bazel`; each
`toolchains/<lang>/` dir owns its own dep pinning and patches. `rules/` holds custom
Starlark rules used across projects; `projects/` holds the actual project code, organized
as `projects/<topic>/...`.

Subsystem-specific notes live closer to their code — see `rules/detail/doc/AGENTS.md` for
the Hugo docs-site build pipeline.

## Bazel/Starlark gotchas specific to this repo

- **No recursion in Starlark.** A `.bzl` function cannot call itself, even indirectly. Any
  rule that needs to walk an unbounded-depth tree has to use an explicit worklist/stack
  inside a bounded `for _ in range(N)` loop, with a `fail()` if the bound is exceeded. This
  is the standard idiom here, not a workaround to avoid (see `rules/detail/doc/_doc_common.bzl`
  for a real example).
- **`ctx.actions.declare_directory` roots are not auto-created.** Unlike `declare_file`,
  where Bazel creates the parent dir for you, a script writing into a declared directory
  output needs its own `mkdir -p` before the first write.
- **Repository rules that shell out (`repository_ctx.execute`) instead of using the
  blessed primitives (`download`, `download_and_extract`, `file`, `template`, `symlink`)
  are easy to make look "externally modified."** Bazel fingerprints a repo's whole output
  tree to decide whether to refetch it. `toolchains/hugo/rules_hugo_repository.patch`
  extracts the Hugo binary from a macOS `.pkg` via `pkgutil --expand-full` because GitHub
  stopped shipping darwin tarballs after Hugo v0.150.0 — it uses a plain `cp` (not
  `repository_ctx.symlink`) to land the binary, since the symlink form reliably triggered
  the "modified externally" refetch loop. If you see that warning again, suspect whatever
  raw filesystem step was added most recently, and prefer letting scratch/intermediate
  files (`hugo.pkg`, `expanded/`) sit in the repo dir untouched afterward rather than
  cleaning them up with extra `execute()` calls.
- **A repository rule only refetches when its declared attrs/patches change**, or when its
  output tree's fingerprint doesn't match. Bazel does *not* refetch on every `bazel run`
  once the rule has stabilized — confirmed empirically (repo marker hash + file mtimes
  identical across repeated `bazel run` invocations of a target depending on `@hugo`). If a
  dep looks like it's refetching "every time," it's almost always because something about
  its `archive_override`/patches is still being actively edited, not a caching bug to route
  around.

## General workflow notes

- To tell whether an odd build/runtime symptom is a regression from an in-progress change
  or pre-existing, `git stash` the change, rebuild, and compare. This repo's history has
  several cases (a `target.html` directory-bundle quirk in the docs site, a
  `docs_site.serve` permission error) that turned out to be pre-existing behavior, not new
  bugs — don't assume a weird symptom you just noticed was caused by the change you're
  mid-way through.
- When validating unfamiliar syntax for a tool/library that will be built and rendered by
  Bazel (Mermaid, Hugo config, etc.), don't trust memory of exact version behavior — spin
  up a minimal standalone harness (e.g. Node + the actual npm package) to check empirically
  before writing it into the repo.
