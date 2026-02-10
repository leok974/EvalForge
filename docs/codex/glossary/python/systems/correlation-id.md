---
id: glossary/python/systems/correlation-id
title: Correlation ID
world: python
level: intermediate
tags: [observability, distributed-systems, debugging]
related:
  - codex:glossary/python/systems/structured-logging
  - codex:glossary/python/systems/observability
  - codex:glossary/python/systems/queue-worker
---

## Definition
A **correlation ID** is a unique identifier that tracks a request across multiple services or processes. When a request enters your system, it gets assigned a correlation ID that's logged and passed to all downstream services, making it easy to trace the request's full journey.

## Usage
- Generate a correlation ID at the API gateway or first service.
- Include it in all logs, database queries, and API calls.
- Use it to filter logs and reconstruct the sequence of events for a single request.

## Example
```python
import uuid
import logging

def handle_request(request):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    
    logging.info("Processing request", extra={"correlation_id": correlation_id})
    
    # Pass to downstream services
    response = requests.get(
        "https://api.service2.com/data",
        headers={"X-Correlation-ID": correlation_id}
    )
    
    return response
```

## Pitfalls

* Not propagating correlation IDs to all services breaks traceability.
* Overwriting correlation IDs at service boundaries loses the connection to the original request.

## Related

* Structured Logging: correlation IDs are included in structured logs.
* Observability: correlation IDs power distributed tracing.
* Queue Worker: workers should preserve correlation IDs from messages.