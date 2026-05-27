## Distance Operator

The operator for Cosine distance is `<=>`.

## Vector Literal

The target vector literal is `'[0.5, 0.5, 0.5]'::vector`.

## Full Query Example

Your query should look like: `SELECT fragment_id, embedding <=> '[0.5, 0.5, 0.5]'::vector as distance FROM historical_fragments;`
