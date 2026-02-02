## Outcome
By the end of this quest you will:
- Use **map** to transform every element in an array
- Use **filter** to keep only the elements you want
- Use **reduce** to combine all elements into one value
- Understand how a **callback** function is used by these methods

## Concept in 30 seconds
Arrays often need the same 3 operations:
- **Transform** every item → `map`
- **Select** some items → `filter`
- **Combine** items into one result → `reduce`

Each method takes a **callback**: a function you provide that runs once per element.

**Mental model:**  
You give the array a “recipe” (callback). The array runs that recipe for each element and returns a new result.

## Key terms
- **array** — an ordered list like `[1, 2, 3]`
- **callback** — a function passed into another function to be called later
- **map** — transforms each element into a new array
- **filter** — keeps elements that pass a condition
- **reduce** — accumulates elements into a single value

## Walkthrough
1) Open `main.js`.
2) Implement `doubleAll(nums)` using `map`.
   - Input: `[1,2,3]` → Output: `[2,4,6]`
3) Implement `onlyEvens(nums)` using `filter`.
   - Input: `[1,2,3,4]` → Output: `[2,4]`
4) Implement `sum(nums)` using `reduce`.
   - Input: `[1,2,3]` → Output: `6`
5) Click **Run** to see the sample outputs.
6) Click **Submit** when all tests pass.

## Example implementation
```js
export function doubleAll(nums) {
  return nums.map((n) => n * 2);
}

export function onlyEvens(nums) {
  return nums.filter((n) => n % 2 === 0);
}

export function sum(nums) {
  return nums.reduce((acc, n) => acc + n, 0);
}
```

## Common mistakes

* **Forgetting to return in map/filter**

  * Wrong: `{ n * 2 }` (block body without `return`)
  * Fix: use `n => n * 2` or `return n * 2`
* **Mutating the input array**

  * `map/filter/reduce` should return new values. Don’t `push` into the original.
* **Missing reduce initial value**

  * If you omit the initial value, edge cases like `[]` are painful.
  * Fix: pass `0` for sums, `[]` for arrays, `{}` for objects.
* **Using map when you need filter**

  * `map` always returns same length. `filter` can shrink.

## Check yourself

1. Which method is best for turning `[1,2,3]` into `[1,4,9]`?
2. Which method should you use to keep only items that match a rule?
3. What does the `acc` (accumulator) represent in `reduce`?
