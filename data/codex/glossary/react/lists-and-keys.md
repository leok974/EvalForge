# Lists and Keys

Rendering lists in React requires **keys** to help React identify which items have changed, been added, or removed.

## Basic List Rendering

```jsx
const items = ['Apple', 'Banana', 'Cherry'];

function FruitList() {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{item}</li>
      ))}
    </ul>
  );
}
```

## Why Keys Matter

Keys give React a stable identity for each element:

```jsx
// Without keys, React might reuse the wrong DOM nodes
<li>Apple</li>
<li>Banana</li>

// If you delete "Apple", React might think you deleted "Banana"
// and update the text instead of removing the first node
```

## Good vs Bad Keys

### ❌ Bad: Array Index

```jsx
{items.map((item, index) => (
  <li key={index}>{item}</li>
))}
```

**Problem:** If you reorder or delete items, indices change, causing bugs.

### ✅ Good: Stable Unique ID

```jsx
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' }
];

{users.map(user => (
  <li key={user.id}>{user.name}</li>
))}
```

## When Index Is Acceptable

Only use index if:
1. List is static (never reordered/filtered)
2. Items have no IDs
3. List is purely for display

```jsx
const staticColors = ['red', 'green', 'blue'];

{staticColors.map((color, i) => (
  <span key={i} style={{ color }}>{color}</span>
))}
```

## Keys in Components

```jsx
function UserCard({ user }) {
  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}

function UserList({ users }) {
  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

## Keys Must Be Unique Among Siblings

```jsx
// ✅ OK: Different lists can have same keys
<div>
  {fruits.map(f => <li key={f.id}>{f.name}</li>)}
</div>
<div>
  {vegetables.map(v => <li key={v.id}>{v.name}</li>)}
</div>
```

## Common Mistakes

### 1. Using Random IDs

```jsx
// ❌ New key every render = remounts component
<li key={Math.random()}>{item}</li>
```

### 2. Not Using Keys

```jsx
// ❌ React will warn you
{items.map(item => <li>{item}</li>)}
```

## Best Practices

- Use stable, unique IDs from your data
- Don't generate keys during render
- Keys only need to be unique among siblings
- Don't use keys for anything other than reconciliation (not props)

## Related Concepts

- [State](codex:glossary/react/state)
