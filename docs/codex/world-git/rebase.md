---
title: "Rebase"
world_id: world-git
type: codex_entry
level: tier1
---

# Rebase

Rebase replays commits on a new base.

## Why use it?
To keep history linear and update your feature branch on top of main.

## Typical flow (feature branch)
```bash
git switch feat/my-work
git fetch origin
git rebase origin/main
```

## Continue / abort

```bash
git rebase --continue
git rebase --abort
```

## Important safety rule

Don’t rebase commits that are already shared with others (unless your team agrees).


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]