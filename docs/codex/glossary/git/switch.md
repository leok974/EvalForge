---
title: Switch
id: glossary/git/switch
world: git
level: beginner
tags: [workflow, fundamentals, commands]
related:
  - codex:glossary/git/branch
  - codex:glossary/git/head
  - codex:glossary/world-git/term-1
---

# Switch

## Definition
`git switch` changes which branch you're working on. It updates HEAD and your working directory to match the target branch.

## Usage
- Create and switch to a new branch with `-c`.
- Switch between existing branches.
- Enter detached HEAD with `--detach`.

## Example
```bash
git switch main
git switch -c feat/new-feature
git switch --detach abc123
```

## Pitfalls

* Unsaved changes can block switching—commit or stash first.
* Creating branches from wrong base can cause merge headaches.

## Related

* Branch: switch changes active branch.
* Head: switch moves HEAD to point at different branches.
* Detached HEAD: switch --detach enters detached HEAD (Term 1).
