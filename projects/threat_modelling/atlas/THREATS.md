Below is a **curated set of 14 concrete ThreatTemplates** that operate cleanly on the v0.1 schema. They are intentionally:

* **Predicate-driven** (no ambiguity)
* **Cross-domain applicable**
* **Non-overlapping at the mechanism level**
* **Grounded in your schema fields only**

These form a solid **v0.1 canonical library**.

---

# Canonical Threat Templates (v0.1)

---

## 1. MITM Data Tampering

```yaml
id: TAMPER_MITM_MODIFY

category: tampering
applies_to: edge

conditions:
  - edge.trust_boundary_crossed == true
  - edge.security.transport_encryption != mutual_tls

parameters:
  - protocol
  - data.classification

mechanism:
  phase: exploit
  actions: [intercept, modify]

required_capabilities:
  network_position: on_path
  privileges: none
  user_interaction: none
  physical_access: false
  sophistication: medium

impact:
  confidentiality: false
  integrity: true
  availability: false
```

---

## 2. MITM Data Disclosure

```yaml
id: DISCLOSURE_MITM_READ

category: disclosure
applies_to: edge

conditions:
  - edge.trust_boundary_crossed == true
  - edge.security.transport_encryption == none
  - edge.data.classification in [confidential, secret]

parameters:
  - protocol

mechanism:
  phase: exploit
  actions: [intercept]

required_capabilities:
  network_position: on_path
  privileges: none

impact:
  confidentiality: true
  integrity: false
  availability: false
```

---

## 3. Credential Exposure in Transit

```yaml
id: DISCLOSURE_CREDENTIALS_IN_TRANSIT

category: disclosure
applies_to: edge

conditions:
  - edge.data.includes_credentials == true
  - edge.security.transport_encryption != mutual_tls

parameters:
  - protocol

mechanism:
  phase: exploit
  actions: [intercept]

required_capabilities:
  network_position: on_path
  privileges: none

impact:
  confidentiality: true
  integrity: false
  availability: false
```

---

## 4. Unauthenticated Privileged Access

```yaml
id: EOP_UNAUTHENTICATED_ACCESS

category: elevation
applies_to: edge

conditions:
  - edge.invocation.authenticated == false
  - node[to].privileges in [admin, system]

parameters:
  - to

mechanism:
  phase: exploit
  actions: [inject]

required_capabilities:
  network_position: adjacent
  privileges: none

impact:
  confidentiality: true
  integrity: true
  availability: true
```

---

## 5. Missing Authorisation on Sensitive Operation

```yaml
id: EOP_MISSING_AUTHZ

category: elevation
applies_to: node

conditions:
  - node.authz == none
  - node.data_handling.stores_sensitive == true

parameters:
  - node.id

mechanism:
  phase: exploit
  actions: [inject]

required_capabilities:
  network_position: adjacent
  privileges: user

impact:
  confidentiality: true
  integrity: true
  availability: false
```

---

## 6. Sensitive Data Exposure Without Encryption

```yaml
id: DISCLOSURE_SENSITIVE_NO_TLS

category: disclosure
applies_to: edge

conditions:
  - edge.data.classification in [confidential, secret]
  - edge.security.transport_encryption == none

parameters:
  - data.classification

mechanism:
  phase: exploit
  actions: [intercept]

required_capabilities:
  network_position: on_path

impact:
  confidentiality: true
```

---

## 7. Integrity Violation Without Protection

```yaml
id: TAMPER_NO_INTEGRITY_PROTECTION

category: tampering
applies_to: edge

conditions:
  - edge.security.integrity_protection == false
  - edge.data.classification in [confidential, secret]

parameters:
  - protocol

mechanism:
  phase: exploit
  actions: [modify]

required_capabilities:
  network_position: on_path

impact:
  integrity: true
```

---

## 8. Public Exposure of Internal Service

```yaml
id: SPOOFING_PUBLIC_INTERNAL_SERVICE

category: spoofing
applies_to: node

conditions:
  - node.exposure == public
  - node.type == service
  - node.trust_zone == internal

parameters:
  - node.id

mechanism:
  phase: recon
  actions: [inject]

required_capabilities:
  network_position: none

impact:
  confidentiality: true
  integrity: true
```

---

## 9. Weak Authentication Mechanism

```yaml
id: SPOOFING_WEAK_AUTHN

category: spoofing
applies_to: node

conditions:
  - node.authn in [none, password]
  - node.exposure == public

parameters:
  - authn

mechanism:
  phase: exploit
  actions: [inject]

required_capabilities:
  sophistication: low

impact:
  confidentiality: true
  integrity: true
```

---

## 10. Denial of Service via Unprotected Endpoint

```yaml
id: DOS_UNPROTECTED_ENDPOINT

category: dos
applies_to: node

conditions:
  - node.exposure == public
  - node.type in [service, datastore]

parameters:
  - node.id

mechanism:
  phase: exploit
  actions: [exhaust]

required_capabilities:
  network_position: none
  sophistication: low

impact:
  availability: true
```

---

## 11. Excessive Privilege Concentration

```yaml
id: EOP_PRIVILEGE_CONCENTRATION

category: elevation
applies_to: node

conditions:
  - node.privileges == system
  - node.data_handling.stores_sensitive == true

parameters:
  - node.id

mechanism:
  phase: exploit
  actions: [escalate]

required_capabilities:
  privileges: user

impact:
  confidentiality: true
  integrity: true
```

---

## 12. Trust Boundary Without Authentication

```yaml
id: SPOOFING_BOUNDARY_NO_AUTH

category: spoofing
applies_to: edge

conditions:
  - edge.trust_boundary_crossed == true
  - edge.invocation.authenticated == false

parameters:
  - from
  - to

mechanism:
  phase: exploit
  actions: [inject]

required_capabilities:
  network_position: adjacent

impact:
  integrity: true
```

---

## 13. Data Exfiltration via Internal Channel

```yaml
id: DISCLOSURE_INTERNAL_EXFIL

category: disclosure
applies_to: edge

conditions:
  - edge.data.classification in [confidential, secret]
  - node[from].trust_zone == internal
  - node[to].trust_zone == external

parameters:
  - from
  - to

mechanism:
  phase: exfiltrate
  actions: [intercept]

required_capabilities:
  privileges: user

impact:
  confidentiality: true
```

---

## 14. Repudiation Due to Missing Authentication

```yaml
id: REPUDIATION_NO_AUTH

category: repudiation
applies_to: edge

conditions:
  - edge.invocation.authenticated == false
  - edge.data.classification in [internal, confidential, secret]

parameters:
  - edge.id

mechanism:
  phase: exploit
  actions: [inject]

required_capabilities:
  user_interaction: none

impact:
  integrity: true
```

---

# Why this set works

This library gives you:

### Coverage across STRIDE-like categories

* Spoofing → 8, 9, 12
* Tampering → 1, 7
* Repudiation → 14
* Disclosure → 2, 3, 6, 13
* DoS → 10
* Elevation → 4, 5, 11

---

### Clean predicate compatibility

Every condition only uses:

* Node fields
* Edge fields
* Simple comparisons

No hidden logic required.

---

### Good propagation behaviour

If you add a new template like:

* “TLS without certificate validation”

Then:

* new matches appear
* coverage drops
* exposure increases

Exactly what you want.

---

# What to expect when you run this

On a real system model, you will immediately see:

* Many **edge-based threats** (dominant)
* Fewer but critical **node-based threats**
* Repeated patterns across flows

That’s correct behaviour.