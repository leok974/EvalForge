---
title: "Conflicts"
world_id: world-git
type: codex_entry
level: tier1
---

# Conflicts

Conflicts happen when Git can’t automatically combine changes.

## Steps to resolve
1) See conflicted files:
```bash
git status
```

2. Open file and resolve markers:

```txt
<<<<<<<
your changes
=======
their changes
>>>>>>>
```

3. Stage resolved files:

```bash
git add <file>
```

4. Continue:

* merge: `git commit`
* rebase: `git rebase --continue`

## Tip

Resolve with intention:

* choose one side
* or combine both
  Then run tests.


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]