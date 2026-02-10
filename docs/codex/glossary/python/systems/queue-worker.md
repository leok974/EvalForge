---
id: glossary/python/systems/queue-worker
title: Queue Worker
world: python
level: advanced
tags: [distributed-systems, async, architecture]
related:
  - codex:glossary/python/systems/idempotency
  - codex:glossary/python/systems/retry
  - codex:glossary/python/systems/correlation-id
---

## Definition
A **queue worker** is a process that consumes messages from a queue (like RabbitMQ, Redis, SQ S) and performs background tasks. Workers decouple heavy processing from request/response cycles, improving API responsiveness.

## Usage
- Offload slow tasks (email sending, image processing, data pipeline jobs) to workers.
- Use queues to handle traffic spikes without overloading servers.
- Ensure workers are idempotent — messages may be delivered more than once.

## Example
```python
import redis

# Producer: enqueue work
queue = redis.Redis()
queue.lpush("tasks", json.dumps({"type": "send_email", "to": "user@example.com"}))

# Worker: process tasks
while True:
    task_json = queue.brpop("tasks", timeout=5)
    if task_json:
        task = json.loads(task_json[1])
        print(f"Processing: {task['type']}")
        send_email(task['to'])
```

## Pitfalls

* Workers that aren't idempotent can process the same message multiple times, causing duplication.
* No dead-letter queue means failed messages are lost forever.

## Related

* Idempotency: workers must handle duplicate messages idempotently.
* Retry: workers need retry logic for transient failures.
* Correlation ID: preserve correlation IDs from queued messages for tracing.