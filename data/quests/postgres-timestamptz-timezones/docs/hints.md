Global applications often store time in UTC but need to display it locally.

## Hint 1 — Timezone Operator
Use the `AT TIME ZONE` operator on the `hired_at` column.

## Hint 2 — Target Timezone
The string to specify the Tokyo timezone is `'Asia/Tokyo'`.

## Hint 3 — Final Syntax
Your query should look like: `SELECT name, email, hired_at AT TIME ZONE 'Asia/Tokyo' AS local_hired_at`.
