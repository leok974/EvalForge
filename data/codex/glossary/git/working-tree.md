# Working Tree

## Definition
The **working tree** is your current set of files on disk — what you edit in your editor. It can include untracked files, modified files, and files that match the last commit.

## Tiny example
Editing `README.md` changes the working tree. Git will show it as “modified” in `git status`.

## Common pitfall
People think “saving a file” automatically stages it. Saving updates the working tree only. You still need `git add` to stage changes for a commit.

## Related
Staging Area, Commit
