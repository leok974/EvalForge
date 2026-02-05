---
id: glossary/cli/paths
title: Paths
world: cli
---

# Paths

A **path** is the address of a file or folder in your filesystem.

## Types of Paths

### Absolute Path
Starts from the root of the filesystem. Always works regardless of your working directory.

**Unix/Linux/Mac:**
```bash
/home/user/documents/notes.txt
```

**Windows:**
```powershell
C:\Users\user\Documents\notes.txt
```

### Relative Path
Starts from your current working directory.

```bash
documents/notes.txt
./scripts/run.sh
../parent-folder/file.txt
```

## Special Shortcuts

- `.` = current directory
- `..` = parent directory
- `~` = home directory (Unix-like systems)
- `/` = root directory (Unix) or drive separator (Windows)

## Best Practices

- Use absolute paths in scripts for reliability
- Use relative paths for portability
- Understand `~` expands differently per user

## Related Concepts

- [Working Directory](codex:glossary/cli/working-directory)