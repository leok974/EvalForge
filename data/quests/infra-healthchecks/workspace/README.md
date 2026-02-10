# Infra Healthchecks: Aggregator

Read fixtures/health.txt (format: "NAME STATUS_CODE LATENCY")
Write outputs/health_status.txt:
STATUS=OK|DEGRADED
FAILED=name1,name2 (comma-separated, empty if none)
SLOWEST=name3 latency

Write outputs/health_score.txt:
Integer percent (ok / total * 100)
