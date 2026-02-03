---
title: Agent Loop
id: agents/agent-loop
---
# Agent Loop

The core cycle of autonomous agent execution.

## Phases
1. **Plan**: Analyze task, break into steps
2. **Act**: Execute actions/tools
3. **Observe**: Gather results
4. **Reflect**: Evaluate progress, adjust

## Example Pattern
```python
while not task_complete:
    plan = planner.create_plan(context)
    result = executor.execute(plan)
    observation = observer.collect(result)
    context = reflector.update(context, observation)
```
