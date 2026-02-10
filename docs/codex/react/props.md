# Props

Props (short for "properties") are the arguments passed into React components.
They are read-only (immutable) from the perspective of the component.

## Passing Props

In JSX:
```jsx
<Welcome name="Sara" />
```

In `React.createElement`:
```javascript
React.createElement(Welcome, { name: "Sara" }, null)
```

## Accessing Props

Functional components receive `props` as the first argument:

```javascript
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
```
