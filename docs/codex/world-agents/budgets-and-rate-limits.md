# Budgets & Rate Limits

Budgets keep agents from spiraling.

---

## What to budget

- max steps per run
- max retries per step
- max tool calls
- max token/cost
- max wall clock time

---

## Budget failure behavior

When the budget is exceeded:
- stop
- report partial progress
- suggest next smallest step

Never “just keep trying.”

---

## Rate limit patterns

- exponential backoff for transient failures
- jitter to avoid thundering herd
- circuit breaker when repeated failures occur
