# Data Flow Diagrams

Data flow models are often the most effective way to perform threat modeling because security issues tend to follow **data flow**, not control flow. They can be applied to both networked systems and standalone software.

A Data Flow Diagram (DFD) is a structured representation of how data moves through a system. DFDs model:

* **Processes** (running code)
* **Data stores** (where data is held)
* **Data flows** (communication paths)
* **External entities** (outside the system boundary)

```mermaid
flowchart LR
    webClients["Web Clients"]
    sqlClients["SQL Clients"]
    dba["DBA (Human)"]
    dbUsers["DB Users (Human)"]
    logAnalysis["Log Analysis"]

    subgraph dbCluster["DB Cluster"]
        subgraph sqlAccount["Original SQL Account"]
            frontend(["Acme Front End(s)"])
            database(["Database"])
            dbAdmin(["DB Admin"])
        end
        data[("Data")]
        management[("Management")]
        logs[("Logs")]
    end

    webClients <--> frontend
    sqlClients <--> frontend
    frontend <--> database
    database <--> dbAdmin
    dba <--> database
    dba <--> dbAdmin
    dbUsers <--> logAnalysis
    database <--> data
    database <--> management
    database <--> logs
    logs --> logAnalysis
    dba <--> logAnalysis

style dbCluster stroke-dasharray: 5 5
style sqlAccount stroke-dasharray: 5 5
```

They are especially effective because they:

* Provide a **clear, shared model** of the system
* Highlight **interactions and trust boundaries**
* Make it easier to systematically identify **threats along data paths**

Data flows are typically shown as **one-way arrows**, even though real communication is often bidirectional. This simplification exists because **threats are asymmetric** (e.g., inbound vs outbound data exposure risks differ).

DFDs do **not clearly distinguish** between:

* Channel security (e.g., TLS, SMTP)
* Message security (e.g., contents of an email)

## Key Features

| Feature | Description | Examples |
| --- | --- | --- |
| **Process** | Any executing code | Application services, APIs |
| **Data Flow** | Movement of data between components | HTTP requests, RPC calls |
| **Data Store** | Persistent storage | Databases, files, registries |
| **External Entity** | Actors outside system control | Users, third-party services |
