# Mission: Choose Your Ruler

Not all distances are the same. In the Archives, we use different "distance metrics" to find similar documents.

### The Three Metrics
1. **L2 Distance (`<->`)**: Measures the straight-line distance between two points. Good if the length of the vector matters.
2. **Cosine Distance (`<=>`)**: Measures the **angle** between vectors. This is the gold standard for text, as it ignores how "long" the text is and focuses on the "direction" of the meaning.
3. **Inner Product (`<#>`)**: A dot product calculation. Often used for speed with specific types of normalized data.

### Your Objective
Compare these metrics. You'll see that while they often agree, they can rank documents differently. Your focus today is mastering **Cosine Distance (`<=>`)**.
