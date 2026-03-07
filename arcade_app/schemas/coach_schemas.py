
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal, Dict, Any

class WorkspaceFile(BaseModel):
    path: str
    content: str

class CoachRequest(BaseModel):
    mode: Literal["explain", "debug", "auto"] = "auto"
    world: str
    quest_slug: str
    student_mode: bool
    runner_result: Optional[Dict[str, Any]] = None
    failing_tests_text: Optional[str] = None
    terminal_output_text: Optional[str] = None
    selected_paths: Optional[List[str]] = None
    workspace_files: List[WorkspaceFile] = []
    attempt_id: Optional[str] = None
    quest_id: Optional[str] = None
    # Context anchoring (prevents model picking wrong file)
    entrypoint_path: Optional[str] = None   # e.g. "task.sql" or "task.py"
    language: Optional[str] = None           # e.g. "sql", "python"
    run_passed: Optional[bool] = None        # True = last run was a clean pass
    
    @field_validator('workspace_files')
    @classmethod
    def no_solutions_in_payload(cls, files: List[WorkspaceFile]):
        """Guardrail: Ensure no solution files are incorrectly submitted."""
        clean = []
        for f in files:
            if "grading/solutions" in f.path or "grading/private" in f.path:
                continue # Silently drop solution files
            clean.append(f)
        return clean

class Hypothesis(BaseModel):
    title: str
    evidence: List[str]

class NextStep(BaseModel):
    label: str
    action: Literal["edit", "run", "read", "think"]
    target: Optional[str] = None

class SafetyAssessment(BaseModel):
    solution_leak_risk: Literal["low", "medium", "high", "blocked"]
    blocked: bool

class UnifiedDiff(BaseModel):
    unified_diff: str

class PrimaryError(BaseModel):
    code: str
    message: str

class CoachResponse(BaseModel):
    mode: Literal["explain", "debug"]
    summary_md: str
    hypotheses: List[Hypothesis]
    next_steps: List[NextStep]
    patch: Optional[UnifiedDiff] = None
    confidence: float
    safety: SafetyAssessment
    primary_error: Optional[PrimaryError] = None
    evidence: List[str] = Field(default_factory=list, description="Exact log lines carrying the failure signal")
    failure_class: Optional[str] = None
