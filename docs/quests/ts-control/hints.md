# Hints — TS Control

## Hint 1
Guard early:
- if not number → invalid
- if not integer → invalid
- if out of range → invalid

## Hint 2
Then check ranges in order:
500s, 400s, 300s, 200s

## Hint 3
Return type is a union. Every branch must return one of the union strings.
