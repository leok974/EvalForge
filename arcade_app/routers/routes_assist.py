from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

# Setup Logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/assist", tags=["assist"])

# --- Request Models ---

class AssistGenericRequest(BaseModel):
    quest_slug: str
    attempt_id: Optional[str] = None
    last_run_stdout: Optional[str] = None
    last_run_stderr: Optional[str] = None
    failing_tests: Optional[List[str]] = None
    # Context
    user_skill_level: Optional[str] = "novice" # novice, intermediate, senior

# --- Response Models (Strict JSON) ---

class PatchFile(BaseModel):
    path: str
    diff: str # Unified diff format

class AssistResponse(BaseModel):
    summary: str
    root_cause: List[str]
    steps: List[str]
    tips: List[str]
    suggested_patch: Optional[Dict[str, List[PatchFile]]] = None

# --- Endpoints ---

@router.post("/explain", response_model=AssistResponse)
async def explain_quest_status(req: AssistGenericRequest):
    """
    Explain the current situation based on the last run output.
    """
    logger.info(f"Assist (Explain) requested for {req.quest_slug}")
    
    # Mock logic (Replace with LLM call later)
    # If there is stderr, explain the error.
    # If failing tests, explain why they failed.
    # If no output, give a general briefing.
    
    summary = "Here is what's happening."
    root_cause = []
    steps = ["Review the quest briefing."]
    tips = ["Check your syntax."]
    
    if req.last_run_stderr:
        summary = "I detected runtime errors in your code."
        root_cause = ["Runtime Exception detected in stderr."]
        steps = ["Read the stack trace below.", "Fix the specific line mentioned."]
        tips = ["Use print statements to debug values before the error."]
        
    elif req.failing_tests:
        count = len(req.failing_tests)
        summary = f"You have {count} failing tests."
        root_cause = ["Logic does not meet specification."]
        steps = ["Focus on the first failing test.", "Read the assertion failure message."]
        tips = ["Run tests individually to isolate the issue."]
        
    else:
        summary = "You haven't run the code yet, or output is clean."
        root_cause = ["No execution data available."]
        steps = ["Run your code to see output.", "Submit to run validation tests."]

    return AssistResponse(
        summary=summary,
        root_cause=root_cause,
        steps=steps,
        tips=tips
    )

@router.post("/debug", response_model=AssistResponse)
async def debug_quest_failure(req: AssistGenericRequest):
    """
    Propose a fix for the current failure.
    """
    logger.info(f"Assist (Debug) requested for {req.quest_slug}")
    
    # Mock logic (Replace with LLM call later)
    
    summary = "Let's debug this issue."
    root_cause = ["Unknown issue."]
    steps = []
    patch = None
    
    if req.last_run_stderr:
        summary = "I found a crash in your application."
        root_cause = ["Unhandled exception."]
        steps = ["Wrap the risky code in a try/catch block.", "Validate input before processing."]
        
        # Mock Patch Suggestion
        patch = {
            "files": [
                {
                    "path": "index.js",
                    "diff": "--- index.js\n+++ index.js\n@@ -1,5 +1,6 @@\n // Fix suggestion\n- const x = null;\n+ const x = 0;\n"
                }
            ]
        }
        
    elif req.failing_tests:
        summary = "Your logic is failing validation checks."
        root_cause = ["Incorrect return value."]
        steps = ["Ensure you return the expected type.", "Check edge cases like empty inputs."]
        
    return AssistResponse(
        summary=summary,
        root_cause=root_cause,
        steps=steps,
        tips=["Double check variable names.", "Ensure all dependencies are installed."],
        suggested_patch=patch
    )
