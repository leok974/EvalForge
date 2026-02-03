---
title: "Merge"
world_id: world-git
type: codex_entry
level: tier1
---

# Merge

Merge combines histories.

## Typical flow
```bash
git switch main
git merge feat/my-work
```

## Fast-forward vs merge commit

* fast-forward: main pointer moves forward (no merge commit)
* merge commit: creates a new commit that has two parents

Some repos prefer:

```bash
git merge --no-ff feat/my-work
```

## Conflicts

If files changed in incompatible ways, Git asks you to resolve them.
See: conflicts.md
