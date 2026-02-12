# Hints — Processes

## Hint 1
`grep` comes before `awk` in this pipeline.

## Hint 2
The PID is the first column (`$1`).

## Hint 3 (Near-solution)
`grep "python" fixtures/ps.txt | awk '{print $1}' | sort > outputs/pids.txt`
