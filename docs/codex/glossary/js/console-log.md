---
title: Console Log
id: glossary/js/console-log
world: js
level: beginner
tags: [debugging, tooling, built-ins]
related:
  - codex:glossary/js/function
  - codex:glossary/js/string
---

# Console Log

## Definition
`console.log()` prints values to the browser devtools console or Node terminal. It's used to inspect values during development and debugging.

## Usage
- Print variables and intermediate values.
- Log structured objects for inspection.
- Debug control flow and state changes.

## Example
```js
const user = { id: 7, name: "Leo" };
console.log("user", user);

const result = doCalculation();
console.log("Result:", result);
```

## Pitfalls

* Leaving logs in production can leak data or clutter output.
* Logging huge objects repeatedly can slow things down.

## Related

* Function: `console.log` is a built-in function.
* String: log output is often formatted as strings.
