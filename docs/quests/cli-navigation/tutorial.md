# Tutorial — CLI Navigation

## What you’re practicing
- `cd` into a directory and confirm where you are (`pwd`)
- Using a “home base” variable so you never get lost
- Redirecting command output into files

## Plan
1) Save the workspace path:
- `WS="$(pwd)"`

2) Create `outputs/`:
- `mkdir -p outputs`

3) Move into the pages directory:
- `cd fixtures/site/pages`

4) Write the pages directory absolute path:
- `pwd > "$WS/outputs/location.txt"`

5) Write a one-per-line file listing:
- `ls > "$WS/outputs/pages.txt"`

6) Return to the workspace:
- `cd "$WS"`

7) Write the workspace absolute path:
- `pwd > outputs/back.txt`

## Pitfalls
- Writing files relative to the wrong directory (use `$WS/outputs/...`)
- Forgetting to `cd` back before writing `back.txt`
- Printing extra output that breaks test determinism
