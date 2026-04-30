# File Descriptors and Redirection

## Overview

A **file descriptor (FD)** is a kernel-managed handle that represents an open I/O resource (file, socket, pipe, etc.). It provides a uniform interface for reading and writing data streams.

> Windows equivalent: *file handle*

## Standard File Descriptors

By convention, every process starts with three predefined descriptors:

| FD  | Name   | Description            |
| --- | ------ | ---------------------- |
| `0` | STDIN  | Standard input stream  |
| `1` | STDOUT | Standard output stream |
| `2` | STDERR | Standard error stream  |

## Basic Redirection

Redirection operators control where data flows between streams and files.

### Redirect STDERR

Suppress errors by redirecting STDERR (`2`) to `/dev/null`:

```bash
find /etc/ -name networks 2>/dev/null
```

* `2>` → redirect STDERR
* `/dev/null` → discard output

### Redirect STDOUT to File

```bash
find /etc/ -name networks > results.txt
```

* `>` overwrites file (creates if missing)

### Redirect STDOUT and STDERR Separately

```bash
find /etc/ -name networks 2>/dev/null 1>stdout.txt
```

* `1>` → STDOUT
* `2>` → STDERR

## STDIN Redirection

### File as Input

```bash
cat < stdout.txt
```

* `<` redirects file contents into STDIN

### Here Document (Heredoc)

Stream input inline using `<<`:

```bash
cat << EOF >> stream.txt
My
Input
Stream
EOF
```

* `<< EOF` → begin input stream
* `EOF` → terminates input
* `>>` → append to file

## Append vs Overwrite

| Operator | Behaviour      |
| -------- | -------------- |
| `>`      | Overwrite file |
| `>>`     | Append to file |

## Pipes

Pipes (`|`) connect STDOUT of one command to STDIN of another.

### Example: Filter + Count

```bash
find /etc/ -name "*.conf" 2>/dev/null | grep systemd | wc -l
```

### Execution Flow

1. `find` → emits file paths (STDOUT)
2. `grep` → filters lines containing `"systemd"`
3. `wc -l` → counts matching lines

## Mental Model

* Each process reads from **FD 0** and writes to **FD 1/2**
* Redirection rewires these streams
* Pipes create **dataflow pipelines** between processes
* `/dev/null` acts as a **sink** (black hole)

## Common Patterns

| Pattern        | Description            |
| -------------- | ---------------------- |
| `2>/dev/null`  | Suppress errors        |
| `> file`       | Capture output         |
| `>> file`      | Append output          |
| `< file`       | Use file as input      |
| `cmd1 \| cmd2` | Chain processing steps |

## Key Takeaways

* File descriptors abstract all I/O
* Redirection enables precise control of data flow
* Pipes enable composition of simple tools into complex workflows
