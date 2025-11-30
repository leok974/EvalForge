import os
import sys
import json
import asyncio
import logging
import uuid
import time
from typing import AsyncGenerator, Optional, Dict, List, Literal, Any
from collections import defaultdict

from fastapi import FastAPI, HTTPException, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

# --- Helper Imports ---
from arcade_app.grading_helper import grade_submission
from arcade_app.coach_helper import stream_coach_feedback
from arcade_app.quest_helper import stream_quest_generator
from arcade_app.explain_helper import stream_explanation
from arcade_app.codex_helper import index_codex, get_codex_entry
from arcade_app.session_state import session_store
from arcade_app.profile_helper import get_profile, add_xp
from arcade_app.auth_helper import get_current_user
from arcade_app.project_helper import list_projects, create_project, sync_project
from arcade_app.socket_manager import websocket_endpoint

# --- 1. Data Models ---

class QueryRequest(BaseModel):
    message: str
    mode: Literal["judge", "quest", "explain", "debug"] = "judge"
    world_id: Optional[str] = None
    track_id: Optional[str] = None

class CreateProjectRequest(BaseModel):
    repo_url: str

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
        
        # 1. Grade
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
        
        # 3. Coach (Stream)
        async for token in stream_coach_feedback(user_input, grade_result, track=track_id):
            yield {"event": "text_delta", "data": token}
            
        yield {"event": "done", "data": "[DONE]"}

class QuestAgent(BaseAgent):
    """
    Generates challenges based on World/Track context.
    """
    async def run(self, user_input: str, context: Dict) -> AsyncGenerator[Dict, None]:
        track = TRACKS.get(context.get("track_id"), {})
        
        yield {"event": "status", "data": f"Generating quest for {track.get('name', 'Unknown Track')}..."}
        
        # Stream the real Quest
        async for token in stream_quest_generator(user_input, track):
            yield {"event": "text_delta", "data": token}
            
        yield {"event": "done", "data": "[DONE]"}

class ExplainAgent(BaseAgent):
    """
    Intelligent Teacher. Uses LangGraph + RAG to look up docs before answering.
    """
    async def run(self, user_input: str, context: Dict) -> AsyncGenerator[Dict, None]:
        from langchain_core.messages import HumanMessage, SystemMessage
        from arcade_app.graph_agent import explain_graph
        
        track = TRACKS.get(context.get("track_id"), {})
        
        # 1. Define System Context
        system_prompt = f"""
ROLE: Senior Staff Engineer / Mentor.
CONTEXT: User is working on '{track.get('name')}' ({track.get('description')}).
STACK: {', '.join(track.get('tags', []))}.

INSTRUCTIONS:
- You have access to a 'retrieve_docs' tool. USE IT if the user asks a technical question about the stack.
- Do not guess syntax. Look it up in the Codex.
- If the user asks something simple, answer directly.
- Answer concisely and code-first.
"""
        
        inputs = {
            "messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input)
            ]
        }
        
        yield {"event": "status", "data": "Initializing Reasoning Graph..."}

        # 2. Stream the Graph Execution
        try:
            # astream_events gives us visibility into the inner workings (tool calls)
            async for event in explain_graph.astream_events(inputs, version="v2"):
                kind = event["event"]
                
                # Visual Feedback: "I am reading the docs..."
                if kind == "on_tool_start":
                    tool_name = event.get("name", "tool")
                    yield {"event": "status", "data": f"Consulting Codex: {tool_name}..."}
                
                # Streaming the Final Answer
                elif kind == "on_chat_model_stream":
                    # We only want chunks from the final answer, not the tool call generation
                    chunk = event.get("data", {}).get("chunk")
                    if chunk and hasattr(chunk, 'content') and chunk.content:
                        yield {"event": "text_delta", "data": chunk.content}
                        
            yield {"event": "done", "data": "[DONE]"}

        except Exception as e:
            yield {"event": "text_delta", "data": f"\n\n[Graph Error: {str(e)}]"}
            yield {"event": "done", "data": "[DONE]"}

class DebugAgent(BaseAgent):
    """
    Senior Engineer persona. Helps troubleshoot.
    """
    async def run(self, user_input: str, context: Dict) -> AsyncGenerator[Dict, None]:
        yield {"event": "text_delta", "data": "🔍 **Debug Mode**\n\n"}
        track = TRACKS.get(context.get("track_id"), {})
        
        # Reuse explanation logic for now, tailored for debugging
        debug_prompt = f"Help me debug this issue: {user_input}"
        async for token in stream_explanation(debug_prompt, track):
            yield {"event": "text_delta", "data": token}
            
        yield {"event": "done", "data": "[DONE]"}

# --- 4. FastAPI Setup ---

app = FastAPI(title="EvalForge Agent Router")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Universe
@app.on_event("startup")
async def startup_event():
    _log_vertex_config()
    load_universe_data()

# Agent Registry
AGENTS = {
    "judge": JudgeAgent(),
    "quest": QuestAgent(),
    "explain": ExplainAgent(),
    "debug": DebugAgent(),
}

@app.post("/apps/arcade_app/users/{user}/sessions/{sid}/query/stream")
async def stream_session(user: str, sid: str, payload: QueryRequest):
    """
    Multi-Agent Router Endpoint.
    """
    print(f"Incoming Request: Mode={payload.mode} | World={payload.world_id} | Track={payload.track_id}")
    
    # 1. Select Agent
    agent = AGENTS.get(payload.mode, AGENTS["judge"])
    
    # 2. Build Context
    context = {
        "world_id": payload.world_id,
        "track_id": payload.track_id,
        "user_id": user,
        "session_id": sid
    }
    
    # 3. Execute & Stream
    return EventSourceResponse(agent.run(payload.message, context))

