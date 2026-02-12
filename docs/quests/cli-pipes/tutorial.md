# Tutorial — Pipes

## Mental model
You’re building a pipeline where each command transforms the stream:

input -> sort -> count -> rank -> select -> format -> output

## Useful tools
- `sort` (groups equal values together)
- `uniq -c` (counts adjacent duplicates)
- `sort -nr` (rank by count)
- `head -n 2` (take top 2)
- `awk` (reformat fields)

## Pitfalls
- Forgetting to sort before `uniq -c` (counts will be wrong)
- Outputting "count name" instead of "name count"
- Printing extra debug output
- Not producing deterministic ordering
