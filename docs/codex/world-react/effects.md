# Effects (`useEffect`)

The Effect Hook lets you perform side effects in function components. Data fetching, setting up a subscription, and manually changing the DOM are all examples of side effects.

## Syntax

```jsx
useEffect(() => {
  // side effect code
  return () => {
    // cleanup code
  };
}, [/* dependency array */]);
```

## Dependencies

Crucial for performance and avoiding infinite loops. Only re-run the effect if one of the dependencies has changed.
