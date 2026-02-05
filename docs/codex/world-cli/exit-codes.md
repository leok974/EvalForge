---
id: glossary/cli/exit-codes
title: Exit Codes
world: cli
---

# Exit Codes

An **exit code** (or return code) is a number a program returns when it finishes, indicating success or failure.

## Convention

- `0` = **success**
- Non-zero (1–255) = **failure** (specific meaning varies by program)

## Checking Exit Codes

```bash
# Bash/Zsh
echo $?

# PowerShell
echo $LASTEXITCODE
```

The variable holds the exit code of the **most recent** command.

## Examples

```bash
ls /valid/path
echo $?
# 0 (success)

ls /invalid/path
echo $?
# 2 (error)
```

## Using in Scripts

### Simple Check

```bash
if command; then
    echo "Success!"
else
    echo "Failed"
fi
```

### Chain with `&&` and `||`

```bash
# Run command2 only if command1 succeeds
command1 && command2

# Run command2 only if command1 fails
command1 || command2

# Common pattern: fallback
command1 || { echo "Failed, exiting"; exit 1; }
```

### Set Your Own

```bash
#!/bin/bash
if [ ! -f "config.txt" ]; then
    echo "Error: config.txt missing"
    exit 1  # Signal failure
fi

# do work...
exit 0  # Signal success
```

## Best Practices

- **Always** set meaningful exit codes in scripts
- Check exit codes for critical operations (deployments, backups, etc.)
- Use `set -e` in Bash to exit immediately on any error

## Related Concepts

- [Scripting Basics](codex:glossary/cli/scripting-basics)