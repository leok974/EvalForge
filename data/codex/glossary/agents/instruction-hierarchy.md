# Instruction Hierarchy

## Definition
**Instruction hierarchy** is the priority order used to resolve conflicting instructions. In most agent setups, higher-priority instructions override lower-priority ones. A simple mental model:
**System rules > User task > Examples/context**.

## Tiny example
System: “Return only JSON.”
User: “Explain in a paragraph.”
Result: Return JSON, not a paragraph.

## Common pitfall
When prompts conflict, the assistant may partially comply with both, creating unreliable outputs. Prevent this by stating explicit conflict rules: “If anything conflicts, follow the system prompt and return a structured error.”

## Related
System Prompt, User Prompt, Output Schema
