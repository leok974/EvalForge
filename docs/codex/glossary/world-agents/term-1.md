---
title: Tool Contract
id: glossary/world-agents/term-1
world: world-agents
level: intermediate
tags: [agents, tools, reliability]
related:
  - codex:glossary/agents/grounding
  - codex:glossary/agents/citation
---

# Tool Contract

## Definition
**Tool Contract** is a strict schema for tool inputs/outputs that the agent must follow. Contracts make tool calls predictable and prevent "stringly-typed" failures.

## Usage
- Define request/response models (e.g., Pydantic/TypeScript types).
- Validate tool output before showing it to users.
- Version contracts when behavior changes.

## Example
```json
{
  "tool": "debug",
  "input": { "stdout": "...", "stderr": "...", "tests_failed": 2 },
  "output": { "observation": "...", "reason": "...", "fix_plan": ["..."] }
}
```

## Pitfalls

* Loose contracts lead to UI breakage and inconsistent behavior.
* Silent coercion ("best effort parsing") hides tool bugs.

## Related

* Grounding: tool outputs provide grounding.
* Citation: citations can reference tool outputs.
