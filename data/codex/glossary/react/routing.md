# Routing

**Routing** enables navigation between different pages/views in a single-page application (SPA).

## React Router Basics

The most popular library is `react-router-dom`.

### Installation

```bash
npm install react-router-dom
```

### Basic Setup

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## URL Parameters

```jsx
import { useParams } from 'react-router-dom';

function App() {
  return (
    <Routes>
      <Route path="/users/:userId" element={<UserProfile />} />
    </Routes>
  );
}

function UserProfile() {
  const { userId } = useParams();
  
  return <div>User ID: {userId}</div>;
}

// Navigate to: /users/123
// userId = "123"
```

## Programmatic Navigation

```jsx
import { useNavigate } from 'react-router-dom';

function LoginForm() {
  const navigate = useNavigate();

  const handleLogin = async (credentials) => {
    await login(credentials);
    navigate('/dashboard');  // Redirect after login
  };

  return <form onSubmit={handleLogin}>...</form>;
}
```

## Nested Routes

```jsx
function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="about" element={<About />} />
        <Route path="users" element={<Users />}>
          <Route path=":userId" element={<UserDetail />} />
        </Route>
      </Route>
    </Routes>
  );
}

function Layout() {
  return (
    <div>
      <nav>...</nav>
      <Outlet />  {/* Child routes render here */}
    </div>
  );
}
```

## Query Parameters

```jsx
import { useSearchParams } from 'react-router-dom';

function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const query = searchParams.get('q');
  const page = searchParams.get('page') || 1;

  return (
    <div>
      <p>Searching for: {query}</p>
      <p>Page: {page}</p>
    </div>
  );
}

// URL: /search?q=react&page=2
// query = "react"
// page = "2"
```

## Protected Routes

```jsx
function ProtectedRoute({ children }) {
  const { user } = useUser();
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
```

## 404 / Not Found

```jsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  <Route path="*" element={<NotFound />} />
</Routes>
```

## Link vs NavLink

```jsx
// Basic link
<Link to="/about">About</Link>

// NavLink (adds 'active' class to current route)
<NavLink
  to="/about"
  className={({ isActive }) => isActive ? 'active' : ''}
>
  About
</NavLink>
```

## Best Practices

- Use `<Link>` instead of `<a>` to avoid full page reloads
- Organize routes in a separate config file for large apps
- Use nested routes to share layouts
- Protect sensitive routes with authentication checks
- Use `replace` prop to avoid adding to history stack (e.g., redirects)

## Related Concepts

- [Components](codex:glossary/react/components)
- [Context](codex:glossary/react/context)
