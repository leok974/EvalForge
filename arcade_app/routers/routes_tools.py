from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

# Setup Logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tools", tags=["tools"])

# --- Request Models ---

class ToolContextRequest(BaseModel):
    quest_slug: str
    attempt_id: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    failing_tests: Optional[List[str]] = None
    # Context
    user_skill_level: Optional[str] = "novice" 
    files: Optional[List[Dict[str, str]]] = Field(default=None, description="Current workspace files {path, sha/content}")

# --- Response Models (Strict JSON) ---

class ToolExplainResponse(BaseModel):
    summary: str
    what_happened: str
    why_it_failed: str
    next_steps: List[str]
    relevant_codex_refs: List[str]

class ToolDebugResponse(BaseModel):
    summary: str
    likely_root_causes: List[str]
    fix_plan: List[str]
    patch_proposal: Optional[Dict[str, Any]] = None # Diff format or structured patch

# --- Endpoints ---

@router.post("/explain", response_model=ToolExplainResponse)
async def explain_quest_status(req: ToolContextRequest):
    """
    Explain the current situation based on input context (stdout/stderr).
    Returns strict JSON: summary, what_happened, why_it_failed, next_steps, references.
    """
    logger.info(f"Tool (Explain) requested for {req.quest_slug}")
    
    # Mock Logic (LLM Placeholder)
    # Ideally this calls an LLM with the context.
    
    summary = "Analysis Complete"
    what_happened = "Your code ran but produced unexpected output."
    why_it_failed = "Execution logic appears correct, but validation failed."
    next_steps = ["Check the quest requirements."]
    refs = ["basics:python_syntax"]

    if req.stderr:
        summary = "Runtime Error Detected"
        what_happened = "The interpreter crashed with an exception."
        why_it_failed = f"Unhandled exception: {req.stderr.splitlines()[-1] if req.stderr else 'Unknown'}"
        next_steps = ["Read the error line number.", "Add try/except blocks.", "Print variable values before the crash."]
        refs = ["python:exceptions", "debugging:print"]
        
    elif req.failing_tests:
        count = len(req.failing_tests)
        summary = f"{count} Tests Failed"
        what_happened = "Your solution ran, but did not match the expected behavior."
        why_it_failed = "Logic error in output formatting or value calculation."
        next_steps = ["Review the first failing test case.", "Hardcode the expected input to verify logic.", "Check edge cases (0, empty list, etc)."]
        refs = ["testing:unit_tests", "python:assertions"]
    
    else:
        summary = "No Context Available"
        what_happened = "You haven't run the code yet."
        why_it_failed = "N/A"
        next_steps = ["Run your code to generate output.", "Check the terminal for print statements."]
        refs = []

    return ToolExplainResponse(
        summary=summary,
        what_happened=what_happened,
        why_it_failed=why_it_failed,
        next_steps=next_steps,
        relevant_codex_refs=refs
    )

@router.post("/debug", response_model=ToolDebugResponse)
async def debug_quest_failure(req: ToolContextRequest):
    """
    Propose a fix for the current failure.
    Returns: summary, root causes, fix plan, optional patch.
    """
    logger.info(f"Tool (Debug) requested for {req.quest_slug}")
    
    summary = "Ready to Debug"
    causes = ["Unknown"]
    plan = ["Run the code."]
    
    if req.stderr:
        summary = "Crash Analysis"
        causes = ["Syntax Error or Runtime Exception", "Undefined Variable"]
        plan = [
            "Identify the line triggering the error.",
            "Verify variable scope.",
            "Ensure imports are correct."
        ]
        
    elif req.failing_tests:
        summary = "Logic Defect Analysis"
        causes = ["Off-by-one error", "Incorrect return type", "Missing edge case handling"]
        plan = [
            "Isolate the failing function.",
            "Trace execution with sample inputs.",
            "Compare actual output vs expected."
        ]
        
    return ToolDebugResponse(
        summary=summary,
        likely_root_causes=causes,
        fix_plan=plan,
        patch_proposal=None
    )
