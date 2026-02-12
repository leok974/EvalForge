# Briefing — Processes

## Objective
Filter a process list to find specific PIDs.

## Success Criteria
1. Read `fixtures/ps.txt`.
2. Extract PIDs where the command contains `python`.
3. Write to `outputs/pids.txt`.
4. Sort numerically ascending.

## Constraints
- Input format: PID COMMAND (space separated, but command may have spaces)
- Output format: One PID per line.
- No header in output.
