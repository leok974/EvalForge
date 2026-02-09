---
title: Shell
id: glossary/infra/shell
world: infra
level: beginner
tags: [command-line, scripting, debugging]
related:
  - codex:glossary/infra/permissions
  - codex:glossary/infra/path
---

# Shell

## Definition
A shell is a command interpreter (`bash`, `sh`, `pwsh`) used to run scripts and commands. Different shells have different syntax rules.

## Usage
- Pick a shell consistent with your environment.
- Use `set -euo pipefail` in bash for safer scripts.
- Prefer portable commands in CI.

## Example
```bash
set -euo pipefail
echo "Hello"
```

## Pitfalls

* Bash scripts don't run the same on PowerShell.
* Quoting rules differ; unquoted variables cause bugs.

## Related

* Permissions: shells execute with user permissions.
* Path: shells resolve paths and navigate directories.