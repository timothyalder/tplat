# Permissions

Linux permissions control access to files and directories via a **user–group–others** model. Each filesystem object is associated with:

* **Owner (user)**
* **Group**
* **Permissions** defining allowed operations

Users can belong to multiple groups, inheriting access rights accordingly.

## Permission Types

| Symbol | Name    | Meaning                                       |
| ------ | ------- | --------------------------------------------- |
| `r`    | Read    | View file contents or list directory contents |
| `w`    | Write   | Modify file or directory contents             |
| `x`    | Execute | Run file or traverse directory                |

## Permission Scope

Permissions are defined for three classes:

| Scope      | Description               |
| ---------- | ------------------------- |
| User (u)   | File owner                |
| Group (g)  | Users in the file’s group |
| Others (o) | All other users           |

## Directory vs File Semantics

Permissions behave differently depending on object type.

### Files

* `r`: Read file contents
* `w`: Modify file contents
* `x`: Execute file (if binary/script)

### Directories

* `r`: List directory contents (`ls`)
* `w`: Create, delete, rename entries
* `x`: Traverse directory (`cd`, access entries)

**Important constraints:**

* Directory traversal **requires `x`**, regardless of `r`
* `x` on a directory **does not grant execution of contained files**
* Modifying directory contents requires **`w` on the directory**, not the files

## Permission Representation

Permissions are displayed via `ls -l`:

```bash
ls -l /etc/passwd
```

Example output:

```bash
-rwxrw-r-- 1 root root 1641 May 4 23:42 /etc/passwd
```

### Breakdown

```
-rwxrw-r--
││  │  │
││  │  └── Others:  r--
││  └───── Group:   rw-
│└──────── Owner:   rwx
└───────── Type:    -
```

### Fields

| Segment       | Meaning                                          |
| ------------- | ------------------------------------------------ |
| `-`           | File type (`-` file, `d` directory, `l` symlink) |
| `rwx`         | Owner permissions                                |
| `rw-`         | Group permissions                                |
| `r--`         | Others permissions                               |
| `1`           | Number of hard links                             |
| `root root`   | Owner and group                                  |
| `1641`        | File size (bytes)                                |
| `May 4 23:42` | Last modified                                    |
| `/etc/passwd` | File path                                        |

## Octal (Numeric) Representation

Permissions map to octal values:

| Permission | Value |
| ---------- | ----- |
| `r`        | 4     |
| `w`        | 2     |
| `x`        | 1     |

Each scope is summed:

| Example       | Meaning |
| ------------- | ------- |
| `7` (`4+2+1`) | `rwx`   |
| `6` (`4+2`)   | `rw-`   |
| `5` (`4+1`)   | `r-x`   |
| `4`           | `r--`   |

### Example

```
rwxrw-r-- → 764
```

* Owner: `rwx` = 7
* Group: `rw-` = 6
* Others: `r--` = 4

## Mental Model

* **Ownership defines baseline control**
* **Groups extend access across users**
* **Permissions gate operations**
* **Directories control access to structure; files control access to content**
