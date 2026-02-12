# Status + Diff

## Objective
Generate a porcelain status snapshot and a diffstat.

## Requirements
Running:
  sh task.sh
must:
1) Create a repo in `sandbox/repo` (main)
2) Commit `app.txt` with content from fixtures/app_v1.txt
3) Modify app.txt by replacing content with fixtures/app_v2.txt (do NOT commit)
4) Create untracked file `notes.md` with content from fixtures/notes.txt (do NOT commit)
5) Write:
   - outputs/porcelain.txt  (git status --porcelain)
   - outputs/diffstat.txt   (git diff --stat)
No extra stdout.
