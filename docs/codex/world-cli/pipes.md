---
id: glossary/cli/pipes
title: Pipes
world: cli
---

# Pipes

A **pipe** (`|`) connects the output of one command to the input of another.

## How Pipes Work

```bash
command1 | command2 | command3
```

- `command1`'s **stdout** becomes `command2`'s **stdin**
- Data flows like water through a series of filters
- Each command processes and transforms the data

## Common Patterns

```bash
# Count lines in output
ls -l | wc -l

# Search in output
ps aux | grep python

# Sort and get unique values
cat names.txt | sort | uniq

# Chain multiple transformations
cat data.csv | grep "error" | cut -d',' -f2 | sort | uniq -c
```

## Useful Filter Commands

- `grep` — search for patterns
- `sort` — sort lines
- `uniq` — remove duplicates
- `wc` — count lines/words/characters
- `head` / `tail` — first/last N lines
- `cut` — extract columns
- `awk` / `sed` — advanced text processing

## Best Practices

- Build complex pipelines incrementally (test each stage)
- Pipes only pass **stdout**, not stderr (use `2>&1` if needed)
- Use `tee` to save intermediate results while piping

## Related Concepts

- [Redirection](codex:glossary/cli/redirection)
- [Search](codex:glossary/cli/search)

## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.