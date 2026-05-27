## Hint 1
Create an object literal with at least one property and one method:
```js
const user = {
  name: "Alice",
  greet() {
    return `Hello, I'm ${this.name}`;
  }
};
```
The grader checks that your code defines an object (using `{}`).

## Hint 2
`this` inside an object method refers to the object itself. Arrow functions do NOT
have their own `this` — use regular function syntax for methods that need `this`.
