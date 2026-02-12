# Tutorial — Performance & Profiling

## Approach
Implement two cost models:
1) naive scan comparisons
2) set strategy ops (build + membership)

Then choose the cheaper one deterministically.

## Steps
1. Implement `naive_comparisons(items, queries)`:
   - scan items for each query and count comparisons
2. Implement `set_ops(items, queries)`:
   - len(items) + len(queries)
3. Implement `choose_strategy`:
   - choose cheaper, tie -> "set"
4. Implement `count_hits`:
   - how many queries exist in items
5. Return the report object and print canonical JSON once.

## Pitfalls
- Off-by-one in naive comparisons when an item is found
- Forgetting tie-break rule
- Printing debug output (breaks stdout JSON parsing)
