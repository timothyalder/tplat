# Focusing on Attackers

An attacker-focused approach to threat modeling—starting from “who might attack us and why”-is intuitive but generally not very effective.

## Method

1. Create attacker profiles (from simple lists to detailed personas).
2. Use these to guide brainstorming about possible attacks.
3. Often shifts toward human-centric scenarios (e.g., social engineering).

**Appeal and use cases:**

* It feels logical: if attackers drive risk, understanding them should help.
* It can work for experienced security practitioners, for incorporating less-technical input, and for communicating risk or prioritisation.
* Makes threats more tangible, especially for non-technical stakeholders.
* Useful for explaining *who* might attack and *why*, aiding communication and buy-in.

## Limitations

* Discussions easily get bogged down in debating attacker capabilities (e.g., “state-sponsored or not?”).
* Personas lack enough structure to reliably derive concrete threats.
* Engineers may project their own assumptions onto attackers, leading to bias and missed risks.
* Human-centric scenarios can be hard to translate into actionable system security measures.

---

Attacker-centric modelling **does not produce consistent or systematic threat identification.** It does not reliably answer the key question: *what will attackers actually do to the system?*

---

## Takeaway

Attacker-centric modeling can support communication and expert intuition, but it’s not a strong foundation for threat modeling. It lacks the structure and reproducibility needed to consistently identify and address threats, so it’s better used as a supplementary perspective rather than the core approach.
