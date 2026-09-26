# Computer Science

## Stack

The stack is a region of preallocated memory on a RAM stick. The stack is last-in, first-out. A good way to understand this is through the call-stack of a program. For example, a program's call stack might look like.

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
```

In the stack, the `main()` function is loaded first, followed by the rest of the call chain.

```mermaid
flowchart TB
    subgraph stack["Stack"]
        compute["`compute()`"]
        preprocess["`preprocess()`"]
        main["`main()`"]
    end
```

Each block on the stack contains some simple information about the function, such as where to return when the function is done, arguments, and any variables this function is using.

```mermaid
flowchart TB
    subgraph preprocess["`preprocess()`"]
        return["return address -> compute()"]
        arguments["arguments<br>image=n"]
        variables["local variables<br>size, shape"]
    end

```

So the call stack, read from bottom to top, preprocess some data (e.g., transforms and normalises some images), then runs a computation on it (e.g., runs a convolution). Despite the `main()` function being loaded first, it is last to leave the stack (at the conclusion of the program). A pointer sits at the top of the stack, so that the processor always knows what function is being run.

A `stack overflow error` occurs when the stack exhausts all available memory. This is most commonly observed during recursion, where the stack is populated by many copies of a single function.

On Linux, the stack defaults to 8MB. On Windows, the stack is only 1MB which means deeply recursive programs will crash faster.

> [*"Smashing the Stack for Fun and Profit"*](https://phrack.org/issues/49/smashing-the-stack-for-fun-and-profit_md) is a famous paper published in [Phrack Magazine](https://phrack.org) detailing how to corrupt the execution stack by writing past the end of an array declared auto in a routine.

## Heap

The heap exists on the same RAM as the stack, but it's function is very different. The heap is a an unordered block of memory. Programs may store information in the heap, wherever they can make it fit. The heap is useful for programs who need to share information between functions.

```mermaid
diagram here of the heap with compute storing some contents throughout the heap wherever it can fit. Other areas of the heap appear as grayed out blocks.
```

Unlike the stack, data in the heap does not automatically clear upon use. This memory must be allocated and freed upon the conclusion of the program. When data is not properly freed, memory leaks occur and the device will eventually crash. Some languages, such as Python, include a garbage collector that will automatically perform this memory allocation and free for you.
