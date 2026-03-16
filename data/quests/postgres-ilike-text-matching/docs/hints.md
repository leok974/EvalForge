In this mission, your goal is to identify users with a specific email domain regardless of how they typed their email address.

## Hint 1 — Case-Insensitive Matching
The ILIKE operator is exactly what you need here. It performs pattern matching but ignores uppercase vs lowercase.

## Hint 2 — Wildcard Usage
Don't forget the `%` wildcard! You want emails that *end* with the domain, so your pattern should look like `'%@example.com'`.

## Hint 3 — Complete Pattern
Your WHERE clause should look something like: `WHERE email ILIKE '%@example.com'`.
