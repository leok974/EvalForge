# Controlled Inputs

A **controlled input** is a form element whose value is managed by React state.

## Controlled vs Uncontrolled

### Uncontrolled (DOM manages value)

```jsx
// ❌ React doesn't know the value
<input type="text" />
```

### Controlled (React manages value)

```jsx
// ✅ React controls the value
const [text, setText] = useState('');

<input 
  value={text} 
  onChange={(e) => setText(e.target.value)} 
/>
```

## Why Use Controlled Inputs?

1. **Validation** — validate as user types
2. **Formatting** — enforce formats (phone numbers, etc.)
3. **Conditional Rendering** — show/hide based on input
4. **Instant Feedback** — real-time character count, etc.

## Full Example

```jsx
function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ email, password });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

## Multiple Inputs

Use a single state object:

```jsx
const [form, setForm] = useState({
  name: '',
  email: '',
  age: ''
});

const handleChange = (e) => {
  const { name, value } = e.target;
  setForm({ ...form, [name]: value });
};

<input name="name" value={form.name} onChange={handleChange} />
<input name="email" value={form.email} onChange={handleChange} />
<input name="age" value={form.age} onChange={handleChange} />
```

## Other Input Types

### Checkbox

```jsx
const [isChecked, setIsChecked] = useState(false);

<input
  type="checkbox"
  checked={isChecked}
  onChange={(e) => setIsChecked(e.target.checked)}
/>
```

### Select

```jsx
const [selected, setSelected] = useState('option1');

<select value={selected} onChange={(e) => setSelected(e.target.value)}>
  <option value="option1">Option 1</option>
  <option value="option2">Option 2</option>
</select>
```

### Textarea

```jsx
const [text, setText] = useState('');

<textarea
  value={text}
  onChange={(e) => setText(e.target.value)}
/>
```

## Best Practices

- Always set `value` + `onChange` together
- Use `name` attribute for multiple inputs
- Initialize state with sensible defaults (empty string, not `null`)

## Related Concepts

- [State](codex:glossary/react/state)
- [Events](codex:glossary/react/events)
