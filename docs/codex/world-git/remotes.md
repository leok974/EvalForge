---
title: "Remotes (origin)"
world_id: world-git
type: codex_entry
level: tier1
---

# Remotes (origin, fetch, pull, push)

A remote is a named reference to another repo (usually GitHub).

## See remotes
```bash
git remote -v
```

## Fetch (download remote refs)

```bash
git fetch origin
```

## Pull (fetch + integrate)

Prefer fast-forward only:

```bash
git pull --ff-only
```

## Push

```bash
git push
git push -u origin feat/my-work
```

## Tip

If your local main is behind:

```bash
git switch main
git fetch origin
git pull --ff-only
```


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]