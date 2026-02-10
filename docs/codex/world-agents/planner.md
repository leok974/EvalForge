# Planner

The planner turns a goal into steps.

A good planner:
- decomposes work
- adds verification per step
- anticipates risks
- respects budgets

---

## Planning outputs

Each step should include:
- action
- expected artifact
- verification method
- rollback note (if step is risky)

---

## Bad planning signs

- “do everything” as one step
- no verification
- no stop condition
- no constraints

---

## Common planning pattern

1) Inspect current state (read-only)
2) Decide minimal change set
3) Propose diff
4) Verify
5) Report


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