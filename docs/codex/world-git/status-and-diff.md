---
title: "Status & Diff"
world_id: world-git
type: codex_entry
level: tier1
---

# Status & Diff

Use these to see what changed and where it lives.

## Status
```bash
git status
```

Shows:

* modified but not staged
* staged changes
* untracked files
* current branch

## Diff

Working tree changes:

```bash
git diff
```

Staged changes:

```bash
git diff --staged
```

Compare commits/branches:

```bash
git diff main..feat/my-branch
```

## Tip

If tests fail due to “wrong contents in commit”, always check:

* `git diff --staged` before committing.
