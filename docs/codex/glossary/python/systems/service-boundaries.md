# Service Boundaries

A **Service Boundary** is the clear line between a domain's internal logic and the external world (e.g., APIs, databases, or user input).

## Why it matters
In large systems, letting "raw" data permeate your core logic leads to fragile code. Boundaries act as a corruption layer where data is:
1. **Validated**: Ensuring required fields exist.
2. **Coerced**: Converting strings like `"42"` to integers.
3. **Classified**: Mapping system failures to domain-specific errors.

## Example
A boundary function takes a dictionary of unknown stability and returns a predictable response.

```python
def boundary_handler(raw_req: dict):
    # Enforce the contract
    user_id = int(raw_req.get("user_id", 0))
    if user_id <= 0:
        return {"ok": False, "error": "INVALID_ID"}
    return {"ok": True, "value": process_logic(user_id)}
```

## Related
- [Data Contracts](codex:glossary/python/systems/data-contracts)
- [Coercion](codex:glossary/python/systems/data-contracts)
- [Separation of Concerns](codex:glossary/python/systems/separation-of-concerns)
