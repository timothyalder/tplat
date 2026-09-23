# Model

In order to protect something, you must first have a understand what that something is.

Start with a block diagram of how data flows through the system at the highest possible level.

```mermaid
block-beta
    browser("Web browser") space server("Web server") space logic("Business logic") space database("Database")
    browser<-->server
    server<-->logic
    logic<-->database
```

Add *trust boundaries* to show who controls what.

```mermaid
flowchart LR
wb["Web browser"]

subgraph corporate["Corporate data center"]
    ws["Web server"]
    bl["Business logic"]
end

subgraph wso["Web storage (offsite)"]
    db["Database"]
end

wb <--> ws <--> bl <--> db 

style corporate stroke-dasharray: 5 5
style wso stroke-dasharray: 5 5
```

> **Note:**
>
> *A **trust boundary** is formed at wherever people control different things. Some typical examples of trust boundaries include accounts, network interfaces, different physical computers, virtual machines, organisational boundaries, etc.*

At this point, it is probably helpful to label data flows.

```mermaid
flowchart LR
wb["Web browser<br>1"]

subgraph corporate["Corporate data center"]
    ws["Web server<br>3"]
    bl["Business logic<br>5"]
end

subgraph wso["Web storage (offsite)"]
    db["Database<br>7"]
end

wb <--|2|--> ws <--|4|--> bl <--|6|--> db 

style corporate stroke-dasharray: 5 5
style wso stroke-dasharray: 5 5
```

You should think of threat model diagrams as a part of the development process, so try to keep your diagram in version control with the rest of your project.

> ## **Tips:**
>
> * Don’t have data sinks: You write the data for a reason. Show who uses it.
> * Data can’t move itself from one data store to another: Show the process that moves it.
> * Keep your diagram simple. For complicated parts of your system (e.g., diode structure), draw a separate diagram that focuses on just that block.
