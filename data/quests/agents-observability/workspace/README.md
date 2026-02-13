# Observability

Implement AuditLog.

- event(name, **fields) appends {name, ...fields, seq}
- span(name) context manager emits span_start / span_end with same span_id
- to_json() returns the list
No real time; use a deterministic sequence counter.
