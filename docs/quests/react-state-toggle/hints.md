# Hints — React State: Toggle

## Hint 1 (nudge)
Store ON/OFF as a boolean, and derive text from it.

## Hint 2 (more specific)
Use `useState(false)` and flip with `setState(v => !v)`.

## Hint 3 (close)
Return:
- `React.createElement("button", { "data-testid": "toggle", onClick: () => setIsOn(v => !v) }, isOn ? "ON" : "OFF")`
