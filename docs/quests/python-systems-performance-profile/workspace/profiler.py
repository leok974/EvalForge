from __future__ import annotations

from typing import Any


def count_hits(items: list[str], queries: list[str]) -> int:
    """
    Return how many queries are present in items.
    Use a set for membership checks (deterministic).
    """
    # TODO
    return 0


def naive_comparisons(items: list[str], queries: list[str]) -> int:
    """
    Deterministic cost model for naive membership:
    comparisons += number of item==query checks performed.
    """
    # TODO
    return 0


def set_ops(items: list[str], queries: list[str]) -> int:
    """
    Deterministic cost model for set membership:
    build_ops = len(items)
    membership_ops = len(queries)
    set_ops = build_ops + membership_ops
    """
    # TODO
    return 0


def choose_strategy(naive_cost: int, set_cost: int) -> str:
    """
    Choose cheaper strategy. Tie-break: choose "set".
    """
    # TODO
    return "set"


def profile_membership_case(case: dict[str, Any]) -> dict:
    """
    Pure function: read case dict and return report dict.

    Required report shape:
    {
      "hits": int,
      "strategy": "naive"|"set",
      "cost": {"naive_comparisons": int, "set_ops": int}
    }
    """
    items = case.get("items", [])
    queries = case.get("queries", [])

    # Basic input validation (keep deterministic)
    if not isinstance(items, list) or not all(isinstance(x, str) for x in items):
        items = []
    if not isinstance(queries, list) or not all(isinstance(x, str) for x in queries):
        queries = []

    ncost = naive_comparisons(items, queries)
    scost = set_ops(items, queries)
    strategy = choose_strategy(ncost, scost)
    hits = count_hits(items, queries)

    return {
        "hits": hits,
        "strategy": strategy,
        "cost": {
            "naive_comparisons": ncost,
            "set_ops": scost,
        },
    }
