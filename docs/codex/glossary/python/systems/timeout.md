---
id: glossary/python/systems/timeout
title: Timeout
world: python
level: intermediate
tags: [resilience, error-handling, systems]
related:
  - codex:glossary/python/systems/retry
  - codex:glossary/python/systems/exception-handling
  - codex:glossary/python/systems/hot-path
---

## Definition
A **timeout** is a maximum time limit for an operation to complete. If the operation takes longer than the timeout, it's aborted and raises an exception. Timeouts prevent hung processes and improve system resilience.

## Usage
- Set timeouts on network requests to avoid waiting forever for slow/dead services.
- Use timeouts in database queries to detect performance issues early.
- Configure timeouts slightly above expected response times (e.g., 5-10 seconds for APIs).

## Example
```python
import requests

# Timeout after 5 seconds
try:
    response = requests.get("https://api.example.com/data", timeout=5)
    print(response.json())
except requests.Timeout:
    print("Request timed out after 5 seconds")

# Separate connect and read timeouts
response = requests.get(url, timeout=(3, 10))  # 3s connect, 10s read
```

## Pitfalls

* No timeout means your code can hang indefinitely waiting for a response.
* Timeouts too short cause false failures; too long wastes resources on slow requests.

## Related

* Retry: combine timeouts with retries for resilient systems.
* Exception Handling: timeouts raise exceptions that must be handled.
* Hot Path: timeouts are critical on latency-sensitive code paths.