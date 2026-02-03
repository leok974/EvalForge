---
title: Executor
id: agents/executor
---
# Executor

Agent component that runs planned actions.

## Responsibilities
- Tool invocation
- Error handling
- Retry logic
- Result collection

## Pattern
```python
class Executor:
    def execute(self, step):
        tool = self.get_tool(step.tool_name)
        return tool.run(**step.params)
```
