---
slug: boss-gradient-nexus-attacks
boss_id: gradient_nexus
tier: 2
world_id: world-synapse
tags:
  - boss
  - gradient_nexus
  - attacks
  - ml
title: "The Gradient Nexus – Failure Modes"
---

> ZERO: "Most bad models aren't wrong, they're unmeasured."

Attack patterns:

1. **Leakage – "Data Echo"**  
   - Same samples appear in train and validation.
   - Tests detect suspiciously perfect metrics.

2. **Frozen Model – "Dead Weight"**  
   - Training loop incorrectly wired, parameters never update.
   - Loss never changes, metrics stagnant.

3. **Wrong Metric – "False Confidence"**  
   - Using accuracy in highly imbalanced data where it’s meaningless.
   - Tests compare against a baseline.

4. **No Repro – "Non-deterministic Fog"**  
   - No seed setting, runs vary wildly.
   - Tests prefer stable behavior.
