# Branch

## Definition
A **branch** is a movable label pointing to a commit. When you create new commits while on a branch, that branch pointer advances.

## Tiny example
`git switch -c feature/x` creates a new branch and checks it out. Commits now move `feature/x` forward.

## Common pitfall
People treat branches like folders. Branches don’t “contain files” — they point to commits that *describe* file states. Switching branches changes your working tree to match the commit the branch points to.

## Related
HEAD, Merge
