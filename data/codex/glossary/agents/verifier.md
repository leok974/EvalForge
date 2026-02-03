---
title: Verifier
id: agents/verifier
---
# Verifier

Agent component that validates results and progress.

## Checks
- **Correctness**: Did it work?
- **Completeness**: Are we done?
- **Quality**: Is it good enough?
- **Safety**: Is it safe?

## Pattern
```python
class Verifier:
    def verify(self, result, expected):
        if not self.is_correct(result):
            return VerificationFailed("Incorrect")
        return VerificationPassed()
```
