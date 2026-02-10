# Agent Loop

The agent loop is the minimal engine of agentic behavior:

**Plan → Act → Verify → Report → Iterate**

If you remove **Verify**, you don’t have an agent — you have a generator.

---

## Step definitions

### Plan
Output a sequence of steps where each step has:
- **action** (what to do)
- **expected result** (what success looks like)
- **verification method** (how to prove it)

### Act
Use tools to do work: read files, run tests, call APIs, query DB, produce diffs.

### Verify
Verification must be independent of the generator:
- tests
- checksums
- grep/search
- structured queries
- diff inspection
- lint/typecheck

### Report
A report answers:
- what changed
- how we know it works
- how to undo it

### Iterate
Repeat only if:
- verification failed but recovery path exists, and
- budget allows it.

---

## Stop conditions

You must define stop conditions:
- success criteria met
- attempts exceeded
- time/cost exceeded
- unsafe action needs approval and was denied

---

## Mini example

Goal: “Fix failing test”

Plan:
1) Run tests → capture failure
2) Locate failing file → inspect relevant code
3) Propose patch diff
4) Re-run tests → confirm
5) Report + rollback instructions


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