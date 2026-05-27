# Mission: The Archive's New Logic

Welcome, Archive Engineer. The Archive has been upgraded with **Vector Search**.

Instead of searching for exact words, we now search by **meaning**. Every text fragment in this vault has been converted into a **Vector**—a set of numbers that represents its semantic position.

### Your Objectives
1. **Inspect the Schema**: Look at the `historical_fragments` table in the Database Explorer. Note the `embedding` column.
2. **Find the First Fragment**: Retrieve the `content` and `embedding` for the very first fragment in our records.
3. **Internalize the Numbers**: Observe how the numbers in the vector correlate to the 'topic' of the content.

### The Topic Map (Conceptual)
In this collection, we use 3-dimensional vectors:
- **Dimension 1**: High value = Astronomy / Space
- **Dimension 2**: High value = Agriculture / Earth
- **Dimension 3**: High value = Politics / Society

When you see a vector like `[0.9, 0.1, 0.1]`, you know it's a celestial record!
