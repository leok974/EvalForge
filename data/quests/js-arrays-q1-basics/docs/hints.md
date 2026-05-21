## Hint 1
The grader checks that you call at least one array method. Common ones that pass:
`push`, `pop`, `shift`, `unshift`, `splice`, `slice`, `includes`, `indexOf`, `find`.

## Hint 2
To create an array and use a method:
```js
const items = [1, 2, 3];
items.push(4);           // mutates the array
const found = items.find(x => x > 2);  // returns 3
```
