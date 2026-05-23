# Loops and Conditionals

Combining iteration with logic allows you to filter and count data streams.

### The Modulo Operator (%)
To check if a number is even, we use the modulo operator. `n % 2 == 0` is true if `n` is divisible by 2 with no remainder.

```python
if 4 % 2 == 0:
    print("Even!")
```

### Counting with Loops
Initialize a counter variable outside your loop and increment it inside your conditional block.

```python
count = 0
for i in range(5):
    if i > 2:
        count += 1
print(f"Greater than 2: {count}")
```

### Your Task
In `task.py`, use a `for` loop and `range(1, 11)` to find and count the even numbers. Make sure your final output matches the required format exactly!
