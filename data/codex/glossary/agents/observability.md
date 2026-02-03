---
title: Agent Observability
id: agents/observability
---
# Agent Observability

Monitoring and debugging agent behavior.

## Instrumentation
- **Audit Logs**: Who did what, when
- **Traces**: Execution flow, timing
- **Run IDs**: Unique execution identifiers
- **Artifacts**: Intermediate outputs

## Example
```python
class ObservabilityTracker:
    def log_action(self, run_id, action, result):
        self.audit_log.append({
            'run_id': run_id,
            'timestamp': now(),
            'action': action,
            'result': result
        })
```

## Use Cases
- Debugging failures
- Cost analysis
- Compliance audits
