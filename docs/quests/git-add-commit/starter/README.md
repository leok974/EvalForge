# Add + Commit

## Objective
Stage specific files, ignore logs, and commit with an exact message.

## Requirements
Running:
  sh task.sh
must:
1) Create `sandbox/repo` git repo (branch main)
2) Create files in repo:
   - greeting.txt (from fixtures/greeting.txt)
   - config.json (from fixtures/config.json)
   - temp.log (from fixtures/temp.log)
3) Ensure `.gitignore` ignores `*.log`
4) Commit ONLY greeting.txt + config.json with message:
   `Add greeting and config`
5) Write `outputs/summary.json`:
   - tracked: ["config.json","greeting.txt"]
   - ignoredPresent: true
   - commitMessage: "Add greeting and config"
