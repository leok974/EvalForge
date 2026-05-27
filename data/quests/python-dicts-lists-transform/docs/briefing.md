# Mission: Data Transformations (Ignition)

In the field, data rarely arrives in the exact format your systems need. One of the most common tasks for an automation engineer is **reshaping data**—taking a raw list of event logs, inventory items, or sensor readings and aggregating them into a summarized report.

### The Inventory Problem
You've been handed a list of dictionaries from the warehouse scanner. Each dictionary represents a single item arrival with a `category` and a `qty` (quantity). Currently, the data is too granular.

### Your Objective
Implement `transform_inventory` in `task.py`. Your goal is to produce a single dictionary where the keys are the **categories** and the values are the **summed quantities** for each category.

This is a foundational skill for building resilient Python automation that can handle varying data inputs.
