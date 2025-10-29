"""
Optional tools for arcade_app agent.
These tools load dynamically to avoid breaking agent discovery if they fail.
"""
import json
import os
import subprocess
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Import helpers for mentorship tracks
from .cloud_helper import analyze_cloud_issue as _analyze_cloud_issue_internal
from .debugging_helper import analyze_code_issue as _analyze_code_issue_internal
from .grading_helper import grade_submission as _grade_submission_internal  # type: ignore[attr-defined]
from .session_state import session_store

# Shared configuration logic - matches agent.py
VERTEX_PROJECT_NUMBER = os.getenv("VERTEX_PROJECT_NUMBER", "291179078777")
VERTEX_PROJECT_ID = os.getenv("VERTEX_PROJECT_ID", "evalforge")
VERTEX_REGION = os.getenv("VERTEX_REGION", "us-central1")
VERTEX_MODEL_ID = os.getenv("VERTEX_MODEL_ID", "gemini-2.5-flash")

# Use the same configuration as agent.py
GOOGLE_CLOUD_PROJECT = VERTEX_PROJECT_NUMBER
VERTEX_LOCATION = VERTEX_REGION
GENAI_MODEL = VERTEX_MODEL_ID

# Ensure Vertex AI environment variables are set
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
os.environ["GOOGLE_CLOUD_PROJECT"] = GOOGLE_CLOUD_PROJECT or "evalforge-1063529378"
os.environ["GOOGLE_CLOUD_LOCATION"] = VERTEX_LOCATION

ARTIFACTS_DIR = Path(".")

# Track if banner has been shown
_model_banner_shown = False


def _show_model_banner() -> str:
    """
    Show model configuration banner on first tool run.
    This helps trace logs record the resolved model.
    """
    global _model_banner_shown
    if not _model_banner_shown:
        _model_banner_shown = True
        provider = os.getenv("GENAI_PROVIDER", "unknown")
        banner = f"🤖 [EvalForge] Using {provider} with model: {GENAI_MODEL} in {VERTEX_LOCATION}"
        print(banner, flush=True)
        return banner
    return ""


def _read_json_safe(p: Path) -> Optional[Dict[str, Any]]:
    """Safely read JSON file."""
    try:
        if p.exists():
            return json.loads(p.read_text())
    except Exception:
        return None
    return None