@app.get("/api/universe")
async def get_universe():
    """
    Returns the loaded Worlds and Tracks.
    Now merges STATIC tracks (from JSON) with DYNAMIC tracks (User Projects).
    """
    # 1. Start with Static Data (Deep copy to avoid mutating global state)
    static_worlds = list(WORLDS.values())
    all_tracks = list(TRACKS.values())
    
    # 2. Load Dynamic Projects
    # In Mock mode, we grab projects for the current mock user ('leo')
    user = get_current_user()
    if user:
        # AWAIT the DB call
        user_projects = await list_projects(user["id"])
        
        # 3. Convert Projects -> Tracks
        for proj in user_projects:
            # Skip if sync is failed or pending (optional, maybe we want to show them as disabled?)
            # For now, we include them so you can try to run quests on them.
            
            stack = proj.get("summary_data", {}).get("stack", [])
            
            dynamic_track = {
                "id": proj["id"],           # e.g. "proj-1234"
                "world_id": proj["default_world_id"], 
                "name": f"{proj['name']} (GitHub)",
                "source": "user-repo",      # Matches our QuestMaster logic
                "description": f"Linked Repo: {proj['repo_url']}",
                "tags": stack,
                "repo_config": {
                    "provider": proj["provider"],
                    "url": proj["repo_url"],
                    "stack": stack,
                    "focus_areas": ["general-maintenance", "refactoring"]
                }
            }
            all_tracks.append(dynamic_track)

    return {
        "worlds": static_worlds,
        "tracks": all_tracks
    }

@app.get("/api/codex")
def list_codex(world: Optional[str] = None):
    """
    Returns the Codex Index.
    Optional: ?world=world-python to filter results.
    """
    all_entries = index_codex()
    
    if world:
        # Return entries matching the world OR generic entries
        return [e for e in all_entries if e["world"] == world or e["world"] == "general"]
    
    return all_entries

@app.get("/api/codex/{entry_id}")
def read_codex(entry_id: str):
    """
    Returns the full Markdown content for an entry.
    """
    entry = get_codex_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Codex Entry not found")
    return entry

@app.get("/api/profile/{user_id}")
async def read_profile(user_id: str):
    return await get_profile(user_id)

@app.get("/api/auth/me")
def auth_me():
    user = get_current_user()
    if not user:
        return {} # Return empty object if not logged in
    return user

@app.get("/api/auth/github/start")
def auth_start():
    # Mock redirect
    return {"url": "/?login_success=true"}

# --- Project Routes ---
@app.get("/api/projects")
async def get_projects():
    user = get_current_user() # Assume 'leo' for now
    if not user: return []
    return await list_projects(user["id"])

@app.post("/api/projects")
async def add_project(payload: CreateProjectRequest):
    user = get_current_user()
    if not user: raise HTTPException(status_code=401)
    try:
        return await create_project(user["id"], payload.repo_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/projects/{pid}/sync")
async def trigger_sync(pid: str):
    return await sync_project(pid)

@app.get("/api/status")
async def api_status():
    return {"status": "EvalForge is running", "version": "Phase 10"}

@app.post("/apps/arcade_app/users/{user_id}/sessions", response_model=SessionResponse)
async def create_session(user_id: str):
    """Create a new session."""
    session_id = str(uuid.uuid4())
    _ = session_store.get(session_id)
    state_dict = session_store.get_state_dict(session_id) or {}
    
    return SessionResponse(
        id=session_id,
        appName="arcade_app",
        userId=user_id,
        state=state_dict,
        events=[],
        lastUpdateTime=time.time()
    )

@app.get("/api/dev/session-state/{session_id}")
async def get_session_state_api(
    session_id: str,
    fields: str | None = Query(default=None, description="Comma-separated field list")
) -> Dict[str, Any]:
    state_dict = session_store.get_state_dict(session_id) or {}
    if fields:
        want = {f.strip() for f in fields.split(",") if f.strip()}
        state_dict = {k: v for k, v in state_dict.items() if k in want}
    return state_dict

# --- WebSocket for Game Events ---
@app.websocket("/ws/game_events")
async def game_events_websocket(websocket: WebSocket):
    """Stream game events from Redis to frontend via WebSocket."""
    await websocket.accept()
    
    redis_client = None
    pubsub = None
    
    try:
        from redis import asyncio as aioredis
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6380/0")
        redis_client = aioredis.from_url(redis_url)
        pubsub = redis_client.pubsub()
        await pubsub.subscribe("game_events")
        
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"].decode())
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        if pubsub:
            await pubsub.unsubscribe("game_events")
        if redis_client:
            await redis_client.close()
        await websocket.close()

# --- Static Files (Must be last) ---
WEB_DIST = os.path.join(os.path.dirname(os.path.dirname(__file__)), "apps", "web", "dist")
if os.path.isdir(WEB_DIST):
    app.mount("/", StaticFiles(directory=WEB_DIST, html=True), name="web")
    
    @app.get("/{full_path:path}")
    def spa_catch_all(full_path: str):
        if full_path.startswith(("api/", "apps/", "metrics", "healthz", "docs")):
            raise HTTPException(status_code=404)
        index = os.path.join(WEB_DIST, "index.html")
        if os.path.isfile(index):
            return FileResponse(index)
        raise HTTPException(status_code=404)
