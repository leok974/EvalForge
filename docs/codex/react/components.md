# Components

Components are the building blocks of any React application.
Conceptually, a component is a JavaScript function that accepts arbitrary inputs (called "props") and returns a React element describing what should appear on the screen.

## Functional Components

The simplest way to define a component is to write a JavaScript function:

```javascript
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
```

## React.createElement

Before JSX is compiled, it becomes a call to `React.createElement`.

```javascript
const element = React.createElement(
  'h1',
  {className: 'greeting'},
  'Hello, world!'
);
```

This is what you'll use in quests where JSX is restricted.
