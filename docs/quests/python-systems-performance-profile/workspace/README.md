# Performance & Profiling (Deterministic)

## Objective
Read a fixture describing membership queries, compute a deterministic “profile report”
using operation counts, choose the cheaper strategy, and print a canonical JSON summary.

This quest trains performance thinking without timing:
- identify a hot path (membership checks)
- compare naive vs indexed approaches
- choose a strategy deterministically

## Input
A JSON object in:
- `fixtures/profile_case.json`

Shape:
- `items`: list[str]
- `queries`: list[str]

## Strategies
### 1) naive
For each query, scan `items` from start to end:
- Count 1 comparison per item checked.
- If found at position p (0-index), comparisons += p+1
- If not found, comparisons += len(items)

### 2) set
Build an index set once, then do O(1) membership checks:
- build_ops = len(items)  (one insert attempt per item)
- membership_ops = len(queries)  (one check per query)
- set_ops = build_ops + membership_ops

## Output
Print exactly one line to stdout: a JSON object using canonical formatting:
`json.dumps(out, sort_keys=True, separators=(",",":"))`

Required output shape:
- `hits` (int): how many queries exist in items
- `strategy` (string): "naive" or "set" (the cheaper one)
- `cost` (object):
  - `naive_comparisons` (int)
  - `set_ops` (int)

Tie-break rule:
- If costs are equal, choose `"set"`.

## Constraints
- Standard library only.
- Core logic must not read files or print.
- Only `main.py` may read the fixture and print stdout.
- Deterministic: no timing, randomness, or current time.

## Verification
Locally:
```bash
python main.py
```

You should see one canonical JSON line printed.
