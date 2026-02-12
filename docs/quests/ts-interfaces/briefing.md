# Briefing — TS Interfaces

## Objective
Define event interfaces and format events deterministically.

## Contract
- BaseEvent: readonly id, readonly ts, type
- UserEvent extends BaseEvent:
  - type is user.login or user.logout
  - has userId, optional ip
- formatEvent:
  - always prints: `<type> id=<id> ts=<ts>`
  - adds `user=<userId>` for user events
  - adds `ip=<ip>` when present

## Success Criteria
Public tests pass with no extra output.
