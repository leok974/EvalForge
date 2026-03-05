$slugs = @(
    "sql-t2-subqueries-exists",
    "sql-t2-cte-basics",
    "sql-t2-recursive-cte-hierarchy",
    "sql-t2-nulls-coalesce",
    "sql-t2-dates-grouping",
    "sql-t2-upsert-on-conflict",
    "sql-t2-indexes-explain",
    "sql-t2-transactions-rollback",
    "sql-t2-boss-data-quality-audit"
)

foreach ($slug in $slugs) {
    Write-Host "Capturing golden for $slug..."
    python scripts/capture_golden_via_unified_runner.py --slug $slug
}
