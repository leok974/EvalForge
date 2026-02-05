---
id: jsx
title: JSX
tags: [react, syntax]
---

# JSX (JavaScript XML)

**JSX** is a syntax extension for JavaScript that looks similar to XML or HTML. It is commonly used with [React] to describe what the UI should look like.

## Does React require JSX?
No. JSX is syntactic sugar for `React.createElement`.

**JSX**:
```jsx
const element = <h1 className="greeting">Hello, world!</h1>;
```

**Compiled JS**:
```javascript
const element = React.createElement(
  'h1',
  { className: 'greeting' },
  'Hello, world!'
);
```

In the **React Foundations** world, we intentionally use `React.createElement` to verify understanding of structure without relying on build tools.
