from datetime import datetime
from typing import Dict, Any, Optional
from arcade_app.progress_models import QuestProgressV2

# Constants (Tunable)
THRESHOLD_LEVEL_1_RUNS = 3
THRESHOLD_LEVEL_1_REPEAT = 2
THRESHOLD_LEVEL_2_RUNS = 5
THRESHOLD_LEVEL_2_SUBMITS = 2
THRESHOLD_LEVEL_3_RUNS = 8
THRESHOLD_LEVEL_3_SUBMITS = 3

HINT_TIERS = ["concept", "guided", "full_solution"]

def get_primary_failure(failure_summary: Dict[str, Any]) -> str:
    """Extracts primary failure mode from summary or heuristic."""
    # Assuming failure_summary has 'primary' key (Implemented in 7.1)
    # If not, implement simple heurisitc here
    if not failure_summary:
        return "unknown"
    return failure_summary.get("primary", "unknown")

def update_stuck_progress(prog: QuestProgressV2, passed: bool, is_submit: bool, failure_summary: Dict[str, Any] = None) -> None:
    """
    Updates the QuestProgressV2 stuck metrics based on the result.
    MUTATES prog object. Caller must save.
    """
    if passed:
        # Reset Logic
        prog.fail_streak_runs = 0
        prog.fail_streak_submits = 0
        prog.repeat_failure_count = 0
        prog.stuck_level = 0
        prog.last_success_at = datetime.utcnow()
        # last_primary_failure can stay for history context or reset? user plan says reset repeat_failure_count
        # We'll leave last_primary_failure as is, or reset to None? 
        # Plan says: set last_primary_failure = primary if failed. doesn't say reset on success. 
        # Cleanest to reset validation history
        prog.last_primary_failure = None
        return

    # Failed Logic
    primary = get_primary_failure(failure_summary)
    
    if not is_submit:
        prog.fail_streak_runs += 1
    else:
        prog.fail_streak_submits += 1
        
    # Repeat Logic
    if prog.last_primary_failure == primary:
        prog.repeat_failure_count += 1
    else:
        prog.last_primary_failure = primary
        prog.repeat_failure_count = 1
        
    # Compute Level (Heurisitc A3)
    # Start with current level, or recompute from scratch? 
    # Recomputing from scratch is safer/deterministic based on counters.
    
    new_level = 0
    
    # Lvl 3 check
    if prog.fail_streak_runs >= THRESHOLD_LEVEL_3_RUNS or prog.fail_streak_submits >= THRESHOLD_LEVEL_3_SUBMITS:
        new_level = 3
    # Lvl 2 check
    elif prog.fail_streak_runs >= THRESHOLD_LEVEL_2_RUNS or prog.fail_streak_submits >= THRESHOLD_LEVEL_2_SUBMITS:
        new_level = 2
    # Lvl 1 check
    elif prog.fail_streak_runs >= THRESHOLD_LEVEL_1_RUNS or prog.repeat_failure_count >= THRESHOLD_LEVEL_1_REPEAT:
        new_level = 1
        
    # Only escalate? Or can we de-escalate if they submit but fail? 
    # Usually stuck level tracks usage. If they are failing, they remain stuck.
    prog.stuck_level = max(prog.stuck_level, new_level)


def generate_coach_response(prog: QuestProgressV2, failure_summary: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Generates the 'coach' dictionary for the API response.
    Returns None if stuck_level < 1.
    """
    if prog.stuck_level < 1:
        return None
        
    primary = get_primary_failure(failure_summary)
    tier = _get_recommended_tier(primary, prog.stuck_level)
    
    # Check if hint is unlocked? Run/Submit logic usually returns unlocked tier.
    # We return recommended tier, frontend decides action (Open vs Unlock)
    
    return {
        "stuck_level": prog.stuck_level,
        "reason": f"repeat_failure:{primary}" if prog.repeat_failure_count > 1 else f"streak:{prog.fail_streak_runs}",
        "recommended_hint_tier": tier,
        "cta": _generate_copy(primary, prog.stuck_level, tier)
    }

def _get_recommended_tier(primary: str, level: int) -> str:
    """
    A4 Rules Breakdown
    """
    if primary == "timeout":
        if level >= 3: return "full_solution"
        if level >= 2: return "guided"
        return "concept"
        
    if primary in ("syntax_error", "runtime_exception", "syntax"):
        # Never jump to full unless lvl 3
        if level >= 3: return "guided" # Plan says "concept->guided (never jump straight to full unless lvl3)"
        return "guided" if level >= 2 else "concept"
        
    if primary in ("objective_missing", "output_mismatch", "logic"):
        # Guided at lvl2+
        return "guided" if level >= 2 else "concept"
        
    if primary == "hidden_tests_failed":
        if level >= 3: return "full_solution"
        if level >= 2: return "guided"
        return "concept"
        
    # Default
    return "concept"

def _generate_copy(primary: str, level: int, tier: str) -> Dict[str, Any]:
    """
    A5 Copy Generation
    """
    actions = ["open_hint", "unlock_hint", "dismiss"]
    
    title = "Stuck?"
    body = "Review the concepts."
    
    if primary == "timeout":
        title = "Infinite Loop Detected?"
        body = "Your code is taking too long. Check your loop conditions."
    elif primary == "syntax_error":
        title = "Syntax Error"
        body = "The parser is confused. Check for missing colons or parentheses."
    elif primary == "output_mismatch":
        title = "Output Mismatch"
        body = "The output isn't quite what we expect. Check the exact formatting."
        
    if level >= 2:
        title = "Need a hand?"
        body += " A code snippet might help."
    if level >= 3:
        title = "Let's get this unstuck"
        body += " The answer key is available if you need it."
        
    return {
        "title": title,
        "body": body,
        "actions": actions
    }
