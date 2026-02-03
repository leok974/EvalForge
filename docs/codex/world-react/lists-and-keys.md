# Lists and Keys

## Rendering Multiple Components

You can build collections of elements and include them in JSX using curly braces `{}`.

```jsx
const listItems = numbers.map((number) =>
  <li key={number.toString()}>
    {number}
  </li>
);
```

## Keys

Keys help React identify which items have changed, are added, or are removed. Keys should be given to the elements inside the array to give the elements a stable identity.
