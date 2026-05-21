## Hint 1
The grader checks your source for an arrow function (`=>`). Make sure at least one
function in your solution uses the arrow syntax:
```js
const add = (a, b) => a + b;
const greet = name => `Hello, ${name}`;
```

## Hint 2
Key difference: Arrow functions inherit `this` from their enclosing scope.
Regular functions have their own `this` bound at call time. Use arrows for
callbacks and short utilities; use regular functions for methods that need `this`.
