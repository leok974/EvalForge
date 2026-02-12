# TS Interfaces

## Objective
Model a small event system using interfaces and implement a formatter function.

This quest trains:
- defining interfaces
- extending interfaces
- readonly fields
- working with optional properties
- returning deterministic strings

## Requirements
Edit `task.ts` to export:

1) `interface BaseEvent`
2) `interface UserEvent extends BaseEvent`
3) `function formatEvent(e: BaseEvent): string`

### Contracts

#### BaseEvent
Must include:
- `readonly id: string`
- `readonly ts: number` (unix epoch ms)
- `type: string`

#### UserEvent
Extends BaseEvent and must include:
- `type: "user.login" | "user.logout"`
- `userId: string`
- optional `ip?: string`

#### formatEvent rules
Return a one-line string:
`<type> id=<id> ts=<ts>`

If the event is a UserEvent (type is user.login or user.logout), append:
` user=<userId>`

If `ip` is present, append:
` ip=<ip>`

Examples:
- `user.login id=evt_1 ts=1700000000000 user=u1 ip=127.0.0.1`
- `system.boot id=evt_9 ts=1700000009999`

## Constraints
- Standard library only.
- No printing.
- Deterministic formatting.

## Success Criteria
Public tests pass.
