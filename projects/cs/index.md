# Computer Science

## Stack

The stack is a region of preallocated memory on a RAM stick. The stack is last-in, first-out. A good way to understand this is through the call stack of a program. For example, a program's call stack might look like this:

```mermaid
flowchart LR
    images@{ shape: docs, label: "Images" }
    subgraph program["Program"]
        direction TB
        main["`main()`"]
        preprocess["`preprocess()`"]
        compute["`compute()`"]
        main --> preprocess --> compute
    end
    array@{ shape: procs, label: "Results"}
    images --> program --> array

    classDef main fill:#26a69a,color:#fff,stroke:#1d7d74
    classDef preprocess fill:#7e57c2,color:#fff,stroke:#5e35b1
    classDef compute fill:#4c8bf5,color:#fff,stroke:#2f5fc1
    classDef data fill:#f9a825,color:#333,stroke:#c17900
    class images,array data
    class main main
    class preprocess preprocess
    class compute compute
```

In the stack, the `main()` function is loaded first, followed by the rest of the call chain.

```mermaid
flowchart TB
    subgraph stack["Stack"]
        compute["`compute()`"]
        preprocess["`preprocess()`"]
        main["`main()`"]
    end

    classDef main fill:#26a69a,color:#fff,stroke:#1d7d74
    classDef preprocess fill:#7e57c2,color:#fff,stroke:#5e35b1
    classDef compute fill:#4c8bf5,color:#fff,stroke:#2f5fc1
    class main main
    class preprocess preprocess
    class compute compute
```

Each block on the stack contains some simple information about the function, such as where to return when the function is done, arguments, and any variables this function is using.

```mermaid
flowchart TB
    subgraph preprocess["`preprocess()`"]
        return["`**RETURN ADDRESS**<br>→ compute()`"]:::compute
        arguments["`**ARGUMENTS**<br>images`"]:::data
        variables["`**LOCAL VARIABLES**<br>size, shape`"]:::local
    end

    classDef frame fill:#f3e5f5,stroke:#7e57c2,stroke-width:2px
    classDef compute fill:#e3f2fd,stroke:#4c8bf5,color:#1a1a1a
    classDef data fill:#fff8e1,stroke:#f9a825,color:#1a1a1a
    classDef local fill:#f5f5f5,stroke:#9e9e9e,color:#1a1a1a
    class preprocess frame
```

So the call stack, read from bottom to top, preprocesses some data (e.g., transforms and normalises some images), then runs a computation on it (e.g., runs a convolution). Despite the `main()` function being loaded first, it is the last to leave the stack (at the conclusion of the program). A pointer sits at the top of the stack, so that the processor always knows what function is being run.

A `stack overflow error` occurs when the stack exhausts all available memory. This is most commonly observed during recursion, where the stack is populated by many copies of a single function.

On Linux, the stack defaults to 8MB. On Windows, the stack is only 1MB, which means deeply recursive programs will crash faster.

> [*"Smashing the Stack for Fun and Profit"*](https://phrack.org/issues/49/smashing-the-stack-for-fun-and-profit_md) is a famous paper published in [Phrack Magazine](https://phrack.org) detailing how to corrupt the execution stack by writing past the end of an array declared auto in a routine.

## Heap

The heap exists on the same RAM as the stack, but its function is very different. The heap is an unordered block of memory. Programs may store information in the heap wherever they can make it fit. The heap is useful for programs that need to share information between functions.

```mermaid
flowchart TB
    compute["`compute()`"]

    subgraph heap["Heap"]
        b1["in use"]:::used
        b2["compute()<br>result"]:::mine
        b3["free"]:::free
        b4["in use"]:::used
        b5["compute()<br>buffer"]:::mine
        b6["free"]:::free
        b7["in use"]:::used
        b8["compute()<br>array"]:::mine
    end

    compute -.pointer.-> b2
    compute -.pointer.-> b5
    compute -.pointer.-> b8

    classDef mine fill:#4c8bf5,color:#fff,stroke:#2f5fc1
    classDef used fill:#9e9e9e,color:#fff,stroke:#707070
    classDef free fill:#e0e0e0,color:#333,stroke:#bbb,stroke-dasharray: 5 5
```

Unlike the stack, `compute()`'s blocks are scattered non-contiguously across the heap, wherever free space is available, and `compute()` keeps a pointer to each one. The grayed-out blocks are memory in use by other parts of the program; the dashed blocks are free.

Unlike the stack, data in the heap does not automatically clear upon use. This memory must be allocated and freed upon the conclusion of the program. When data is not properly freed, memory leaks occur and the device will eventually crash. Some languages, such as Python, include a garbage collector that will automatically perform this memory allocation and free for you.
