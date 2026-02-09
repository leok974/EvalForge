---
title: Cwd
id: glossary/infra/cwd
world: infra
level: beginner
tags: [filesystem, debugging, shell]
related:
  - codex:glossary/infra/path
  - codex:glossary/infra/shell
---

# Cwd

## Definition
**CWD** (current working directory) is the directory a process treats as "here." Relative paths resolve from CWD, so wrong CWD causes file-not-found errors.

## Usage
- Set CWD in scripts and runners.
- Use `WORKDIR` in Dockerfile.
- In Node/Python, log the working dir when debugging.

## Example
```bash
pwd
cd /app
```

## Pitfalls

* CI often runs from repo root; local runs might not.
* Tools that spawn subprocesses may change CWD unexpectedly.

## Related

* Path: paths are resolved relative to CWD.
* Shell: shells track and change CWD.