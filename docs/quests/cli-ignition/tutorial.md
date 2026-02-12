# Tutorial — CLI Ignition

## What you’re practicing
- Reading your environment: `pwd`, `basename`
- Counting files safely (no hardcoding)
- Printing deterministic output

## Implementation
1) Compute the working directory basename:
- `basename "$(pwd)"`

2) Count **only** regular files directly under `fixtures/`:
- `find fixtures -maxdepth 1 -type f | wc -l`

3) Print the three lines in order:
- `CWD=...`
- `FILES=...`
- `OK`

## Testing
Run:
```sh
sh task.sh
```

You should see three lines and nothing else.

## Pitfalls

* Counting subdirectories (use `-type f`)
* Counting nested files (use `-maxdepth 1`)
* Extra spaces from `wc -l` (trim or normalize)
* Adding “debug” output that breaks the exact contract
