---
title: Return Value
id: glossary/js/return-value
world: js
level: beginner
tags: [functions, control-flow, basics]
related:
  - codex:glossary/js/function
  - codex:glossary/js/parameter
  - codex:glossary/js/callback
---

# Return Value

## Definition
A **return value** is the value a function sends back to the caller using `return`. If a function doesn't explicitly return, JavaScript returns `undefined`.

## Usage
- Return computed results.
- Exit early from a function.
- Return objects/arrays for structured output.

## Example
```js
function isEven(n) {
  return n % 2 === 0;
}

const ok = isEven(10); // true

function getUserData(id) {
  if (!id) return null; // Early return
  return { id, name: "Leo" };
}
```

## Pitfalls

* `return;` returns `undefined` (not "no return").
* Returning inside a loop only exits the function, not "just the loop."

## Related

* Function: functions produce return values.
* Parameter: parameters are inputs; return values are outputs.
* Callback: callbacks often return values for processing.
