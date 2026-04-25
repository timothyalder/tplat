# Implement ATLAS v0.1 (Threat Modelling as Code)

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds.

This repository includes `PLANS.md` at the repo root, which defines the ExecPlan format and maintenance requirements. This document must be maintained in accordance with `PLANS.md`.

## Purpose / Big Picture

After this change, a user can model a system as data (a typed node/edge/asset graph), load a canonical threat library of predicate-driven templates, and run a deterministic evaluation that produces concrete threat instances, metrics, and policy-style assertions. This turns threat modelling from a static document into a repeatable, CI-friendly computation.

The user-visible “it works” moment is running a single Bazel target that evaluates an example system model against the v0.1 threat templates and prints a JSON report listing matched threat instances and coverage/exposure metrics.

## Progress

- [x] (2026-04-25) Create Bazel + Python package skeleton for ATLAS.
- [x] (2026-04-25) Implement v0.1 schema types + model linting.
- [x] (2026-04-25) Implement predicate parsing and evaluation for templates.
- [x] (2026-04-25) Implement deterministic threat instantiation + risk scoring.
- [x] (2026-04-25) Implement metrics and invariant-style tests.
- [x] (2026-04-25) Add CLI and example data; wire Bazel targets.
- [x] (2026-04-25) Validate with `bazel test` and a sample `atlas eval`.

## Surprises & Discoveries

- Observation: Bazel needs write access to its output base under the user cache directory.
  Evidence: Running `bazel test //projects/threat_modelling/atlas/test:test` initially failed with “Output base directory ... must be readable and writable.”

- Observation: `py_test` defaults the main file name to `test.py` unless `main` is specified.
  Evidence: `//projects/threat_modelling/atlas/test:test` initially failed analysis with “corresponding default 'test.py' does not appear in srcs”.

## Decision Log

- Decision: Implement ATLAS as a Python library with Bazel targets (`py_library`, `py_binary`, `py_test`) under `projects/threat_modelling/atlas`.
  Rationale: The repo already contains several Bazel-managed Python libraries/tests; matching the existing build/test toolchain reduces integration risk.
  Date/Author: 2026-04-25 / Codex

- Decision: Support JSON as the primary on-disk format in v0.1, and treat YAML loading as optional (best-effort) to avoid forcing a toolchain-wide dependency update during initial delivery.
  Rationale: The spec allows YAML/JSON; Bazel-pinned Python dependencies are centrally managed and updating them can be disruptive. JSON enables a working end-to-end engine immediately.
  Date/Author: 2026-04-25 / Codex

## Outcomes & Retrospective

Delivered a working v0.1 engine with:

- A Bazel-built Python library (`//projects/threat_modelling/atlas:atlas`)
- A CLI (`//projects/threat_modelling/atlas:atlas_cli`) with `lint`, `eval`, `metrics`
- Example data (`projects/threat_modelling/atlas/data/*.json`) including the curated v0.1 templates
- A passing pytest suite (`//projects/threat_modelling/atlas/test:test`)

## Context and Orientation

The ATLAS v0.1 specification lives in `projects/threat_modelling/atlas/ATLAS.md`. It defines:

1. A typed system model (nodes, edges, trust boundaries, assets).
2. A canonical threat template schema with predicate-based `conditions`.
3. A deterministic evaluation engine that instantiates threats from structure.
4. A test/metrics layer (coverage, exposure, drift) computed from instances.

The curated v0.1 template set is written in `projects/threat_modelling/atlas/THREATS.md` as YAML snippets. This implementation will encode those templates as JSON in-repo for deterministic loading without additional dependencies.

This change will add a new Python package at `projects/threat_modelling/atlas/atlas/` and Bazel targets in `projects/threat_modelling/atlas/BUILD` and `projects/threat_modelling/atlas/test/BUILD`.

Definitions used in this ExecPlan:

- System model: A directed graph with typed nodes and edges, plus explicit assets and trust boundaries, represented as JSON on disk.
- Threat template: A rule with an `applies_to` type (node/edge/asset) and a set of boolean predicate expressions that match against the system model.
- Threat instance: A concrete instantiation of a template against a specific node/edge/asset in the system model, with extracted parameters and a computed risk score.
- Deterministic: Running evaluation twice with the same inputs produces byte-for-byte identical outputs (modulo JSON key ordering, which we will make stable).

