**Quest: CTE Basics**

### The Mission
Our data analyst needs a report on frequent event types. Instead of one long, messy query, you've been asked to use a [CTE](glossary/sql/cte-with) to organize the logic.

First, calculate the volume of each event type, then filter for the high-volume ones.

### Requirements
1. **CTE**: Create a CTE named `EventCounts` that selects `event_type` and the [count](glossary/sql/count) of events (aliased as `num_events`).
2. **Filter**: In the main `SELECT`, pull from `EventCounts` and filter for types with **more than 1** event (`num_events > 1`).
3. **Sort**: Order the results by `event_type` in [ascending](glossary/sql/asc) order.
