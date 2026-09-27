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
- **`filegroup(output_group = "…")` silently yields nothing when that output group doesn't
  exist.** No error, no warning — the consumer just gets an empty input and loses its
  dependency edge, so it stops being invalidated by the thing it supposedly depends on.
  This masqueraded as an upstream `rules_hugo` caching bug in the docs site for a long time
  (see `rules/detail/doc/AGENTS.md`). Before blaming caching for stale output, check the
  edge exists — an output group that prints nothing is the tell:
  `bazel cquery //projects/docs:docs_site.prepare.content --output=files`.
- **A repository rule only refetches when its declared attrs/patches change**, or when its
  output tree's fingerprint doesn't match. Bazel does *not* refetch on every `bazel run`
  once the rule has stabilized — confirmed empirically (repo marker hash + file mtimes
  identical across repeated `bazel run` invocations of a target depending on `@hugo`). If a
  dep looks like it's refetching "every time," it's almost always because something about
  its `archive_override`/patches is still being actively edited, not a caching bug to route
  around.

## Code review workflow

- When doing new feature development or a code refactor, run the
  `voltagent-qa-sec:code-reviewer` subagent to get feedback before considering the work
  done. Scope the review to only the additions and removals introduced by the change
  (e.g. the current diff/branch vs. `main`), not the whole file or surrounding
  pre-existing code. Use the subagent's findings to decide whether the change needs
  further iteration; address findings that matter before wrapping up.
- A passing test suite is not evidence that the tests pin the behaviour you care about.
  Mutating the code under test and re-running — does anything actually fail? — reliably
  exposes tests that pass for the wrong reason (asserting against a hard-coded fixture
  rather than the code path named in the test). Worth doing directly for anything with
  non-trivial logic, rather than waiting for review to catch it.

## Recording findings

At the end of each major task in a session, record what you learned in the relevant
`AGENTS.md`:

- **This file** for repo-wide Bazel/workflow lessons.
- **The nearest existing subsystem file** (e.g. `rules/detail/doc/AGENTS.md`) for anything
  local to one area.
- **Mint a new `AGENTS.md`**, in the directory that owns the code, when the findings are
  local to an area that has no file yet *and* there is enough substance to justify one —
  roughly two or more findings meeting the bar below. A single note belongs in the nearest
  existing ancestor file instead; scattered one-line files are harder to find than one good
  section. When you mint one, link it from the "Subsystem-specific notes" line near the top
  of this file so it is discoverable, and keep it scoped to that subsystem rather than
  restating anything already covered here.

Record only what the next session can't get faster by reading the code:

- A non-obvious failure mode, ideally with the command that diagnoses it.
- A constraint that isn't visible from the code alone — why a design *had* to be that way,
  so nobody "simplifies" it back into a bug.
- **A correction to something already written here.** Stale notes are worse than missing
  ones: this file once sent a session chasing an upstream bug that was actually a typo in
  our own rule. Fix or delete wrong claims rather than appending around them.

Don't record what the code already states, a narrative of what changed in a session (that
belongs in the commit message), or anything not actually verified while doing the work. If
a task turned up nothing meeting the bar above, add nothing.

## General workflow notes

- **A symptom already written up here as a known external bug is still worth re-deriving.**
  The docs site's "stale `hugo_site` output" sat documented as an unfixable upstream quirk
  and turned out to be a one-word mismatch in our own output-group name. Long-lived notes
  accumulate confident explanations that were never actually verified — treat them as
  leads, not conclusions.
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
