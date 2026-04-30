# Linux

**Linux** is an open-source operating system built around the Linux kernel. It is distributed in many variants—called *distributions* (distros)—which package the kernel with different userland tools, package managers, and defaults.

## Key Characteristics

* **Security**: Strong permission model; lower malware prevalence compared to Windows
* **Stability**: Long uptimes, predictable behaviour under load
* **Performance**: Efficient resource usage; minimal overhead
* **Flexibility**: Highly configurable; modular design
* **Trade-offs**: Steeper learning curve; hardware/driver support can lag behind Windows

## Core Design Principles

| Principle                      | Description                                                                   |
| ------------------------------ | ----------------------------------------------------------------------------- |
| Everything is a file           | Devices, processes, and system resources are exposed as file-like interfaces  |
| Small, single-purpose programs | Tools are designed to do one thing well                                       |
| Composability                  | Programs can be chained (e.g., via pipes) to perform complex workflows        |
| Shell-centric interaction      | CLI provides primary control surface                                          |
| Text-based configuration       | System and application configs are stored in plain text (e.g., `/etc/passwd`) |

## System Components

| Component                            | Description                                                  |
| ------------------------------------ | ------------------------------------------------------------ |
| Bootloader                           | Initializes the system and loads the OS kernel (e.g., GRUB)  |
| Kernel                               | Core component managing hardware resources and system calls  |
| Daemons                              | Background services (e.g., scheduling, logging, networking)  |
| Shell                                | Command-line interface between user and OS (e.g., Bash, Zsh) |
| Graphics Server                      | Provides graphical subsystem (e.g., X11 / X-server)          |
| Window Manager / Desktop Environment | GUI layer (e.g., GNOME, KDE, MATE, Cinnamon)                 |
| Utilities                            | User-space tools and applications                            |

## System Architecture Layers

| Layer            | Description                                              |
| ---------------- | -------------------------------------------------------- |
| Hardware         | Physical components (CPU, RAM, storage, peripherals)     |
| Kernel           | Abstracts hardware and manages resources                 |
| Shell            | Interface for issuing commands to the kernel             |
| System Utilities | Provide higher-level functionality to users and programs |

## Filesystem Hierarchy

Linux uses a unified hierarchical filesystem rooted at `/`.

| **Path** | **Description**                               |
| -------- | --------------------------------------------- |
| `/`      | Root filesystem; contains everything          |
| `/bin`   | Essential user binaries                       |
| `/boot`  | Bootloader and kernel files                   |
| `/dev`   | Device files representing hardware            |
| `/etc`   | System-wide configuration files               |
| `/home`  | User home directories                         |
| `/lib`   | Shared libraries required for boot            |
| `/media` | Mount point for removable media               |
| `/mnt`   | Temporary mount point                         |
| `/opt`   | Optional / third-party software               |
| `/root`  | Root user’s home directory                    |
| `/sbin`  | System administration binaries                |
| `/tmp`   | Temporary files (often cleared on reboot)     |
| `/usr`   | User-space programs, libraries, documentation |
| `/var`   | Variable data (logs, mail, caches, etc.)      |

## Mental Model

At a high level:

* The **kernel** abstracts hardware into manageable resources.
* The **filesystem** exposes these resources uniformly.
* The **shell + utilities** provide mechanisms to manipulate them.
* Complex operations emerge from **composition of simple tools**.
