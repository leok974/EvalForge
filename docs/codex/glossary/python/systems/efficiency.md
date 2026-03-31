# System Efficiency

Efficiency in distributed systems is the measure of resource utilization (CPU, memory, network) relative to the work performed.

### Dimensions of Efficiency
-   **Time Complexity**: How the execution time grows with input size (Big O).
-   **Space Complexity**: How the memory footprint grows with input size.
-   **Resource Utilization**: Ensuring idle time is minimized and throughput is maximized.

### Optimizing Python
Python's interpreted nature makes efficiency critical. Common optimizations include:
-   Using `sets` for O(1) membership lookups instead of `lists` (O(n)).
-   Leveraging generators to minimize memory usage on large data streams.
-   Moving "Hot Paths" to specialized libraries (like NumPy) or C-extensions.

### Relevance in EvalForge
In the **Performance & Profiling** quest, you move from a naive approach to an efficient one by choosing the right data structures for the task.
