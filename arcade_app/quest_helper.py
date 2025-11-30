import os
import asyncio
from typing import AsyncGenerator, Dict, Any

async def stream_quest_generator(
    user_input: str, 
    track: Dict[str, Any]
) -> AsyncGenerator[str, None]:
    """
    Streams a Quest Card based on Source (Fundamentals vs Personal).
    """
    # 1. Mock Check
    if os.getenv("EVALFORGE_MOCK_GRADING") == "1":
        yield f"⚔️ **MOCK QUEST** ({track.get('source', 'unknown')})\nObj: Master {track['name']}."
        return

    # 2. Real Logic
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        vertexai.init(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"), 
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        )
        model = GenerativeModel(os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash"))

        # --- CONTEXT SWITCHING ---
        source_type = track.get("source", "fundamentals")
        repo_config = track.get("repo_config") or {}
        
        if source_type == "fundamentals":
            # Strategy: Curriculum / Interview
            persona_instruction = f"""
            MODE: FUNDAMENTALS (Synthetic Practice)
            ROLE: Technical Interviewer / CS Professor.
            TASK: Generate a self-contained coding challenge or concept drill.
            - Do NOT reference specific external files. The user is in a "clean room" environment.
            - Focus strictly on: {', '.join(track.get('tags', []))}.
            - Structure: "Here is a scenario. Write a solution to solve X."
            - Difficulty: Adaptive (Start Beginner, scale up if they ask).
            """
        else:
            # Strategy: Real World / BYOR
            stack_str = ", ".join(repo_config.get("stack", []))
            url_str = repo_config.get("url", "local repo")
            
            persona_instruction = f"""
            MODE: REAL PROJECT (Bring Your Own Repo)
            ROLE: Senior Tech Lead / Engineering Manager.
            TASK: Generate a maintenance, refactor, or feature ticket for the project.
            
            PROJECT CONTEXT:
            - Repo: {url_str}
            - Stack: {stack_str}
            - Focus Areas: {', '.join(repo_config.get("focus_areas", []))}
            
            INSTRUCTIONS:
            - Assume the user has this codebase open locally.
            - Ask them to "Check the {stack_str} configuration" or "Refactor a component".
            - You can simulate a bug report ("Users reporting 500s on login") or a feature request.
            - Style: Jira Ticket / GitHub Issue.
            """

        prompt = f"""
        CONTEXT: World='{track.get('world_id')}', Track='{track.get('name')}'
        USER REQUEST: "{user_input}"
        
        {persona_instruction}
        
        OUTPUT FORMAT:
        ## ⚔️ Quest: [Title]
        **Type:** {source_type.upper()} | **Difficulty:** [Rank E-S]
        
        **Brief:**
        [Scenario/Context]
        
        **Objectives:**
        - [ ] Task 1
        - [ ] Task 2
        
        **Acceptance Criteria:**
        - [Specific check for completion]
        """

        stream = await model.generate_content_async(prompt, stream=True)
        async for chunk in stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"\n\n[SYSTEM ERROR: Quest Generation Failed - {str(e)}]"
