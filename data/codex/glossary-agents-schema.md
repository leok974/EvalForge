---
id: glossary/agents/schema
title: Schema (Structured Output)
section: Glossary
world: Agents
---

# Schema (Structured Output)

A **schema** defines the structure and constraints for data, enabling AI agents to produce consistent, machine-readable outputs.

## Why Schemas Matter for Agents

When building AI agents, you need responses in predictable formats (JSON, XML, etc.) that your code can parse and use. Schemas enforce:

- **Type safety**: Fields have defined types (string, number, boolean, etc.)
- **Required fields**: Ensure critical data is always present
- **Validation**: Reject invalid or malformed responses
- **Documentation**: Self-documenting API contracts

## Common Schema Formats

### JSON Schema

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "number" },
    "active": { "type": "boolean" }
  },
  "required": ["name"]
}
```

### Pydantic (Python)

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    active: bool = True
```

### TypeScript Types

```typescript
interface User {
  name: string;
  age: number;
  active?: boolean;
}
```

## Structured Output in Prompts

Many LLM APIs support schema-constrained generation:

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Extract user info"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "user_info",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "number"}
                },
                "required": ["name"]
            }
        }
    }
)
```

## Best Practices

1. **Start simple**: Begin with required fields only
2. **Add constraints**: Use `minimum`, `maximum`, `pattern` for validation
3. **Provide examples**: Include sample outputs in prompts
4. **Handle errors**: LLMs may still violate schemas—validate responses
5. **Iterate**: Refine schemas based on real-world outputs

## Tools & Libraries

- **JSON Schema**: Industry standard, language-agnostic
- **Pydantic**: Python validation with excellent LLM integration
- **Zod**: TypeScript-first schema validation
- **Instructor**: Python library for structured LLM outputs

## Related Terms

- **Prompt Engineering**: Crafting prompts to guide schema adherence
- **Function Calling**: LLM feature to return structured function arguments
- **Type Safety**: Preventing runtime errors via compile-time checks
