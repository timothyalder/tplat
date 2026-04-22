# Example Attack Tree

## Goal: Access a Building

This is a simple OR-based attack tree.

```mermaid
graph TD
    A[Access building]

    A --> B[Through a door]
    A --> C[Through a window]
    A --> D[Through a wall]
    A --> E[Other means]

    %% Door branch
    B --> B1[Unlocked]
    B --> B2[Drill lock]
    B --> B3[Pick lock]
    B --> B4[Use key]
    B --> B5[Social engineering]

    B1 --> B11[Get lucky]
    B1 --> B12[Block latch]
    B1 --> B13[Distract staff]

    B4 --> B41[Find key]
    B4 --> B42[Steal key]
    B4 --> B43[Copy key]
    B4 --> B44[Social engineer key]

    B5 --> B51[Follow someone in]
    B5 --> B52[Build relationship]
    B5 --> B53[Carry items to appear legitimate]

    %% Window branch
    C --> C1[Break window]
    C --> C2[Lift window]

    %% Wall branch
    D --> D1[Use tools]
    D --> D2[Use vehicle]

    %% Other means
    E --> E1[Fire escape]
    E --> E2[Roof access]
    E --> E3[Another tenant]
