---
title: "Async/Await & Promises"
world_id: world-node
type: codex_entry
level: tier1
---

# Async/Await & Promises

Async code is the #1 source of subtle bugs in Node quests and tests.

A promise represents a value **available later**.  
`await` pauses inside an `async` function until that promise settles.

---

## Basics

```js
async function run() {
  const res = await fetch("https://example.com");
  return res.status;
}
```

If you forget `await`, you return a promise instead of a value.

---

## Parallel vs sequential

Sequential:

```js
const a = await f();
const b = await g();
```

Parallel:

```js
const [a, b] = await Promise.all([f(), g()]);
```

---

## Error handling

Use try/catch around awaited code:

```js
try {
  const x = await doThing();
} catch (err) {
  // handle
}
```

If you don’t catch, tests may fail with unhandled rejections.

---

## Common pitfalls

### “Fire and forget”

You started async work but didn’t await it — tests read output too early.

### “Promise.all with one failure”

If any promise rejects, the whole `Promise.all` rejects.

### “Async function returns undefined”

You forgot a `return` inside the async function.

---

## Tiny patterns

### Convert callback API to a promise

```js
import { promisify } from "node:util";
```

### Sleep (for testing timing)

```js
await new Promise((r) => setTimeout(r, 0));
```
