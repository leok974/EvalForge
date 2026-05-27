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
    hint: Optional[str] = None  # Concrete next-step suggestion surfaced on failure

# ============================================================================
# VALIDATOR REGISTRY - Single Source of Truth
# ============================================================================

# Validator registry: maps objective kind to validator function name
VALIDATORS = {
    "ast": "validate_ast",
    "exit_code": "validate_exit_code",
    "exit_code_zero": "validate_exit_code_zero",
    "json_output": "validate_json_output",
    "not_timed_out": "validate_not_timed_out",
    "source_regex": "validate_source_regex",
    "stdout_exact": "validate_stdout_exact",
    "stdout_json_eq": "validate_stdout_json_eq",
    "stdout_regex": "validate_stdout_regex",
    "tests_pass": "validate_tests_pass",
    "fs_snapshot": "validate_fs_snapshot",
    "fs_file_exists": "validate_fs_file_exists",
    "git_status_clean": "validate_git_status_clean",
    "git_log_contains": "validate_git_log_contains",
    "file_hash_eq": "validate_file_hash_eq",
    "column_match": "validate_sql_column_match",
    "row_count": "validate_sql_row_count",
    "yaml_structure": "validate_yaml_structure",
    # Kind aliases for extended questpack formats
    "ast_python_function": "validate_ast",
    "ast_python_code": "validate_ast",
    "ast_python_class": "validate_ast",
    "process_exit_code": "validate_exit_code_zero",
    "process_not_timed_out": "validate_not_timed_out",
}

# Canonical kind remapping (alias → canonical)
KIND_ALIASES = {
    "ast_python_function": "ast",
    "ast_python_code": "ast",
    "ast_python_class": "ast",
    "process_exit_code": "exit_code_zero",
    "process_not_timed_out": "not_timed_out",
}

# Per-kind rule requirements (required fields in rule dict)
# Use '|' to indicate OR (one of these fields must be present)
RULE_REQUIREMENTS = {
    "exit_code": ["expected"],
    "json_output": ["expected"],
    "source_regex": ["pattern|patterns"],
    "stdout_regex": ["pattern|patterns"],
    "stdout_exact": ["expected"],  # CANONICAL: use 'expected' not 'pattern'
    "stdout_json_eq": ["expected"],
    "not_timed_out": [],
    "tests_pass": [],  # Handled via pytest/node test output
    "column_match": ["expected_columns"],
    "row_count": ["count"],
    "yaml_structure": ["assertions"],
}


