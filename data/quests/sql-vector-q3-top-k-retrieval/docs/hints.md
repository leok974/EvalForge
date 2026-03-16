## Top-K Pattern

The pattern is: ORDER BY (vector <=> target) LIMIT K.

## The Target Vector

Remember the target vector is `'[0.1, 0.1, 0.9]'::vector`.

## Result Capping

Your query needs `LIMIT 2` at the very end.
