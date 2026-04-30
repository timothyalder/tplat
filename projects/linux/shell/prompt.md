# Shell Prompt

The **shell prompt** is the textual indicator that the shell is ready to accept input. It typically encodes contextual information such as the current user, host, and working directory.

## Default Format

```bash
<username>@<hostname><current-working-directory>$
```

Example:

```bash
user@host[/path/to/dir]$
```

## Common Symbols

| Symbol | Meaning                 |
| ------ | ----------------------- |
| `~`    | User’s home directory   |
| `$`    | Regular (non-root) user |
| `#`    | Root (privileged) user  |

### Examples

```bash
user@host[~]$
```

```bash
root@host[/root]#
```

## Prompt Configuration (`PS1`)

The prompt is controlled by the `PS1` environment variable.

### Example

```bash
PS1="\u@\h[\w]\$ "
```

### Common Escape Sequences

| Sequence     | Description               |
| ------------ | ------------------------- |
| `\u`         | Username                  |
| `\h`         | Hostname (short)          |
| `\H`         | Hostname (full)           |
| `\w`         | Current working directory |
| `\d`         | Date (e.g., Mon Feb 6)    |
| `\D{format}` | Custom date format        |
| `\t`         | Time (24-hour)            |
| `\T`         | Time (12-hour)            |
| `\@`         | Time (AM/PM format)       |
| `\j`         | Number of jobs            |
| `\s`         | Shell name                |
| `\n`         | Newline                   |
| `\r`         | Carriage return           |

## Customisation

Prompt configuration is typically defined in:

```bash
~/.bashrc
```

Changes can include:

* User and host display
* Working directory format
* Time/date stamps
* Exit status of last command
* Colour formatting (via ANSI escape codes)

## Command Logging

### History File

Commands are persisted in:

```bash
~/.bash_history
```

* Stores previously executed commands
* Useful for auditing and recall

### Session Recording

```bash
script
```

* Records full terminal session (input + output)
* Useful for documentation and reproducibility

## Minimal Prompts

```bash
$
```

```bash
#
```

Used in:

* Documentation
* Scripts
* Minimalist environments

## Mental Model

* Prompt = **context + readiness indicator**
* `PS1` = **formatting definition**
* Symbols (`$`, `#`) = **privilege level**
* Customisation improves **situational awareness and efficiency**
