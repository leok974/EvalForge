
class BudgetExceeded(Exception):
    pass

class BudgetGuardrail:
    def __init__(self, max_tool_calls: int, max_cost: int):
        self._max_calls = int(max_tool_calls)
        self._max_cost = int(max_cost)
        self._calls = 0
        self._cost = 0

    def charge_tool(self, cost: int) -> None:
        self._calls += 1
        self._cost += int(cost)
        if self._calls > self._max_calls or self._cost > self._max_cost:
            raise BudgetExceeded("BUDGET_EXCEEDED")

    @property
    def tool_calls(self) -> int:
        return self._calls

    @property
    def cost(self) -> int:
        return self._cost
