Below is a **clean, implementation-ready v0.1 specification** for your system. It is written as if you were handing it to an engineer (or Codex) to build against. It is intentionally tight, typed, and unambiguous.

---

# Threat Modelling as Code (TMaC) — v0.1 Specification

## 1. Purpose

This specification defines a minimal, executable framework for threat modelling based on:

* A **canonical threat library** (rule-based templates)
* A **typed system model** (graph of nodes and interactions)
* A **deterministic evaluation engine** (predicate matching)
* A **test and metrics layer**

The system is designed to:

* Automatically instantiate threats from system structure
* Measure coverage and risk
* React to changes in the canonical model

This aligns with established threat modelling practices that rely on system structure, assets, and trust boundaries to identify threats ([Palo Alto Networks][1]).

---

# 2. System Overview

## 2.1 Architecture

The system consists of three layers:

```id="b1qv0c"
Layer A: Canonical Threat Library (CTL)
  - Parameterised threat templates (rules)

Layer B: System Model (SM)
  - Typed graph of nodes, edges, assets, boundaries

Layer C: Evaluation Engine
  - Applies CTL rules to SM
  - Produces Threat Instances
```

---

# 3. System Model Schema (SM)

The system model is a **typed directed graph**.

## 3.1 Root Object

```yaml
SystemModel:
  nodes: [Node]
  edges: [Edge]
  trust_boundaries: [TrustBoundary]
  assets: [Asset]
```

---

## 3.2 Node

Represents a computational or control entity.

```yaml
Node:
  id: string
  type: enum [service, client, datastore, queue, identity, external, human]

  trust_zone: string                # REQUIRED
  exposure: enum [public, internal, restricted]

  privileges: enum [none, user, admin, system]

  authn: enum [none, password, token, mfa, mutual_tls]
  authz: enum [none, role_based, attribute_based]

  data_handling:
    stores_sensitive: boolean
    processes_sensitive: boolean
```

---

## 3.3 Edge (Data Flow)

Represents interaction between nodes.

```yaml
Edge:
  id: string
  from: Node.id
  to: Node.id

  protocol: enum [http, https, grpc, tcp, udp, file, internal_api, unknown]
  directionality: enum [request, response, bidirectional]

  data:
    classification: enum [public, internal, confidential, secret]
    includes_credentials: boolean

  security:
    transport_encryption: enum [none, tls, mutual_tls]
    integrity_protection: boolean

  invocation:
    authenticated: boolean
    user_initiated: boolean

  trust_boundary_crossed: boolean   # REQUIRED
```

---

## 3.4 Trust Boundary

Explicit representation of trust transitions.

```yaml
TrustBoundary:
  id: string
  from_zone: string
  to_zone: string

  type: enum [network, privilege, process, physical]
```

Trust boundaries are fundamental to threat modelling as they separate areas of differing trust or privilege ([drata.com][2]).

---

## 3.5 Asset

Represents something of value to protect.

```yaml
Asset:
  id: string
  owner: Node.id

  type: enum [data, credential, key, service_availability, infrastructure]

  sensitivity: enum [low, medium, high, critical]

  properties:
    confidentiality: boolean
    integrity: boolean
    availability: boolean
```

---

# 4. Canonical Threat Library (CTL)

## 4.1 Concept

A **ThreatTemplate** is a rule that:

* Matches elements in the system model
* Produces concrete threat instances

This extends traditional approaches like STRIDE, which classify threats but do not define executable rules.

---

## 4.2 ThreatTemplate Schema

```yaml
ThreatTemplate:
  id: string

  category: enum [spoofing, tampering, repudiation, disclosure, dos, elevation]

  applies_to: enum [node, edge, asset]

  conditions: PredicateExpression   # REQUIRED

  parameters: [string]              # values extracted from matched element

  mechanism:
    phase: enum [recon, exploit, persist, exfiltrate]
    actions: [enum [intercept, modify, inject, replay, exhaust, escalate]]

  required_capabilities:
    network_position: enum [none, adjacent, on_path]
    privileges: enum [none, user, admin, system]
    user_interaction: enum [none, required]
    physical_access: boolean
    sophistication: enum [low, medium, high]

  impact:
    confidentiality: boolean
    integrity: boolean
    availability: boolean
```

