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
