---
id: glossary/python/systems/hot-path
title: Hot Path
world: python
level: intermediate
tags: [performance, optimization, systems]
related:
  - codex:glossary/python/systems/bottleneck
  - codex:glossary/python/systems/profiling
  - codex:glossary/python/systems/time-complexity
---

## Definition
The **hot path** is the code path that executes most frequently or handles the most critical requests. Optimizing the hot path has the biggest performance impact; optimizing cold paths is usually wasted effort.

## Usage
- Identify hot paths via profiling or request logs.
- Optimize hot paths for latency, throughput, and resource usage.
- Avoid adding complexity to hot paths (logging, validation, etc.).

## Example
```python
# Hot path: called millions of times per second
def calculate_price(quantity, unit_price):
    return quantity * unit_price  # Keep this simple and fast

# Cold path: called once per deployment
def initialize_config():
    # OK to have complex logic here
    config = load_yaml_config()
    validate_config(config)
    return config
```

## Pitfalls

* Optimizing cold paths while ignoring hot paths wastes time.
* Adding logging or expensive checks to hot paths kills performance.

## Related

* Bottleneck: the hot path often contains the bottleneck.
* Profiling: profiling identifies the hot path.
* Time Complexity: hot paths must have low time complexity.