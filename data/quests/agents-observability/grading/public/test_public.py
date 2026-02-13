import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa

def test_auditlog_span_order_and_id():
    log = main.AuditLog()
    with log.span("exec") as sid:
        log.event("tool_call", tool="add")

    events = log.to_json()
    assert events[0]["name"] == "span_start"
    assert events[1]["name"] == "tool_call"
    assert events[2]["name"] == "span_end"
    assert events[0]["span_id"] == sid
    assert events[2]["span_id"] == sid
