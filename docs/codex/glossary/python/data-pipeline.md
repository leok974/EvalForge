---
id: glossary/python/data-pipeline
title: Data Pipeline
world: python
level: intermediate
tags: [data, architecture, systems]
related:
  - codex:glossary/python/csv
  - codex:glossary/python/parse
  - codex:glossary/python/systems/queue-worker
---

## Definition
A **data pipeline** is a series of data processing steps where each step transforms, filters, or enriches data before passing it to the next step. Pipelines move data from sources (APIs, files, databases) to destinations (warehouses, dashboards, ML models).

## Usage
- Extract data from sources (APIs, databases, CSV files).
- Transform data (clean, aggregate, enrich).
- Load data into destinations (databases, data warehouses).
- Use tools like Airflow, Prefect, or custom Python scripts.

## Example
```python
# Simple ETL pipeline
def extract():
    # Read from source
    with open('data.csv', 'r') as f:
        return list(csv.DictReader(f))

def transform(data):
    # Clean and filter
    return [row for row in data if row['age'].isdigit()]

def load(data):
    # Write to database
    db.insert_many(data)

# Run pipeline
data = extract()
data = transform(data)
load(data)
```

## Pitfalls

* Pipelines without error handling fail silently and corrupt data.
* Not tracking pipeline runs makes debugging data issues nearly impossible.

## Related

* CSV: CSV files are common pipeline inputs.
* Parse: parsing is the first transform step in pipelines.
* Queue Worker: workers process pipeline tasks asynchronously.