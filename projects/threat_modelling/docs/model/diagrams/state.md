# State Diagrams

State diagrams model a system as a set of **states** and **transitions** between those states. They are useful for analysing how a system behaves in response to inputs and how it enforces rules over time.

* A system is represented as a **state machine** with:

  * **States** (current condition of the system)
  * **Transitions** (movement between states)
  * **Inputs/messages** that trigger transitions
  * **Internal data/memory** influencing behavior

```mermaid id="vnjfyp"
stateDiagram-v2
    [*] --> Closed

    Closed --> Opened: open
    Opened --> Closed: close

    Closed --> Locked: lock
    Locked --> Closed: unlock
```

* Each **state** is shown as a labeled node

* Each **transition** is shown as an arrow labeled with the condition or event that triggers it

## Use in Threat Modeling

* Evaluate whether **each transition enforces proper validation and security checks**
* Identify:

  * Invalid or unexpected transitions
  * Missing validation on inputs
  * States that should not be reachable

This helps uncover logic flaws and state-based vulnerabilities.

### Practical Considerations

* State diagrams can become **complex quickly** as more states and transitions are added

* Simpler models are generally:

  * Easier to reason about
  * Easier to secure
  * More reflective of good system design

* Overly complex state spaces (e.g., ambiguous states like “ajar”) increase:

  * Implementation difficulty
  * Risk of security gaps

### Key Takeaway

State diagrams help identify **security issues in system behavior and transitions**, ensuring that only valid, properly checked state changes are possible.
