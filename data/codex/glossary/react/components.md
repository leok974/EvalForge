# Components

**Components** are reusable, self-contained pieces of UI in React.

## Function Components

The modern standard:

```jsx
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

// Arrow function syntax
const Welcome = (props) => {
  return <h1>Hello, {props.name}</h1>;
};
```

## Using Components

```jsx
function App() {
  return (
    <div>
      <Welcome name="Alice" />
      <Welcome name="Bob" />
    </div>
  );
}
```

## Component Rules

### 1. Names Must Start With Capital Letter

```jsx
// ✅ Correct
function UserProfile() { /* ... */ }

// ❌ Wrong (treated as HTML tag)
function userProfile() { /* ... */ }
```

### 2. Must Return JSX (or null)

```jsx
function EmptyComponent() {
  return null;  // Valid: renders nothing
}
```

### 3. Can Only Return One Root Element

Use fragments if needed:

```jsx
function List() {
  return (
    <>
      <li>Item 1</li>
      <li>Item 2</li>
    </>
  );
}
```

## Composition

Build complex UIs from simple components:

```jsx
function Avatar({ src, name }) {
  return <img src={src} alt={name} />;
}

function UserCard({ user }) {
  return (
    <div className="card">
      <Avatar src={user.avatar} name={user.name} />
      <h2>{user.name}</h2>
      <p>{user.bio}</p>
    </div>
  );
}
```

## Best Practices

- One component per file (usually)
- Keep components focused (single responsibility)
- Extract reusable UI patterns
- Name components clearly (describe what they render)

## Related Concepts

- [JSX](codex:glossary/react/jsx)
- [Props](codex:glossary/react/props)
