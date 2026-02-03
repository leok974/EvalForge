---
title: "Error Handling"
world_id: world-node
type: codex_entry
level: tier1
---

# Error Handling

Node errors come from:
- sync exceptions (throw)
- async rejections (promise rejects)
- callback errors (err-first callbacks)

Good apps and good quests handle errors **intentionally**.

---

## Sync errors
```js
try {
  risky();
} catch (err) {
  // recover or rethrow
}
```

---

## Async errors

```js
try {
  await riskyAsync();
} catch (err) {
  // handle
}
```

If you don’t catch async errors, you often get:

* unhandled rejection
* flaky tests
* server crash

---

## Error mapping (server mindset)

You typically map errors to:

* client errors (400/401/403/404)
* server errors (500)

Even if the quest is small, it’s good practice to be explicit.

---

## EvalForge guidance

If the quest specifies:

* exact stderr message
* exact exit code
  follow the contract exactly.

Otherwise:

* keep stderr for real failures
* keep stdout clean for “happy path”
