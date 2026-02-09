---
title: "Event Loop"
world_id: world-node
type: codex_entry
level: tier1
---

# Event Loop

Node.js runs your JavaScript on a **single thread**, and uses the **event loop** to handle I/O (files, network, timers) without blocking the whole program.

Think: **“Do a little work, schedule the rest, repeat.”**

---

## What you need to know for EvalForge

### Sync code runs first
Anything not async runs immediately, top-to-bottom.

### Async work runs later
Timers, I/O callbacks, and resolved promises run on later turns of the event loop.

This is why you see:
- “my log order is weird”
- “tests pass locally but hang in CI”
- “server keeps running after the test ends”

---

## Microtasks vs tasks (the useful mental model)

- **Microtasks**: promise callbacks (`then`, `await` continuations)
- **Tasks**: timers (`setTimeout`), I/O callbacks, etc.

Practical rule:
> Promises usually run *before* timers scheduled in the same turn.

Example:
```js
console.log("A");

setTimeout(() => console.log("timeout"), 0);

Promise.resolve().then(() => console.log("promise"));

console.log("B");

// A, B, promise, timeout (typical)
```

---

## Common failure mode: hanging tests

Tests hang when Node still has “open handles”:

* a server still listening
* an interval still running
* an open socket/stream

Fix: close what you open.

* `server.close()`
* `clearInterval(id)`
* ensure streams end

---

## Tiny patterns

### Let async complete

```js
await new Promise((r) => setTimeout(r, 0));
```

### “Run after current call stack”

```js
queueMicrotask(() => {
  // runs after current sync code, before timers
});
```

---

## Checklist

If something is “not happening”:

* Did you `await` the promise?
* Did you accidentally exit early?
* Are you expecting a timer to run while you’re blocking the thread?

If something “never ends”:

* Did you start an interval?
* Did you forget to close the server?


## Pitfalls

- Blocking the event loop with heavy synchronous operations.
- Unhandled promise rejections can crash the process.

## Related

- [[node/event-loop]]
- [[node/modules]]