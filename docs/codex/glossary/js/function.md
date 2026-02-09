---
title: Function
id: glossary/js/function
world: js
level: beginner
tags: [functions, basics, first-class]
related:
  - codex:glossary/js/parameter
  - codex:glossary/js/return-value
  - codex:glossary/js/callback
---

# Function

## Definition
A **function** is a reusable block of code you can call with inputs (parameters) to produce an output (return value). In JavaScript, functions are "first-class," meaning you can store them in variables, pass them as arguments, and return them from other functions.

## Usage
- Encapsulate logic.
- Create reusable utilities.
- Pass behavior into other functions (callbacks).

## Example
```js
function add(a, b) {
  return a + b;
}

const greet = (name) => `Hello, ${name}!`;
console.log(greet("Leo")); // "Hello, Leo!"
```

## Pitfalls

* If you forget `return`, the function returns `undefined`.
* Arrow functions handle `this` differently than `function` declarations (lexical `this`).

## Related

* Parameter: functions accept parameters as inputs.
* Return Value: functions produce return values.
* Callback: functions passed as arguments to other functions.
