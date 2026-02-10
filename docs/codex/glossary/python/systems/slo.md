---
id: glossary/python/systems/slo
title: SLO
world: python
level: advanced
tags: [reliability, monitoring, systems]
related:
  - codex:glossary/python/systems/sli
  - codex:glossary/python/systems/observability
  - codex:glossary/python/systems/retry
---

## Definition
A **Service Level Objective (SLO)** is a target for an SLI over a time window. SLOs define acceptable service quality (e.g., "99.9% of requests succeed in the last 30 days"). Missing an SLO signals reliability issues.

## Usage
- Set SLOs based on user expectations, not perfect uptime (99.9% is often better than 99.99%).
- Use error budgets: if SLO is 99.9%, you can afford 0.1% errors (error budget).
- Violating SLOs triggers incident response or feature freezes.

## Example
```python
# SLO: 99.5% success rate over 30 days
slo_target = 0.995
current_sli = 0.993  # 99.3% actual success rate

if current_sli < slo_target:
    print("⚠️ SLO VIOLATION: Success rate below target")
    print(f"Error budget consumed: {(slo_target - current_sli) / (1 - slo_target) * 100:.1f}%")
else:
    print("✓ SLO met")
```

## Pitfalls

* Setting SLOs too high (99.99%+) is expensive and often unnecessary for non-critical features.
* Ignoring SLO violations trains teams to treat alerts as noise.

## Related

* SLI: SLOs are targets for SLIs.
* Observability: observability validates SLO compliance.
* Retry: retries help maintain SLOs during transient failures.