## Plan of Work

1. Add Bazel targets for ATLAS: a `py_library` for the core engine, a `py_binary` CLI entrypoint, and a `py_test` suite. Keep the code self-contained with only stdlib dependencies.

2. Implement data types and validation:

   - Create lightweight dataclasses for nodes/edges/assets/trust boundaries.
   - Implement model linting checks from the spec: required fields and trust-boundary consistency.
   - Compute derived properties (e.g., whether an edge crosses trust zones) for evaluation and linting.

3. Implement predicate parsing and evaluation:

   - Parse condition strings of the form `lhs == rhs`, `lhs != rhs`, and `lhs in [a, b]`.
   - Resolve `lhs` paths against the current element (node/edge/asset) and allow references from an edge to `node[from]` and `node[to]`.
   - Evaluate predicates deterministically with clear errors for unknown paths.

4. Implement evaluation and threat instantiation:

   - Iterate templates over relevant elements.
   - For matches, instantiate a ThreatInstance with a deterministic `id`.
   - Extract parameter values using the template’s `parameters` list.
   - Compute a simple, stable risk score from impact and required capabilities.
   - Optionally overlay statuses from a separate acknowledgements file (mapping instance ids to `mitigated`/`accepted`/...).

5. Implement metrics and invariant checks:

   - Compute coverage, risk-weighted coverage, exposure score, and drift (if a prior report is provided).
   - Implement invariant checks described in `ATLAS.md` as Python functions and validate them in tests.

6. Add example inputs and CLI:

   - Provide `data/` JSON files: example system model and the curated v0.1 threat templates as a JSON list.
   - Provide a CLI with `lint`, `eval`, and `metrics` subcommands using `argparse`.
   - `eval` writes a stable JSON report to disk and prints a short summary.

## Concrete Steps

All commands run from the repository root (`/Users/timothyalder/Documents/tplat`).

1. Run unit tests:

    bazel test //projects/threat_modelling/atlas/test:test

   Expected: `1` test target passes.

2. Run the CLI evaluation over example data:

    bazel run //projects/threat_modelling/atlas:atlas_cli -- eval --model projects/threat_modelling/atlas/data/system_model_example.json --templates projects/threat_modelling/atlas/data/templates_v0_1.json --out /tmp/atlas_report.json

   Expected: The command prints counts like “instances: N” and writes `/tmp/atlas_report.json` containing `instances` and `metrics`.

## Validation and Acceptance

Acceptance is met when:

1. `bazel test //projects/threat_modelling/atlas/test:test` passes.
2. Running the CLI `eval` command on the example inputs produces a deterministic report (same output on repeated runs) containing:
   - A non-empty `instances` list.
   - `metrics.coverage` and `metrics.exposure` fields.
3. The report includes at least one instance bound to an edge where `trust_boundary_crossed` is true (exercising boundary-crossing logic).

## Idempotence and Recovery

The implementation is additive. Re-running `bazel test` and `bazel run` is safe. If evaluation fails due to invalid input, the CLI should exit non-zero with a clear error message and no partial output file.

## Artifacts and Notes

Key artifacts produced by this plan:

- `projects/threat_modelling/atlas/atlas/`: ATLAS library package.
- `projects/threat_modelling/atlas/data/`: JSON templates and example system model.
- `/tmp/atlas_report.json`: sample evaluation output produced by CLI.

## Interfaces and Dependencies

This v0.1 implementation uses only Python standard library modules (notably `dataclasses`, `enum`, `json`, `argparse`, `hashlib`, `typing`).

The core public interface provided by `projects/threat_modelling/atlas/atlas/__init__.py` will include:

    def load_system_model(path: str) -> SystemModel
    def load_templates(path: str) -> list[ThreatTemplate]
    def lint_model(model: SystemModel) -> list[LintIssue]
    def evaluate(model: SystemModel, templates: list[ThreatTemplate], statuses: dict[str, str] | None = None) -> ThreatReport

ThreatReport will be a dataclass with:

    instances: list[ThreatInstance]
    metrics: Metrics
    lint: list[LintIssue]
    template_ids: list[str]

The CLI entrypoint is a `py_binary` named `//projects/threat_modelling/atlas:atlas_cli`.

## ExecPlan Changes

- 2026-04-25: Marked all Progress items complete and recorded Bazel/py_test gotchas encountered during implementation.
