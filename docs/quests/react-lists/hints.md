# Hints — React Lists: User Directory

## Hint 1 (nudge)
You’ll use `users.map(...)` to create an array of `li` elements.

## Hint 2 (more specific)
Each `li` should be created like:
- `React.createElement("li", { key: user.id }, user.name)`

## Hint 3 (close)
Create the list items, then pass them as children to the `ul`:
- `React.createElement("ul", { "data-testid": "user-list" }, ...items)`
(or pass the array as the children argument if your renderer supports it cleanly).