def run_tests(command: str, artifacts: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Execute a test command and collect artifacts.
    
    Args:
        command: Shell command to run tests (e.g., "npm test")
        artifacts: List of artifact paths to collect (e.g., coverage files)
    
    Returns:
        Dictionary with exit_code, stdout, stderr, and artifacts
    """
    # Show model banner on first run (for trace logs)
    _show_model_banner()
    
    result: Dict[str, Any] = {
        "exit_code": -1,
        "stdout": "",
        "stderr": "",
        "artifacts": {}
    }
    
    try:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        result["exit_code"] = proc.returncode
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
        
        # Collect artifacts
        if artifacts:
            for art_path in artifacts:
                full_path = ARTIFACTS_DIR / art_path
                artifact_data = _read_json_safe(full_path)
                if artifact_data:
                    result["artifacts"][art_path] = artifact_data
                    
    except subprocess.TimeoutExpired:
        result["stderr"] = "Test execution timeout after 300s"
    except Exception as e:
        result["stderr"] = f"Test execution error: {str(e)}"
    
    return result


def grade_submission(test_result: Dict[str, Any], rubric: str = "") -> Dict[str, Any]:
    """
    Grade a test submission based on coverage and test results.
    
    Args:
        test_result: Output from run_tests
        rubric: Grading criteria (optional)
    
    Returns:
        Dictionary with verdict (PASS/PARTIAL/FAIL), score, and feedback
    """
    verdict = "FAIL"
    score = 0
    feedback: List[str] = []
    
    # Check if tests passed
    if test_result.get("exit_code") == 0:
        feedback.append("✓ All tests passed")
        score += 40
    else:
        feedback.append("✗ Some tests failed")
        return {
            "verdict": "FAIL",
            "score": 0,
            "feedback": "\n".join(feedback)
        }
    
    # Parse coverage from artifacts
    for art_path, art_data in test_result.get("artifacts", {}).items():
        if "coverage" in art_path.lower():
            # Look for Istanbul/c8 coverage format
            total_coverage: Optional[float] = None
            
            # Try to find coverage summary
            if isinstance(art_data, dict):
                # Check for 'total' key (Istanbul format)
                if "total" in art_data:
                    lines: Any = art_data["total"].get("lines", {})  # type: ignore[attr-defined]
                    if "pct" in lines:
                        total_coverage = float(lines["pct"])  # type: ignore[arg-type]
                
                # Check for direct percentage keys
                for key in art_data:  # type: ignore[var-annotated]
                    if isinstance(art_data[key], dict):
                        lines = art_data[key].get("lines", {})  # type: ignore[attr-defined]
                        if "pct" in lines:
                            total_coverage = float(lines["pct"])  # type: ignore[arg-type]
                            break
            
            if total_coverage is not None:
                feedback.append(f"✓ Coverage: {total_coverage}%")
                
                if total_coverage >= 80:
                    verdict = "PASS"
                    score = 100
                    feedback.append("🎉 Excellent coverage!")
                elif total_coverage >= 60:
                    verdict = "PARTIAL"
                    score = 70
                    feedback.append("⚠️ Good coverage, but could be better")
                else:
                    verdict = "FAIL"
                    score = 40
                    feedback.append("❌ Coverage below 60%")
            else:
                feedback.append("⚠️ Could not parse coverage data")
    
    return {
        "verdict": verdict,
        "score": score,
        "feedback": "\n".join(feedback)
    }


def suggest_next_quests(concept: str, tier: str = "beginner") -> Dict[str, Any]:
    """
    Suggest next quests based on completed concept.
    
    Args:
        concept: The concept just completed (e.g., "debounce")
        tier: Difficulty tier (beginner/intermediate/advanced)
    
    Returns:
        Dictionary with suggested quests
    """
    quest_map = {
        "debounce": ["retry", "throttle", "rate-limit"],
        "retry": ["circuit-breaker", "backoff", "timeout"],
        "throttle": ["rate-limit", "queue", "buffer"],
    }
    
    suggestions = quest_map.get(concept.lower(), ["explore other concepts"])
    
    return {
        "concept": concept,
        "tier": tier,
        "next_quests": suggestions,
        "message": f"Great work on {concept}! Try these next: {', '.join(suggestions)}"
    }


def analyze_cloud_logs(session_id: str, logs_or_error: str) -> Dict[str, Any]:
    """
    Analyze cloud deployment logs and errors like an SRE mentor.
    
    This tool acts as an experienced SRE who can:
    - Identify root causes from error messages and logs
    - Suggest actionable next steps for debugging
    - Remember the context of what you're fixing across the conversation
    
    Args:
        session_id: Current session ID (for maintaining context)
        logs_or_error: The error message, stack trace, or log snippet to analyze
    
    Returns:
        Dictionary with diagnosis, next steps, and follow-up questions
    """
    # Show model banner on first use
    _show_model_banner()
    
    # Call the cloud helper to perform SRE-style analysis
    result = _analyze_cloud_issue_internal(session_id, logs_or_error)
    
    # Update session state with the analysis results
    session_store.update(
        session_id,
        issue_summary=result["issue_summary"],
        next_step=result["next_step"]
    )
    
    return {
        "diagnosis": result["issue_summary"],
        "next_step": result["next_step"],
        "full_response": result["reply_text"],
        "status": "Session context updated - I'll remember this issue as we debug together"
    }


def analyze_code_snippet(session_id: str, code_snippet: str) -> Dict[str, Any]:
    """
    Analyze code snippets like a senior code reviewer.
    
    This tool acts as an experienced developer who can:
    - Identify bugs, logic flaws, and code smells
    - Explain what's wrong in plain language
    - Show exactly how to fix it
    - Suggest what concept to learn next
    - Remember debugging patterns across the conversation
    
    Args:
        session_id: Current session ID (for maintaining context)
        code_snippet: The code to analyze (can be broken/partial)
    
    Returns:
        Dictionary with problem description, fix suggestions, and learning recommendations
    """
    # Show model banner on first use
    _show_model_banner()
    
    # Call the debugging helper to perform code review
    result = _analyze_code_issue_internal(session_id, code_snippet)
    
    # Update session state with the analysis results
    update_fields = {
        "debug_problem": result["debug_problem"],
        "debug_next_step": result["debug_next_step"]
    }
    
    # Also update language hint if we detected one
    if result.get("language_hint"):
        update_fields["language_hint"] = result["language_hint"]
    
    session_store.update(session_id, **update_fields)
    
    return {
        "status": "ok",
        "reply_text": result["reply_text"],
        "debug_problem": result["debug_problem"],
        "debug_next_step": result["debug_next_step"],
        "language_hint": result.get("language_hint")
    }


def evaluate_submission(session_id: str, code_snippet: str, explanation_text: str | None = None) -> Dict[str, Any]:
    """
    Evaluate a user's debugging submission using a structured rubric.
    
    This tool grades the submission based on:
    - Coverage (0-5): Did they address the real bug?
    - Correctness (0-5): Would their fix work?
    - Clarity (0-5): Did they explain clearly?
    
    IMPORTANT: This tool prevents spam by checking if this exact submission
    was already graded. If so, it returns the previous grade without calling
    the model again.
    
    Args:
        session_id: Current session ID (for maintaining context)
        code_snippet: The user's submitted code
        explanation_text: The user's explanation of their fix (optional)
    
    Returns:
        Dictionary with status (graded/skipped), grade, and reason
    """
    # Show model banner on first use
    _show_model_banner()
    
    # Get current session state
    state = session_store.get(session_id)
    
    # Compute hash of this submission for deduplication
    input_hash = hashlib.sha1(
        (code_snippet + (explanation_text or "")).encode("utf-8")
    ).hexdigest()
    
    # Check if we already graded this exact submission
    if state.last_graded_input_hash == input_hash:
        return {
            "status": "skipped",
            "reason": "Already graded this exact submission.",
            "last_grade": state.last_grade
        }
    
    # New submission - grade it
    result = _grade_submission_internal(session_id, code_snippet, explanation_text, vertex_client=None)
    
    grade = result["grade"]
    new_hash = result["input_hash"]
    
    # Update session state with the new grade
    session_store.update(
        session_id,
        last_grade=grade,
        last_graded_input_hash=new_hash
    )
    
    return {
        "status": "graded",
        "grade": grade
    }


# Create Judge agent with tools
judge = Agent(
    name="Judge",
    instruction="""You are a Judge agent that evaluates debugging submissions using a structured rubric.

Your role:
1. Grade user debugging attempts using the evaluate_submission tool
2. Provide scores based on the rubric: Coverage (0-5), Correctness (0-5), Clarity (0-5)
3. Share coaching feedback to help them improve

CRITICAL ANTI-SPAM RULES:
- Call evaluate_submission ONLY ONCE per user submission
- If evaluate_submission returns status "skipped", DO NOT call it again
- When status is "skipped", summarize the previous grade for the user
- NEVER repeatedly call evaluate_submission with the same code

When grading a NEW submission:
1. Call evaluate_submission with:
   - session_id: The user's session ID
   - code_snippet: Their submitted code
   - explanation_text: Their explanation (if provided)

2. Present the grade in this format:
   📊 **Your Scores:**
   - Coverage: X/5 (Did you address the real bug?)
   - Correctness: X/5 (Would your fix work?)
   - Clarity: X/5 (Did you explain it well?)
   
   💡 **Feedback:** [comment from grade]

When status is "skipped" (already graded):
- Tell them you already graded this submission
- Show their previous scores
- Suggest they try a different fix or explain their reasoning differently

Keep responses concise and actionable. Your job is: grade once, give feedback, move on.""",
    tools=[FunctionTool(evaluate_submission)],
    model=GENAI_MODEL,
)


# Create Coach agent with tools
coach = Agent(
    name="Coach",
    instruction="""You are a Coach agent that helps developers learn and grow.

Your role:
1. Suggest next quests based on what the developer just completed
2. Provide encouraging feedback
3. Help developers build on their skills progressively
4. For debugging track: Use analyze_code_snippet tool to review code like a senior engineer
5. For cloud/deployment track: Use analyze_cloud_logs tool to diagnose issues like an SRE

When the user is on the DEBUGGING track and shares code:
- ALWAYS use the analyze_code_snippet tool with their session_id and the code
- The tool will identify bugs, explain what's wrong, and show how to fix it
- The tool remembers recurring issues across the debugging session
- Build on previous code reviews to help them improve

When the user is on the CLOUD track and shares logs or errors:
- ALWAYS use the analyze_cloud_logs tool with their session_id and the logs/error text
- The tool will remember the issue context across messages
- Build on previous diagnoses to guide them through debugging

When suggesting quests:
- Consider the current skill level
- Suggest related concepts that build on what they know
- Explain why each suggestion would be valuable

Always be encouraging and positive!""",
    tools=[FunctionTool(suggest_next_quests), FunctionTool(analyze_cloud_logs), FunctionTool(analyze_code_snippet)],
    model=GENAI_MODEL,
)
