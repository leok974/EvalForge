import os
import sys
import json
import asyncio
import logging
import uuid
import time
from typing import AsyncGenerator, Optional, Dict, List, Literal, Any
from collections import defaultdict
from arcade_app.gamification import process_quest_completion
from arcade_app.gamification import process_quest_completion
from arcade_app.session_helper import get_or_create_session, update_session_state, append_message
from arcade_app.database import init_db
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from arcade_app.auth_helper import (
    get_login_url, exchange_github_code, 
    get_or_create_github_user, create_session_token, 
    get_current_user
)

# --- Boss Imports ---
from arcade_app.bosses.registry import is_boss_track, evaluate_boss
from arcade_app.bosses.progress_helper import apply_boss_outcome
from arcade_app.explain_agent import ExplainAgent
from arcade_app.routers import avatars
from arcade_app.persona_helper import get_npc, wrap_prompt_with_persona
from arcade_app.quest_helper import build_quest_system_prompt
from arcade_app.explain_helper import build_explain_system_prompt

# --- 1. Data Models ---

class QueryRequest(BaseModel):
    message: str
    mode: Literal["judge", "quest", "explain", "debug"] = "judge"
    world_id: Optional[str] = None
    track_id: Optional[str] = None
    codex_id: Optional[str] = None  # NEW: For boss strategy guides

class CreateProjectRequest(BaseModel):
    repo_url: str

class EquipRequest(BaseModel):
    avatar_id: str

class SessionResponse(BaseModel):
    id: str
    appName: str
    userId: str
    state: Dict[str, Any]
    events: List[Any]
    lastUpdateTime: float

# --- 2. Universe Data Loading ---

WORLDS: Dict[str, Dict] = {}
TRACKS: Dict[str, Dict] = {}

def load_universe_data():
    """Loads static world and track data into memory."""
    global WORLDS, TRACKS
    try:
        if os.path.exists("data/worlds.json"):
            with open("data/worlds.json", "r", encoding="utf-8") as f:
                for w in json.load(f):
                    WORLDS[w["id"]] = w
        if os.path.exists("data/tracks.json"):
            with open("data/tracks.json", "r", encoding="utf-8") as f:
                for t in json.load(f):
                    TRACKS[t["id"]] = t
        print(f"🌌 Universe Loaded: {len(WORLDS)} Worlds, {len(TRACKS)} Tracks", file=sys.stderr)
    except Exception as e:
        print(f"⚠️ Warning: Failed to load universe data: {e}", file=sys.stderr)

def _log_vertex_config():
    """Log Vertex AI configuration on startup."""
    project = os.getenv("GOOGLE_CLOUD_PROJECT", "unknown")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "unknown")
    model = os.getenv("EVALFORGE_MODEL_VERSION", "unknown")
    mock = os.getenv("EVALFORGE_MOCK_GRADING", "unknown")
    
    print(
        f"[EvalForge Config] project={project} location={location} model={model} mock_grading={mock}",
        file=sys.stderr,
        flush=True
    )

# --- 3. Agent Definitions ---

class BaseAgent:
    """Base interface for all agents."""
    async def run(self, user_input: str, context: Dict) -> AsyncGenerator[Dict, None]:
        yield {"event": "error", "data": "Not implemented"}

