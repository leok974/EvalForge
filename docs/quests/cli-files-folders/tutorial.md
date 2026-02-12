# Tutorial — CLI Files & Folders

## What you’re practicing
- Creating nested directories safely (`mkdir -p`)
- Copying files (preserving the source) (`cp`)
- Removing a directory if it exists (`rm -rf`)
- Idempotent scripts: running twice still succeeds

## Plan
1) Create the destination directory:
- `mkdir -p sandbox/archive/2026`

2) Copy the invoice (copy, don’t move):
- `cp fixtures/invoice.txt sandbox/archive/2026/invoice.txt`

3) Copy + rename the README:
- `cp fixtures/readme.md sandbox/README.md`

4) Ensure tmp is gone (even if it existed):
- `rm -rf sandbox/tmp`

## Pitfalls
- Using `mv` (breaks the “fixtures are read-only” rule)
- Forgetting `-p` (script fails if directories don’t exist)
- Using `rm -r` without `-f` (fails if the folder doesn’t exist)
- Writing extra debug output that breaks deterministic grading
