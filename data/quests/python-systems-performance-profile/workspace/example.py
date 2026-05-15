def count_hits(items: list[str], queries: list[str]) -> int:
    item_set = set(items)
    return sum(1 for q in queries if q in item_set)


def naive_comparisons(items: list[str], queries: list[str]) -> int:
    return len(items) * len(queries)


def set_ops(items: list[str], queries: list[str]) -> int:
    return len(items) + len(queries)


def choose_strategy(naive_cost: int, set_cost: int) -> str:
    return "naive" if naive_cost < set_cost else "set"


def profile_membership_case(case: dict) -> dict:
    items = [x for x in case.get("items", []) if isinstance(x, str)]
    queries = [x for x in case.get("queries", []) if isinstance(x, str)]
    ncost = naive_comparisons(items, queries)
    scost = set_ops(items, queries)
    return {
        "hits": count_hits(items, queries),
        "strategy": choose_strategy(ncost, scost),
        "cost": {"naive_comparisons": ncost, "set_ops": scost},
    }
