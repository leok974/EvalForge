from arcade_app.services.stuck_detector import update_stuck_progress, generate_coach_response
from arcade_app.progress_models import QuestProgressV2

def test_stuck_detector_logic():
    # 1. Fresh Progress
    qp = QuestProgressV2(user_id="test", quest_id="q1")
    update_stuck_progress(qp, passed=False, is_submit=False, failure_summary={"primary": "syntax"})
    assert qp.fail_streak_runs == 1
    assert qp.stuck_level == 0
    
    # 2. Reach Level 1 (3 run failures)
    update_stuck_progress(qp, passed=False, is_submit=False, failure_summary={"primary": "syntax"})
    update_stuck_progress(qp, passed=False, is_submit=False, failure_summary={"primary": "syntax"})
    assert qp.fail_streak_runs == 3
    assert qp.stuck_level == 1
    
    # 3. Reach Level 2 (5 run failures)
    update_stuck_progress(qp, passed=False, is_submit=False, failure_summary={"primary": "syntax"})
    update_stuck_progress(qp, passed=False, is_submit=False, failure_summary={"primary": "syntax"})
    assert qp.fail_streak_runs == 5
    assert qp.stuck_level == 2
    
    # 4. Success resets streaks (but level stays? Logic says reset level to 0)
    update_stuck_progress(qp, passed=True, is_submit=False)
    assert qp.fail_streak_runs == 0
    assert qp.stuck_level == 0
    
    # 5. Submit Failure (More weight)
    # Reset
    qp.stuck_level = 0
    qp.fail_streak_runs = 0
    qp.fail_streak_submits = 0
    
    # 1 submit failure -> Level 0
    update_stuck_progress(qp, passed=False, is_submit=True, failure_summary={"primary": "logic"})
    assert qp.stuck_level == 0 # Threshold for Level 1 repeat is 2, or Level 2 submit is 2
    
    # 2 submit failures -> Level 2
    update_stuck_progress(qp, passed=False, is_submit=True, failure_summary={"primary": "logic"})
    assert qp.fail_streak_submits == 2
    assert qp.stuck_level == 2
    
def test_coach_response():
    qp = QuestProgressV2(user_id="test", quest_id="q1", stuck_level=1)
    coach = generate_coach_response(qp, failure_summary={"primary": "syntax_error"})
    
    assert coach is not None
    assert coach["stuck_level"] == 1
    assert coach["recommended_hint_tier"] == "concept"
    assert "Syntax" in coach["cta"]["title"]

    # Level 3 -> Solution (if enabled)
    qp.stuck_level = 3
    coach = generate_coach_response(qp, failure_summary={"primary": "timeout"})
    # timeout at level 3 -> full_solution
    assert coach["recommended_hint_tier"] == "full_solution"
