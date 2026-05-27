---
title: Upstream Tracking Branch
id: glossary/world-git/term-2
world: world-git
level: intermediate
tags: [branches, remotes, workflow]
related:
  - codex:glossary/git/branch
  - codex:glossary/git/switch
---

# Upstream Tracking Branch

## Definition
An **upstream tracking branch** links your local branch to a remote branch (often `origin/main` or `origin/feature-x`). It enables simple `git pull` and shows "ahead/behind" status.

## Usage
- Set tracking when creating a branch from a remote.
- Push with `-u` to establish upstream.
- Use `status` to see divergence.

## Example
```bash
git switch -c feature-x
git push -u origin feature-x

git status   # shows ahead/behind
git pull     # uses upstream automatically
```

## Pitfalls

* Pulling without understanding merge vs rebase can create noisy history.
* Tracking the wrong remote branch can cause confusing diffs and pushes.

## Related

* Branch: upstream links local branches to remote branches.
* Switch: switch creates branches that can track upstreams.
