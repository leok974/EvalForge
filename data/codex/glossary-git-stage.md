---
id: glossary/git/stage
title: Staging Area (Git Index)
section: Glossary
world: Git
---

# Staging Area (Git Index)

The **staging area** (also called the "index") is Git's holding zone where you prepare changes before committing them. It sits between your working directory and the repository history.

## Three States of Files

Git files exist in one of three states:

```
Working Directory → Staging Area → Repository
  (modified)          (staged)      (committed)
```

1. **Modified**: Changed but not staged
2. **Staged**: Marked for inclusion in next commit
3. **Committed**: Permanently saved in repository

## Why Stage Before Commit?

The staging area gives you granular control:

- **Selective commits**: Stage only related changes
- **Review changes**: Preview what will be committed
- **Atomic commits**: Group logical changes together
- **Partial staging**: Stage portions of a file

## Common Commands

### Stage Files

```bash
# Stage a specific file
git add file.txt

# Stage all changes in current directory
git add .

# Stage all tracked files
git add -A

# Interactively stage hunks
git add -p
```

### View Staging Status

```bash
# Show working tree status
git status

# Show staged changes
git diff --staged
# or
git diff --cached
```

### Unstage Files

```bash
# Unstage a file (keep changes)
git restore --staged file.txt
# or (older syntax)
git reset HEAD file.txt

# Unstage all files
git restore --staged .
```

## Interactive Staging

Stage parts of a file with `git add -p`:

```bash
git add -p myfile.py
```

Git shows each "hunk" and prompts:
- `y` - stage this hunk
- `n` - don't stage this hunk
- `s` - split into smaller hunks
- `e` - manually edit the hunk

## Best Practices

1. **Review before staging**: Use `git diff` to see changes
2. **Stage related changes**: Keep commits focused
3. **Use interactive mode**: For complex changes
4. **Check status**: Run `git status` frequently
5. **Commit staged changes**: Don't leave files staged indefinitely

## Common Workflows

### Stage and Commit

```bash
git add file1.py file2.py
git commit -m "Add feature X"
```

### Quick Commit (Skip Staging)

```bash
# Stage and commit tracked files in one step
git commit -am "Fix bug Y"
```

⚠️ **Warning**: This only works for tracked files (ignores new files)

### Undo Staging

```bash
# Accidentally staged wrong file
git restore --staged wrong-file.txt
```

## Visual Representation

```
Working Directory     Staging Area         Repository
─────────────────    ───────────────     ──────────────
   file.txt          file.txt (v2)       file.txt (v1)
   (modified)        (staged for         (last commit)
                      commit)
                                              ↑
                         git add              git commit
   Change file ────────→ Stage ──────────────→ Commit
```

## Related Commands

- `git status` - Show staging area state  
- `git diff` - Show unstaged changes  
- `git diff --staged` - Show staged changes  
- `git commit` - Commit staged changes  
- `git restore --staged` - Unstage changes
