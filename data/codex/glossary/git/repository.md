# Repository

## Definition
A **repository** is the Git database that stores your project’s history (commits, branches, tags). A repo is usually a folder containing a hidden `.git/` directory.

## Tiny example
Running `git init` creates `.git/` and turns the folder into a repository.

## Common pitfall
If you run Git commands outside the repo folder, Git can’t find `.git/` and will error. When in doubt:
- `pwd`
- `ls -a` (look for `.git`)

## Related
Commit, Branch
