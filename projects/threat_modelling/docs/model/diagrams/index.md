# Diagrams

Different diagram types are useful in different threat modeling contexts. Diagrams should:

* Show the events that drive the system.
* Show the processes that are driven.
* Determine what responses each process will generate and send.
* Identify data sources for each request and response.
* Identify the recipient of each response.
* Ignore the inner workings, focus on scope.
* Ask if something will help you think about what goes wrong, or what will help you find threats.

Think of them as interchangeable tools: choose the one that best fits the system and the conversation you need to have.

All diagrams serve the same goal: **establish a shared understanding of how the system works**.

**Disagreements about diagrams often reveal hidden misunderstandings about the system**. Those misunderstandings frequently surface **security issues**.

> **Tips:**
>
> * Don't cram too much detail into a single diagram. Split your diagram into sub-processes if necessary.
> * Labels in diagrams should be short and descriptive, while helping to tell the overarching story. Avoid verbs, favour nouns.
> * Use colors intuitively (e.g. green for safe, red for compromised).

## Validating Diagrams

Validating a system diagram ensures it is both **accurate** and **useful for threat modeling**.

A good threat modeling diagram is one that is **accurate, complete enough for security analysis, and actively used to align understanding across the team**.

### Accuracy

A diagram is accurate if it reflects reality:

* All important components are included
* No non-existent components or flows are shown
* All significant data flows are represented
* You can explain the system without mentally “fixing” the diagram

If you need to mentally edit the diagram to tell the system story, it is not accurate.

### Usefulness (“Goodness”)

A useful diagram highlights what matters for security:

* Focus on elements that affect security outcomes
* Include edge cases and conditional behavior (“sometimes”, “also”)
* Expand details when they affect security decisions
* Capture disagreement about system design explicitly

Experience is key: knowing what is “important” improves with practice.

## How to Validate a Diagram

Validation is best done collaboratively with system experts:

* Walk through key use cases using the diagram
* Ensure the story can be told end-to-end
* Avoid needing external or missing information
* Ensure no diagram changes are required to explain behavior

## Diagram Quality Rules of Thumb

Improve diagrams iteratively using these principles:

* **Clarify ambiguity**: expand “sometimes/also” cases into explicit flows
* **Show security-relevant detail** when needed
* **Label trust boundaries clearly**
* **Include disagreement points** to align team understanding
* **No data sinks**: show where data is used
* **Show data movement explicitly** (no implicit transfers)
* **Show all entry and exit flows for processes**
* **Include control mechanisms** (e.g. firewalls, permissions)
* **Avoid overly complex diagrams (“eye charts”)**
* **Keep diagrams printable and readable**

A process must have both input and output—otherwise it is either incomplete or mischaracterised.
