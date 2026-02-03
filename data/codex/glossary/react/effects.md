# Effects

**Effects** let you synchronize components with external systems (APIs, subscriptions, DOM, timers, etc.).

## Using `useEffect`

```jsx
import { useEffect, useState } from 'react';

function Example() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);  // Re-run when count changes

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

## Dependency Array

Controls when the effect runs:

```jsx
// ❌ Runs after EVERY render
useEffect(() => {
  console.log('Runs every render');
});

// ✅ Runs only once (on mount)
useEffect(() => {
  console.log('Runs once');
}, []);

// ✅ Runs when dependencies change
useEffect(() => {
  console.log('Count changed:', count);
}, [count]);
```

## Cleanup

Return a function to clean up subscriptions, timers, etc.:

```jsx
useEffect(() => {
  const timer = setInterval(() => {
    console.log('Tick');
  }, 1000);

  // Cleanup: runs before next effect and on unmount
  return () => {
    clearInterval(timer);
  };
}, []);
```

## Fetching Data

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let ignore = false;

    async function fetchUser() {
      setLoading(true);
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();
      
      if (!ignore) {
        setUser(data);
        setLoading(false);
      }
    }

    fetchUser();

    return () => {
      ignore = true;  // Prevent state update if component unmounts
    };
  }, [userId]);

  if (loading) return <p>Loading...</p>;
  return <div>{user.name}</div>;
}
```

## Common Patterns

### Run Once on Mount

```jsx
useEffect(() => {
  console.log('Component mounted');
}, []);
```

### Subscribe to External Events

```jsx
useEffect(() => {
  function handleResize() {
    console.log('Window resized');
  }

  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

### Sync with Prop Changes

```jsx
useEffect(() => {
  console.log('User ID changed to:', userId);
}, [userId]);
```

## Common Mistakes

### 1. Missing Dependencies

```jsx
// ❌ Wrong (missing 'count' in deps)
useEffect(() => {
  console.log(count);
}, []);

// ✅ Include ALL dependencies
useEffect(() => {
  console.log(count);
}, [count]);
```

### 2. Infinite Loops

```jsx
// ❌ Creates infinite loop
useEffect(() => {
  setCount(count + 1);
}, [count]);  // count changes → effect runs → count changes → ...
```

### 3. No Cleanup

```jsx
// ❌ Memory leak (subscription continues after unmount)
useEffect(() => {
  subscribe();
}, []);

// ✅ Cleanup
useEffect(() => {
  subscribe();
  return () => unsubscribe();
}, []);
```

## Best Practices

- **Always** include dependencies (use ESLint rule)
- Clean up subscriptions and timers
- Use separate effects for unrelated logic
- Avoid setting state from effects when possible (derive from state/props instead)

## Related Concepts

- [State](codex:glossary/react/state)
- [Custom Hooks](codex:glossary/react/custom-hooks)
