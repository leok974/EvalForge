import os
from langchain_google_vertexai import ChatVertexAI

def get_chat_model(agent_name: str = "default"):
    """
    Factory for getting a chat model instance.
    """
    model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
    llm = ChatVertexAI(
        model_name=model_name,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        temperature=0.3
    )
    return llm


def call_zero_boss_judge(rubric, payload: dict) -> dict:
    """
    Call ZERO (JudgeAgent) to evaluate a boss submission according to the given rubric.
    
    Args:
        rubric: BossRubric object with dimensions and instructions
        payload: Dictionary with player, run, and submission fields
        
    Returns:
        Dictionary matching BossEvalLLMChoice schema
    """
    from .prompts.zero_boss_judge import ZERO_BOSS_JUDGE_SYSTEM_PROMPT, ZERO_BOSS_PROMPTS
    import json
    
    # Check if this boss has a specialized system prompt
    if rubric.boss_slug in ZERO_BOSS_PROMPTS:
        try:
            with open(ZERO_BOSS_PROMPTS[rubric.boss_slug], "r", encoding="utf-8") as f:
                base_prompt = f.read()
        except Exception:
            # Fallback if file missing
            base_prompt = ZERO_BOSS_JUDGE_SYSTEM_PROMPT
    else:
        base_prompt = ZERO_BOSS_JUDGE_SYSTEM_PROMPT

    # Combine the base instructions (Generic or Custom) with the rubric-specific instructions
    system_prompt = (
        base_prompt.strip()
        + "\n\n--- RUBRIC-SPECIFIC INSTRUCTIONS ---\n"
        + rubric.llm_judge_instructions.strip()
    )

    user_content = {
        "rubric": rubric.dict(),
        "player": payload.get("player"),
        "run": payload.get("run"),
        "submission": payload.get("submission"),
    }

    # Call LLM with JSON mode
    response_json = chat_completion_json(
        system_prompt=system_prompt,
        user_payload=user_content,
    )

    # Expecting ZERO to return the BossEvalLLMChoice shape
    if not isinstance(response_json, dict):
        raise ValueError("ZERO boss judge returned non-dict JSON")

    return response_json


def chat_completion_json(
    system_prompt: str,
    user_payload: dict,
    model_name: str | None = None,
) -> dict:
    """
    Generic helper: send system + user JSON, get back pure JSON and parse it.
    
    Args:
        system_prompt: System instructions for the LLM
        user_payload: User data as a dictionary (will be JSON-stringified)
        model_name: Optional model override
        
    Returns:
        Parsed JSON response from the LLM
    """
    import json
    import vertexai
    from vertexai.generative_models import GenerativeModel
    
    if model_name is None:
        model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    
    # Construct the full prompt
    full_prompt = (
        f"{system_prompt}\n\n"
        f"--- INPUT DATA ---\n"
        f"{json.dumps(user_payload, indent=2)}\n\n"
        f"--- YOUR RESPONSE (JSON ONLY) ---"
    )
    
    # Call with JSON response format
    response = model.generate_content(
        full_prompt,
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.1,
        }
    )
    
    # Parse and return
    return json.loads(response.text)
