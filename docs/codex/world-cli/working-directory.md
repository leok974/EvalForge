---
id: glossary/cli/working-directory
title: Working Directory
world: cli
---

# Working Directory

The **working directory** (also called the **current directory**) is the folder your terminal is "in" right now.

## Why It Matters

- Commands operate relative to this location by default
- File paths you type are interpreted from here unless they're absolute
- You can check it anytime with `pwd` (print working directory)

## Common Pitfalls

- Forgetting where you are and creating files in the wrong place
- Using `cd` without understanding the impact on subsequent commands

## Quick Example

```bash
pwd
# /home/user/projects

ls
# Shows files in /home/user/projects

cd documents
pwd
# /home/user/projects/documents
```

## Related Concepts

- [Paths](codex:glossary/cli/paths)

## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.