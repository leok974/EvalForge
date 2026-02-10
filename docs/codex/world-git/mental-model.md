---
title: "Git Mental Model"
world_id: world-git
type: codex_entry
level: tier1
---

# Git Mental Model (Working Tree / Index / HEAD)

Git becomes easy when you know *where* your changes are.

## The three zones

### 1) Working Tree
Your files on disk right now.

### 2) Index (Staging Area)
A “prep area” for the next commit. You choose what goes in.

### 3) HEAD
Your current commit (and the commit your branch points to).

## The one command that explains everything
```bash
git status
```

## Snapshot mindset

A commit is a snapshot of the repo state. Diffs are how Git *shows* changes.

## Tiny patterns

* stage: `git add <file>` or `git add -p`
* commit: `git commit -m "msg"`
* unstage: `git restore --staged <file>`
* undo working edits: `git restore <file>`


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]