# Stash

## Objective
Stash WIP changes (including untracked), then restore them.

## Requirements
Running:
  sh task.sh
must:
1) Create repo sandbox/repo (main) with notes.txt committed
2) Modify notes.txt and create untracked tmp.txt
3) Stash INCLUDING untracked with message "wip"
4) After stashing, repo must be clean
5) Apply the stash so changes return
6) Write:
   - outputs/status_clean.txt (git status --porcelain after stash; must be empty)
   - outputs/status_dirty.txt (git status --porcelain after apply; must show changes)
   - outputs/stash_list.txt (git stash list)
