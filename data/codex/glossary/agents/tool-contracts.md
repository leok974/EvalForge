---
title: Tool Contracts
id: agents/tool-contracts
---
# Tool Contracts

JSON schemas defining agent tool interfaces.

## Structure
```json
{
  "name": "search_web",
  "description": "Search the web for information",
  "parameters": {
    "query": {"type": "string", "required": true}
  },
  "returns": {"type": "array"}
}
```

## Best Practices
- Clear descriptions
- Strict types
- Error handling
- Validate inputs/outputs
