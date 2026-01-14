import os
import asyncio
import json
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger("evalforge.judge")

async def grade_submission(user_input: str, track: str = "default") -> Dict[str, Any]:
    """
    Grades submission using Vertex AI. 
    Strict mode: No silent fallback to mocks if connection fails.
    """
    
    # 1. Check if we are explicitly in Mock Mode (Dev only)
    if os.getenv("EVALFORGE_MOCK_GRADING") == "1":
        from .mock_grader import mock_grader_instance
        return await mock_grader_instance.grade(user_input, track)

    # 2. Real Gemini Execution
    try:
        # Lazy imports are still good practice for startup speed
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
        
        # Initialize Vertex
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel(model_name)
        
        # Construct Prompt (Standardized Judge Prompt)
        from arcade_app.persona_helper import wrap_prompt_with_persona
        
        base_task = f"""
        TASK: Evaluate the following code based on the '{track}' track.
        INPUT: {user_input}
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "coverage": <int 0-5>,
            "correctness": <int 0-5>,
            "clarity": <int 0-5>,
            "comment": "<string>"
        }}
        """
        
        prompt = wrap_prompt_with_persona(base_task, "judge")
        
        # Call with timeout protection
        response = await asyncio.wait_for(
            model.generate_content_async(prompt, generation_config={"response_mime_type": "application/json"}),
            timeout=15.0
        )
        
        # Parse Result
        data = json.loads(response.text)
        
        # Add metadata (Weighted Score logic)
        return _calculate_final_grade(data, track)

    except Exception as e:
        logger.error(f"CRITICAL: Vertex AI Grading Failed: {e}")
        # In Prod, we re-raise. We do NOT fallback to mock.
        raise RuntimeError(f"Judge System Offline: {e}")

def _calculate_final_grade(raw_grade: Dict, track: str) -> Dict:
    """Helper to add the weighted_score math."""
    # (Reuse your existing math logic here)
    # Default weights
    w = {"coverage": 0.4, "correctness": 0.4, "clarity": 0.2}
    if track == "debugging":
        w = {"coverage": 0.3, "correctness": 0.5, "clarity": 0.2}
        
    score = (
        (raw_grade.get("coverage", 0) * w["coverage"]) +
        (raw_grade.get("correctness", 0) * w["correctness"]) +
        (raw_grade.get("clarity", 0) * w["clarity"])
    ) / 5.0 * 100
    
    return {**raw_grade, "weighted_score": round(score, 1), "rubric_used": track}

async def judge_boss_submission(user_id: str, encounter_id: int, code: str) -> int:
    """
    Evaluates a Boss Fight submission using the specific boss rubric.
    Returns a score (0-100).
    """
    from arcade_app.database import get_session
    from arcade_app.models import BossRun, BossDefinition
    from sqlmodel import select

    # Fetch Boss Definition to get Rubric
    async for session in get_session():
        enc = await session.get(BossRun, encounter_id)
        if not enc:
            return 0
        boss = await session.get(BossDefinition, enc.boss_id)
        if not boss:
            return 0
            
        # Mock Mode Check
        if os.getenv("EVALFORGE_MOCK_GRADING") == "1":
            if "MAGIC_BOSS_PASS" in code:
                return 100
            return 45 # Fail but not zero

        # Construct Custom Prompt
        prompt = f"""
        ROLE: Senior Code Reviewer (Boss Fight Judge).
        TASK: Evaluate the following code against the specific RUBRIC below.
        
        TECHNICAL OBJECTIVE: {boss.technical_objective}
        
        RUBRIC:
        {boss.rubric}
        
        INPUT CODE:
        {code}
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "coverage": <int 0-5>,
            "correctness": <int 0-5>,
            "clarity": <int 0-5>,
            "comment": "<string>",
            "weighted_score": <int 0-100>
        }}
        
        NOTE: 'weighted_score' should be calculated based on the rubric points. 
        If the rubric defines specific points (e.g. 40 pts for Async), sum them up to get the final score out of 100.
        Ignore the standard 0-5 coverage/correctness/clarity if they don't fit, but fill them with reasonable values.
        The 'weighted_score' is the most important field here.
        """
        
        try:
            import vertexai
            from vertexai.generative_models import GenerativeModel
            
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
            model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
            
            vertexai.init(project=project_id, location=location)
            model = GenerativeModel(model_name)
            
            response = await model.generate_content_async(prompt, generation_config={"response_mime_type": "application/json"})
            data = json.loads(response.text)
            
            return int(data.get("weighted_score", 0))
            
        except Exception as e:
            logger.error(f"Boss Grading Failed: {e}")
            # Fallback or re-raise
            return 0
            
    return 0

async def grade_quest_submission(user: Any, quest: Any, code: str, language: str | None = None) -> tuple[int, bool]:
    """
    Grades a standard quest submission.
    Returns (score, passed).
    """
    # For now, we map quest track to the track expected by grade_submission
    # or just pass "default" if not specified.
    track = quest.track_id if hasattr(quest, "track_id") else "default"
    
    # Call the existing grade_submission
    # Note: grade_submission returns a dict with 'weighted_score' etc.
    result = await grade_submission(code, track=track)
    
    score = int(result.get("weighted_score", 0))
    
    # Define pass threshold (e.g. 70)
    passed = score >= 70
    
    return score, passed


