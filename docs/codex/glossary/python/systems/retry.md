---
id: glossary/python/systems/retry
title: Retry
world: python
level: intermediate
tags: [resilience, error-handling, systems]
related:
  - codex:glossary/python/systems/timeout
  - codex:glossary/python/systems/idempotency
  - codex:glossary/python/systems/exception-handling
---

## Definition
A **retry** is a strategy for handling transient failures by automatically re-attempting an operation after a delay. Retries are essential for resilient systems that call external APIs, databases, or unreliable services.

## Usage
- Retry network requests that might fail temporarily (503, timeouts).
- Use exponential backoff (increasing delays) to avoid overwhelming a recovering service.
- Set a maximum retry count to prevent infinite loops.

## Example
```python
import time

def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait)
            else:
                raise
```

## Pitfalls

* Retrying non-idempotent operations (like payments) can cause duplicate charges.
* No backoff strategy hammers failing services and makes outages worse.

## Related

* Timeout: combine retries with timeouts to avoid hanging.
* Idempotency: only retry idempotent operations safely.
* Exception Handling: retries catch and handle exceptions.