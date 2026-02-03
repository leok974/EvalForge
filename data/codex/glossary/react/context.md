# Context

**Context** provides a way to pass data through the component tree without manually passing props at every level.

## When to Use Context

✅ **Good use cases:**
- Theme (light/dark mode)
- Current user
- Language/locale
- UI preferences

❌ **Not for:**
- Frequent updates (can cause performance issues)
- Most state (prefer props or state managers)

## Basic Setup

### 1. Create Context

```jsx
import { createContext } from 'react';

const ThemeContext = createContext('light');  // default value
```

### 2. Provide Context

```jsx
function App() {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={theme}>
      <Toolbar />
      <Content />
    </ThemeContext.Provider>
  );
}
```

### 3. Consume Context

```jsx
import { useContext } from 'react';

function Button() {
  const theme = useContext(ThemeContext);
  
  return (
    <button className={theme === 'dark' ? 'btn-dark' : 'btn-light'}>
      Click me
    </button>
  );
}
```

## Complete Example

```jsx
import { createContext, useContext, useState } from 'react';

// 1. Create context
const UserContext = createContext(null);

// 2. Provider component
function UserProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = (userData) => setUser(userData);
  const logout = () => setUser(null);

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}

// 3. Custom hook for convenience
function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within UserProvider');
  }
  return context;
}

// 4. Usage
function App() {
  return (
    <UserProvider>
      <Header />
      <Dashboard />
    </UserProvider>
  );
}

function Header() {
  const { user, logout } = useUser();
  
  return (
    <header>
      {user ? (
        <>
          <span>Welcome, {user.name}</span>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <span>Not logged in</span>
      )}
    </header>
  );
}
```

## Multiple Contexts

```jsx
function App() {
  return (
    <ThemeProvider>
      <UserProvider>
        <LanguageProvider>
          <Content />
        </LanguageProvider>
      </UserProvider>
    </ThemeProvider>
  );
}
```

## Updating Context

```jsx
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

## Performance Considerations

Context triggers re-render of **all consumers** when value changes.

### Optimization: Split Contexts

```jsx
// ❌ Everything re-renders on any change
<StateContext.Provider value={{ user, theme, settings }}>

// ✅ Only relevant components re-render
<UserContext.Provider value={user}>
  <ThemeContext.Provider value={theme}>
    <SettingsContext.Provider value={settings}>
```

### Optimization: Memoize Value

```jsx
function Provider({ children }) {
  const [user, setUser] = useState(null);

  const value = useMemo(() => ({
    user,
    setUser
  }), [user]);

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}
```

## Best Practices

- Create custom hooks for each context (`useUser`, `useTheme`, etc.)
- Throw error in hook if used outside provider
- Don't overuse—props are often simpler
- Split contexts by update frequency

## Related Concepts

- [Custom Hooks](codex:glossary/react/custom-hooks)
- [Performance Basics](codex:glossary/react/performance-basics)
