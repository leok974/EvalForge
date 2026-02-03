---
title: "Branches"
world_id: world-git
type: codex_entry
level: tier1
---

# Branches

A branch is just a **pointer to a commit**.

## Create and switch
```bash
git switch -c feat/my-work
```

## Switch branches

```bash
git switch main
```

## See branches

```bash
git branch
git branch -vv
```

## Rename branch

```bash
git branch -m old-name new-name
```

## Key idea

Creating a branch does not copy files. It creates a new pointer.
