# Codex: The Foundry – Loop

*“The flame is lit. Now the metal flows.”*

## Loop Track – What this teaches

Loop is about **shaping data** with Python:

* Read and filter **CSV** and structured data.
* Use `list`, `dict`, `defaultdict`, `Counter`.
* Group and aggregate records (totals per category/month/etc.).
* Separate **pure transformation logic** from IO.
* Build a small, configurable “mini-ETL” that behaves like a real tool.

By the end of Loop, a player should be comfortable thinking:

> “Give me a pile of records and a config; I can shape it into the report you want.”

---

## Quest Hints

### Q1 – CSV Scraper – First Data Tap

**Essence:** Read CSV → filter by criteria.

* Use `csv.DictReader`, not manual `split(',')`.
* Make filter thresholds **parameters** (function args or CLI flags).
* Keep IO and core logic separate:

  * `load_transactions(path) → list[dict]`
  * `filter_transactions(transactions, min_amount, category) → list[dict]`

Common pitfalls:

* Treating everything as strings (not casting numbers).
* Hard-coding paths or filters.

---

### Q2 – Frequency Forge – Count the Logs

**Essence:** Count and rank things.

* Reach for `collections.Counter` first.

* Build helpers:

  ```python
  def count_by_level(logs): ...
  def top_messages(logs, n=3): ...
  ```

* Return structured results, e.g.:

  ```python
  {
    "by_level": {"INFO": 10, "ERROR": 3},
    "top_messages": [{"message": "X", "count": 5}, ...]
  }
  ```

Common pitfalls:

* Manual nested loops that are hard to read.
* No handling of empty input.

---

### Q3 – Grouping – Buckets of Molten Metal

**Essence:** Group-by and aggregate.

* Work with group keys like `(month, category)`:

  * Derive `month` from `created_at` or a `month` field.

* Use dict-of-accumulators:

  ```python
  totals[(month, category)] += amount
  ```

* At the end, convert keys back into dicts with explicit fields.

Common pitfalls:

* Copy-pasting accumulation logic in multiple places.
* Mutating nested structures in confusing ways.

---

## Boss: The Data Crucible

> *“Anyone can eyeball a few rows. The Crucible demands a repeatable transformation.”*

**Boss concept**

You build a **config-driven data summarizer**:

* Input:

  * A CSV file of records (transactions, events, etc.).
  * A JSON config describing how to group and aggregate.
* Output:

  * A JSON summary of grouped aggregates.

This is the first time the player:

* Treats **config as a first-class input**.
* Decouples IO and transform.
* Produces something that looks like a real “reporting job”.

---

### Boss Hints (player-facing)

* Let config drive behavior, e.g.:

  ```json
  {
    "group_by": ["month", "category"],
    "value_field": "amount"
  }
  ```

* Keep a clear pipeline:

  ```text
  load_config → load_rows → transform(rows, config) → write_output
  ```

* Make transform pure:

  ```python
  def aggregate(rows, group_by: list[str], value_field: str) -> list[dict]:
      ...
  ```

* Handle bad inputs:

  * Missing columns,
  * Invalid config keys,
  * Empty CSV.

---

### How Judge should think

Strong solutions:

* Treat **config + CSV** as parameters, not hard-coded.
* Have a **pure aggregation function** that can be tested without touching files.
* Produce JSON that reflects group fields + metrics.
* Handle missing/invalid inputs without ugly tracebacks.

Weak solutions:

* Ignore config; hard-code grouping.
* Mix IO and computation in one big function.
* Explode on minor input issues.
