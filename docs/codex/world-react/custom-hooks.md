# Custom Hooks

Building your own Hooks lets you extract component logic into reusable functions.

## Naming Convention

A custom Hook is a JavaScript function whose name starts with "use" and that may call other Hooks.

## Example

```jsx
function useFriendStatus(friendID) {
  const [isOnline, setIsOnline] = useState(null);
  // ...
  return isOnline;
}
```
