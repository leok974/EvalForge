---
id: glossary/python/systems/observability
title: Observability
world: python
level: intermediate
tags: [monitoring, systems, debugging]
related:
  - codex:glossary/python/systems/structured-logging
  - codex:glossary/python/systems/sli
  - codex:glossary/python/systems/slo
---

## Definition
**Observability** is the ability to understand a system's internal state by examining its outputs (logs, metrics, traces). In production, observability lets you debug issues, measure performance, and understand user behavior without modifying code.

## Usage
- Instrument code with structured logs, metrics (counters, gauges), and traces.
- Use observability platforms (Datadog, New Relic, Prometheus) to aggregate signals.
- Answer questions like "Why is this endpoint slow?" or "Which users are hitting errors?"

## Example
```python
import logging
from prometheus_client import Counter, Histogram

# Metrics
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'Request duration')

@request_duration.time()
def handle_request():
    request_count.inc()
    logging.info("Processing request", extra={"user_id": 123})
    # ... process request
```

## Pitfalls

* Instrumenting everything creates noise; focus on high-value signals (errors, latency, traffic).
* Poor observability means debugging production issues requires deploying new code with more logging.

## Related

* Structured Logging: logs are a key observability signal.
* SLI: observability powers SLI measurements.
* SLO: observability validates whether SLOs are met.