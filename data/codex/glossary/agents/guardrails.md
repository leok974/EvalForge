---
title: Guardrails
id: agents/guardrails
---
# Guardrails

Safety constraints and policy enforcement for agents.

## Types
- **Allow/Deny Lists**: Restrict tools/actions
- **Sandboxing**: Isolate execution environment
- **Policy Gates**: Validate against rules
- **Rate Limits**: Prevent abuse

## Pattern
```python
class Guardrails:
    def check_action(self, action):
        if action.tool in self.deny_list:
            raise ActionBlocked("Tool not allowed")
        if not self.policy.allows(action):
            raise PolicyViolation("Action violates policy")
```
