---
title: Break and Continue
id: codex:glossary/python/break-continue
world: python
---

# Break and Continue

Loop control statements allow you to change the execution flow of loops.

## Break

`break` terminates the current loop and resumes execution at the next statement after the loop.

```python
for i in range(10):
    if i == 5:
        break
    print(i)
# Prints 0, 1, 2, 3, 4
```

## Continue

`continue` skips the rest of the code inside the loop for the current iteration and jumps to the next iteration.

```python
for i in range(5):
    if i == 2:
        continue
    print(i)
# Prints 0, 1, 3, 4
```
