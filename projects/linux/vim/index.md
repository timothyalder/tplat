# Vim

**Vim** is a modal, open-source text editor derived from `vi`. It emphasizes efficient text manipulation and integrates well with Unix tooling (e.g., `grep`, `awk`, `sed`) rather than reimplementing their functionality.

Key properties:

* Lightweight and fast
* Highly composable with external tools
* Optimized for keyboard-driven workflows
* Steep initial learning curve, high long-term efficiency

## Design Philosophy

Vim adheres to the Unix principle:

> Build small, specialised tools and compose them.

* Editing is handled in Vim
* Complex processing is delegated to external utilities
* Results are combined into flexible workflows

## Modal Editing Model

Vim distinguishes between **command input** and **text input** via modes.

| Mode          | Description                                     |
| ------------- | ----------------------------------------------- |
| Normal        | Default mode; keystrokes are commands           |
| Insert        | Text insertion into buffer                      |
| Visual        | Text selection (character/line/block)           |
| Command (`:`) | Execute single-line commands                    |
| Replace       | Overwrite existing text                         |
| Ex            | Batch command execution (extended command mode) |

## Mode Semantics

### Normal Mode

* Navigation and editing commands
* No text insertion
* Entry point on startup

### Insert Mode

* Standard text entry
* Enter via:

  * `i` (insert before cursor)
  * `a` (insert after cursor)
  * `o` (new line below)

### Visual Mode

* Select text for operations
* Variants:

  * `v` → character-wise
  * `V` → line-wise
  * `Ctrl+v` → block-wise
* Common operations: delete, yank (copy), replace

### Command Mode (`:`)

* Executes commands at bottom of screen

Examples:

```vim
:w        " save
:q        " quit
:wq       " save and quit
:%s/foo/bar/g   " replace all occurrences
```

### Replace Mode

* Overwrites existing characters
* Enter via:

```vim
R
```

### Ex Mode

* Extended command execution
* Supports chaining multiple commands
* Less commonly used directly (subset exposed via `:`)

## Integration with Unix Tools

Vim can interface with external commands:

* Filter buffer through tools (`:!command`)
* Use tools like `grep`, `sed`, `awk` for advanced processing

Example:

```vim
:!grep pattern %
```

## Learning Resource

### `vimtutor`

Interactive tutorial for learning core workflows:

```bash
vimtutor
```

Or inside Vim:

```vim
:Tutorial
```

## Mental Model

* **Normal mode = control plane**
* **Insert mode = data entry**
* **Visual mode = selection**
* **Command mode = batch operations**

Efficiency comes from:

* Minimizing mode switches
* Composing small commands
* Leveraging motion + action patterns (e.g., `dw`, `ci(`)

## Key Takeaways

* Vim is **modal**, not linear like typical editors
* Most power comes from **Normal mode commands**
* Designed for **speed, precision, and composability**
* Mastery yields significant productivity gains
