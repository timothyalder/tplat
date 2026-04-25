Project: ATLAS
Subtitle: Attack Template & Logical Analysis System

Description:
An executable threat modelling engine that evaluates
canonical threat templates against system models,
producing testable, measurable security outcomes.

Quickstart (Bazel):

- Run tests:
  - `bazel test //projects/threat_modelling/atlas/test:test`
- Evaluate example model + templates:
  - `bazel run //projects/threat_modelling/atlas:atlas_cli -- eval --model projects/threat_modelling/atlas/data/system_model_example.json --templates projects/threat_modelling/atlas/data/templates_v0_1.json --out /tmp/atlas_report.json`
- Lint example model:
  - `bazel run //projects/threat_modelling/atlas:atlas_cli -- lint --model projects/threat_modelling/atlas/data/system_model_example.json`

Notes:

- v0.1 loads system models and templates from JSON. YAML can be added later by wiring in a YAML parser dependency.
