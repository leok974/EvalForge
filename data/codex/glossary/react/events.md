# Events

**Events** in React handle user interactions like clicks, typing, form submissions, etc.

## Basic Event Handling

```jsx
function Button() {
  const handleClick = () => {
    console.log('Clicked!');
  };

  return <button onClick={handleClick}>Click me</button>;
}

// Inline (for simple cases)
<button onClick={() => console.log('Clicked!')}>
  Click me
</button>
```

## Common Events

```jsx
function Example() {
  return (
    <div>
      <button onClick={handleClick}>Click</button>
      <input onChange={handleChange} />
      <form onSubmit={handleSubmit}>
        <input type="text" />
        <button type="submit">Submit</button>
      </form>
      <div onMouseEnter={handleHover}>Hover me</div>
      <input onFocus={handleFocus} onBlur={handleBlur} />
    </div>
  );
}
```

## Event Object

```jsx
const handleClick = (event) => {
  event.preventDefault();  // Stop default behavior
  event.stopPropagation(); // Stop event bubbling
  console.log(event.target.value);
};
```

## Passing Arguments

```jsx
// ❌ Wrong (calls immediately)
<button onClick={handleClick(id)}>Delete</button>

// ✅ Correct (arrow function)
<button onClick={() => handleClick(id)}>Delete</button>

// ✅ Also correct (bind)
<button onClick={handleClick.bind(null, id)}>Delete</button>
```

## Form Events

### Controlled Inputs

```jsx
function Form() {
  const [text, setText] = useState('');

  const handleChange = (e) => {
    setText(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted:', text);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={text} 
        onChange={handleChange} 
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Event Naming

React uses camelCase:

| HTML | React |
|------|-------|
| `onclick` | `onClick` |
| `onchange` | `onChange` |
| `onsubmit` | `onSubmit` |

## Best Practices

- Use descriptive handler names (`handleSubmit`, not `submit`)
- Prevent default for form submissions
- Use controlled inputs for forms
- Extract complex handlers to separate functions

## Related Concepts

- [State](codex:glossary/react/state)
- [Controlled Inputs](codex:glossary/react/controlled-inputs)
