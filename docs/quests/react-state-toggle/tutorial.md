# Tutorial — React State: Toggle

## What You’ll Learn
- Using boolean state to drive UI text
- Wiring a click handler to flip state
- Keeping render output deterministic

## Approach
Use a boolean like `isOn`.
Render text based on it:
- `isOn ? "ON" : "OFF"`
Flip it on click:
- `setIsOn(v => !v)`

## Implementation Plan
1. Add state:
   - `const [isOn, setIsOn] = useState(false)`
2. Render button with handler:
   - `onClick: () => setIsOn(v => !v)`
3. Render the label:
   - `isOn ? "ON" : "OFF"`

## Testing
```bash
node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution
```

## Pitfalls

* Forgetting the click handler
* Returning `"On"`/`"Off"` with wrong casing (must be `"ON"`/`"OFF"`)
* Adding extra whitespace around text

## Self-Check

* Start: OFF
* Click: ON
* Click: OFF
