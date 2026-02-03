# Props

**Props** (properties) are how you pass data from parent components to child components.

## Basic Usage

```jsx
function Greeting(props) {
  return <h1>Hello, {props.name}!</h1>;
}

// Usage
<Greeting name="Alice" />
```

## Destructuring Props

Cleaner syntax:

```jsx
function Greeting({ name, age }) {
  return (
    <div>
      <h1>Hello, {name}!</h1>
      <p>Age: {age}</p>
    </div>
  );
}

<Greeting name="Alice" age={30} />
```

## Props Are Read-Only

Never modify props:

```jsx
// ❌ NEVER do this
function Component(props) {
  props.value = 10;  // ERROR!
}

// ✅ Use state instead
function Component({ initialValue }) {
  const [value, setValue] = useState(initialValue);
  // ...
}
```

## Passing Different Types

```jsx
<Component
  text="hello"           // string
  count={42}             // number
  isActive={true}        // boolean
  items={[1, 2, 3]}      // array
  user={{ name: "Alice" }}  // object
  onClick={handleClick}  // function
/>
```

## Default Props

```jsx
function Greeting({ name = "Guest" }) {
  return <h1>Hello, {name}!</h1>;
}

<Greeting />          // Hello, Guest!
<Greeting name="Alice" />  // Hello, Alice!
```

## Children Prop

Special prop for content between tags:

```jsx
function Card({ children }) {
  return (
    <div className="card">
      {children}
    </div>
  );
}

<Card>
  <h1>Title</h1>
  <p>Content</p>
</Card>
```

## Spreading Props

```jsx
const userProps = { name: "Alice", age: 30 };
<UserProfile {...userProps} />
```

## Best Practices

- Use descriptive prop names
- Destructure for readability
- Provide defaults for optional props
- Document complex prop shapes with TypeScript or PropTypes

## Related Concepts

- [Components](codex:glossary/react/components)
- [State](codex:glossary/react/state)