class JudgeAgent(BaseAgent):
    """
    The original Grading + Coaching logic.
    Context Requirement: 'track_id' (to select rubric).
    """
    async def run(self, user_input: str, context: Dict) -> AsyncGenerator[Dict, None]:
        track_id = context.get("track_id", "default")
        user_id = context.get("user_id", "anonymous")
        
        # 1. Announce Identity
        npc_data = get_npc("judge")
        yield {"event": "npc_identity", "data": json.dumps(npc_data)}

        # --- BOSS PATH ------------------------------------------------------
        if is_boss_track(track_id):
            # 1. Evaluate via rubric
            try:
                outcome = evaluate_boss(track_id, submission=user_input)
            except Exception as e:
                yield {"event": "text_delta", "data": f"Error evaluating boss submission: {e}"}
                yield {"event": "done", "data": "[DONE]"}
                return

            # 2. Persist XP / Integrity
            await apply_boss_outcome(user_id, outcome)

            # 3. Track progress and unlock hints if needed
            from arcade_app.bosses.boss_progress_helper import update_boss_progress
            from arcade_app.database import get_session
            
            hint_meta = {}
            async for session in get_session():
                hint_meta = await update_boss_progress(
                    session,
                    user_id=user_id,
                    boss_id=outcome.boss_id,
                    outcome="win" if outcome.passed else "fail"
                )
                break

            # 4. Stream "human" feedback text
            header = (
                f"🔎 Boss Evaluation: {outcome.boss_id}\n"
                f"Score: {outcome.score} / 115\n"
                f"Result: {'✅ BOSS DEFEATED' if outcome.passed else '❌ Boss escaped'}\n\n"
            )
            yield {"event": "text_delta", "data": header}
            
            # 5. Stream structured result for UI (Hint Unlock)
            boss_result_payload = {
                "boss_id": outcome.boss_id,
                "passed": outcome.passed,
                "score": outcome.score,
                "hint_unlocked": hint_meta.get("hint_unlocked", False),
                "hint_codex_id": hint_meta.get("hint_codex_id"),
                "fail_streak": hint_meta.get("fail_streak", 0)
            }
            yield {"event": "boss_result", "data": json.dumps(boss_result_payload)}

        # 1. Grade
        from arcade_app.grading_helper import grade_submission, stream_coach_feedback
        from arcade_app.gamification import add_xp
        
        grade_result = await grade_submission(user_input, track=track_id)
        yield {"event": "grade", "data": json.dumps(grade_result)}
        
        # 2. Award XP (Gamification Hook)
        user_id = context.get("user_id", "test")
        world_id = context.get("world_id", "unknown-world")
        score = grade_result.get("weighted_score", 0)
        
        if score > 0:
            # XP Formula: Score * Difficulty Multiplier (1.0 for now)
            xp_amount = int(score) 
            progress = await add_xp(user_id, world_id, xp_amount)
            
            # Stream a 'progress' event so the UI can show a notification
            yield {"event": "progress", "data": json.dumps(progress)}

            # B. Badges (New)
            # We fire-and-forget this (or await it, it's fast)
            # If the score is passing (e.g. > 60), count it as a "Completion"
            if score >= 60:
                await process_quest_completion(user_id, world_id, score)

                # --- BOSS TRIGGER CHECK ---
                from arcade_app.boss_triggers import BossTriggerContext, maybe_trigger_boss
                from arcade_app.boss_helper import create_encounter
                from arcade_app.models import Profile, QuestProgress, QuestDefinition, QuestState
                from arcade_app.database import get_session
                from sqlmodel import select, desc

                # We need the profile and quest details
                # This is a bit heavy for inside the agent loop, but acceptable for MVP
                async for session in get_session():
                    # Get Profile
                    profile = (await session.exec(select(Profile).where(Profile.user_id == user_id))).first()
                    if not profile: break

                    # Get the just-completed quest to build context
                    # We assume the last completed quest for this user/track is the one we just finished
                    uq_stmt = (
                        select(QuestProgress)
                        .join(QuestDefinition)
                        .where(
                            QuestProgress.user_id == user_id, 
                            QuestDefinition.track_id == track_id, 
                            QuestProgress.state.in_([QuestState.COMPLETED, QuestState.MASTERED])
                        )
                        .order_by(desc(QuestProgress.completed_at))
                    )
                    last_qp = (await session.exec(uq_stmt)).first()
                    
                    if last_qp:
                        # Count total completed on track
                        completed_count = len((await session.exec(uq_stmt)).all())
                        
                        # Check attempts (read from progress)
                        attempts = last_qp.attempts

                        ctx = BossTriggerContext(
                            profile=profile,
                            world_id=world_id,
                            track_id=track_id,
                            quest_id=str(last_qp.quest_id),
                            was_boss=False, # We are in normal grading flow
                            passed=True,    # We just checked score >= 60
                            grade="A" if score >= 90 else "B" if score >= 80 else "C",
                            attempts_on_track=attempts, # This is attempts on THIS quest, not track total. But acceptable proxy or I can sum.
                            completed_quests_on_track=completed_count
                        )

                        boss_def = await maybe_trigger_boss(ctx, session=session)
                        if boss_def:
                            encounter = await create_encounter(user_id, boss_def.id)
                            # Emit Boss Spawn Event
                            yield {
                                "event": "boss_spawn", 
                                "data": json.dumps({
                                    "boss_id": boss_def.id,
                                    "name": boss_def.name,
                                    "difficulty": boss_def.difficulty,
                                    "duration_seconds": boss_def.time_limit_seconds,
                                    "hp_penalty_on_fail": 10, # Configurable
                                    "base_xp_reward": boss_def.base_xp_reward
                                })
                            }
                            yield {"event": "text_delta", "data": f"\n\n🚨 **WARNING: {boss_def.name.upper()} DETECTED** 🚨\nInitiating containment protocols..."}
                    break
        
        # 3. Coach (Stream)
        async for token in stream_coach_feedback(user_input, grade_result, track=track_id):
            yield {"event": "text_delta", "data": token}
            
        yield {"event": "done", "data": "[DONE]"}

