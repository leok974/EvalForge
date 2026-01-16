import ast
import re
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

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

def validate_quest_attempt(
    code: str, 
    stdout: Optional[str], 
    stderr: Optional[str], 
    exit_code: int = 0, 
    timed_out: bool = False,
    quest_def: Any = None # QuestDefinition or dict
) -> List[Dict]:
    """
    Generic validator engine.
    """
    results: List[ObjResult] = []
    
    # 1. Parse AST once if needed
    tree = None
    syntax_error = None
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        syntax_error = e

    # 2. Runtime Rules
    rules = getattr(quest_def, "runtime_rules_json", {}) or {}
    
    # Defaults
    require_zero = rules.get("require_exit_code_zero", True)
    require_no_timeout = rules.get("require_no_timeout", True)
    # timeout_ms handled by runner, we just see timed_out result
    
    runtime_ok = True
    runtime_fail_reason = ""

    if require_no_timeout and timed_out:
        runtime_ok = False
        runtime_fail_reason = "Execution timed out"
    elif require_zero and exit_code != 0:
        runtime_ok = False
        runtime_fail_reason = f"Execution failed (Exit Code: {exit_code})"
        
    if rules.get("enabled", False):
        results.append(ObjResult(id="runtime", ok=runtime_ok, detail=runtime_fail_reason or "Execution successful"))

    # 3. Process Objectives
    objectives = getattr(quest_def, "objectives_json", []) or []
    
    stdout_clean = (stdout or "").lower()

    for obj in objectives:
        oid = obj.get("id")
        kind = obj.get("kind")
        rule = obj.get("rule", {})
        title = obj.get("title", oid)
        
        res = ObjResult(id=oid, ok=False, detail=title)

        # Skip logic checks if syntax error exists (unless it's a syntax checking objective?)
        if syntax_error and kind not in ["stderr_empty"]:
             res.detail = f"SyntaxError: {syntax_error.msg}"
             res.line = syntax_error.lineno
             results.append(res)
             continue

        # Skip logic checks if runtime failed (and rule implies runtime dependency)
        # For now, regex/stdout checks imply runtime success
        if not runtime_ok and kind in ["stdout_regex", "exit_code_zero"]:
            res.detail = "Skipped due to runtime failure"
            results.append(res)
            continue
            
        try:
            if kind == "ast":
                if "must_define_function" in rule:
                    fn_name = rule["must_define_function"]
                    found = False
                    for n in ast.walk(tree):
                        if isinstance(n, ast.FunctionDef) and n.name == fn_name:
                            found = True
                            res.line = n.lineno
                            break
                    res.ok = found
                    res.detail = f"Define function '{fn_name}'" if not found else "Function defined"

                elif "must_assign_variable" in rule:
                    var_name = rule["must_assign_variable"]
                    found = False
                    for n in ast.walk(tree):
                        if isinstance(n, ast.Assign):
                            for t in n.targets:
                                if isinstance(t, ast.Name) and t.id == var_name:
                                    found = True
                                    res.line = n.lineno
                                    break
                    res.ok = found
                    res.detail = f"Assign variable '{var_name}'" if not found else "Variable assigned"
                    
            elif kind == "stdout_regex":
                pattern = rule.get("pattern", "")
                if re.search(pattern, stdout or "", re.IGNORECASE | re.MULTILINE):
                    res.ok = True
                    res.detail = "Output matches pattern"
                else:
                    res.detail = "Output mismatch"

            elif kind == "exit_code_zero":
                res.ok = (exit_code == 0)
                res.detail = "Exit code 0"

            elif kind == "not_timed_out":
                res.ok = not timed_out
                res.detail = "Timely execution"
                
        except Exception as e:
            res.detail = f"Validation Error: {str(e)}"

        results.append(res)

    return [r.__dict__ for r in results]

# Deprecated but kept for backward compat import if needed
def validate_first_sparks_with_runtime(code, stdout, stderr, exit_code=0, timed_out=False):
    # This should be mapped to new generic validator via config
    return [] 

