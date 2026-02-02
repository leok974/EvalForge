# Commit

## Definition
A **commit** is a snapshot of the staging area saved into the repository history. It includes the changed content plus metadata (author, timestamp, message, parent commit).

## Tiny example
`git commit -m "Add greeting file"` creates a new commit and moves the current branch forward.

## Common pitfall
A commit only includes what is staged. If you forgot to stage a file, it will not be part of the commit even if it’s modified in your working tree.

## Related
Commit Message, Branch
