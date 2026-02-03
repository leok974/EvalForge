# Components

Components are the building blocks of React applications. They let you split the UI into independent, reusable pieces.

## Function Components

```jsx
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
```

## Props

Components accept arbitrary inputs called "props" and return React elements describing what should appear on the screen.

## Composition

Components can refer to other components in their output. This lets us use the same component abstraction for any level of detail.
