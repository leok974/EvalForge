import ast
import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class ObjResult:
    id: str
    ok: bool
    detail: Optional[str] = None
    line: Optional[int] = None

def _find_main_func(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            return node
    return None

def validate_first_sparks_python(code: str) -> list[dict]:
    results: list[ObjResult] = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [
            {"id":"syntax", "ok": False, "detail": f"SyntaxError: {e.msg}", "line": e.lineno}
        ]

    main_fn = _find_main_func(tree)
    results.append(ObjResult(
        id="def_main", # Matching frontend ID
        ok=main_fn is not None,
        detail="Define a main() function",
        line=getattr(main_fn, "lineno", None) if main_fn else None
    ))

    # loop check
    has_for = False
    loop_line = None
    if main_fn:
        for n in ast.walk(main_fn):
            if isinstance(n, ast.For):
                has_for = True
                loop_line = getattr(n, "lineno", None)
                break
    results.append(ObjResult(
        id="loop",
        ok=has_for,
        detail="Countdown loop (T-minus)",
        line=loop_line
    ))

    # output check (cheap)
    liftoff_ok = re.search(r"liftoff", code, re.IGNORECASE) is not None
    # Try to find line number of print if possible
    liftoff_line = None
    if liftoff_ok and main_fn:
         for n in ast.walk(main_fn):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print":
                 # Check args
                 if n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str) and "liftoff" in n.args[0].value.lower():
                     liftoff_line = n.lineno
                     break
                 
    results.append(ObjResult(
        id="print",
        ok=liftoff_ok,
        detail="Confirm Liftoff",
        line=liftoff_line
    ))

    return [r.__dict__ for r in results]
