---
title: Callback
id: glossary/js/callback
world: js
level: beginner
tags: [functions, async, patterns]
related:
  - codex:glossary/js/function
  - codex:glossary/js/map
  - codex:glossary/world-js/term-2
  - codex:glossary/world-js/term-3
---

# Callback

## Definition
A **callback** is a function passed into another function to be called later. Callbacks are used for iteration (`map`), events (click handlers), and async operations (timers, network).

## Usage
- Handle events.
- Transform arrays (`map/filter/reduce`).
- Run code after async work completes.

## Example
```js
setTimeout(() => {
  console.log("Done!");
}, 500);

const nums = [1, 2, 3];
const squared = nums.map(n => n * n);

// Event handler callback
button.addEventListener("click", () => {
  console.log("Clicked!");
});
```

## Pitfalls

* Callback-heavy async code can become hard to read ("callback hell").
* Be careful with shared mutable state inside callbacks.

## Related

* Function: callbacks are functions passed as arguments.
* Map: map takes a callback to transform elements.
* Promise: modern alternative to nested callbacks (Term 2).
* Async/Await: cleaner async syntax built on Promises (Term 3).
