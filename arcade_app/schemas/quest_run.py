from pydantic import BaseModel
from typing import Any, Optional, List

class RunRequest(BaseModel):
    code: str
    language: str = "python"
    mode: str = "validate"  # validate|execute (execute later)
    entrypoint: Optional[str] = None
    workspace: Optional[List[Any]] = None # List of {path, content}

class ObjectiveResult(BaseModel):
    id: str
    ok: bool
    detail: Optional[str] = None
    line: Optional[int] = None

    # Phase 7.1.2: Success Debrief
    debrief: Optional[dict] = None

class Diagnostic(BaseModel):
    path: str
    line: int
    column: int = 1
    severity: str = "error"
    kind: str = "runtime" # syntax, runtime, test
    message: str

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
