---
title: Main Branch
id: glossary/git/main-branch
world: git
level: beginner
tags: [workflow, fundamentals, convention]
related:
  - codex:glossary/git/branch
  - codex:glossary/git/merge
  - codex:glossary/world-git/term-3
---

# Main Branch

## Definition
The **main branch** (often `main` or `master`) is the primary branch where production-ready code lives. Feature branches merge into main after passing review and tests.

## Usage
- Protect main from direct pushes (use PRs).
- Merge only tested and reviewed changes.
- Tag releases from main.

## Example
```bash
git switch main
git pull
git merge feat/new-feature
git push
```

## Pitfalls

* Pushing broken code to main breaks deployments and other developers.
* Not tagging releases makes rollbacks harder.

## Related

* Branch: main is a special branch by convention.
* Merge: feature branches merge into main.
* Pull Request (PR): PRs protect main from direct pushes (Term 3).
