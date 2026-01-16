from pydantic import BaseModel
from typing import Any, Optional, List

class RunRequest(BaseModel):
    code: str
    language: str = "python"
    mode: str = "validate"  # validate|execute (execute later)

class ObjectiveResult(BaseModel):
    id: str
    ok: bool
    detail: Optional[str] = None
    line: Optional[int] = None

class RunResponse(BaseModel):
    passed: bool
    objective_results: List[ObjectiveResult]
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    ready_to_submit: bool
