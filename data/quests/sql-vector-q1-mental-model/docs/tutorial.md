# Understanding Embeddings

In pgvector, an **embedding** is stored in a special column type called `vector`.

### Viewing Vectors
You can select vector columns just like normal text or numbers:

```sql
SELECT content, embedding FROM historical_fragments;
```

### Why Vectors?
A vector is a coordinate in a multi-dimensional space. "Closer" coordinates mean "similar meaning." If two fragments are both about stars, their vectors will be close to each other.

### Your Task
Find the `fragment_id`, `content`, and `embedding` for the fragment with `fragment_id = 1`. 

Don't worry about the math yet—just focus on seeing the raw data that represents meaning.