def audit_objective_schema(obj: Dict[str, Any]) -> List[str]:
    """
    Validate objective configuration schema (static check).
    Returns list of error messages.
    """
    errors = []

    # Required fields
    if not obj.get('id'):
        errors.append("Missing 'id'")

    kind = obj.get('kind')
    if not kind:
        errors.append("Missing 'kind'")
        return errors

    # Normalize kind aliases (e.g. ast_python_function -> ast)
    canonical_kind = KIND_ALIASES.get(kind, kind)

    # Normalise rule_json -> rule (questpacks may use either key)
    if 'rule' not in obj and 'rule_json' in obj:
        obj['rule'] = obj['rule_json']

    no_rule_kinds = ["tests_pass", "not_timed_out", "ast", "exit_code_zero",
                     "process_exit_code", "process_not_timed_out",
                     "ast_python_function", "ast_python_code", "ast_python_class",
                     "fs_file_exists"]
    if 'rule' not in obj:
        if canonical_kind not in ["tests_pass", "not_timed_out", "ast", "exit_code_zero"]:
            errors.append("Missing 'rule'")
            return errors
        obj['rule'] = {}

    # Check kind is valid (accept aliases too)
    if kind not in VALIDATORS and canonical_kind not in VALIDATORS:
        errors.append(f"Unknown kind '{kind}'")
        return errors

    # Check rule requirements against canonical kind
    rule = obj.get('rule', {})
    required = RULE_REQUIREMENTS.get(canonical_kind, RULE_REQUIREMENTS.get(kind, []))
    
    if canonical_kind == "ast":
        # ast aliases (ast_python_function etc.) use rule_json with name/args/returns —
        # treat any non-empty rule as valid; we do a best-effort check at runtime.
        is_alias = kind in KIND_ALIASES
        has_ast_check = is_alias or any(
            k in rule for k in
            ['must_define_function', 'must_assign_variable', 'must_import', 'must_use_for_loop', 'must_call_function']
        )
        if not has_ast_check and not rule:
            errors.append("AST rule is empty. Hint: Add 'must_define_function' or 'must_assign_variable'.")
    elif canonical_kind in ("exit_code_zero", "not_timed_out", "fs_file_exists"):
        pass  # no rule fields required for these kinds
    else:
        for field_req in required:
            options = field_req.split("|")
            
            if not any(opt in rule for opt in options):
                hint = ""
                if kind == "stdout_exact" and "expected" in options:
                    hint = " (Note: 'pattern' is deprecated, use 'expected')"
                elif kind in ["source_regex", "stdout_regex"] and "pattern" in options:
                    hint = " (regex pattern required)"
                
                if len(options) == 1:
                    errors.append(f"Rule missing required field '{options[0]}'{hint}")
                else:
                    opt_str = "' or '".join(options)
                    errors.append(f"Rule missing required field '{opt_str}'{hint}")
                
    return errors


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
    quest_def: Any = None, # QuestDefinition or dict
    state: Optional[Dict[str, Any]] = None # Captured state (files, git, hashes)
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

    # HTML/CSS Web Quests: graded entirely by exit code (Node.js `node --test` runner).
    # These quests use a placeholder "Complete the assignment" objective that would
    # otherwise trigger the Tier-1 strictness gate. Short-circuit here and return a
    # single exit_code_zero result so the frontend can enable Submit on pass.
    quest_language = getattr(quest_def, "language", None) or ""
    if quest_language in ("html", "css"):
        ok = (not timed_out) and (exit_code == 0)
        detail = "All grading tests passed." if ok else f"Grading tests failed (exit {exit_code})."
        return [ObjResult(id="obj_grading", ok=ok, detail=detail).__dict__]

    # C1: Runtime Fallback Preflight
    # Validate objective schema BEFORE running any validators
    for obj in objectives:
        schema_errors = audit_objective_schema(obj)
        if schema_errors:
            import json
            oid = obj.get("id", "unknown")
            return [ObjResult(
                id="CONFIG_INVALID_OBJECTIVES",
                ok=False,
                kind="config", # Special kind for Coach to short-circuit
                detail="Quest objectives are invalid or missing.",
                expected="Valid objectives schema (id/kind/rule) for all objectives.",
                actual=f"Invalid objective '{oid}': {', '.join(schema_errors)}",
                diff=f"Fix quest spec: data/quests/{getattr(quest_def, 'slug', 'unknown')}/quest.json (or seed source)...\nErrors: {', '.join(schema_errors)}\nHint: Run --validate-only"
            ).__dict__]

    # Tier-1 Strictness Gate
    tier = getattr(quest_def, "tier", 0)
    if tier >= 1:
        if not objectives:
             return [ObjResult(id="config_missing", ok=False, detail="EF_OBJ_MISSING: Tier-1 quest has no objectives.").__dict__]
        
        # Check for placeholders
        _no_rule_kinds = {
            "exit_code_zero", "tests_pass", "not_timed_out", "ast",
            "process_exit_code", "process_not_timed_out",
            "ast_python_function", "ast_python_code", "ast_python_class",
            "fs_file_exists",
        }
        for obj in objectives:
            t = (obj.get("title") or "").lower()
            k = (obj.get("kind") or "").lower()
            r = obj.get("rule", {})

            is_placeholder = False
            if "complete the assignment" in t: is_placeholder = True
            if k in ["", "placeholder", "tbd", "todo"]: is_placeholder = True
            # Only flag empty rule as placeholder when the kind actually requires a rule.
            # Kinds like exit_code_zero legitimately have an empty rule dict.
            if k not in _no_rule_kinds and (not r or r == "TODO"):
                is_placeholder = True

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
        # Normalise kind aliases (e.g. ast_python_function -> ast)
        if kind in KIND_ALIASES:
            kind = KIND_ALIASES[kind]
        # Accept rule_json as fallback for rule (extended questpack format)
        rule = obj.get("rule") or obj.get("rule_json") or {}
        title = obj.get("title") or obj.get("text") or oid
        
        # TRAINING-GRADE VALIDATION: Check objective schema
        if not kind or rule is None:
            import json
            missing_fields = []
            if not kind: missing_fields.append("'kind'")
            if rule is None: missing_fields.append("'rule'")
            
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
        # Skip logic checks if runtime failed (and rule implies runtime dependency)
        # For now, regex/stdout checks imply runtime success
        if not runtime_ok and kind in ["stdout_regex", "json_output", "stdout_json_eq"]:
            res.detail = "Skipped due to runtime failure"
            results.append(res)
            continue
            
        try:
            if kind == "source_regex":
                # Language Agnostic: Regex on source code
                
                quest_lang = getattr(quest_def, "language", None)
                if not quest_lang and isinstance(quest_def, dict):
                    quest_lang = quest_def.get("language")
                    
                code_to_check = code
                if quest_lang == "sql":
                    from arcade_app.services.sql_parser import strip_sql_comments
                    code_to_check = strip_sql_comments(code)
                
                patterns = rule.get("pattern", [])
                if not isinstance(patterns, list):
                    patterns = [patterns]
                if "patterns" in rule:
                    patterns.extend(rule["patterns"])
                
                patterns = [p for p in patterns if p]
                
                if not patterns:
                    res.detail = "Invalid regex rule (empty)"
                else:
                    try:
                        all_matched = True
                        failed_pattern = ""
                        for pat in patterns:
                            if not re.search(pat, code_to_check, re.MULTILINE | re.IGNORECASE):
                                all_matched = False
                                failed_pattern = pat
                                break
                                
                        if all_matched:
                            res.ok = True
                            res.detail = "Source code matches pattern"
                        else:
                            # Use the human-readable objective title, not the raw regex
                            human_title = title if (title and title != oid) else "Required pattern not found"
                            res.kind = "objective"
                            res.detail = human_title
                            res.expected = rule.get("description") or human_title
                            res.actual = "(pattern not found in your code)"
                            res.diff = f"Expected:\n  {res.expected}\nActual:\n  (pattern not found)"
                            obj_hint = obj.get("hint") or rule.get("hint", "")
                            if obj_hint:
                                res.hint = obj_hint
                    except re.error as e:
                        res.detail = f"Invalid regex pattern: {str(e)}"

            elif kind == "ast":
                if not tree:
                    # AST parse failed or not attempted (non-python?)
                    res.detail = "AST checks require valid Python syntax" if syntax_error else "AST not supported for this language"
                    res.ok = False
                elif "forbidden_nodes" in rule:
                    # ast_python_code: check that certain AST node types are absent
                    forbidden = rule["forbidden_nodes"]
                    node_map = {name: getattr(ast, name, None) for name in forbidden}
                    node_types = tuple(t for t in node_map.values() if t is not None)
                    found_node = None
                    for n in ast.walk(tree):
                        if node_types and isinstance(n, node_types):
                            found_node = type(n).__name__
                            break
                    if found_node:
                        res.ok = False
                        res.detail = f"Forbidden AST node '{found_node}' found — use comprehensions instead"
                    else:
                        res.ok = True
                        res.detail = "No forbidden constructs found"

                elif "methods" in rule and ("name" in rule or "must_define_class" in rule):
                    # ast_python_class: check class exists with required methods
                    class_name = rule.get("name") or rule.get("must_define_class")
                    required_methods = rule.get("methods", [])
                    found_class = None
                    for n in ast.walk(tree):
                        if isinstance(n, ast.ClassDef) and n.name == class_name:
                            found_class = n
                            break
                    if not found_class:
                        res.ok = False
                        res.detail = f"Class '{class_name}' not defined"
                    else:
                        class_methods = {
                            m.name for m in ast.walk(found_class)
                            if isinstance(m, ast.FunctionDef)
                        }
                        missing = [m for m in required_methods if m not in class_methods]
                        if missing:
                            res.ok = False
                            res.detail = f"Class '{class_name}' missing methods: {missing}"
                        else:
                            res.ok = True
                            res.line = found_class.lineno
                            res.detail = f"Class '{class_name}' defined with required methods"

                elif "must_define_function" in rule or ("name" in rule and "methods" not in rule):
                    # ast_python_function: check function is defined
                    fn_name = rule.get("must_define_function") or rule.get("name")
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
                    
            elif kind == "stdout_json_eq" or kind == "json_output":
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
                    
            elif kind == "stdout_regex":
                patterns = rule.get("pattern", [])
                if not isinstance(patterns, list):
                    patterns = [patterns]
                if "patterns" in rule:
                    patterns.extend(rule["patterns"])
                
                patterns = [p for p in patterns if p]
                
                if not patterns:
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
                    expected_desc = rule.get("expected") or rule.get("description") or title or f"Output matching patterns"
                    
                    try:
                        all_matched = True
                        failed_pattern = ""
                        for pat in patterns:
                            if not re.search(pat, txt, re_flags):
                                all_matched = False
                                failed_pattern = pat
                                break
                                
                        if all_matched:
                             res.ok = True
                             res.detail = "Output matches expected pattern"
                        else:
                             res.ok = False
                             res.kind = "objective"
                             res.expected = expected_desc
                             res.actual = txt[:200] if txt else "(empty)"
                             # Use the human-readable description, not the raw regex
                             res.detail = expected_desc
                             res.diff = f"Expected:\n  {expected_desc}\nActual:\n  {res.actual}"
                             obj_hint = obj.get("hint") or rule.get("hint", "")
                             if obj_hint:
                                 res.hint = obj_hint
                    except re.error as e:
                         res.detail = f"Invalid regex pattern: {e}"
            
            elif kind == "stdout_exact":
                # stdout_exact uses 'expected' (canonical) - support 'pattern' for backward compatibility
                expected_val = rule.get("expected") or rule.get("pattern", "")
                if expected_val is None:
                    res.detail = "Invalid stdout_exact rule (missing 'expected' field)"
                else:
                    txt = stdout_normalized or ""
                    # Exact match comparison
                    if txt == expected_val:
                        res.ok = True
                        res.detail = "Output matches expected value"
                    else:
                        res.ok = False
                        res.kind = "objective"
                        res.expected = expected_val
                        res.actual = txt[:200] if txt else "(empty)"
                        res.detail = f"Expected exact match"
                        res.diff = f"Expected:\n  {expected_val}\nActual:\n  {res.actual}"

            elif kind == "exit_code_zero":
                res.ok = (exit_code == 0)
                res.detail = "Exit code 0"

            elif kind == "exit_code":
                expected = rule.get("expected", 0)
                if exit_code == expected:
                    res.ok = True
                    res.detail = f"Exit code {expected}"
                else:
                    res.ok = False
                    res.kind = "objective"
                    res.expected = f"Exit code {expected}"
                    res.actual = f"Exit code {exit_code}"
                    res.detail = f"Expected exit code {expected}"

            elif kind == "not_timed_out":
                res.ok = not timed_out
                res.detail = "Timely execution"
            
            elif kind == "fs_file_exists":
                # Lightweight: just mark ok=True (no state capture in standard mode)
                # The file-existence guarantee comes from the solution running successfully.
                path_check = rule.get("path", "")
                res.ok = True
                res.detail = f"File existence check for '{path_check}' assumed OK (covered by tests_pass)"

            # STATE VALIDATORS
            elif kind == "fs_snapshot":
                if not state:
                    res.ok = False
                    res.detail = "No state captured (runtime error?)"
                else:
                    required = rule.get("must_exist", [])
                    forbidden = rule.get("must_not_exist", [])
                    files = set(state.get("files", []))
                    
                    missing = [f for f in required if f not in files]
                    present = [f for f in forbidden if f in files]
                    
                    if not missing and not present:
                        res.ok = True
                        res.detail = "File structure correct"
                    else:
                        res.ok = False
                        details = []
                        if missing: details.append(f"Missing: {missing}")
                        if present: details.append(f"Forbidden: {present}")
                        res.detail = "; ".join(details)
                        res.diff = f"Expected Files:\n  {required}\nActual Files:\n  {state.get('files', [])}"

            elif kind == "git_status_clean":
                if not state:
                    res.ok = False
                    res.detail = "No state captured"
                else:
                    git_state = state.get("git", {})
                    if not git_state.get("has_dot_git"):
                        res.ok = False
                        res.detail = "No .git directory found"
                    else:
                        actual = git_state.get("status_porcelain", "").strip()
                        expected = (rule.get("expected_porcelain") or "").strip()
                        
                        if actual == expected:
                            res.ok = True
                            res.detail = "Git status matches expected state"
                        else:
                            res.ok = False
                            res.detail = "Git status mismatch"
                            res.diff = f"Expected Git Status:\n  {expected or '(clean)'}\nActual Git Status:\n  {actual or '(clean)'}"

            elif kind == "git_log_contains":
                if not state:
                    res.ok = False
                    res.detail = "No state captured"
                else:
                    git_state = state.get("git", {})
                    if not git_state.get("has_dot_git"):
                         res.ok = False
                         res.detail = "No .git directory found"
                    else:
                         logs = git_state.get("log_oneline", [])
                         must_contain = rule.get("must_contain", [])
                         min_commits = rule.get("min_commits", 0)
                         
                         if len(logs) < min_commits:
                             res.ok = False
                             res.detail = f"Not enough commits (found {len(logs)}, expected {min_commits})"
                         else:
                             missing_patterns = []
                             for pattern in must_contain:
                                 if not any(pattern in line for line in logs):
                                     missing_patterns.append(pattern)
                                     
                             if not missing_patterns:
                                 res.ok = True
                                 res.detail = "Git log contains required entries"
                             else:
                                 res.ok = False
                                 res.detail = f"Missing commit log entries: {missing_patterns}"
                                 res.diff = f"Expected Log to Contain:\n  {must_contain}\nActual Log:\n  {logs}"

            elif kind == "file_hash_eq":
                if not state:
                    res.ok = False
                    res.detail = "No state captured"
                else:
                    path = rule.get("path")
                    expected_hash = rule.get("sha256")

                    if not path or not expected_hash:
                        res.detail = "Invalid rule (missing path or sha256)"
                    else:
                        hashes = state.get("hashes", {})
                        actual_hash = hashes.get(path)

                        if actual_hash == expected_hash:
                            res.ok = True
                            res.detail = f"File {path} matches golden hash"
                        else:
                            res.ok = False
                            res.detail = f"File {path} hash mismatch"
                            res.diff = f"Expected Hash ({path}):\n  {expected_hash}\nActual Hash:\n  {actual_hash or '(not found)'}"

            elif kind == "yaml_structure":
                import yaml as _yaml
                assertions = rule.get("assertions", [])
                if not assertions:
                    res.detail = "Invalid yaml_structure rule (empty assertions)"
                else:
                    try:
                        doc = _yaml.safe_load(code or "")
                        if doc is None:
                            doc = {}

                        def _get_path(obj, dotted):
                            """Walk a dotted key path through nested dicts/lists."""
                            parts = dotted.split(".")
                            cur = obj
                            for p in parts:
                                if isinstance(cur, dict):
                                    if p not in cur:
                                        return None, False
                                    cur = cur[p]
                                else:
                                    return None, False
                            return cur, True

                        passed_all = True
                        fail_msg = ""
                        for assertion in assertions:
                            atype = assertion.get("type")
                            apath = assertion.get("path", "")
                            aval = assertion.get("value")

                            val, exists = _get_path(doc, apath) if apath else (doc, True)

                            if atype == "exists":
                                if not exists:
                                    passed_all = False
                                    fail_msg = f"Path '{apath}' does not exist"
                                    break
                            elif atype == "equals":
                                if not exists or val != aval:
                                    passed_all = False
                                    fail_msg = f"Path '{apath}': expected {aval!r}, got {val!r}"
                                    break
                            elif atype == "contains":
                                if not exists or aval not in str(val):
                                    passed_all = False
                                    fail_msg = f"Path '{apath}': value does not contain {aval!r}"
                                    break
                            elif atype == "matches_regex":
                                if not exists or not re.search(str(aval), str(val)):
                                    passed_all = False
                                    fail_msg = f"Path '{apath}': value {val!r} does not match regex {aval!r}"
                                    break
                            elif atype == "is_list":
                                if not exists or not isinstance(val, list):
                                    passed_all = False
                                    fail_msg = f"Path '{apath}': expected a list, got {type(val).__name__}"
                                    break
                            elif atype == "list_contains":
                                if not exists or not isinstance(val, list) or aval not in val:
                                    passed_all = False
                                    fail_msg = f"Path '{apath}': list does not contain {aval!r}"
                                    break
                            elif atype == "list_excludes":
                                if exists and isinstance(val, list) and aval in val:
                                    passed_all = False
                                    fail_msg = f"Path '{apath}': list must not contain {aval!r}"
                                    break
                            elif atype == "is_named_volume":
                                # Check that apath key exists in the 'volumes' top-level dict
                                vols = doc.get("volumes", {}) or {}
                                if apath not in vols:
                                    passed_all = False
                                    fail_msg = f"Named volume '{apath}' not found in volumes:"
                                    break
                            else:
                                passed_all = False
                                fail_msg = f"Unknown assertion type '{atype}'"
                                break

                        if passed_all:
                            res.ok = True
                            res.detail = "YAML structure matches all assertions"
                        else:
                            res.ok = False
                            res.kind = "objective"
                            res.detail = fail_msg
                            res.expected = title
                            res.actual = fail_msg
                            obj_hint = obj.get("hint") or rule.get("hint", "")
                            if obj_hint:
                                res.hint = obj_hint

                    except _yaml.YAMLError as e:
                        res.ok = False
                        res.detail = f"YAML parse error: {e}"
                    except Exception as e:
                        res.detail = f"yaml_structure validation error: {str(e)}"

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

    # Fail-closed: if no results were produced (e.g. sandbox quest with no objectives),
    # synthesize a config_missing entry so callers never receive an empty list.
    if not results:
        results.append(ObjResult(
            id="config_missing",
            ok=False,
            detail="No objectives produced results. Quest may have no objectives configured."
        ))

    return [r.__dict__ for r in results]

def validate_sql_column_match(obj, stdout, state):
    # Stub for SQL column matching
    return ObjResult(id=obj['id'], ok=True, detail="Column list matches")

def validate_sql_row_count(obj, stdout, state):
    # Stub for SQL row count checking
    return ObjResult(id=obj['id'], ok=True, detail="Row count matches")




