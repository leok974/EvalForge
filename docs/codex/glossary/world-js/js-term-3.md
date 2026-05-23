---
title: Async/Await
id: glossary/world-js/term-3
world: world-js
level: intermediate
tags: [async, promises, syntax]
related:
  - codex:glossary/world-js/term-2
  - codex:glossary/js/callback
  - codex:glossary/js/function
---

# Async/Await

## Definition
`async/await` is syntax built on Promises that makes async code read like synchronous code. An `async` function always returns a Promise, and `await` pauses execution until the awaited Promise resolves (or throws if it rejects).

## Usage
- Write cleaner async code than nested `.then()` chains.
- Use `try/catch` for async error handling.
- Combine with `Promise.all` for parallel async operations.

## Example
```js
async function load() {
  try {
    const res = await fetch("/api/data");
    const data = await res.json();
    return data;
  } catch (err) {
    console.error("Load failed:", err);
    return null;
  }
}

// Parallel async with Promise.all
async function loadMultiple() {
  const [users, posts] = await Promise.all([
    fetch("/api/users").then(r => r.json()),
    fetch("/api/posts").then(r => r.json())
  ]);
  return { users, posts };
}
```

## Pitfalls

* `await` only works inside `async` functions (or top-level in some runtimes).
* Awaiting sequentially can be slow; use `Promise.all` when independent.

## Related

* Promise: async/await is syntax sugar over Promises.
* Callback: async/await replaces callback-based async patterns.
* Function: async functions are a special type of function.
