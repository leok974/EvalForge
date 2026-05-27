# Mission: Hybrid Precision

You've mastered semantic ranking. But in the real world, we often need to narrow our search space **before** we rank.

If a curator wants "Political documents similar to our peace treaty," they don't want results from the Biology or Astronomy departments, no matter how "close" the vectors might be.

### Hybrid Search
**Hybrid Search** is the practice of combining traditional SQL filters (`WHERE category = ...`) with vector distance ranking. This allows for extremely precise retrieval.

### Your Objective
Find the most similar fragment in the **Astronomy** category to the target vector `[0.9, 0.1, 0.1]`.
