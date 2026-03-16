# Mission: Semantic Discovery

Now that you understand the rulers, let's execute a real search.

In the Archive, we don't just calculate distance—we use it to **rank** our records. When a curator asks for "documents about politics," we don't just give them a random list; we give them the fragments that are **statistically closest** to the idea of politics.

### Natural Selection
By ordering by distance and capping the result with `LIMIT`, you perform what's known as **Top-K Retrieval**.

### Your Objective
Find the **Top 2** fragments most similar to the idea of **Politics** (represented by the vector `[0.1, 0.1, 0.9]`).
