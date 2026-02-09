---
title: Branch
id: glossary/git/branch
world: git
level: beginner
tags: [workflow, fundamentals, branching]
related:
  - codex:glossary/git/head
  - codex:glossary/git/switch
  - codex:glossary/git/main-branch
  - codex:glossary/git/merge
---

# Branch

## Definition
A **branch** is a named pointer to a commit. Branches let you develop features in isolation without affecting main, then merge changes back when ready.

## Usage
- Create branches for features, bug fixes, or experiments.
- Keep branches focused and short-lived.
- Merge or rebase back to main when done.

## Example
```bash
git switch -c feat/new-feature
git add .
git commit -m "Add feature"
git switch main
git merge feat/new-feature
```

## Pitfalls

* Long-lived branches diverge quickly and create painful merges.
* Forgetting to switch branches can commit to the wrong one.

## Related

* Head: HEAD points to the current branch.
* Switch: use switch to change branches.
* Main Branch: feature branches typically merge into main.
* Merge: branches are merged together.
