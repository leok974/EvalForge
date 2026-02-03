# State

**State** is data that changes over time and triggers re-renders when updated.

## Using `useState`

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

## How It Works

1. `useState(initialValue)` returns `[currentValue, setterFunction]`
2. Call the setter to update state
3. React re-renders the component with the new value

## Multiple State Variables

```jsx
function Form() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // ...
}
```

## Object State

```jsx
const [user, setUser] = useState({
  name: 'Alice',
  age: 30
});

// ❌ Wrong (mutates state)
user.age = 31;

// ✅ Correct (creates new object)
setUser({ ...user, age: 31 });
```

## Array State

```jsx
const [items, setItems] = useState([1, 2, 3]);

// Add item
setItems([...items, 4]);

// Remove item
setItems(items.filter(item => item !== 2));

// Update item
setItems(items.map(item => 
  item === 2 ? 99 : item
));
```

## Functional Updates

When new state depends on old state:

```jsx
// ❌ Can be buggy in async scenarios
setCount(count + 1);

// ✅ Always safe
setCount(prev => prev + 1);
```

## State vs Props

| State | Props |
|-------|-------|
| Owned by component | Passed from parent |
| Can be changed | Read-only |
| Triggers re-render when updated | Component re-renders when they change |

## Best Practices

- Keep state minimal (derive values when possible)
- Don't duplicate props in state
- Use functional updates for dependent changes
- Prefer multiple `useState` over complex objects (easier to update)

## Related Concepts

- [Props](codex:glossary/react/props)
- [Events](codex:glossary/react/events)
