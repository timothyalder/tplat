# Digital Communications

## Communication System

```mermaid
flowchart LR

    %% Main blocks
    S["Source of Information"]
    T["Transmitter"]
    C["Channel"]
    R["Receiver"]
    U["User of Information"]

    %% Connections with customizable labels
    S -- "Message signal" --> T
    T -- "Transmitted signal" --> C
    C -- "Received signal" --> R
    R -- "Estimate of message signal" --> U

    %% Dashed subgraph for communicated signal
    subgraph CS["Communicated Signal"]
        T
        C
        R
    end

    style CS stroke-dasharray: 5 5
```

## Analog versus Digital

In analog communiciations, the transmitted message is a modulated electrical signal.

> ***Note:***
>
> *In modulation, a waveform is used to represent the transmitted bit. By altering waveform frequency, amplitude, and phase different bits and sequences of bits may be encoded.*

In digital communications, the transmitted message is a sequence of binary data.

## Digital Communication System

```mermaid
flowchart LR

    %% Main blocks
    IS["Information source and input transducer"]
    SE["Source encoder"]
    CE["Channel encoder"]
    DM["Digital modulator"]
    %% Arrow down here
    C["Channel"]
    %% RL here
    DD["Digital demodulator"]
    CD["Channel decoder"]
    SD["Source decoder"]
    OT["Output transducer"]
    OS["Output signal"]

    %% Connections with customizable labels
    IS --> SE
    SE --> CE
    CE --> DM
    DM --> C
    C --> DD
    DD --> CD
    CD --> SD
    SD --> OT
    OT --> OS


    style CS stroke-dasharray: 5 5
```