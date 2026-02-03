---
title: "node:test"
world_id: world-node
type: codex_entry
level: tier1
---

# node:test

`node:test` is Node’s built-in test runner. EvalForge uses it because it’s:
- fast
- dependency-free
- predictable in CI

Run tests:
```bash
node --test
```

Run a file:

```bash
node --test path/to/test.mjs
```

---

## Basic test

```js
import test from "node:test";
import assert from "node:assert/strict";

test("adds", () => {
  assert.equal(1 + 1, 2);
});
```

---

## Async test

```js
test("async works", async () => {
  const v = await Promise.resolve(42);
  assert.equal(v, 42);
});
```

---

## The #1 issue: hanging tests

Tests hang when there are open handles:

* servers still listening
* intervals still running
* streams not closed

Fix by:

* closing servers
* clearing timers
* awaiting async work

---

## Useful debugging

* Add logs inside the test temporarily
* Print values before assertions
* Confirm the working directory / paths
