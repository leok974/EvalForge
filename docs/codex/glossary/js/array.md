---
title: Array
id: glossary/js/array
world: js
level: beginner
tags: [data-structures, built-ins, iteration]
related:
  - codex:glossary/js/map
  - codex:glossary/js/filter
  - codex:glossary/js/reduce
---

# Array

## Definition
An **array** is an ordered list of values in JavaScript. Arrays are zero-indexed and can hold mixed types, though most code uses a consistent type. Arrays are commonly used to collect items, iterate, transform data, and produce new arrays.

## Usage
- Store a list of items in order.
- Add/remove items (`push`, `pop`, `shift`, `unshift`, `splice`).
- Transform data (`map`, `filter`, `reduce`).

## Example
```js
const nums = [1, 2, 3];
nums.push(4);              // [1,2,3,4]
const doubled = nums.map(n => n * 2); // [2,4,6,8]
```

## Pitfalls

* `push/pop` **mutate** the array; `map/filter` return new arrays.
* `for...in` is not ideal for arrays (it iterates keys); prefer `for...of` or array methods.

## Related

* Map: transform arrays with `map()`.
* Filter: remove items with `filter()`.
* Reduce: combine array elements with `reduce()`.
