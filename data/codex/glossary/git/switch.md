# Switch/Checkout

## Definition
`git switch` (and older `git checkout`) changes your current branch/commit, updating your working tree to match it. It’s how you move between branches.

## Tiny example
`git switch main` moves you to `main`.
`git switch -c feature/y` creates and switches to `feature/y`.

## Common pitfall
Switching branches with uncommitted changes can fail (or cause conflicts). Commit your work, stash it, or revert changes before switching if Git warns you.

## Related
HEAD, Branch
