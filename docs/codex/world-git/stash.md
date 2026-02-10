---
title: "Stash"
world_id: world-git
type: codex_entry
level: tier1
---

# Stash

Stash lets you temporarily park uncommitted work.

## Save
```bash
git stash push -m "wip"
```

## List

```bash
git stash list
```

## Apply

```bash
git stash apply
```

## Pop (apply + remove)

```bash
git stash pop
```

## When to use

* switching branches quickly
* pulling changes without committing messy work

Prefer committing small WIP commits if stashing becomes frequent.


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]