---
title: Detached HEAD
id: glossary/world-git/term-1
world: world-git
level: intermediate
tags: [branches, debugging, concepts]
related:
  - codex:glossary/git/head
  - codex:glossary/git/branch
  - codex:glossary/git/switch
---

# Detached HEAD

## Definition
A **detached HEAD** state means `HEAD` points directly to a commit instead of a branch name. You can still make commits, but they won't belong to any branch unless you create one—so they're easy to "lose" later.

## Usage
- Happens when you `checkout` a commit hash or a tag.
- Useful for quick experiments or inspecting old states.
- Convert work into a branch if you want to keep it.

## Example
```bash
git switch --detach <commit>
git status

# Keep your work:
git switch -c fix/experiment
```

## Pitfalls

* Committing in detached HEAD without creating a branch can make the commits hard to find later.
* Switching branches without saving can "orphan" your work (recoverable via reflog).

## Related

* Head: detached HEAD is when HEAD points to a commit instead of a branch.
* Branch: create a branch to save detached HEAD work.
* Switch: use switch to enter/exit detached HEAD state.
