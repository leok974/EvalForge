# Tutorial — Loop

## What You’ll Learn
- Iterating a numeric range with `for`
- Filtering values with a conditional (`if`)
- Accumulating a count safely

## Approach
This is a standard “filter + accumulate” pattern:
1) Loop through numbers 1..10
2) If a number is even, print it and increment a counter
3) Print the final counter

## Implementation Plan
1. Initialize `count = 0`
2. Loop with `for n in range(1, 11):`
3. Check evenness with `if n % 2 == 0:`
4. Inside the if:
   - `print(n)`
   - `count += 1`
5. After the loop:
   - `print(f"EVEN_COUNT={count}")`

## Testing
Run your questpack runner in solution mode and confirm `python-loop` is green.

## Pitfalls
- Using the wrong range end (must include 10 → `range(1, 11)`)
- Printing the summary inside the loop (creates extra lines)
- Extra whitespace or extra blank line at the end
