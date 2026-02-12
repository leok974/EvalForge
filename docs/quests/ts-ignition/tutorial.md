# Tutorial — TS Ignition

## What You’ll Learn
- How TypeScript enforces a return-shape contract
- Literal types: values that must be exact (not just “string” or “number”)
- Exporting a function from a module

## Approach
1. Define a type alias `Handshake`
2. Make `handshake()` return that type
3. Return the exact object required by the contract

## Implementation Plan
- In `Handshake`, use literal types:
  - message: "System Online"
  - code: 42
  - ok: true
- Return the matching object in `handshake()`

## Pitfalls
- Using `message: string` instead of the exact literal
- Returning `code: number` instead of `42`
- Misspelling keys or changing casing
