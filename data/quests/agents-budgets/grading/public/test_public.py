import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa

def test_budget_guardrail_limits():
    b = main.BudgetGuardrail(max_tool_calls=2, max_cost=5)
    b.charge_tool(3)
    assert b.tool_calls == 1 and b.cost == 3

    try:
        b.charge_tool(3)  # cost becomes 6 -> exceeds
        assert False
    except main.BudgetExceeded as e:
        assert str(e) == "BUDGET_EXCEEDED"
