# Tutorial: Loops and Output

## Printing a line of text

`print()` sends one line to the console. Every time you call it, a new line appears:

```python
print("Hello")
print("World")
```

Output:
```
Hello
World
```

The order matters — Python runs each statement top to bottom, one at a time.

## Counting down with range()

`range(start, stop, step)` produces a sequence of numbers. To count *down* from 5
to 1 (stopping before 0), use a negative step:

```python
for i in range(5, 0, -1):
    print(i)
```

Output:
```
5
4
3
2
1
```

`range(5, 0, -1)` starts at 5, goes down by 1 each iteration, and stops before it
reaches 0. The stop value is never included.

## Combining a loop with a final statement

Sometimes you need to do something *after* the loop finishes — just place that
statement outside the indented block:

```python
for i in range(5, 0, -1):
    print(i)

print("Liftoff")
```

The `print("Liftoff")` line runs once, after all the loop iterations are done.

## Verifying your output

Run your code and check the console panel. Each line should appear on its own row.
If the lines are in the wrong order, check that your statements are in the right
sequence — Python executes them exactly as written.
