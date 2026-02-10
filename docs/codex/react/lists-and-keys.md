# Lists and Keys

Rendering lists of data is a common pattern in React.

## Rendering Multiple Components

You can build collections of elements and include them in JSX using curly braces `{}`.

```javascript
const numbers = [1, 2, 3, 4, 5];
const listItems = numbers.map((number) =>
  <li>{number}</li>
);
```

## Keys

Keys help React identify which items have changed, are added, or are removed. Keys should be given to the elements inside the array to give the elements a stable identity.

```javascript
const listItems = numbers.map((number) =>
  <li key={number.toString()}>
    {number}
  </li>
);
```
