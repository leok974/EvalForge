# Tutorial — React Lists: User Directory

## What You’ll Learn
- Mapping arrays to element lists
- Why keys matter (reconciliation)
- How to build nested elements with `React.createElement`

## Approach
Your component should return:
- a `ul` with a test id
- a list of `li` children produced by mapping over `users`

Each `li` should be created with:
- type: `"li"`
- props: `{ key: user.id }`
- child text: `user.name`

## Implementation Plan
1. Keep the `ul` root:
   - `React.createElement("ul", { "data-testid": "user-list" }, ...)`
2. Build `li` children:
   - `const items = users.map(u => React.createElement("li", { key: u.id }, u.name))`
3. Pass items as children:
   - Spread or pass the array correctly so React sees multiple children.

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Pitfalls

* Forgetting keys (React warns; hidden tests may enforce)
* Passing the array incorrectly (you want `ul` to have multiple `li` children)
* Not handling `users` being missing/empty (safe default is `[]`)

## Self-Check

* With 3 users, you get 3 `li`s.
* First `li` child is `"Alice"` (matches fixture).
