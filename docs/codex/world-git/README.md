---
title: "World Git — Codex"
world_id: world-git
type: codex_landing
version: 1
---

# World Git — Codex (Workflow Foundations)

This Codex is your **map + debugger** for Git in [oaicite:0]{index=0}.

Git problems aren’t “hard” — they’re usually **unclear mental models**.
If you learn the model (Working Tree / Index / HEAD) and the recovery tools (reflog), you stop being afraid of Git.

---

## How to use this Codex

- **Learning mode:** read the Core Model once, then follow the Quest Map.
- **Stuck mode:** jump to the exact tool you need (reset vs revert, rebase vs merge).
- **Panic mode:** go straight to Recovery (Reset/Revert/Reflog).

---

## Core Model (the 80/20)

### Git tracks *snapshots*, not “diff files”
A commit is a snapshot of the repository state.

### There are 3 key places your changes can live
1) **Working Tree** (your files)
2) **Index / Staging Area** (what will go into the next commit)
3) **HEAD** (your last commit / current commit)

Read: **[mental-model](./mental-model.md)**

---

## Quick Links (most used)

- **[mental-model](./mental-model.md)** — Working Tree / Index / HEAD
- **[status-and-diff](./status-and-diff.md)** — see what changed
- **[add-and-commit](./add-and-commit.md)** — stage + commit correctly
- **[branches](./branches.md)** — create/switch/understand branch pointers
- **[merge](./merge.md)** — combine histories safely
- **[rebase](./rebase.md)** — rewrite history carefully
- **[conflicts](./conflicts.md)** — resolve with confidence
- **[reset-vs-revert](./reset-vs-revert.md)** — undo safely (the #1 confusion)
- **[stash](./stash.md)** — park work temporarily
- **[reflog](./reflog.md)** — recovery superpower
- **[remotes](./remotes.md)** — origin, fetch, pull, push
- **[gitignore](./gitignore.md)** — keep junk out of commits

---

## Quest Map (by skill)

### Foundation
- See what changed → [status-and-diff](./status-and-diff.md)
- Stage correctly → [add-and-commit](./add-and-commit.md)

### Branching and integration
- Work in branches → [branches](./branches.md)
- Integrate work → [merge](./merge.md) + [rebase](./rebase.md)

### “Fix it” skills
- Resolve conflicts → [conflicts](./conflicts.md)
- Undo changes → [reset-vs-revert](./reset-vs-revert.md)
- Save unfinished work → [stash](./stash.md)

### Recovery & collaboration
- Recover “lost” commits → [reflog](./reflog.md)
- Work with origin → [remotes](./remotes.md)
- Ignore build artifacts → [gitignore](./gitignore.md)

---

## Diagnostics Checklist (when something goes wrong)

### 1) Identify where your change lives
- Working Tree only? → `git status`
- Staged? → `git status` (staged section)
- Committed? → `git log --oneline --decorate -n 10`

### 2) Choose the right “undo”
- Undo **uncommitted** file edits → `git restore <file>`
- Undo **staged** changes (unstage) → `git restore --staged <file>`
- Undo a **commit** safely on shared branches → `git revert <sha>`
- Move branch pointer (local/private) → `git reset --hard <sha>`

### 3) If you’re panicking: use reflog
- “I lost my commit” → `git reflog` then reset back.

Read: [reflog](./reflog.md)

---

## Tiny Patterns (copy/paste friendly)

```bash
# see state
git status
git diff
git diff --staged

# stage + commit
git add -p
git commit -m "message"

# branch
git switch -c feat/my-work
git switch main

# update local main
git fetch origin
git switch main
git pull --ff-only

# merge feature into main
git switch main
git merge --no-ff feat/my-work

# rebase feature onto main (local)
git switch feat/my-work
git rebase main

# conflict help
git status
git add <resolved-files>
git rebase --continue  # or: git commit after merge conflict

# “oh no” recovery
git reflog
git reset --hard <sha-from-reflog>
```
