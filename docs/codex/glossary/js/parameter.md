---
title: Parameter
id: glossary/js/parameter
world: js
level: beginner
tags: [functions, arguments, basics]
related:
  - codex:glossary/js/function
  - codex:glossary/js/return-value
  - codex:glossary/js/callback
---

# Parameter

## Definition
A **parameter** is a named variable in a function definition that receives a value when the function is called. Parameters define what inputs a function expects.

## Usage
- Accept required inputs (e.g., `name`).
- Provide defaults (`function f(x = 10) {}`).
- Accept variable numbers of args (`...rest`).

## Example
```js
function clamp(value, min = 0, max = 100) {
  return Math.min(Math.max(value, min), max);
}

console.log(clamp(150));       // 100
console.log(clamp(-5, 0, 50)); // 0
```

## Pitfalls

* Missing args become `undefined`, which can cause subtle bugs.
* Mutating object parameters can cause side effects for the caller.

## Related

* Function: parameters are part of function definitions.
* Return Value: parameters become inputs; return values are outputs.
* Callback: callbacks are functions passed as parameters.
