---
title: Pull Request (PR)
id: glossary/world-git/term-3
world: world-git
level: intermediate
tags: [workflow, collaboration, ci]
related:
  - codex:glossary/git/merge
  - codex:glossary/git/main-branch
  - codex:glossary/git/branch
---

# Pull Request (PR)

## Definition
A **pull request (PR)** is a workflow for proposing changes: you push a branch, open a PR, run automated checks, and request review before merging. PRs provide discussion, traceability, and quality gates.

## Usage
- Create a feature branch, push to remote, open PR into main.
- Let CI validate tests/lint before merge.
- Use PRs to review diffs and manage release history.

## Example
```bash
git switch -c feat/codex-cleanup
git add .
git commit -m "Promote Git placeholder terms"
git push -u origin feat/codex-cleanup
# Open PR in GitHub UI
```

## Pitfalls

* Merging without updating from main can cause painful conflicts.
* Squash vs merge vs rebase affects history—be consistent.

## Related

* Merge: PRs result in merges into the target branch.
* Main Branch: PRs typically merge into main.
* Branch: PRs are created from feature branches.
