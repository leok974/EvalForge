---
id: glossary/sql/data-quality
title: data-quality
world: sql
---

# data-quality

**Data quality** refers to the accuracy, completeness, and reliability of the data stored in a database. Poor data quality often results from bugs, human error, or system migrations.

## Common Issues

- **Orphaned Records**: A child record exists but its parent was deleted.
- **Inconsistencies**: The same data is stored differently in two places.
- **Invalid Values**: Data that violates constraints (e.g., negative age).

Engineers use techniques like [anti-joins](glossary/sql/anti-join) and audit queries to identify and fix these issues.