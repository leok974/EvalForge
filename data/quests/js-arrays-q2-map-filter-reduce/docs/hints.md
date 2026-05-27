## Hint 1
The grader checks your source for `.map(`, `.filter(`, and `.reduce(`. All three must
appear somewhere in your solution — each call can be on separate arrays if you like.

## Hint 2
Quick reference:
```js
const doubled = [1,2,3].map(x => x * 2);          // [2,4,6]
const evens   = [1,2,3,4].filter(x => x % 2 === 0); // [2,4]
const sum     = [1,2,3].reduce((acc, x) => acc + x, 0); // 6
```
`.reduce()` takes a callback and an initial accumulator value as its second argument.
