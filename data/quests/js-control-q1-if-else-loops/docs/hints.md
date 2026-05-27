## Hint 1
The grader checks your source for an `if` statement. Make sure your solution contains
an explicit `if (...) { ... } else { ... }` block, not just a ternary operator.

## Hint 2
Common loop patterns:
```js
for (let i = 0; i < arr.length; i++) { ... }  // classic
for (const item of arr) { ... }               // modern, preferred
arr.forEach(item => { ... });                  // functional
```
All three satisfy the "loops" requirement.
