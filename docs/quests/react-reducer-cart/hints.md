# Hints — React Reducer: Shopping Cart

## Hint 1 (nudge)
Focus on the reducer first: given an action, return the next `{ total: ... }`.

## Hint 2 (more specific)
Handle two action types:
- `"ADD"` uses `action.amount`
- `"RESET"` returns `{ total: 0 }`

## Hint 3 (close)
Reducer shape:
```js
switch (action.type) {
  case "ADD": return { total: state.total + action.amount };
  case "RESET": return { total: 0 };
  default: return state;
}
```

Buttons:

* add-10 dispatches `{ type: "ADD", amount: 10 }`
* reset dispatches `{ type: "RESET" }`
