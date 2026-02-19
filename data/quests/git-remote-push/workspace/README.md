# Remote + Push (Local Bare)

## Objective
Add a local bare remote and push main to it.

## Requirements
Running:
  sh task.sh
must:
1) Create repo sandbox/repo (main) with a single commit "init"
2) Create bare remote at sandbox/remote.git
3) Add it as origin and push main
4) Write outputs/refs.txt containing `git --git-dir=sandbox/remote.git show-ref`
