# Trust Boundaries

A **trust boundary** is any point where entities with different privileges or trust levels interact.

Every system has at least one trust boundary because all computation occurs in some context.

If no boundaries are visible:

* Either everything is incorrectly assumed to have equal privilege
* Or the model is missing structure

In the extreme case where everything truly shares the same trust level, draw one boundary around the entire system and move on.

Trust boundaries help structure analysis, but threats are driven by **attacker-influenced data flows and parsing logic**, not solely by boundary crossings.

## Drawing Trust Boundaries

After creating a system model, boundaries can be added in two ways:

### 1. Start from known boundaries

Add explicit privilege separations such as:

* Unix UIDs
* Windows sessions
* Machines or containers
* Network segments

Represent each as a **boxed region** containing the relevant principals.

### 2. Start from principals

* Begin at a privilege extreme (e.g. `root/admin` or anonymous users)
* Add boundaries whenever interaction occurs between different principals

---

## Boundary Placement Guidance

At a fine-grained level, trust boundaries should ideally align with **data flows**:

* Crossing a **data store** may imply different table/procedure permissions
* Crossing a **host** may reflect different user roles or access groups

If a boundary cuts through a single element:

* Split the element, or
* Create a subdiagram showing separation

Clarity of boundaries is the main objective.

## Where Threats Appear

Threats often cluster around trust boundaries—but not exclusively.

Even if multiple internal components are trusted relative to each other, threats can still enter via:

* External interfaces (e.g. web browser to server)
* Data flows crossing system edges
* Complex input parsing (e.g. order processing logic)

Threats follow **data controlled by an attacker**, not just boundaries.
