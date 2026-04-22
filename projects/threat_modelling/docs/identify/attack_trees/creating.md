# Creating Attack Trees

Creating attack trees helps structure your thinking about threats.

## Core Steps

1. Decide on a representation
2. Create a root node
3. Create subnodes
4. Consider completeness
5. Prune the tree
6. Check presentation

---

## 1. Decide on a Representation

Choose:

* **OR tree (most common)**: any child achieves the parent
* **AND tree**: all children required

Also decide:

* Graphical vs outline format

---

## 2. Create a Root Node

Two common approaches:

* **Attacker goal** (recommended)
* **System component**

Best practice:

* Use attacker goal or high-impact outcome
* Prefer OR trees
* Keep layout readable (grid-like)

---

## 3. Create Subnodes

Use:

* Brainstorming
* Structured categories

### Common Structures

**By attack method**

* Physical access
* Software compromise
* Social engineering

**By domain**

* People
* Process
* Technology

**By lifecycle**

* Design
* Production
* Distribution
* Usage
* Disposal

---

## 4. Consider Completeness

Ask:

* “Is there another way this could happen?”
* “Are there missing attacker types or motivations?”

You can cross-check with:

* STRIDE
* Attack libraries
* Literature reviews

---

## 5. Prune the Tree

For each node:

* Remove duplicates
* Mark mitigated or impossible attacks

---

## 6. Check Presentation

Ensure:

* Tree fits on a page (or split logically)
* Labels are consistent and action-oriented
* Layout is readable and structured

Good presentation directly impacts usability.
