# Focusing on Software

According to Adam Shostack, software-centric threat modeling (focusing on the system’s actual architecture and behavior) is more effective and practical than asset or attacker-centric modelling.

* **How software-centric modelling works:**

  * Model the software itself (architecture, data flows, components, APIs).
  * Use diagrams or shared representations to build a common understanding of how the system works.

* **Major advantages:**

  * **Shared understanding:** Exposes mismatches in how team members think the system behaves, often revealing security gaps.
  * **Handles complexity:** Helps untangle and make visible the accumulated complexity of long-running or large systems.
  * **Surfaces assumptions:** Forces explicit identification of hidden or incorrect assumptions between components.
  * **Immediate security value:** Even before identifying threats, aligning understanding improves security posture.

* **Applicability:**

  * Works across different types of software:
    * “Boxed” software (clearly defined boundaries like apps or packages)
    * Deployed systems (evolving infrastructure and services)
  * Data flow diagrams are especially effective across both contexts.
  * Can integrate with infrastructure models (e.g., data centers, networks, trust boundaries).

* **Why it’s superior:**

  * Developers are familiar with their own software. This is reliable, unlike assumptions about assets or attackers.
  * Doesn’t rely on vague or inconsistent concepts (like “assets” or “attacker personas”).
  * Provides a concrete, structured foundation for systematically identifying threats.

Software-centric modeling works because it starts from something concrete, shared, and well-understood: the system itself. This makes it more reliable, reproducible, and effective for identifying and addressing threats than asset or attacker-focused approaches.
