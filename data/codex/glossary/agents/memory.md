---
title: Agent Memory
id: agents/memory
---
# Agent Memory

Information storage and retrieval for agents.

## Types
- **Working Memory**: Current task context
- **Long-term Memory**: Past experiences, facts
- **Semantic Memory**: Knowledge graph, embeddings

## Retrieval
```python
class Memory:
    def store(self, key, value, scope='working'):
        self.db[scope][key] = value
    
    def recall(self, query, scope='all'):
        return self.search(query, scope)
```

## Safety
- Limit memory size (prevent leaks)
- Sandboxed retrieval
- Privacy/consent controls
