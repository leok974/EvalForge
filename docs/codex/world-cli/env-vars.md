---
id: glossary/cli/env-vars
title: Env Vars
world: cli
---

# Environment Variables

**Environment variables** are key-value pairs that configure how programs behave.

## What They Do

- Store configuration (API keys, database URLs, preferences)
- Control program behavior without changing code
- Pass information from parent processes to child processes

## Viewing Variables

```bash
# Print all environment variables
printenv
# or
env

# Print specific variable
echo $HOME
echo $USER
```

## Setting Variables

### Temporary (current session only)

```bash
# Bash/Zsh
export API_KEY="secret123"

# PowerShell
$env:API_KEY = "secret123"
```

### Permanent

Add to your shell's config file:
- Bash: `~/.bashrc` or `~/.bash_profile`
- Zsh: `~/.zshrc`
- PowerShell: Profile script

```bash
export DATABASE_URL="postgres://localhost/mydb"
```

## Common Variables

- `HOME` — user's home directory
- `USER` — current username
- `PATH` — where to find executables
- `SHELL` — current shell program
- `EDITOR` — default text editor

## Best Practices

- Use UPPERCASE names by convention
- Never commit secrets to version control
- Use `.env` files + loaders for projects
- Document required variables in README

## Related Concepts

- [PATH](codex:glossary/cli/path)