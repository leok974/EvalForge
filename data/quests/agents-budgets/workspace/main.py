
class BudgetExceeded(Exception):
    pass

class BudgetGuardrail:
    def __init__(self, max_tool_calls: int, max_cost: int):
        raise NotImplementedError

    def charge_tool(self, cost: int) -> None:
        raise NotImplementedError

    @property
    def tool_calls(self) -> int:
        raise NotImplementedError

    @property
    def cost(self) -> int:
        raise NotImplementedError
