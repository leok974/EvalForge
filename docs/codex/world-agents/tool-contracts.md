# Tool Contracts

Tools are how agents touch reality. Tool contracts prevent chaos.

A tool contract defines:
- name
- input schema
- output schema
- failure modes
- idempotency and side effects
- timeouts and budgets

---

## Why it matters

Without contracts:
- tools return unstructured text
- the agent guesses what happened
- verification becomes impossible

With contracts:
- tools return structured signals
- retry logic is safe
- logs can be reasoned about

---

## Example tool contract

Tool: run_tests  
Input:
- command (string)
- timeout_ms (int)

Output:
- ok (bool)
- exit_code (int)
- stdout (string)
- stderr (string)
- duration_ms (int)

Failure modes:
- timeout
- non-zero exit
- missing binary

---

## Side effect rules

Prefer tools that are:
- read-only by default
- diff/proposal based for edits
- commit/apply only with approval


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