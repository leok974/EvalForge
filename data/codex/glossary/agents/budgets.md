---
title: Agent Budgets
id: agents/budgets
---
# Agent Budgets

Resource limits and cost controls for agents.

## Budget Types
- **Token Budget**: Max LLM tokens
- **Cost Budget**: Max API spend
- **Time Budget**: Max execution time
- **Step Budget**: Max tool calls

## Pattern
```python
class Budget:
    def __init__(self, max_tokens=10000, max_cost=1.0):
        self.max_tokens = max_tokens
        self.max_cost = max_cost
        self.used_tokens = 0
        self.used_cost = 0
    
    def check(self):
        if self.used_cost > self.max_cost:
            raise BudgetExceeded("Cost limit reached")
```
