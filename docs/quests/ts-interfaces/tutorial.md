# Tutorial — TS Interfaces

## What You’re Practicing
- Interfaces for object contracts
- Extending interfaces to add stricter requirements
- Optional properties (`ip?`)
- Narrowing using a discriminant (`type`)

## Implementation Plan
1. Start with the base format string.
2. Detect user events using the `type` field.
3. If user event, append `user=<userId>`.
4. If ip exists, append `ip=<ip>`.

## Pitfalls
- Forgetting that BaseEvent doesn’t guarantee `userId`
- Appending `ip=` when ip is missing
- Formatting order mismatches (tests expect exact order)
