---
title: Planner
id: agents/planner
---
# Planner

Agent component that decomposes tasks into executable steps.

## Responsibilities
- Task analysis
- Step sequencing
- Dependency resolution
- Resource allocation

## Pattern
```python
class Planner:
    def create_plan(self, task, context):
        steps = self.decompose(task)
        return self.sequence(steps, context)
```
