---
title: "Reflog"
world_id: world-git
type: codex_entry
level: tier1
---

# Reflog (Recovery Superpower)

Reflog records where HEAD and branch pointers have been.

If you think you “lost” commits, you almost never did — reflog can find them.

## View reflog
```bash
git reflog
```

You’ll see entries like:

* `HEAD@{0}`
* commit hashes from previous states

## Recover by resetting

```bash
git reset --hard <sha-from-reflog>
```

## Tip

Reflog is local. If you rewrote history and pushed, you may also need remote recovery, but reflog is still the first step.


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]