from pydantic import BaseModel
from typing import Any, Optional, List

class RunRequest(BaseModel):
    code: str
    language: str = "python"
    mode: str = "validate"  # validate|execute (execute later)
    entrypoint: Optional[str] = None
    workspace: Optional[List[Any]] = None # List of {path, content}
    idempotency_key: Optional[str] = None  # Phase 8.x PR 3: Idempotency
    run_target_path: Optional[str] = None  # Optional target file to run (e.g. example.sql)

class ObjectiveResult(BaseModel):
    id: str
    ok: bool
    detail: Optional[str] = None
    line: Optional[int] = None

    # Actionable error fields
    kind: Optional[str] = None  # "runtime" | "objective" | "tests" | "system"
    expected: Optional[str] = None
    actual: Optional[str] = None
    diff: Optional[str] = None

    # Phase 7.1.2: Success Debrief
    debrief: Optional[dict] = None

class Diagnostic(BaseModel):
    path: str
    line: int
    column: int = 1
    severity: str = "error"
    kind: str = "runtime" # syntax, runtime, test, runner, sql_entrypoint
    message: str
    runner: Optional[str] = None # For runner identity diagnostics

class QuickFix(BaseModel):
    id: str
    kind: str  # apply_patch | copy_snippet | navigate
    title: str
    why: str
    severity: str = "safe" # safe | suggestion
    locator: Optional[dict] = None # {path, line, column}
    patch: Optional[dict] = None # {path, replacement_full_content} - keeping it simple for now
    snippet: Optional[str] = None # for copy_snippet

class RunResponse(BaseModel):
    passed: bool
    objective_results: List[ObjectiveResult]
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    ready_to_submit: bool
    
    # Artifact / History Fields
    attempt_id: str
    run_number: int
    duration_ms: int
    exit_code: Optional[int] = None
    timed_out: bool = False
    
    # Stuck Detector
    coach: Optional[dict] = None
    
    # Phase 7.1.2: Success Debrief
    debrief: Optional[dict] = None
    
    # Phase 7.1.3: Inline Diagnostics
    diagnostics: List[Diagnostic] = []

    # Phase 7.1.4: Quick Fixes
    quick_fixes: List[QuickFix] = []

    # Phase R: SQL Execution Tracing
    artifacts: Optional[dict] = None
