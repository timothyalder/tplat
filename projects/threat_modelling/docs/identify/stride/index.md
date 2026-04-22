# STRIDE

STRIDE is a mnemonic for things that go wrong in security. It is a threat modelling technique that can help you identify vulnerabilities in your system based on categories of threats. STRIDE stands for:

* [Spoofing](spoofing.md)
* [Tampering](tampering.md)
* [Repudiation](repudiation.md)
* [Information Disclosure](information-disclosure.md)
* [Denial of Service](dos.md)
* [Elevation of Privelege](eop.md)

## Variants

There are several variants of STRIDE.

### STRIDE-per-Element

STRIDE-per-element refines traditional STRIDE by mapping specific threat types to particular diagram elements (e.g., processes, data flows, data stores), making threat modeling more structured and targeted. Instead of exhaustively applying all STRIDE categories everywhere, analysts focus on the most relevant threats for each element—for example, tampering, information disclosure, and denial of service for data flows.

This approach treats each element as the victim of threats, clarifying analysis (e.g., spoofing a connection ultimately targets the endpoint, not the data flow itself). It improves efficiency and consistency, helping both experienced and less experienced practitioners identify common and novel vulnerabilities.

However, it has limitations:

* It can produce repetitive findings within a model.
* The standard mapping (e.g., Microsoft’s) may not cover all domains, such as privacy concerns, requiring customisation.

There is also a trade-off between completeness and focus: adding more threat mappings increases coverage but reduces prioritisation. A practical completion criterion is identifying at least one plausible threat per applicable STRIDE category for each element.

### STRIDE-per-Interaction

STRIDE-per-interaction shifts threat modeling focus from static elements to **interactions between components**, analysing tuples of (origin, destination, interaction). This reflects the reality that most threats emerge through system communication rather than isolated components.

Each interaction (e.g., process-to-process, process-to-data store, external input) is mapped to relevant STRIDE categories, helping analysts reason about threats in context. While originally intended to reduce analysis scope, it produces a similar number of threats as STRIDE-per-element, but often with **clearer, more intuitive reasoning** because threats are tied directly to data flows and trust boundaries.

Key advantages:

* Models threats where they actually occur—at interaction boundaries.
* Improves interpretability by grounding threats in concrete system behavior.
* Encourages systematic review of inbound/outbound flows and external interfaces.

Limitations:

* Does not reduce overall analysis effort.
* Still requires structured enumeration across all interactions.

In practice, it provides a more interaction-centric lens for STRIDE, complementing element-based approaches by emphasising communication paths and trust boundaries as primary attack surfaces.

### DESIST

DESIST stands for Dispute, Elevation of privilege, Spoofing, Information disclosure, Service denial, and Tampering. This is similar to STRIDE, except Dispute replaces repudiation with a less fancy word, and Service denial replaces Denial of Service to make the acronym work.
