---
id: glossary/cli/path
title: Path
world: cli
---

# PATH

The `PATH` environment variable tells your shell **where to find executable programs**.

## How It Works

When you type a command like `python`, the shell searches each directory in `PATH` (in order) until it finds an executable named `python`.

```bash
# View your PATH
echo $PATH
# /usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Directories are separated by `:` (Unix/Mac) or `;` (Windows).

## Adding to PATH

### Temporary

```bash
# Bash/Zsh
export PATH="/my/custom/bin:$PATH"

# PowerShell
$env:PATH = "C:\MyTools;$env:PATH"
```

**Important:** Put new paths at the **start** to prioritize them.

### Permanent

Add to your shell config:

```bash
# ~/.bashrc or ~/.zshrc
export PATH="$HOME/bin:$PATH"
```

## Troubleshooting

### "Command not found" errors

1. Check if the program is installed
2. Find where it's installed: `which python` or `where python`
3. Add that directory to PATH
4. Restart your terminal

### Multiple versions conflict

The **first match** in PATH wins. Reorder directories to change priority.

## Best Practices

- Prepend custom paths (don't replace PATH entirely)
- Use absolute paths in scripts if tools aren't in standard locations
- Check `which <command>` to see which binary will run

## Related Concepts

- [Environment Variables](codex:glossary/cli/env-vars)