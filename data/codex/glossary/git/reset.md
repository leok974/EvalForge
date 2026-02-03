---
title: git reset
id: git/reset
---
# git reset

Undoes commits or unstages files.

## Modes
```bash
git reset --soft HEAD~1   # Keep changes staged
git reset --mixed HEAD~1  # Unstage (default)
git reset --hard HEAD~1   # Discard changes (dangerous!)
```

## See Also
- [git revert](codex:git/revert)
