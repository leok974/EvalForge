# Handling Events

Handling events with React elements is very similar to handling events on DOM elements. There are some syntax differences:

* React events are named using camelCase, rather than lowercase.
* With JSX you pass a function as the event handler, rather than a string.

## Example

```javascript
<button onClick={activateLasers}>
  Activate Lasers
</button>
```

In `React.createElement`:

```javascript
React.createElement('button', { onClick: activateLasers }, 'Activate Lasers')
```
