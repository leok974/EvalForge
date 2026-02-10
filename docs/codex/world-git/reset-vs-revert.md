---
title: "Reset vs Revert"
world_id: world-git
type: codex_entry
level: tier1
---

# Reset vs Revert (Undo the right way)

This is the #1 Git confusion.

## Revert (safe on shared branches)
Creates a new commit that undoes another commit.
```bash
git revert <sha>
```

Use when:

* you already pushed
* others may have pulled

## Reset (moves branch pointer)

Changes what HEAD/branch points to.

### Soft reset (keep staged/working)

```bash
git reset --soft <sha>
```

### Mixed reset (default: unstages, keeps working)

```bash
git reset <sha>
```

### Hard reset (danger: discards working changes)

```bash
git reset --hard <sha>
```

## Rule of thumb

* public/shared history → **revert**
* local/private cleanup → **reset**


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]