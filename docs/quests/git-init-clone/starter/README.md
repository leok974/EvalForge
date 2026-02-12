# Git Init + Clone (Local)

## Objective
Create a repo, make an initial commit, create a local bare "remote", and clone it.

## Requirements
Running:
  sh task.sh
must:
1) Create `sandbox/repo` as a git repository (branch `main`)
2) Copy `fixtures/hello.txt` into `sandbox/repo/hello.txt`
3) Commit it with message: `init`
4) Create a bare remote at `sandbox/remote.git`
5) Clone that remote into `sandbox/clone`
6) Write `outputs/report.json` with:
   - repoExists: true
   - branch: "main"
   - commitCount: 1
   - headMessage: "init"
   - cloneHasGit: true

## Notes
- Do not print extra stdout.
- Use safe defaults (create folders if missing).
