---
title: Object
id: glossary/world-js/term-1
world: world-js
level: beginner
tags: [data-structures, objects, basics]
related:
  - codex:glossary/js/array
  - codex:glossary/js/function
  - codex:glossary/world-js/term-2
---

# Object

## Definition
An **object** is a key/value data structure used to represent structured data. Keys are usually strings (or symbols), and values can be any type. Objects are the backbone of most JavaScript data modeling.

## Usage
- Store structured records (user, config).
- Create dictionaries/lookup tables.
- Group related data and methods together.

## Example
```js
const user = { id: 1, name: "Leo", active: true };
console.log(user.name); // "Leo"

// Add/modify properties
user.email = "leo@example.com";

// Method shorthand
const calculator = {
  add(a, b) { return a + b; },
  sub(a, b) { return a - b; }
};
```

## Pitfalls

* Accessing missing keys returns `undefined` (watch for typos).
* Mutating shared objects can cause unexpected side effects.

## Related

* Array: arrays are ordered lists; objects are key/value maps.
* Function: objects can contain methods (functions as properties).
* Promise: Promises are objects representing async operations.
