import os
import asyncio
from typing import AsyncGenerator, Dict, Any

async def stream_explanation(
    user_input: str, 
    track: Dict[str, Any]
) -> AsyncGenerator[str, None]:
    """
    Streams a tailored explanation grounded in the Track's specific technology stack.
    """
    if os.getenv("EVALFORGE_MOCK_GRADING") == "1":
        yield f"👨‍🏫 **Mock Explanation** for {track.get('name')}: {user_input} is interesting."
        return

    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash")
        
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel(model_name)

        track_name = track.get('name', 'General')
        tags = ', '.join(track.get('tags', []))

        prompt = f"""
        ROLE: Senior Staff Engineer acting as a Mentor.
        CONTEXT: The user is working on '{track_name}' ({track.get('description')}).
        TECHNOLOGIES: {tags}
        
        USER QUESTION: "{user_input}"
        
        INSTRUCTION:
        Explain the concept clearly. 
        CRITICAL: Use examples specific to the technologies in this track. 
        (e.g., If tags include 'React', explain state using Hooks, not generic classes. If 'FastAPI', use Pydantic examples).
        Do not give generic advice. Relate it to the specific stack defined in the track.
        Use Markdown for code blocks.
        """

        stream = await model.generate_content_async(prompt, stream=True)
        async for chunk in stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"\n\n[SYSTEM ERROR: Explanation Failed - {str(e)}]"
