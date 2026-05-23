## Concept
Use `range(1, 11)` to include both 1 and 10 in your loop.

## Guided
Inside the loop, check `if i % 2 == 0:`. If it is, print the number and increment your counter. Don't forget to print the `EVEN_COUNT=` prefix at the very end.

## Full Solution
```python
def main():
    count = 0
    for i in range(1, 11):
        if i % 2 == 0:
            print(i)
            count += 1
    print(f"EVEN_COUNT={count}")

if __name__ == "__main__":
    main()
```
*Note: The loop must be inside the `main()` function as provided in the starter code.*
