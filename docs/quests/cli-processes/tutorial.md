# Tutorial — Processes

## Tools
- `grep` to filter lines.
- `awk` to extract columns.
- `sort` to order results.

## Pipeline thought process
1. Select lines: `grep "python"`
2. Pick column: `awk '{print $1}'` (assuming PID is col 1)
3. Sort: `sort`

## Handling headers
`grep` usually filters out the header "PID COMMAND" automatically if you search for "python", but be careful if "python" appears in the header (unlikely here).
