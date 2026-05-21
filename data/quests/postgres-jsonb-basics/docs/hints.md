## Hint 1
The `->>` operator extracts a JSONB field as text. Syntax: `payload->>'fieldname'`. This gives you a regular SQL text value you can alias and filter on.

## Hint 2
To extract `user_id` as a column: `payload->>'user_id' AS user_id`. Repeat for `action`.

## Hint 3
Filter with `WHERE payload->>'status' = 'active'`. This compares the extracted text value to the string literal `'active'`.
