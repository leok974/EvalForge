# Rebase: Linear History

## Objective
Rebase feature onto main, then fast-forward merge so history stays linear (no merge commit).

## Requirements
Running:
  sh task.sh
must:
1) Create repo sandbox/repo (main)
2) Commit "base" on main
3) Create branch feature, commit "feature"
4) Switch to main, commit "main"
5) Switch to feature, rebase onto main
6) Switch to main, merge --ff-only feature
7) Write outputs/parents.txt = `git rev-list --parents -n 1 HEAD`
8) Write outputs/log.txt = `git log --oneline -3` (newest first)
