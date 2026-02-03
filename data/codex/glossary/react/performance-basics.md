# Performance Basics

Understanding and preventing unnecessary re-renders is key to React performance.

## When Components Re-Render

A component re-renders when:
1. Its **state** changes
2. Its **props** change
3. Its **parent** re-renders (even if props haven't changed)
4. **Context** it uses changes

## Identifying Performance Issues

```jsx
// Add to component to see when it renders
useEffect(() => {
  console.log('Component rendered');
});
```

Or use React DevTools Profiler.

## React.memo

Prevents re-renders when props haven't changed:

```jsx
import { memo } from 'react';

const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
  console.log('Rendering expensive component');
  return <div>{/* complex UI */}</div>;
});

// Only re-renders when 'data' prop actually changes
```

### Custom Comparison

```jsx
const Component = memo(
  ({ user }) => <div>{user.name}</div>,
  (prevProps, nextProps) => {
    return prevProps.user.id === nextProps.user.id;
  }
);
```

## useMemo

Memoize expensive calculations:

```jsx
import { useMemo } from 'react';

function DataTable({ items, filters }) {
  const filteredItems = useMemo(() => {
    console.log('Filtering items...');
    return items.filter(item => {
      // expensive filtering logic
      return filters.every(f => f(item));
    });
  }, [items, filters]);  // Only recalculate when these change

  return <table>{/* render filteredItems */}</table>;
}
```

### Don't Overuse

```jsx
// ❌ Useless (simple calculation)
const doubled = useMemo(() => count * 2, [count]);

// ✅ Just do it directly
const doubled = count * 2;
```

## useCallback

Memoize function references:

```jsx
import { useCallback } from 'react';

function Parent() {
  const [count, setCount] = useState(0);

  // ❌ New function every render
  const handleClick = () => {
    console.log('Clicked');
  };

  // ✅ Same function reference unless dependencies change
  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []);

  return <ExpensiveChild onClick={handleClick} />;
}

const ExpensiveChild = memo(({ onClick }) => {
  console.log('Child rendered');
  return <button onClick={onClick}>Click</button>;
});
```

## Key Patterns

### Lift Content Up

```jsx
// ❌ SlowComponent re-renders when count changes
function Parent() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>{count}</button>
      <SlowComponent />
    </div>
  );
}

// ✅ SlowComponent doesn't re-render
function Parent() {
  return (
    <div>
      <Counter />
      <SlowComponent />
    </div>
  );
}

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Children Prop

```jsx
function Wrapper({ children }) {
  const [state, setState] = useState(0);
  
  return (
    <div>
      <button onClick={() => setState(state + 1)}>Update</button>
      {children}  {/* Doesn't re-render when state changes */}
    </div>
  );
}

<Wrapper>
  <SlowComponent />
</Wrapper>
```

## Virtual Lists

For long lists, only render visible items:

```bash
npm install react-window
```

```jsx
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          {items[index].name}
        </div>
      )}
    </FixedSizeList>
  );
}
```

## Best Practices

1. **Measure first** — don't optimize prematurely
2. **Use React DevTools Profiler** to find slow components
3. **memo** — for expensive components with stable props
4. **useMemo** — for expensive calculations
5. **useCallback** — when passing functions to memoized children
6. **Virtual lists** — for rendering 1000+ items
7. **Code splitting** — lazy-load routes and heavy components

```jsx
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

<Suspense fallback={<div>Loading...</div>}>
  <HeavyComponent />
</Suspense>
```

## Related Concepts

- [State](codex:glossary/react/state)
- [Effects](codex:glossary/react/effects)
- [Context](codex:glossary/react/context)
