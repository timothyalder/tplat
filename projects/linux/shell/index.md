# Shell

## Overview

A **shell** is a command-line interface (CLI) that mediates between the user and the OS kernel. It accepts commands, executes programs, and manages I/O streams.

> Terminology:

* **Terminal**: Interface for interacting with a shell
* **Console**: Physical or virtual text display (historically distinct from terminal windows)

## Terminal Emulators

A **terminal emulator** provides a GUI-based environment to run shell sessions.

Examples:

* GNOME Terminal
* iTerm2
* Windows Terminal

### Characteristics

* Emulates legacy text terminals
* Supports multiple sessions (tabs/panes)
* Provides access to CLI tools within a GUI

## Shell

The shell is the **command interpreter** responsible for:

* Parsing user input
* Executing commands/programs
* Managing processes and I/O redirection

### Common Shells

| Shell     | Description                                |
| --------- | ------------------------------------------ |
| Bash      | Default on most Linux systems; GNU project |
| Zsh       | Extended Bash with improved UX/features    |
| Fish      | User-friendly, modern shell                |
| KornShell | Advanced scripting capabilities            |
| Tcsh      | C-shell derivative                         |

## Mental Model

* **Terminal emulator** = interface
* **Shell** = interpreter
* **Kernel** = execution layer

```
User -> Terminal -> Shell -> Kernel -> Hardware
```
