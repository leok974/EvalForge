---
title: "Add & Commit"
world_id: world-git
type: codex_entry
level: tier1
---

# Add & Commit

## Stage files
```bash
git add file.txt
```

## Stage interactively (recommended)

```bash
git add -p
```

This lets you create clean commits by selecting hunks.

## Commit

```bash
git commit -m "feat: message"
```

## Amend (local only)

```bash
git commit --amend
```

Use for fixing the last commit before pushing.

## Common pitfall

Accidentally committing extra files.
Fix: unstage then stage carefully:

```bash
git restore --staged .
git add -p
```
