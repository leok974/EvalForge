# Hints — Internal Tooling & DX

## Hint 1
A good slugify pipeline is:
normalize spaces → spaces to hyphens → remove invalid chars → collapse hyphens → strip hyphens

## Hint 2
Use regex:
- remove invalid: `re.sub(r"[^a-z0-9-]+", "", s)`
- collapse hyphens: `re.sub(r"-{2,}", "-", s)`

## Hint 3
For unique_sorted:
`sorted(set(cleaned_items))`
