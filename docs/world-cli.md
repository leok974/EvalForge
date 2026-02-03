# world-cli — Command Line Foundations

Welcome to the CLI world in [oaicite:0]{index=0}.

This world teaches you the **portable command line skills** you’ll use everywhere: navigating directories, inspecting files, searching text, composing pipelines, handling env vars, and writing small scripts.

You’ll solve each quest by editing a single file:

> `workspace/task.sh` (POSIX `sh`, not Bash)

EvalForge grades your script in a **Linux/Docker environment**, so your solution should behave consistently there.

---

## How quests work

### What you edit
- `workspace/task.sh` — the only file you should modify.

### What you run (locally)
From the quest’s `workspace/` directory:

```bash
sh task.sh
```

### What the grader does

* Runs `sh task.sh` inside the quest workspace
* Checks:

  * **stdout/stderr output**
  * **exit code**
  * **files you create in outputs/** (or sandbox/**)
* Runs “dynamic” tests too (hidden tests may add files or change fixture contents to ensure you **didn’t hardcode** the answer)

---

## Golden rules (how to pass consistently)

1. **Don’t hardcode.**
   If the test can add a file or change input, your script must still work.

2. **Be deterministic.**
   Prefer `sort` before writing lists. Don’t depend on filesystem ordering.

3. **Don’t write to stderr on success.**
   Keep errors for actual failures.

4. **Use POSIX `sh` features only.**
   Avoid Bashisms like arrays, `[[ ... ]]`, or `source`.

5. **Prefer simple, readable commands.**
   You’re learning patterns you’ll reuse in Node/React/Infra worlds.

---

## Common pitfalls (and quick fixes)

### “It works on my machine, fails in EvalForge”

EvalForge runs in Linux. Differences you’ll feel:

* Line endings: prefer **LF**, not CRLF.
* `sh` vs `bash`: use portable syntax.
* Paths: use forward slashes, avoid Windows-only tools.

### Scripts fail immediately

If your script uses:

```sh
set -eu
```

That’s good — but it means:

* referencing an unset var crashes (`$MODE` when MODE not set)
* any failing command crashes (so guard with `|| true` if appropriate)

### Quoting mistakes

When in doubt, quote:

* ✅ `"$dst"`
* ✅ `"$(dirname "$dst")"`
* ❌ `$dst` (breaks with spaces)

---

## CLI cheat sheet (the “you’ll use this constantly” list)

### Navigation

```bash
pwd
cd path/to/dir
cd ..         # up
cd -          # previous dir
```

### Listing

```bash
ls -1
ls -la
```

### Searching text

```bash
grep "ERROR" file
grep -l "ERROR" *.log     # list matching files
grep -w "FAIL" input.txt  # whole word
```

### Finding files

```bash
find fixtures -maxdepth 1 -type f
```

### Redirection

```bash
echo "HEADER" > out.txt   # overwrite
echo "FOOTER" >> out.txt  # append
cat file.txt >> out.txt
```

### Pipes

```bash
cat names.txt | sort | uniq -c
```

### Exit codes

```bash
exit 0   # success
exit 2   # usage error
exit 5   # explicit failure (quest-defined)
```

### Env vars with defaults

```sh
mode="${MODE:-dev}"
[ -n "$mode" ] || mode="dev"
```

### Args

```sh
if [ "$#" -ne 2 ]; then
  echo "Usage: sh task.sh <src> <dst>" 1>&2
  exit 2
fi
```

---

## Learning path (recommended order)

1. **cli-ignition** — print basics + count files (introduces `pwd`, `find`, `wc`)
2. **cli-navigation** — `cd` into nested dirs + write proof (`pwd`, `ls -1`)
3. **cli-files-folders** — `mkdir -p`, `cp`, `mv`, `rm -rf` safely
4. **cli-globs-search** — search across files (`grep`, globs like `*.log`)
5. **cli-redirection** — build a file with `>` and `>>`
6. **cli-pipes** — compose tools (`sort | uniq -c | awk | sort`)
7. **cli-env-vars** — config from environment with defaults
8. **cli-exit-codes** — error handling + stderr + specific exit codes
9. **cli-processes** — parse a simulated `ps` table (sorting numeric columns)
10. **cli-scripting** — arguments + directory creation + robust copy

---

## Debugging tips

### Print what you’re doing (temporarily)

```sh
set -x
```

Remove it when done (some quests require clean stdout).

### Inspect outputs

```bash
cat outputs/*.txt
ls -R sandbox
```

### Verify exit codes

```bash
sh task.sh
echo $?
```

---

## Safety constraints (intentional)

Some quests simulate real system behavior (like processes) using fixture files to keep grading safe and deterministic:

* No real process killing
* No network dependency
* No OS-specific assumptions

---

## What “good” looks like

A great solution:

* is short and readable
* works if fixtures change (dynamic tests)
* produces exact output format
* uses standard CLI tools and POSIX `sh`

When you’re ready, jump into **cli-ignition** and run:

```bash
sh task.sh
```

Then iterate until the public + hidden tests pass.
