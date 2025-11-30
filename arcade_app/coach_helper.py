import os
import asyncio
from typing import AsyncGenerator, Dict, Any

async def stream_coach_feedback(
    user_input: str, 
    grade: Dict[str, Any], 
    track: str = "default"
) -> AsyncGenerator[str, None]:
    """
    Streams Socratic feedback using Gemini 2.5 Flash.
    """
    
    # 1. Dev Mode Check
    if os.getenv("EVALFORGE_MOCK_GRADING") == "1":
        # Mock logic for dev/test
        yield "[MOCK MODE ENABLED] "
        yield "This is a simulated response."
        return

    # 2. Real Gemini Execution
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        vertexai.init(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"), 
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        )
        
        model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
        model = GenerativeModel(model_name)
        
        # Build prompt
        prompt = _build_socratic_prompt(user_input, grade, track)
        
        # Stream
        stream = await model.generate_content_async(prompt, stream=True)
        async for chunk in stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        # In production, we stream the error to the UI so the user sees it
        yield f"\n\n[SYSTEM ERROR: Coach Disconnected - {str(e)}]"

async def generate_coach_feedback(
    user_input: str, 
    grade: Dict[str, Any], 
    track: str = "default"
) -> str:
    """
    Non-streaming version for legacy/fallback endpoints.
    """
    # 1. Dev Mode Check
    if os.getenv("EVALFORGE_MOCK_GRADING") == "1":
        return "[MOCK MODE ENABLED] Simulated response."

    # 2. Real Gemini Execution
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        vertexai.init(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"), 
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        )
        
        model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
        model = GenerativeModel(model_name)
        
        prompt = _build_socratic_prompt(user_input, grade, track)
        
        response = await model.generate_content_async(prompt)
        return response.text

    except Exception as e:
        return f"[SYSTEM ERROR: Coach Disconnected - {str(e)}]"

def _build_socratic_prompt(user_input, grade, track):
    return f"Act as a Socratic Coach. User Score: {grade.get('weighted_score')}. Input: {user_input}"
