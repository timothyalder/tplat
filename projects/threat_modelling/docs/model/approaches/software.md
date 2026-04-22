# Focusing on Software

Shostack argues software-centric threat modelling (focusing on the system’s actual architecture and behavior) is more effective and practical than asset or attacker-centric modelling.

## Method

1. Model the software itself (architecture, data flows, components, APIs).
2. Use diagrams or shared representations to build a common understanding of how the system works.

## Advantages

* **Shared understanding:** Exposes mismatches in how team members think the system behaves, often revealing security gaps.
* **Handles complexity:** Helps untangle and make visible the accumulated complexity of long-running or large systems.
* **Surfaces assumptions:** Forces explicit identification of hidden or incorrect assumptions between components.
* **Immediate security value:** Even before identifying threats, aligning understanding improves security posture.
* Works across different types of software:
  * “Boxed” software (clearly defined boundaries like apps or packages)
  * Deployed systems (evolving infrastructure and services)
* Developers are familiar with their own software. This is reliable, unlike assumptions about assets or attackers.
* Doesn’t rely on vague or inconsistent concepts (like “assets” or “attacker personas”).
* Provides a concrete, structured foundation for systematically identifying threats.

## Takeaway

Software-centric modeling works because it starts from something concrete, shared, and well-understood: the system itself. This makes it more reliable, reproducible, and effective for identifying and addressing threats than asset or attacker-focused approaches.
