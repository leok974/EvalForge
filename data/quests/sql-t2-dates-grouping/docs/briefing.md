**Quest: Date Bucketing & Grouping**

### The Mission
Our activity logs are overflowing with timestamps. We need a summary report that shows the total number of events for **each specific day**.

Convert the high-precision timestamps into simple date buckets and count the results.

### Requirements
1. **Columns**: 
   - Use `strftime('%Y-%m-%d', event_date)` to create a date-only column aliased as `event_date_only`.
   - Select a [count](glossary/sql/count) of all events aliased as `num_events`.
2. **Mechanism**: Group the results by your new `event_date_only` alias.
3. **Sort**: Order the results by [date](glossary/sql/order-by) in ascending order.
