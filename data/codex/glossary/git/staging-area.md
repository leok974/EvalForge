# Staging Area

## Definition
The **staging area** (also called the index) is where you choose which changes will be included in the next commit. Staging is how you build a clean, intentional commit.

## Tiny example
`git add hello.txt` stages changes to `hello.txt`. `git diff --staged` shows what will be committed.

## Common pitfall
If you edit a file after staging it, the staging area still contains the older version. Re-run `git add` to include the latest edits.

## Related
Working Tree, Commit
