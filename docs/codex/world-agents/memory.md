# Memory

Memory makes agents better over time—but also makes them brittle if misused.

---

## Types of memory

### Short-term (working memory)
- current plan
- recent tool outputs
- active constraints

### Long-term (preferences / facts)
- user preferences
- project conventions
- known invariants

### Artifact memory
- saved diffs
- reports
- run logs

---

## What to store

Store stable, reusable signals:
- “We require starter fails / solution passes”
- “Disk is source of truth in CI”
- “Unsafe actions require approval”

Avoid storing:
- temporary tokens/secrets
- large raw logs (store references)
- anything that goes stale quickly

---

## Memory hygiene

- version memory entries
- include last-updated timestamp
- prefer “rules” over “opinions”


## Pitfalls

- Premature optimization can lead to complex, unmaintainable code.
- Ignoring error handling can lead to silent failures.

## Related

- [[general/clean-code]]
- [[general/debugging]]

## Example

``` typescript
const example = () => {
  console.log('Hello');
};
```