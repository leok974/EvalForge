# Search

**Search** tools help you find files and content across your filesystem.

## Common Search Commands

### `find` (Unix/Linux/Mac)
Search by filename, type, size, modification time, etc.

```bash
# Find all .py files
find . -name "*.py"

# Find files modified in last 7 days
find . -mtime -7

# Find and delete empty files
find . -empty -delete
```

### `Get-ChildItem` (PowerShell/Windows)
```powershell
# Recursive search for .log files
Get-ChildItem -Recurse -Filter *.log

# Find files larger than 10MB
Get-ChildItem -Recurse | Where-Object { $_.Length -gt 10MB }
```

### `grep` (Content Search)
Search **inside** files for text patterns.

```bash
# Find files containing "TODO"
grep -r "TODO" .

# Case-insensitive search
grep -ri "error" logs/
```

## Best Practices

- Use `find` for **filenames**, `grep` for **contents**
- Add `-type f` to find only files, `-type d` for directories
- Combine with other tools via pipes

## Related Concepts

- [Globs](codex:glossary/cli/globs)
- [Pipes](codex:glossary/cli/pipes)
