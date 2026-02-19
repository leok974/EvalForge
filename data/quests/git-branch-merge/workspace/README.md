# Branch + Merge (No Conflicts)

## Objective
Create a feature branch, commit work, then merge it into main with a merge commit.

## Requirements
Running:
  sh task.sh
must:
1) Create repo `sandbox/repo` (main)
2) Commit base.txt ("base")
3) Create branch `feature`, add feature.txt, commit "feature work"
4) Switch back to main, add main.txt, commit "main work"
5) Merge feature into main producing a MERGE COMMIT with message: "Merge feature"
6) Write outputs/parents.txt containing `git rev-list --parents -n 1 HEAD`
