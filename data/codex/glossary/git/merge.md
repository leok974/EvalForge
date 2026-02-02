# Merge

## Definition
A **merge** combines changes from one branch into another. Typically, you merge a feature branch into `main` after it’s ready.

## Tiny example
On `main`:
`git merge feature/readme-update`

## Common pitfall
Merges can create conflicts when both branches changed the same lines. The fix is to resolve conflicts in files, then commit the merge result. Merge is easier when commits are small and focused.

## Related
Branch, Main Branch
