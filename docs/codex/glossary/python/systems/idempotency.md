---
id: glossary/python/systems/idempotency
title: Idempotency
world: python
level: intermediate
tags: [systems, reliability, api-design]
related:
  - codex:glossary/python/systems/retry
  - codex:glossary/python/systems/side-effect
  - codex:glossary/python/systems/queue-worker
---

## Definition
An operation is **idempotent** if calling it multiple times produces the same result as calling it once. Idempotency is critical for safe retries, distributed systems, and APIs that clients might call repeatedly.

## Usage
- Design PUT/DELETE REST endpoints to be idempotent (safe to retry).
- Use unique request IDs to de-duplicate operations.
- Avoid idempotency for non-repeatable actions (payments, sending emails).

## Example
```python
# Idempotent: setting a user's email (can safely retry)
def set_user_email(user_id, email):
    db.users.update({"id": user_id}, {"email": email})

# NOT idempotent: incrementing a counter (retries cause double-counting)
def increment_view_count(post_id):
    db.posts.update({"id": post_id}, {"$inc": {"views": 1}})

# Fix: use idempotency key
def increment_view_count_safe(post_id, request_id):
    if not db.requests.find_one({"id": request_id}):
        db.posts.update({"id": post_id}, {"$inc": {"views": 1}})
        db.requests.insert_one({"id": request_id})
```

## Pitfalls

* Assuming all operations are safely retryable without checking idempotency.
* Using POST for idempotent operations instead of PUT/PATCH.

## Related

* Retry: only retry idempotent operations safely.
* Side Effect: idempotent operations may have side effects but produce the same final state.
* Queue Worker: workers must handle duplicate messages idempotently.