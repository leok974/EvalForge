from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class BossScore:
    """
    Result of evaluating a Boss submission.

    total: aggregate numeric score (0–~115)
    breakdown: per-dimension scores (async/model/structure/style)
    comments: human-readable feedback for the player
    """
    total: int
    breakdown: Dict[str, int]
    comments: List[str]


def score_reactor_core(submission: str) -> BossScore:
    """
    Score a submission for the 'Reactor Core Meltdown' boss.

    Expectations (Reactor World):
    - Non-blocking design (async def + asyncio.sleep).
    - Pydantic model ReactorStatus(BaseModel) with fields:
        core_id: str
        temperature: float
        status: str
    - fetch_reactor_status delegates to reactor_status rather than duplicating logic.
    - Reasonable style: no bare `except:`, docstring on reactor_status.

    Returns a BossScore; typical pass threshold ~80.
    """
    breakdown: Dict[str, int] = {
        "async": 0,
        "model": 0,
        "structure": 0,
        "style": 0,
    }
    comments: List[str] = []

    # --- Parse code ---------------------------------------------------------
    try:
        tree = ast.parse(submission)
    except SyntaxError as e:
        comments.append(f"Syntax error: {e}")
        return BossScore(total=0, breakdown=breakdown, comments=comments)

    # --- Helpers ------------------------------------------------------------
    def find_func(name: str):
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
                return node
        return None

    def class_named(name: str):
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == name:
                return node
        return None

    reactor_func = find_func("reactor_status")
    fetch_func = find_func("fetch_reactor_status")
    model_cls = class_named("ReactorStatus")

    # --- Async behaviour ----------------------------------------------------
    # 1) reactor_status should be async
    if isinstance(reactor_func, ast.AsyncFunctionDef):
        breakdown["async"] += 15
    else:
        comments.append("reactor_status should be defined as an async function.")

    # 2) Penalize blocking time.sleep; reward asyncio.sleep
    uses_time_sleep = False
    uses_asyncio_sleep = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                # time.sleep(...)
                if node.func.value.id == "time" and node.func.attr == "sleep":
                    uses_time_sleep = True
                # asyncio.sleep(...)
                if node.func.value.id == "asyncio" and node.func.attr == "sleep":
                    uses_asyncio_sleep = True

    if uses_time_sleep:
        comments.append("Blocking time.sleep detected; use asyncio.sleep for non-blocking I/O.")
    else:
        breakdown["async"] += 10  # "No blocking sleep" bonus

    if uses_asyncio_sleep:
        breakdown["async"] += 15
    else:
        comments.append("No asyncio.sleep found; simulate I/O asynchronously to avoid blocking.")

    # --- Pydantic model quality --------------------------------------------
    if model_cls:
        # Inheritance check
        inherits_basemodel = any(
            (isinstance(base, ast.Name) and base.id in ("BaseModel", "pydantic.BaseModel"))
            or (isinstance(base, ast.Attribute) and getattr(base, "attr", "") == "BaseModel")
            for base in model_cls.bases
        )

        if inherits_basemodel:
            breakdown["model"] += 20
        else:
            comments.append("ReactorStatus should inherit from BaseModel.")

        # Fields check
        field_names = {
            node.target.id
            for node in model_cls.body
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
        }

        expected = {"core_id", "temperature", "status"}
        missing = expected - field_names

        if not missing:
            breakdown["model"] += 15
        else:
            comments.append(
                f"ReactorStatus is missing required fields: {', '.join(sorted(missing))}."
            )
    else:
        comments.append("ReactorStatus Pydantic model not found.")

    # --- Structural design --------------------------------------------------
    # fetch_reactor_status should delegate to reactor_status
    if fetch_func and reactor_func:
        calls_reactor = False
        for node in ast.walk(fetch_func):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == "reactor_status":
                    calls_reactor = True
                    break

        if calls_reactor:
            breakdown["structure"] += 20
        else:
            comments.append(
                "fetch_reactor_status should delegate to reactor_status instead of duplicating logic."
            )
    else:
        if not fetch_func:
            comments.append("fetch_reactor_status function not found.")
        if not reactor_func:
            comments.append("reactor_status function not found.")

    # --- Style / hygiene ----------------------------------------------------
    has_bare_except = any(
        isinstance(node, ast.ExceptHandler) and node.type is None
        for node in ast.walk(tree)
    )
    if has_bare_except:
        comments.append("Avoid bare `except:`; catch specific exception types instead.")
    else:
        breakdown["style"] += 10

    # Simple docstring requirement for reactor_status
    if reactor_func and ast.get_docstring(reactor_func):
        breakdown["style"] += 10
    else:
        comments.append("Add a docstring to reactor_status explaining what it does.")

    total = sum(breakdown.values())
    return BossScore(total=total, breakdown=breakdown, comments=comments)
