# Hints — React Conditional Render

## Hint 1 (nudge)
You can conditionally include an element by returning `null` when it shouldn’t render.

## Hint 2 (more specific)
You’re already returning a wrapper `div` with an `h2`. Add a second child for the `p`.

## Hint 3 (close)
Use a ternary inside the wrapper:
- `isVisible ? React.createElement("p", null, "Now you see me") : null`