---

# 5. Evaluation Engine

## 5.1 Execution Model

For each template:

```pseudo
for each element in SystemModel:
  if template.conditions(element):
    instantiate ThreatInstance
```

---

## 5.2 ThreatInstance

```yaml
ThreatInstance:
  id: string

  template_id: string
  bound_element: Node.id | Edge.id | Asset.id

  parameter_values: map<string, value>

  risk_score: float

  status: enum [unmitigated, mitigated, accepted, not_applicable]
```

---

## 5.3 Determinism Requirement

Evaluation MUST be:

* deterministic
* stateless (given same inputs → same outputs)

---

# 6. Predicate System

## 6.1 Allowed Inputs

Predicates operate over:

* Node attributes
* Edge attributes
* Asset attributes
* Derived properties

---

## 6.2 Example Predicates

### Boundary crossing

```pseudo
edge.trust_boundary_crossed == true
```

### Weak transport security

```pseudo
edge.security.transport_encryption != mutual_tls
```

### Sensitive data exposure

```pseudo
edge.data.classification in {confidential, secret}
```

---

# 7. Derived Properties

The engine MAY compute:

```pseudo
edge.crosses_trust_boundary =
  (node[from].trust_zone != node[to].trust_zone)

edge.exposes_sensitive_data =
  (classification in {confidential, secret})
```

---

# 8. Tests (Security Invariants)

Tests operate over generated ThreatInstances.

---

## 8.1 Structural Tests

**All boundary-crossing edges must have threats**

```pseudo
for edge where trust_boundary_crossed:
  assert exists ThreatInstance(edge)
```

---

## 8.2 Coverage Tests

```pseudo
for each ThreatInstance:
  assert status in {mitigated, accepted}
```

---

## 8.3 Policy Tests

```pseudo
for each ThreatInstance where risk_score > threshold:
  assert status == mitigated
```

---

## 8.4 Regression Tests

```pseudo
assert current_exposure_score <= previous_exposure_score
```

---

# 9. Metrics

## 9.1 Applicability Coverage

```pseudo
coverage = acknowledged_threats / total_threats
```

---

## 9.2 Risk-Weighted Coverage

```pseudo
coverage = sum(risk_mitigated) / sum(total_risk)
```

---

## 9.3 Exposure Score

```pseudo
exposure = sum(risk_unmitigated)
```

---

## 9.4 Drift Metric

```pseudo
drift = new_threat_instances_after_update
```

---

# 10. Update Propagation

When CTL changes:

1. Re-run evaluation
2. Generate new ThreatInstances
3. Re-run tests
4. Recompute metrics

Expected behaviour:

* Coverage may drop
* Exposure may increase
* Tests may fail

This enforces continuous alignment with evolving threats.

---

# 11. Validation Rules (Model Linting)

Before evaluation:

### Required

* All nodes have `trust_zone`
* All edges define:

  * `transport_encryption`
  * `authenticated`

### Consistency

```pseudo
if node[from].trust_zone != node[to].trust_zone:
  assert edge.trust_boundary_crossed == true
```

---

# 12. Non-Goals (v0.1)

* No probabilistic risk modelling
* No full attacker simulation
* No deep protocol semantics
* No UI or visual modelling requirements

---

# 13. Implementation Notes

* Store SM and CTL as declarative files (YAML/JSON)
* Engine = rule evaluator over graph
* Tests = executable assertions (CI-compatible)
* Metrics = computed post-evaluation

---

# 14. Summary

This system converts threat modelling from:

> static documentation

into:

> executable, testable, continuously evaluated security logic

It builds on established foundations (system models, assets, trust boundaries, and threat categorisation) ([Palo Alto Networks][1]) while introducing:

* rule-based threat generation
* invariant-driven validation
* measurable coverage and drift