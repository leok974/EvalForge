---
title: Head
id: glossary/git/head
world: git
level: beginner
tags: [fundamentals, concepts, internal]
related:
  - codex:glossary/git/branch
  - codex:glossary/world-git/term-1
  - codex:glossary/git/switch
---

# Head

## Definition
**HEAD** is a pointer to the current commit you're on. Usually it points to a branch name (like `main`), but in detached HEAD state it points directly to a commit.

## Usage
- View current position with `git status` or `git log`.
- HEAD typically follows your current branch.
- Detaching HEAD lets you inspect old commits.

## Example
```bash
git log   # shows HEAD position
cat .git/HEAD   # shows what HEAD points to
```

## Pitfalls

* Working in detached HEAD without creating a branch can lose commits.
* HEAD moves when you commit or switch branches—it's not static.

## Related

* Branch: HEAD usually points to a branch.
* Detached HEAD: HEAD can point directly to a commit (Term 1).
* Switch: switching branches moves HEAD.
