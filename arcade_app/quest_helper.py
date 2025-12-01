import os
import json
import asyncio
from typing import AsyncGenerator, Dict, Any
from sqlmodel import select, desc
from arcade_app.database import get_session
from arcade_app.models import QuestDefinition, UserQuest, QuestSource

# Cache for worlds data
_WORLDS_CACHE = None

def _get_narrative_config(world_id: str) -> Dict:
    global _WORLDS_CACHE
    if _WORLDS_CACHE is None:
        try:
            with open("data/worlds.json", "r") as f:
                _WORLDS_CACHE = json.load(f)
        except Exception:
            _WORLDS_CACHE = []
            
    world = next((w for w in _WORLDS_CACHE if w["id"] == world_id), None)
    if world:
        return world.get("narrative_config", {})
    return {}

async def stream_quest_generator(
    user_input: str, 
    track: Dict[str, Any],
    user_id: str = "leo" # Default for now
) -> AsyncGenerator[str, None]:
    
    # 1. Mock Check
    if os.getenv("EVALFORGE_MOCK_GRADING") == "1":
        yield f"⚔️ **MOCK QUEST**\n\nObjective: Master {track.get('name')}.\nTask: {user_input}"
        return

    technical_task = ""
    source_type = track.get("source", "fundamentals")
    quest_title = "Mission"

    # --- PATH A: FUNDAMENTALS (Curriculum) ---
    if source_type == "fundamentals":
        async for session in get_session():
            # Find last completed quest order
            # We join UserQuest -> QuestDefinition
            statement = (
                select(QuestDefinition.sequence_order)
                .join(UserQuest, UserQuest.quest_def_id == QuestDefinition.id)
                .where(
                    UserQuest.user_id == user_id,
                    UserQuest.status == "completed",
                    QuestDefinition.track_id == track.get("id")
                )
                .order_by(desc(QuestDefinition.sequence_order))
            )
            result = await session.execute(statement)
            last_seq = result.scalars().first() or 0
            
            next_seq = last_seq + 1
            
            # Fetch Next Definition
            q_def = (await session.execute(
                select(QuestDefinition)
                .where(QuestDefinition.track_id == track.get("id"), QuestDefinition.sequence_order == next_seq)
            )).scalars().first()
            
            if not q_def:
                yield f"🎉 **TRACK COMPLETE**\n\nYou have mastered the {track.get('name')} curriculum. Select a new track to continue."
                return

            # Activate Quest in DB
            # Check if already active to avoid duplicates
            active_check = await session.execute(
                select(UserQuest).where(
                    UserQuest.user_id == user_id, 
                    UserQuest.quest_def_id == q_def.id,
                    UserQuest.status == "active"
                )
            )
            if not active_check.scalars().first():
                new_uq = UserQuest(
                    user_id=user_id,
                    source=QuestSource.fundamentals,
                    quest_def_id=q_def.id,
                    status="active"
                )
                session.add(new_uq)
                await session.commit()
            
            technical_task = q_def.technical_objective
            quest_title = q_def.title
            
    else:
        # --- PATH B: PROJECT (Dynamic) ---
        # Existing logic for repo scanning...
        repo_config = track.get("repo_config") or {}
        technical_task = f"Analyze the repo at {repo_config.get('url')} and find a refactor opportunity related to {', '.join(repo_config.get('stack', []))}."
        quest_title = "Field Operation"

    # --- SHARED: GENERATE FLAVOR TEXT ---
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
        
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel(model_name)

        # Narrative Config
        world_id = track.get("world_id", "world-python")
        story = _get_narrative_config(world_id)
        
        alias = story.get("alias", "THE SYSTEM")
        role = story.get("role", "Engineer")
        theme = story.get("theme", "Standard Tech")
        vocab = ", ".join(story.get("vocabulary", []))
        analogy = story.get("analogy_prompt", "Use standard analogies.")

        prompt = f"""
        ROLE: You are {role} inside {alias}.
        THEME: {theme}
        VOCABULARY: {vocab}
        
        TASK: Present this mission to the operative.
        QUEST TITLE: {quest_title}
        TECHNICAL OBJECTIVE: {technical_task}
        
        INSTRUCTIONS:
        1. Narrative Hook: Describe the technical problem as a crisis within the theme ({theme}). 
        2. Tactical Analysis: Briefly explain the concept using this analogy: {analogy}
        3. Mission Objectives: List the *exact* technical steps from the objective.
        
        FORMAT:
        ## 📡 INCOMING TRANSMISSION: {alias}
        **Crisis Level:** CRITICAL | **Role:** {role}
        
        **Briefing:**
        [Narrative Paragraph]
        
        **Tactical Analysis:**
        [Analogy Paragraph]
        
        **Mission Objectives:**
        [Technical Steps]
        
        **Loot:** +XP
        """

        stream = await model.generate_content_async(prompt, stream=True)
        async for chunk in stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"\n\n[SYSTEM ERROR: Quest Generation Failed - {str(e)}]\n\nFallback Task: {technical_task}"
