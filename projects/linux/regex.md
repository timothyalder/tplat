# Regular Expressions (Regex)

Regular Expressions (**regex**) are patterns used to match and filter text. In Linux, they are commonly used with tools like `grep`, `sed`, and `awk`.

> Practical note: Regex is dense but composable—focus on common patterns and reuse.

## Core Constructs

| Pattern | Meaning                         |
| ------- | ------------------------------- |
| `.`     | Any character                   |
| `*`     | 0 or more of previous           |
| `+`     | 1 or more of previous           |
| `?`     | 0 or 1 of previous              |
| `^`     | Start of line                   |
| `$`     | End of line                     |
| `\b`    | Word boundary                   |
| `\w`    | Word character (`[a-zA-Z0-9_]`) |
| `[]`    | Character class                 |
| `()`    | Grouping                        |
| `\|`    | OR operator                     |

## `grep` Modes

| Option    | Description                               |          |
| --------- | ----------------------------------------- | -------- |
| `grep`    | Basic regex                               |          |
| `grep -E` | Extended regex (preferred; enables `+`, ` | `, etc.) |
| `grep -v` | Invert match                              |          |

## Exercises

### 1. Exclude Lines Containing `#`

```bash
cat /etc/ssh/sshd_config | grep -v "#"
```

* `-v` → invert match (exclude comments)

### 2. Words Starting with `Permit`

```bash
grep -E '\bPermit\w*' /etc/ssh/sshd_config
```

* `\bPermit` → word starts with "Permit"
* `\w*` → remaining characters

### 3. Words Ending with `Authentication`

```bash
grep -E '\w*Authentication\b' /etc/ssh/sshd_config
```

* `\w*` → prefix
* `Authentication\b` → word ends with target

### 4. Lines Containing `Key`

```bash
grep 'Key' /etc/ssh/sshd_config
```

* Simple substring match (no regex needed)

### 5. Lines Starting with `Password` **and** Containing `yes`

⚠️ Original pattern is incorrect (`^Password|yes` = OR logic)

#### Correct:

```bash
grep -E '^Password.*yes' /etc/ssh/sshd_config
```

* `^Password` → start of line
* `.*` → any characters
* `yes` → must appear later in line

### 6. Lines Ending with `yes`

```bash
grep -E 'yes$' /etc/ssh/sshd_config
```

* `$` → end of line anchor

## Common Patterns

| Use Case                   | Pattern    |
| -------------------------- | ---------- |
| Starts with word           | `^word`    |
| Ends with word             | `word$`    |
| Contains word              | `word`     |
| Word boundary              | `\bword\b` |
| Starts with A, ends with B | `^A.*B$`   |
| OR condition               | `A\|B`     |

## Best Practices

* Prefer `grep -E` (extended regex)
* Avoid unnecessary `cat`:

  ```bash
  grep pattern file
  ```
  
* Build patterns incrementally
* Validate assumptions (anchors, grouping, precedence)

## Mental Model

* Regex = **pattern → match set**
* Anchors (`^`, `$`) constrain position
* Quantifiers (`*`, `+`) control repetition
* Pipes (`|`) introduce branching logic
* Most errors come from **incorrect grouping or precedence**
