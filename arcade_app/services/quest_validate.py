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
    # Actionable error fields
    kind: Optional[str] = None  # "runtime" | "objective" | "tests" | "system"
    expected: Optional[str] = None
    actual: Optional[str] = None
    diff: Optional[str] = None

# ============================================================================
# VALIDATOR REGISTRY - Single Source of Truth
# ============================================================================

# Supported objective kinds
VALIDATORS = {
    "stdout_regex": "validate_stdout_regex",
    "stdout_exact": "validate_stdout_exact",  # Alias for stdout_regex
    "ast": "validate_ast",
    "source_regex": "validate_source_regex",
    "json_output": "validate_json_output",
    "stdout_json_eq": "validate_json_output",  # Alias
    "exit_code_zero": "validate_exit_code",
    "exit_code": "validate_exit_code",
    "not_timed_out": "validate_not_timed_out",
    "tests_pass": "validate_tests_pass",
}

# Per-kind rule requirements
# Empty list means no required fields, but at least one optional field expected
RULE_REQUIREMENTS = {
    "stdout_regex": ["pattern"],  # Optional: flags, description
    "stdout_exact": ["pattern"],  # Alias
    "ast": [],  # Requires at least one of: must_define_function, must_assign_variable, must_import
    "source_regex": ["pattern"],  # Optional: flags
    "json_output": ["expected"],
    "stdout_json_eq": ["expected"],
    "exit_code_zero": [],  # No required fields
    "exit_code": ["expected"],
    "not_timed_out": [],
    "tests_pass": [],  # Handled via pytest/node test output
}


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
    
    # Tier-1 Strictness Gate
    tier = getattr(quest_def, "tier", 0)
    if tier >= 1:
        if not objectives:
             return [ObjResult(id="config_missing", ok=False, detail="EF_OBJ_MISSING: Tier-1 quest has no objectives.").__dict__]
        
        # Check for placeholders
        for obj in objectives:
            t = (obj.get("title") or "").lower()
            k = (obj.get("kind") or "").lower()
            r = obj.get("rule", {})
            
            is_placeholder = False
            if "complete the assignment" in t: is_placeholder = True
            if k in ["", "placeholder", "tbd", "todo"]: is_placeholder = True
            if not r or r == "TODO": is_placeholder = True
            
            if is_placeholder:
                return [ObjResult(id="config_placeholder", ok=False, detail=f"EF_OBJ_PLACEHOLDER: Tier-1 quest has placeholder objective '{t}'.").__dict__]

    if not objectives and not getattr(quest_def, "sandbox", False) and not getattr(quest_def, "is_sandbox", False):
         # CRITICAL: Still return config error, but include stderr for debugging
         config_error = ObjResult(
             id="config_no_objectives",
             ok=False,
             kind="system",
             detail="Quest has no objectives configured",
             expected="At least 1 objective",
             actual="0 objectives found"
         )
         
         # Include stderr if execution produced errors (preserve actionable details)
         if stderr:
             runtime_error = ObjResult(
                 id="runtime_stderr",
                 ok=False,
                 kind="runtime",
                 detail=f"Stderr: {stderr[:500]}"  # Truncate but preserve
             )
             return [config_error.__dict__, runtime_error.__dict__]
         
         return [config_error.__dict__]
    
    def normalize_stdout(text: str) -> str:
        if not text: return ""
        text = text.replace("\r\n", "\n")
        return text.rstrip()

    stdout_clean = normalize_stdout(stdout).lower()
    stdout_normalized = normalize_stdout(stdout) # For case-sensitive checks if needed

    for obj in objectives:
        oid = obj.get("id") or "unknown_objective"
        kind = obj.get("kind")
        rule = obj.get("rule", {})
        title = obj.get("title") or obj.get("text") or oid
        
        # TRAINING-GRADE VALIDATION: Check objective schema
        if not kind or not rule:
            import json
            missing_fields = []
            if not kind: missing_fields.append("'kind'")
            if not rule: missing_fields.append("'rule'")
            
            return [ObjResult(
                id="config_invalid_objective",
                ok=False,
                kind="system",
                detail=f"Objective '{oid}' missing required fields: {', '.join(missing_fields)}",
                expected="Every objective must have 'kind' and 'rule' fields",
                actual=f"Objective structure: {json.dumps(obj, indent=2)}",
                diff=f"Missing fields: {', '.join(missing_fields)}\n\nFix in quest seed data or database."
            ).__dict__]
        
        res = ObjResult(id=oid, ok=False, detail=title)

        # Skip logic checks if syntax error exists (unless it's a syntax checking objective?)
        # For non-Python languages, syntax_error will be populated if treated as Python, so we ignore it here
        # and checking explicitly in AST block.
        # if syntax_error and kind not in ["stderr_empty"]:
        #      res.detail = f"SyntaxError: {syntax_error.msg}"
        #      res.line = syntax_error.lineno
        #      results.append(res)
        #      continue

        # Skip logic checks if runtime failed (and rule implies runtime dependency)
        # For now, regex/stdout checks imply runtime success
        if not runtime_ok and kind in ["stdout_regex", "exit_code_zero"]:
            res.detail = "Skipped due to runtime failure"
            results.append(res)
            continue
            
        try:
            if kind == "source_regex":
                # Language Agnostic: Regex on source code
                pattern = rule.get("pattern", "")
                if not pattern:
                    res.detail = "Invalid regex rule (empty)"
                else:
                    try:
                        if re.search(pattern, code, re.MULTILINE):
                            res.ok = True
                            res.detail = "Source code matches pattern"
                        else:
                            res.detail = "Source code missing required pattern"
                    except re.error as e:
                        res.detail = f"Invalid regex pattern: {str(e)}"

            elif kind == "ast":
                if not tree:
                    # AST parse failed or not attempted (non-python?)
                    res.detail = "AST checks require valid Python syntax" if syntax_error else "AST not supported for this language"
                    res.ok = False
                elif "must_define_function" in rule:
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
                            for target in n.targets:
                                if isinstance(target, ast.Name) and target.id == var_name:
                                    found = True
                                    res.line = n.lineno
                                    break
                    res.ok = found
                    
                    # Enhanced error reporting
                    if found:
                        res.detail = f"Variable '{var_name}' assigned"
                    else:
                        res.kind = "objective"
                        res.expected = f"Variable '{var_name}' must be assigned"
                        res.actual = f"Variable '{var_name}' not found in code"
                        res.detail = f"Assign variable '{var_name}'"
                        res.diff = f"Expected:\n  {var_name} = <value>\n\nActual:\n  Variable not assigned in code"
                    
            elif kind == "stdout_json_eq":
                import json
                expected = rule.get("expected")
                if expected is None:
                     res.detail = "Invalid rule (missing 'expected')"
                else:
                    try:
                        # Parse stdout as JSON
                        # normalize to single line if needed? json.loads handles whitespace
                        actual = json.loads(stdout or "")
                        
                        # Deep equality check
                        if actual == expected:
                            res.ok = True
                            res.detail = "JSON output matches expected data"
                        else:
                            res.detail = "JSON output mismatch"
                            # Optional: diff details?
                    except json.JSONDecodeError:
                        res.detail = "Output is not valid JSON"
                    except Exception as e:
                        res.detail = f"JSON validation error: {str(e)}"
                    
            elif kind == "stdout_regex" or kind == "stdout_exact": # Alias
                pattern = rule.get("pattern", "")
                if not pattern:
                    res.detail = "Invalid regex rule (empty pattern)"
                else:
                    # Parse flags
                    flags = rule.get("flags", "")
                    re_flags = 0
                    if "i" in flags.lower(): re_flags |= re.IGNORECASE
                    if "m" in flags.lower(): re_flags |= re.MULTILINE
                    if "s" in flags.lower(): re_flags |= re.DOTALL
                    
                    # Normalize stdout
                    txt = stdout_normalized or ""
                    
                    # Get human-readable description
                    expected_desc = rule.get("description") or title or f"Output matching pattern: {pattern[:50]}"
                    
                    try:
                        if re.search(pattern, txt, re_flags):
                             res.ok = True
                             res.detail = "Output matches expected pattern"
                        else:
                             res.ok = False
                             res.kind = "objective"
                             res.expected = expected_desc
                             res.actual = txt[:200] if txt else "(empty)"
                             res.detail = f"Expected {expected_desc}"
                             # Simple diff
                             res.diff = f"Expected:\n  {expected_desc}\nActual:\n  {res.actual}"
                    except re.error as e:
                         res.detail = f"Invalid regex pattern: {e}"

            elif kind == "exit_code_zero":
                res.ok = (exit_code == 0)
                res.detail = "Exit code 0"

            elif kind == "not_timed_out":
                res.ok = not timed_out
                res.detail = "Timely execution"
            
            elif kind == "tests_pass":
                import json
                
                # Check if we have valid test output
                if not stdout:
                     res.detail = "No test output received"
                     res.ok = False
                else:
                    summary = None
                    try:
                        # Try parsing full stdout first
                        summary = json.loads(stdout)
                    except json.JSONDecodeError:
                        # Try finding JSON blob in last line
                        lines = stdout.strip().split('\n')
                        if lines:
                            try:
                                summary = json.loads(lines[-1])
                            except:
                                pass
                    
                    if not summary or "passed" not in summary:
                        res.detail = "Could not parse test results"
                        res.ok = False
                    else:
                        failed_count = summary.get("failed", 0)
                        res.ok = (failed_count == 0)
                        
                        if res.ok:
                            res.detail = f"All {summary.get('total', 0)} tests passed"
                        else:
                            # Extract failure details
                            # Extract failure details
                            failures = summary.get("failures", [])
                            
                            # Redact hidden tests
                            grading = getattr(quest_def, "grading_json", {}) or {}
                            hidden_files = grading.get("hidden_tests", [])
                            # Normalize hidden files keys (e.g. "test_hidden.py" -> "test_hidden")
                            hidden_modules = [f.replace('.py', '') for f in hidden_files]
                            reveal = grading.get("reveal_hidden_failures", False)
                            
                            cleaned_failures = []
                            for f in failures:
                                name = f.get("name", "Unknown")
                                is_hidden = any(h in name for h in hidden_modules)
                                
                                if is_hidden and not reveal:
                                    cleaned_failures.append({"name": "Hidden Test", "message": "Failure details hidden."})
                                else:
                                    cleaned_failures.append(f)
                                    
                            # Re-summarize
                            fail_names = [f.get("name", "Unknown") for f in cleaned_failures]
                            # De-dupe "Hidden Test"
                            if "Hidden Test" in fail_names:
                                visible_fails = [n for n in fail_names if n != "Hidden Test"]
                                hidden_count = fail_names.count("Hidden Test")
                                fail_msg = f"Tests failed: {', '.join(visible_fails[:3])}"
                                if visible_fails: 
                                    fail_msg += ", "
                                fail_msg += f"{hidden_count} hidden test(s) failed."
                                res.detail = fail_msg
                            else:
                                res.detail = f"Tests failed: {', '.join(fail_names[:3])}"
                                if len(fail_names) > 3:
                                    res.detail += f" and {len(fail_names)-3} more"
                
        except Exception as e:
            res.detail = f"Validation Error: {str(e)}"

        results.append(res)

    return [r.__dict__ for r in results]

# Deprecated but kept for backward compat import if needed
def validate_first_sparks_with_runtime(code, stdout, stderr, exit_code=0, timed_out=False):
    # This should be mapped to new generic validator via config
    return [] 

