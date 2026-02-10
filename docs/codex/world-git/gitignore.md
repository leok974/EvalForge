---
title: ".gitignore"
world_id: world-git
type: codex_entry
level: tier1
---

# .gitignore

.gitignore tells Git which files to ignore (not track).

Common examples:
- `node_modules/`
- build outputs (`dist/`, `build/`)
- local env files (`.env`)

## Example
```gitignore
node_modules/
dist/
.env
```

## Important gotcha

.gitignore does not remove files already tracked.
To stop tracking a file:

```bash
git rm --cached <file>
```

Then commit.


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]