---
title: String
id: glossary/js/string
world: js
level: beginner
tags: [primitives, data-types, basics]
related:
  - codex:glossary/js/console-log
  - codex:glossary/js/array
---

# String

## Definition
A **string** is text data in JavaScript, written with quotes (`" "`, `' '`, or backticks `` ` ` ``). Strings are immutable, meaning operations create new strings rather than changing the original.

## Usage
- Represent names, messages, IDs.
- Build templates with backticks (template literals).
- Manipulate text with built-in methods.

## Example
```js
const name = "Leo";
const msg = `Hello, ${name}!`; // template literal
console.log(msg.toUpperCase()); // "HELLO, LEO!"

const substring = "JavaScript".slice(0, 4); // "Java"
```

## Pitfalls

* `+` concatenation can be error-prone; prefer template literals for readability.
* Don't confuse string numbers `"42"` with numbers `42` (types differ).

## Related

* Console Log: log strings to debug.
* Array: strings behave like character arrays in some ways.
