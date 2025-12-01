---
id: langgraph-state-management
title: LangGraph State Management
world: world-agents
tier: 3
difficulty: advanced
tags: [langgraph, agents, ai]
summary: >-
  Managing the shared memory context between nodes in a cyclic graph.
version: 1
last_updated: 2025-11-29
xp_reward: 200
prerequisites: []
stack: [langgraph]
source: curated
trust_level: high
---

# Definition
> TL;DR: In LangGraph, "State" is a `TypedDict` or Pydantic model passed between nodes. Unlike a linear chain, the state is persistent and mutable across cycles.

# The Golden Path (Best Practice)
Use `Annotated` with `operator.add` for list fields (like messages) so nodes *append* history rather than overwriting it.

```python
import operator
from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    # ✅ Appends new messages to the existing list
    messages: Annotated[List[BaseMessage], operator.add]
    # Overwrites the value (default behavior)
    current_step: str
```

# Common Pitfalls (Anti-Patterns)

❌ **Overwriting History:**
If you define `messages: List[BaseMessage]` without `Annotated`, every node output replaces the *entire* conversation history, causing the agent to develop amnesia.

# Deep Dive (Internals)

LangGraph treats the State as a Reducer. When a node returns `{"messages": [new_msg]}`, the framework looks at the `Annotated` operator. If it's `operator.add`, it performs `old_list + [new_msg]`. If no operator is defined, it performs `state["key"] = new_value`.