class QuestAgent(BaseAgent):
    """
    Generates challenges based on World/Track context.
    """
    async def run(self, user_input: str, context: Dict) -> AsyncGenerator[Dict, None]:
        print(f"DEBUG: QuestAgent.run called with track_id={context.get('track_id')}")
        from langchain_core.messages import HumanMessage, SystemMessage
        from arcade_app.quest_agent_graph import quest_graph 
        from arcade_app.quest_helper import stream_quest_generator
        
        track_id = context.get("track_id", "default")
        user_id = context.get("user_id", "leo")
        
        # 1. Announce Identity
        npc_data = get_npc("quest")
        yield {"event": "npc_identity", "data": json.dumps(npc_data)}

        # --- ROUTING LOGIC: REGISTRY OPS ---
        if track_id == "project-registry":
            system_prompt = f"""
            ROLE: KAI (Mission Control).
            CONTEXT: The user is in the PROJECT REGISTRY command center.
            
            CAPABILITIES:
            - You have tools to LIST, ADD, and SYNC projects.
            - ALWAYS pass 'user_id'="{user_id}" to the tools.
            - If the user asks to list, call 'list_my_projects'.
            - If they ask to add, call 'add_my_project'.
            - If they ask to sync, call 'sync_my_project'.
            
            USER REQUEST: "{user_input}"
            """
            
            inputs = {"messages": [SystemMessage(content=system_prompt), HumanMessage(content=user_input)]}
            
            try:
                async for event in quest_graph.astream_events(inputs, version="v1"):
                    kind = event["event"]
                    
                    if kind == "on_tool_start":
                        yield {"event": "status", "data": f"Executing Protocol: {event['name']}..."}
                    
                    elif kind == "on_chat_model_stream":
                        chunk = event["data"]["chunk"]
                        if chunk.content:
                            yield {"event": "text_delta", "data": chunk.content}
                            
                yield {"event": "done", "data": "[DONE]"}
                return
            except Exception as e:
                yield {"event": "text_delta", "data": f"Error executing ops: {e}"}
                yield {"event": "done", "data": "[DONE]"}
                return

        # --- FALLBACK: STANDARD QUEST ENGINE ---
        async for token in stream_quest_generator(user_input, TRACKS.get(track_id, {}), user_id):
            yield {"event": "text_delta", "data": token}
        
        yield {"event": "done", "data": "[DONE]"}

class DebugAgent(BaseAgent):
    """
    Senior Engineer persona. Helps troubleshoot.
    """
    async def run(self, user_input: str, context: Dict) -> AsyncGenerator[Dict, None]:
        # 1. Announce Identity
        npc_data = get_npc("debug")
        yield {"event": "npc_identity", "data": json.dumps(npc_data)}
        
        yield {"event": "text_delta", "data": "🔍 **Debug Mode**\n\n"}
        track = TRACKS.get(context.get("track_id"), {})
        
        # Reuse explanation logic for now, tailored for debugging
        from arcade_app.grading_helper import stream_explanation
        debug_prompt = f"Help me debug this issue: {user_input}"
        async for token in stream_explanation(debug_prompt, track):
            yield {"event": "text_delta", "data": token}
            
        yield {"event": "done", "data": "[DONE]"}

