---
title: "World CLI — Codex"
world_id: world-cli
type: codex_landing
version: 1
---

# World CLI — Codex (Command Line Foundations)

This Codex is your **reference map** for the command line skills used throughout EvalForge.  
If you ever get stuck in a CLI quest, come back here to refresh the exact concept you need.

## How to use this Codex

- **Learning mode:** skim the “Core Loop” sections top-to-bottom once.
- **Stuck mode:** jump straight to the concept link you need (pipes, redirection, quoting, exit codes).
- **Debug mode:** use the “Diagnostics” checklist near the bottom.

> **Rule of thumb:** When your output is wrong, it’s usually a **format** issue (whitespace/order), a **search/sort** issue, or a **quoting** issue.

---

## The Core Loop (the 80/20)

### 1) Navigate with intent
You always want to know: *Where am I? What files exist?*
- `pwd` — print current directory
- `ls -la` — list details (hidden files too)
- `cd ..` / `cd -` — up / previous

### 2) Inspect before you edit
- `cat file.txt` — show contents
- `head -n 5` / `tail -n 5` — preview edges

### 3) Transform data with small tools
Most CLI problems are **pipeline composition**:
- `grep` filters lines
- `sort` orders lines deterministically
- `uniq -c` counts duplicates
- `awk` reshapes columns

### 4) Write results to files
- `>` overwrite
- `>>` append

### 5) Control behavior with exit codes
- `0` success
- non-zero = failure (quest-defined)

---

## Quick Links (most-used concepts)

### Output + files
- **Redirection** — [`>` and `>>`](./redirection.md)  
- **Outputs folders** — [`mkdir -p outputs`](./working-directory.md)  
- **Path basics** — [relative vs absolute paths](./paths.md)

### Search + filtering
- **Globs** — [`*.log`, `fixtures/*`](./globs.md)  
- **Grep** — [`grep`, `grep -l`, `grep -w`](./search.md)  
- **Find** — [`find … -type f`](./search.md)

### Pipelines + sorting
- **Pipes** — [`|` connects tools](./pipes.md)  
- **Sorting** — [stable, deterministic `sort`](./pipes.md)  
- **Counting** — [`uniq -c`](./pipes.md)  
- **Reshaping** — [`awk '{print $2}'`](./pipes.md)

### Scripting fundamentals
- **Args** — [`$1`, `$2`, `$#`](./scripting-basics.md)  
- **Env vars** — [`${MODE:-dev}`](./env-vars.md)  
- **Quoting** — [why `"${var}"` matters](./scripting-basics.md)  
- **Exit codes** — [`exit 2`, `exit 5`](./exit-codes.md)

---

## CLI Quest Map (by concept)

Use this to jump from “what I’m learning” → “which quest uses it”.

### Navigation & filesystem
- **cli-ignition** → folders, listing, baseline muscle memory  
- **cli-navigation** → `cd`, path correctness, verifying location  
- **cli-files-folders** → `mkdir -p`, copy/move/delete safely

### Searching & matching patterns
- **cli-globs-search** → globs + grep across files, filename extraction

### Building outputs deterministically
- **cli-redirection** → exact file construction with `>`/`>>`
- **cli-pipes** → sort/uniq/awk pipelines (and why `sort` matters)

### Runtime configuration & correctness
- **cli-env-vars** → defaults, empty handling, config output  
- **cli-exit-codes** → stderr vs stdout, exit code contracts  
- **cli-processes** → parsing a table, numeric sorting  
- **cli-scripting** → args + usage errors + mkdir for destination paths

---

## Diagnostics Checklist (when tests fail)

### A) Output formatting
- Did you include an extra trailing space?
- Did you include an extra blank line at end?
- Are you writing to the correct file path?

### B) Ordering / determinism
- Are you relying on filesystem order?  
  ✅ fix: add `| sort` before writing lists

### C) Match correctness
- Should it be case-sensitive?
- Do you need whole-word matching (`grep -w`)?
- Are you mistakenly matching substrings (FAIL vs FAILURE)?

### D) Quoting & paths
- Are you quoting variables?  
  ✅ `cp "$src" "$dst"`
- Are you creating the destination directory?  
  ✅ `mkdir -p "$(dirname "$dst")"`

### E) Exit codes & streams
- On success: stdout only, exit 0
- On error: stderr, correct non-zero code

---

## Recommended “tiny patterns” to memorize

### Safe directory creation
```sh
mkdir -p outputs
```

### Write file (overwrite / append)

```sh
echo "HEADER" > outputs/report.txt
cat fixtures/data.txt >> outputs/report.txt
echo "FOOTER" >> outputs/report.txt
```

### Count + list files with matches

```sh
count="$(grep "ERROR" fixtures/logs/*.log 2>/dev/null | wc -l | tr -d ' ')"
grep -l "ERROR" fixtures/logs/*.log 2>/dev/null | xargs -n 1 basename | sort
```

### Args + usage contract

```sh
if [ "$#" -ne 2 ]; then
  echo "Usage: sh task.sh <src> <dst>" 1>&2
  exit 2
fi
```

### Env var defaults (empty-safe)

```sh
mode="${MODE:-dev}"
[ -n "$mode" ] || mode="dev"
```

---

## Next expansions (future-proof hooks)

If/when we expand world-cli to Tier-2:

* permissions + `chmod`
* archives + `tar`, `gzip`
* `sed` and more complex `awk`
* process signals (simulated)
* git-style CLI ergonomics

But Tier-1 already covers the reusable core that powers most engineering workflows.

---

### Tip: Use Codex while solving

If you’re stuck, don’t guess. Open the relevant concept page, copy the “tiny pattern”, and adapt it to the quest.


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]