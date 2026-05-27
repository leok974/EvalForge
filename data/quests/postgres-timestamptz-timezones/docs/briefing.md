# The Tokyo Transition

Our `employees` table stores the `hired_at` date as a `TIMESTAMPTZ`, which guarantees it represents an absolute moment in global time (stored internally as UTC).

However, the managers in our Tokyo office generate local reports, and looking at UTC times confuses them.

Your objective is to read from the `employees` table and return each employee's `name`, `email`, and their `hired_at` time converted to the `Asia/Tokyo` timezone. 

Alias the converted time column as `local_hired_at`.