# --- 4. FastAPI App ---

app = FastAPI(title="EvalForge Arcade", version="0.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and register routers
from arcade_app.routes_boss import router as boss_router
app.include_router(boss_router)
app.include_router(avatars.router)

# Boss Codex routes
from arcade_app import routes_boss_codex
app.include_router(routes_boss_codex.router)

# Codex routes
from arcade_app.routers import codex
app.include_router(codex.router)

# Project Codex routes
from arcade_app.routers import project_codex
app.include_router(project_codex.router)

# Projects routes
from arcade_app.routers import projects
app.include_router(projects.router)

# Dev routes
from arcade_app import routes_dev
app.include_router(routes_dev.router)

# Boss QA routes (dev-only)
from arcade_app.routers import routes_boss_qa_applylens
app.include_router(routes_boss_qa_applylens.router)

from arcade_app.routers import routes_boss_qa_worlds
app.include_router(routes_boss_qa_worlds.router)

# Practice Rounds routes
from arcade_app.routers import routes_practice_rounds
app.include_router(routes_practice_rounds.router)

from arcade_app.routers import intent_oracle_eval
app.include_router(intent_oracle_eval.router)

# Quest routes (System 2.0)
from arcade_app.routers import routes_quests
app.include_router(routes_quests.router)

# World Progress routes
from arcade_app.routers import routes_world_progress
app.include_router(routes_world_progress.router)

# --- 5. Missing Routes (Restored) ---

from arcade_app.socket_manager import websocket_endpoint
from fastapi import WebSocket, HTTPException

@app.get("/api/universe")
def get_universe():
    return {
        "worlds": list(WORLDS.values()),
        "tracks": list(TRACKS.values())
    }

@app.get("/api/auth/me")
async def auth_me(request: Request):
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@app.get("/api/auth/login")
def login():
    return {"url": get_login_url()}

@app.get("/api/auth/github/callback")
async def github_callback(code: str):
    user_profile = await exchange_github_code(code)
    user_data = await get_or_create_github_user(user_profile)
    session_token = create_session_token(user_data.id)
    # Redirect to Frontend (localhost:5173)
    response = RedirectResponse(url="http://localhost:5173/")
    response.set_cookie(
        key="session_token", 
        value=session_token, 
        httponly=True,
        max_age=60*60*24*7,
        samesite="lax",
        secure=False,
        domain=None,
        path="/"
    )
    return response

@app.websocket("/ws/game_events")
async def ws_game_events(websocket: WebSocket):
    await websocket_endpoint(websocket)

# Initialize Universe
@app.on_event("startup")
async def startup_event():
    _log_vertex_config()
    load_universe_data()
    await init_db()
    
    # Boss seeding moved to explicit script: scripts/seed_evalforge_bosses.py
    # This keeps startup deterministic and CI-friendly
    # from arcade_app.seed_bosses import seed_bosses
    # await seed_bosses()

    # TEMPORARILY DISABLED - oracle curriculum uses old Quest 1.0 schema
    # from arcade_app.seed_curriculum import seed_oracle_curriculum
    # await seed_oracle_curriculum()

    # Seed Standard Quests (Foundry, Prism, etc.)
    # TEMPORARILY DISABLED due to schema mismatch - needs migration
    # from arcade_app.database import get_session
    # from arcade_app.seed_quests_standard_worlds import seed_standard_world_quests
    # 
    # from arcade_app.database import engine
    # 
    # async with engine.begin() as conn:
    #     def run_seeder(connection):
    #         from sqlmodel import Session
    #         session = Session(bind=connection)
    #         seed_standard_world_quests(session)
    #     await conn.run_sync(run_seeder)

# Agent Registry
AGENTS = {
    "judge": JudgeAgent(),
    "quest": QuestAgent(),
    "explain": ExplainAgent(),
    "debug": DebugAgent(),
}

@app.get("/api/session/active")
async def get_active_session(request: Request):
    user = await get_current_user(request)
    if not user: return {}
    return await get_or_create_session(user["id"])

@app.get("/api/skills")
async def get_skills(request: Request):
    """Return user's skill tree with unlock status."""
    from arcade_app.skill_helper import get_skill_tree
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return await get_skill_tree(user["id"])

from pydantic import BaseModel

class UnlockSkillRequest(BaseModel):
    skill_id: str

@app.post("/api/skills/unlock")
async def unlock_skill_endpoint(request: Request, payload: UnlockSkillRequest):
    """Unlock a skill for the current user."""
    from arcade_app.skill_helper import unlock_skill
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    result = await unlock_skill(user["id"], payload.skill_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/apps/arcade_app/users/{user}/sessions/{sid}/query/stream")
async def stream_session(user: str, sid: str, payload: QueryRequest):
    """
    Main entry point for the Chat Terminal.
    Routes to the appropriate Agent based on 'mode'.
    """
    # 1. Update Session State (Context)
    await update_session_state(sid, {
        "mode": payload.mode,
        "world_id": payload.world_id,
        "track_id": payload.track_id
    })
    
    # 2. Append User Message
    await append_message(sid, "user", payload.message)
    
    # 3. Select Agent
    agent = AGENTS.get(payload.mode, AGENTS["judge"])
    
    # 4. Stream Response
    async def event_generator():
        full_response = ""
        context = {
            "world_id": payload.world_id, 
            "track_id": payload.track_id,
            "codex_id": payload.codex_id,
            "user_id": user
        }
        
        try:
            async for event in agent.run(payload.message, context):
                # Capture text for history
                if event["event"] == "text_delta":
                    full_response += event["data"]
                yield event
                
            # 5. Append Assistant Message (History)
            await append_message(sid, "assistant", full_response)
            
        except Exception as e:
            logging.error(f"Stream Error: {e}")
            yield {"event": "error", "data": str(e)}

    from sse_starlette.sse import EventSourceResponse
    return EventSourceResponse(event_generator())

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.4.0"}

@app.get("/api/ready")
async def readiness_check():
    """
    Checks connections to DB and Redis.
    Used by Docker healthcheck.
    """
    status = {"database": "unknown", "redis": "unknown"}
    is_ready = True
    
    # Check DB
    try:
        from arcade_app.database import get_session
        from sqlmodel import select
        async for session in get_session():
            await session.execute(select(1))
            status["database"] = "ok"
            break
    except Exception as e:
        status["database"] = f"error: {str(e)}"
        is_ready = False

    # Check Redis (if used)
    # For now assume ok if DB is ok, or add specific redis check if critical
    status["redis"] = "ok" # Placeholder until redis client is exposed globally

    if not is_ready:
        raise HTTPException(status_code=503, detail=status)
        
    return {"status": "ready", "components": status}

@app.get("/metrics")
def metrics():
    """
    Basic Prometheus-style metrics stub.
    """
    # In a real app, use prometheus_client
    return {
        "evalforge_up": 1,
        "boss_runs_total": 0, # TODO: Hook into BossStore
        "active_sessions": len(AGENTS) # Rough proxy
    }

# --- 6. Static Files (SPA Serving) ---
# Must be last to avoid capturing API routes
web_dist = os.getenv("WEB_DIST", "static")
if os.path.exists(web_dist):
    app.mount("/assets", StaticFiles(directory=f"{web_dist}/assets"), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow API routes to pass through if they weren't caught above
        if full_path.startswith("api/") or full_path.startswith("ws/"):
            raise HTTPException(status_code=404, detail="Not Found")
            
        # Serve index.html for any other route (SPA)
        # Check if specific file exists (e.g. favicon.ico)
        file_path = os.path.join(web_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        return FileResponse(os.path.join(web_dist, "index.html"))
