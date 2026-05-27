---
title: Promise
id: glossary/world-js/term-2
world: world-js
level: intermediate
tags: [async, promises, control-flow]
related:
  - codex:glossary/js/callback
  - codex:glossary/world-js/term-3
  - codex:glossary/js/function
---

# Promise

## Definition
A **Promise** represents a value that may be available now, later, or never. Promises are the foundation of modern async JavaScript and can be chained with `.then()` / `.catch()` or awaited with `async/await`.

## Usage
- Handle async operations (fetch, timers, I/O).
- Chain async workflows without nested callbacks.
- Handle errors with `.catch()` or `try/catch` in async functions.

## Example
```js
function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

wait(200).then(() => console.log("done"));

// Error handling
fetch("/api/data")
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error("Failed:", err));
```

## Pitfalls

* Forgetting to handle errors leads to unhandled rejections.
* Mixing callbacks and promises can make control flow confusing.

## Related

* Callback: Promises are an alternative to callback-based async.
* Async/Await: modern syntax for working with Promises.
* Function: Promises are created by functions and consumed via chaining.
