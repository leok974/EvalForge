"""
Prometheus metrics for EvalForge.
Exposes /metrics endpoint for monitoring Judge grading performance.
"""
from prometheus_client import Counter, Histogram, Summary, CONTENT_TYPE_LATEST, generate_latest
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route

# Judge grading metrics
JUDGE_GRADE_TOTAL = Counter(
    "judge_grade_total",
    "Judge grading outcomes",
    ["result"]  # new|dedupe
)

JUDGE_GRADE_SEC = Histogram(
    "judge_grade_duration_seconds",
    "Judge grading duration in seconds"
)

JUDGE_INPUT_BYTES = Summary(
    "judge_input_bytes",
    "Bytes of input graded by Judge"
)


async def metrics_endpoint(request):
    """Serve Prometheus metrics."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Starlette app for mounting at /metrics
metrics_app = Starlette(routes=[Route("/", metrics_endpoint)])
