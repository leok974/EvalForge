---
id: glossary/python/normalization
title: Data Normalization
world: python
level: intermediate
tags: [data, systems, architecture]
related:
  - codex:glossary/python/type-coercion
  - codex:glossary/python/data-pipeline
  - codex:glossary/python/systems/data-contracts
---

## Definition
**Data Normalization** is the process of transforming raw, inconsistent input into a standardized, "canonical" format. In system engineering, this ensures that downstream services can rely on a stable, predictable data structure regardless of the source.

## Why it Matters
Scaleable systems cannot afford "ad-hoc" handling of messy data in every component. By normalizing at the edge (Ingestion), you achieve:
- **Consistency**: All IDs are integers, all currencies are decimals, all timestamps are UTC.
- **Reliability**: No `KeyError` or `TypeError` deep in the business logic.
- **Interoperability**: Different services (e.g., Python, Go, Rust) can share data without parsing surprises.

## Implementation Patterns
In Python, normalization often involves a "Mapping" or "Schema" level of transformation:

### 1. The Strategy Pattern
```python
def normalize_record(raw: dict) -> dict:
    return {
        "id": int(raw.get("id", 0)),
        "email": raw.get("email", "").strip().lower() or None,
        "is_active": str(raw.get("active", "")).lower() == "true",
        "tags": [t.strip() for t in raw.get("tags", []) if t.strip()]
    }
```

### 2. Validator Libraries
For high-scale production, use dedicated libraries rather than hand-rolled logic:
- **Pydantic**: Uses type hints to enforce schemas.
- **Marshmallow**: Flexible schema-based serialization/deserialization.

## Related
- **Type Coercion**: Forcing values into a specific type (e.g., `str` to `int`).
- **Data Contracts**: Defining the expected shape of system-to-system communication.
- **Data Pipelines**: The automated flow that moves data through normalization stages.
