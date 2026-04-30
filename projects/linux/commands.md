# Core Linux Commands

## `man`

Display manual pages for commands:

```bash
man ls
```

* Comprehensive reference (syntax, options, behaviour)
* Organized into sections (e.g., user commands, system calls)

## `apropos`

Search manual page descriptions by keyword:

```bash
apropos network
```

* Useful when you don’t know the exact command name

## External Resource

* explainshell — explains command syntax interactively

## Common System Commands

| Command    | Description                       |
| ---------- | --------------------------------- |
| `whoami`   | Print current user                |
| `id`       | Show user and group IDs           |
| `hostname` | Get/set system hostname           |
| `uname`    | System/kernel information         |
| `pwd`      | Print current directory           |
| `env`      | Show or set environment variables |

## Networking

| Command    | Description                                        |
| ---------- | -------------------------------------------------- |
| `ifconfig` | Configure/view network interfaces (legacy)         |
| `ip`       | Modern network configuration tool                  |
| `netstat`  | Network status (legacy)                            |
| `ss`       | Socket inspection (modern replacement for netstat) |

## Process & System Inspection

| Command | Description             |
| ------- | ----------------------- |
| `ps`    | Process status          |
| `who`   | Logged-in users         |
| `lsof`  | Open files by processes |

## Hardware Inspection

| Command | Description           |
| ------- | --------------------- |
| `lsblk` | Block devices (disks) |
| `lsusb` | USB devices           |
| `lspci` | PCI devices           |

## File & Path Utilities

### `ls`

List directory contents:

```bash
ls -l /etc
```

### `which`

Locate executable in `$PATH`:

```bash
which python
```

* Returns the path of the command being executed

## File Search

### `find`

Search filesystem with filters and actions.

#### Example

```bash
find / -type f -name "*.conf" -user root -size +20k -newermt 2020-03-03 -exec ls -al {} \; 2>/dev/null
```

#### Key Options

| Option           | Description                            |
| ---------------- | -------------------------------------- |
| `-type f`        | Search for files (`d` for directories) |
| `-name "*.conf"` | Match filename pattern                 |
| `-user root`     | Filter by owner                        |
| `-size +20k`     | Files larger than 20 KiB               |
| `-newermt DATE`  | Modified after date                    |
| `-exec ... {}`   | Execute command per result             |
| `2>/dev/null`    | Suppress errors (not a `find` option)  |

#### Notes

* `{}` is replaced with each match
* `\;` terminates `-exec` (escaped to avoid shell interpretation)

### `locate`

Fast file search using indexed database:

```bash
locate "*.conf"
```

#### Update Database

```bash
sudo updatedb
```

#### Characteristics

| Feature       | `find`         | `locate`       |
| ------------- | -------------- | -------------- |
| Search Method | Real-time scan | Prebuilt index |
| Speed         | Slower         | Very fast      |
| Accuracy      | Always current | May be stale   |
| Filtering     | Advanced       | Limited        |

## Mental Model

* Use **`man` / `apropos`** for discovery
* Use **`which`** to resolve execution path
* Use **`find`** for precise, real-time queries
* Use **`locate`** for fast, broad searches
