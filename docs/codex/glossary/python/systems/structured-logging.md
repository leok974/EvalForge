---
id: glossary/python/systems/structured-logging
title: Structured Logging
world: python
level: intermediate
tags: [observability, logging, debugging]
related:
  - codex:glossary/python/systems/observability
  - codex:glossary/python/systems/correlation-id
  - codex:glossary/python/systems/sli
---

## Definition
**Structured logging** emits log messages as JSON objects (or similar structured formats) instead of plain text strings. This makes logs queryable, filterable, and machine-readable — essential for modern observability tools.

## Usage
- Use JSON logging to make logs searchable by field (user_id, request_id, status_code).
- Include context like timestamps, severity levels, and correlation IDs in every log.
- Send structured logs to aggregation tools (Datadog, Splunk, CloudWatch).

## Example
```python
import logging
import json_log_formatter

# Configure JSON logging
formatter = json_log_formatter.JSONFormatter()
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Emit structured logs
logger.info("User logged in", extra={"user_id": 123, "ip": "192.168.1.1"})
# Output: {"message": "User logged in", "user_id": 123, "ip": "192.168.1.1", "timestamp": "2024-01-15T..."}
```

## Pitfalls

* Logging sensitive data (passwords, tokens) in structured logs exposes them to log aggregators.
* Over-logging creates noise and increases storage costs; log only actionable information.

## Related

* Observability: structured logging enables better observability.
* Correlation ID: include correlation IDs in structured logs to trace requests.
* SLI: structured logs power SLI calculations (error rates, latencies).