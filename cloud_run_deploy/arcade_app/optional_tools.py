"""
Optional tools for arcade_app agent.
These tools load dynamically to avoid breaking agent discovery if they fail.
"""
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

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


def _read_json_safe(p: Path) -> Optional[dict]:
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
    
    result = {
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
    feedback = []
    
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
            total_coverage = None
            
            # Try to find coverage summary
            if isinstance(art_data, dict):
                # Check for 'total' key (Istanbul format)
                if "total" in art_data:
                    lines = art_data["total"].get("lines", {})
                    if "pct" in lines:
                        total_coverage = lines["pct"]
                
                # Check for direct percentage keys
                for key in art_data:
                    if isinstance(art_data[key], dict):
                        lines = art_data[key].get("lines", {})
                        if "pct" in lines:
                            total_coverage = lines["pct"]
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


# Create Judge agent with tools
judge = Agent(
    name="Judge",
    instruction="""You are a Judge agent that evaluates code submissions.
    
Your role:
1. Run tests using the run_tests tool
2. Grade submissions using the grade_submission tool based on test results and coverage
3. Provide clear, actionable feedback

When grading:
- PASS: ≥80% coverage + all tests passing
- PARTIAL: 60-79% coverage + all tests passing  
- FAIL: <60% coverage or tests failing

Always be constructive and specific in your feedback.""",
    tools=[FunctionTool(run_tests), FunctionTool(grade_submission)],
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

When suggesting quests:
- Consider the current skill level
- Suggest related concepts that build on what they know
- Explain why each suggestion would be valuable

Always be encouraging and positive!""",
    tools=[FunctionTool(suggest_next_quests)],
    model=GENAI_MODEL,
)
