# Infra Logs & Metrics: Parser

Parse fixtures/app.log.
Write outputs/metrics.prom:
app_log_info_total N
app_log_warnings_total N
app_log_errors_total N

Write outputs/top_error.txt:
Most frequent ERROR token (e.g. E_CONNREFUSED). Tie-break lexicographically.