async def judge_boss_with_rubric(
    boss, 
    run,
    player,
    submission_context: Dict[str, Any]
):
    """
    Use ZERO + rubric JSON to evaluate a boss submission and compute
    score + grade + per-dimension breakdown.
    
    Args:
        boss: BossDefinition with rubric_id
        run: BossRun being evaluated
        player: Profile of the player
        submission_context: Code, metrics, and any other context for evaluation
        
    Returns:
        BossEvalResult with score, grade, and combat numbers
    """
    from .boss_rubric_helper import load_boss_rubric, score_boss_eval
    from .boss_rubric_models import BossEvalLLMChoice
    
    rubric_id = boss.rubric
    rubric = load_boss_rubric(rubric_id)

    # Build the payload for ZERO
    zero_payload = {
        "boss_slug": boss.id,
        "rubric_id": rubric.id,
        "player": {
            "id": str(player.id),
            "name": player.user_id,
            "level": player.global_level,
        },
        "run": {
            "id": run.id,
            "attempt_index": getattr(run, "attempt", 1),
        },
        "submission": submission_context,
    }

    # Call ZERO
    if os.getenv("EVALFORGE_MOCK_GRADING") == "1":
        # Mock ZERO response for dev/testing
        code = submission_context.get("code", "")
        if "MAGIC_BOSS_PASS" in code:
            # Perfect score across all dimensions
            choice_data = {
                "dimensions": [
                    {"key": dim.key, "level": max(b.level for b in dim.bands), "rationale": "Perfect implementation"}
                    for dim in rubric.dimensions
                ],
                "autofail_conditions_triggered": [],
                "summary": "Mock Judge: Excellent work! You recovered the history perfectly.",
                "strengths": ["Perfect graph diagnosis", "Safe recovery strategy"],
                "improvements": []
            }
        elif "MAGIC_BOSS_PASS" in code and "world-sql" in str(rubric.world_slug):
             # SQL Boss Perfect Score
             choice_data = {
                "dimensions": [
                    {"key": dim.key, "level": max(b.level for b in dim.bands), "rationale": "Precise and performant."}
                    for dim in rubric.dimensions
                ],
                "autofail_conditions_triggered": [],
                "summary": "Mock Judge: Excellent analytics runbook.",
                "strengths": ["Clear grain definitions", "Explicit EXPLAIN checks", "Safe rollouts"],
                "improvements": [] 
             }
        elif "MAGIC_BOSS_PASS" in code and "world-ml" in str(rubric.world_slug):
             # ML Boss Perfect Score
             choice_data = {
                "dimensions": [
                    {"key": dim.key, "level": max(b.level for b in dim.bands), "rationale": "Scientifically rigorous."}
                    for dim in rubric.dimensions
                ],
                "autofail_conditions_triggered": [],
                "summary": "Mock Judge: Outstanding analysis of the gradient storm.",
                "strengths": ["Disciplined baselines", "Deep understanding of leakage", "Ops-ready monitoring"],
                "improvements": [] 
             }
        else:
            # Mid-range score
            choice_data = {
                "dimensions": [
                    {"key": dim.key, "level": 1, "rationale": "Partial implementation"}
                    for dim in rubric.dimensions
                ],
                "autofail_conditions_triggered": [],
                "summary": "Mock Judge: Partial implementation.",
                "strengths": [],
                "improvements": ["Need better recovery steps"]
            }
        choice = BossEvalLLMChoice.model_validate(choice_data)
    else:
        # Real ZERO call via LLM
        from .llm import call_zero_boss_judge
        
        try:
            zero_resp = call_zero_boss_judge(rubric=rubric, payload=zero_payload)
            choice = BossEvalLLMChoice.model_validate(zero_resp)
        except Exception as e:
            logger.error(f"ZERO boss judge failed: {e}")
            # Fallback to mid-range score
            choice_data = {
                "dimensions": [
                    {"key": dim.key, "level": 1, "rationale": f"Eval failed: {str(e)[:50]}"}
                    for dim in rubric.dimensions
                ],
                "autofail_conditions_triggered": []
            }
            choice = BossEvalLLMChoice.model_validate(choice_data)

    # Score the evaluation
    eval_result = score_boss_eval(rubric, choice)

    # Compute HP + Integrity deltas based on score
    boss_hp_before = run.hp_remaining if run.hp_remaining is not None and run.hp_remaining > 0 else boss.max_hp
    hp_fraction = eval_result.total_score / max(1, eval_result.max_score)
    damage = int(round(boss.max_hp * hp_fraction))
    boss_hp_after = max(0, boss_hp_before - damage)
    boss_hp_delta = boss_hp_after - boss_hp_before

    # Integrity damage if score is low
    integrity_before = getattr(player, "integrity", 100)
    integrity_damage = 0
    if eval_result.total_score < eval_result.max_score * 0.5:
        integrity_damage = 10  # tune this
    integrity_after = max(0, integrity_before - integrity_damage)
    integrity_delta = integrity_after - integrity_before

    # Attach combat numbers to result
    eval_result.boss_hp_before = boss_hp_before
    eval_result.boss_hp_after = boss_hp_after
    eval_result.boss_hp_delta = boss_hp_delta
    eval_result.integrity_before = integrity_before
    eval_result.integrity_after = integrity_after
    eval_result.integrity_delta = integrity_delta

    return eval_result

async def stream_coach_feedback(user_input: str, grade_result: Dict[str, Any], track: str = "default"):
    """
    Streams constructive feedback based on the grade.
    """
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
        
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel(model_name)
        
        prompt = f"Provide feedback on code that got coverage={grade_result.get('coverage')}..."
        
        stream = await model.generate_content_async(prompt, stream=True)
        async for chunk in stream:
            if chunk.text:
                yield chunk.text
                
    except Exception as e:
        logger.error(f"Feedback stream failed: {e}")
        yield "Good job!"
