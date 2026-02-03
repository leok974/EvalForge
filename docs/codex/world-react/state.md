# State (`useState`)

State allows React components to remember information.

## Hook

```jsx
const [count, setCount] = useState(0);
```

## Updates

State updates trigger re-renders. Updates may be asynchronous.

## Functional Updates

If the new state is computed using the previous state, you can pass a function to `setState`.

```jsx
setCount(prevCount => prevCount + 1);
```
