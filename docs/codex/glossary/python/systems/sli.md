---
id: glossary/python/systems/sli
title: SLI
world: python
level: advanced
tags: [reliability, monitoring, systems]
related:
  - codex:glossary/python/systems/slo
  - codex:glossary/python/systems/observability
  - codex:glossary/python/systems/structured-logging
---

## Definition
A **Service Level Indicator (SLI)** is a quantitative measure of service quality, typically expressed as a percentage. Common SLIs include request success rate, latency percentiles (p50, p99), and availability. SLIs form the foundation of SLOs.

## Usage
- Define SLIs for critical user journeys (e.g., "99% of login requests succeed").
- Measure SLIs from real production traffic, not synthetic tests.
- Track SLIs in dashboards to spot degradations early.

## Example
```python
# SLI: Request success rate
total_requests = 1000
successful_requests = 995
error_requests = 5

sli_success_rate = (successful_requests / total_requests) * 100
print(f"SLI: {sli_success_rate}% success rate")  # 99.5%

# SLI: Latency p99
import numpy as np
latencies = [10, 15, 20, 25, 500]  # milliseconds
p99 = np.percentile(latencies, 99)
print(f"SLI: p99 latency = {p99}ms")
```

## Pitfalls

* Measuring SLIs on non-representative traffic (e.g., health checks) gives false confidence.
* Too many SLIs dilute focus; pick 2-3 per service that matter to users.

## Related

* SLO: SLOs set targets for SLIs (e.g., "SLI must be >99.9%").
* Observability: observability tools measure SLIs.
* Structured Logging: logs power SLI calculations.