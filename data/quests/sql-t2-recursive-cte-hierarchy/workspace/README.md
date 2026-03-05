# Mission: Recursive CTEs (Hierarchy)
**Goal**: Use `WITH RECURSIVE` to find all employees and their distance from the CEO (Alice, id 1).
Return `id, name, distance`.
- Alice has distance 0.
- Her direct reports have distance 1, and so on.
**Order**: By `distance` ASC, then `id` ASC.