# JSX

**JSX** is a syntax extension for JavaScript that lets you write HTML-like markup inside JavaScript code.

## What It Looks Like

```jsx
const element = <h1>Hello, world!</h1>;

const greeting = (
  <div className="container">
    <h1>Welcome, {name}!</h1>
    <p>Current time: {new Date().toLocaleTimeString()}</p>
  </div>
);
```

## Key Rules

### 1. Must Return Single Parent Element

```jsx
// ❌ Wrong
return (
  <h1>Title</h1>
  <p>Text</p>
);

// ✅ Correct
return (
  <div>
    <h1>Title</h1>
    <p>Text</p>
  </div>
);

// ✅ Also correct (Fragment)
return (
  <>
    <h1>Title</h1>
    <p>Text</p>
  </>
);
```

### 2. Use `className` Instead of `class`

```jsx
<div className="card">Content</div>
```

### 3. Close All Tags

```jsx
<img src="photo.jpg" />
<input type="text" />
```

### 4. JavaScript in Curly Braces

```jsx
const user = { name: "Alice", age: 30 };

<div>
  <h1>{user.name}</h1>
  <p>Age: {user.age}</p>
  <p>Next year: {user.age + 1}</p>
</div>
```

## Under the Hood

JSX compiles to `React.createElement()` calls:

```jsx
// JSX
<button onClick={handleClick}>Click me</button>

// Compiles to:
React.createElement('button', { onClick: handleClick }, 'Click me')
```

## Best Practices

- Use fragments (`<>...</>`) to avoid extra `<div>` wrappers
- Keep expressions in `{}` simple (extract complex logic to variables)
- Use proper indentation for readability

## Related Concepts

- [Components](codex:glossary/react/components)
