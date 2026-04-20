# Unified Modeling Language

**Unified Modeling Language (UML)** diagrams can be adapted for threat modeling, especially if they are already part of the development workflow. In this case, you need only **add trust boundaries** to highlight security-relevant separations between components.

## Advantages

* **Leverages existing artifacts (presuming you are already using UML in your project)**: No need to redraw system models
* **Expressive and detailed**: UML supports a wide range of diagram types:

  * Structure diagrams
  * Behavior diagrams
  * Interaction diagrams

## Challenges

* **High complexity**: UML includes many symbol conventions, requiring strong familiarity to interpet correctly
* **Risk of misunderstanding**:

  * Misinterpreted symbols reduce effectiveness
  * Team members may not realize they are confused
  * Social barriers can prevent clarification (e.g., reluctance to ask questions)

## Practical Guidance

* Use UML for threat modeling **only if the team is already comfortable with it**
* Focus on **augmenting diagrams with trust boundaries** rather than increasing detail
* Avoid relying on UML if it introduces ambiguity or slows down understanding
