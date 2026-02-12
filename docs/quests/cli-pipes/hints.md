# Hints — Pipes

## Hint 1 (Concept)
To count duplicates reliably, you usually need:
`sort | uniq -c`

## Hint 2 (Guided)
To get top 2:
`... | sort -nr | head -n 2`

## Hint 3 (Near-solution)
`uniq -c` prints: `count name`.
You can swap it to `name count` using something like:
`awk '{print $2" "$1}'`
