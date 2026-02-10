# React Reducer: Shopping Cart

Edit `task.mjs` to export `ShoppingCart`.

Requirements:
1. Use `useReducer` to manage state. Initial state: `{ total: 0 }`.
2. Render a `div` with `data-testid="total"` showing the current total.
3. Render a button with `data-testid="add-10` that adds 10 to the total.
4. Render a button with `data-testid="reset"` that resets total to 0.

Actions should roughly be `{ type: 'ADD', amount: 10 }` and `{ type: 'RESET' }`.
