---
title: Merge
id: glossary/git/merge
world: git
level: beginner
tags: [workflow, integration, branching]
related:
  - codex:glossary/git/branch
  - codex:glossary/git/main-branch
  - codex:glossary/world-git/term-3
---

# Merge

## Definition
**Merge** combines changes from one branch into another. Git creates a "merge commit" that ties together both branches' histories.

## Usage
- Merge feature branches into main after testing.
- Use `--no-ff` to preserve branch history.
- Use `--squash` to compress commits when desired.

## Example
```bash
git switch main
git merge feat/new-feature
# Creates merge commit combining both histories
```

## Pitfalls

* Merging without pulling main first can create conflicts.
* Merge commits can clutter history—consider squash merges for small features.

## Related

* Branch: merges combine branches.
* Main Branch: feature branches merge into main.
* Pull Request (PR): PRs trigger merges after review (Term 3).
