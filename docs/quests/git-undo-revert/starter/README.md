# Undo with Revert

## Objective
Undo a bad commit safely using `git revert` (no history rewriting).

## Requirements
Running:
  sh task.sh
must:
1) Create repo sandbox/repo (main)
2) Commit app.txt="good" with message "good"
3) Commit app.txt="bad" with message "bad"
4) Revert the bad commit (creates a new commit)
5) Write:
   - outputs/app.txt (final content of app.txt)
   - outputs/log.txt (last 3 commit subjects, newest first)
