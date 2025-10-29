"""
Multi-agent system for AI Trainer Arcade.
Safe dynamic loading ensures discovery works even if optional tools fail.
"""
import os
import sys
import logging
import hashlib
import asyncio
from typing import Final, Tuple, Dict, Any, List

from google.adk.agents import Agent, SequentialAgent

# ADK + GenAI
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.agents.run_config import RunConfig
from google.genai.types import Content, Part
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.agents.run_config import RunConfig
from google.genai.types import Content, Part

# ---- Vertex AI Configuration ----
# Single model, single region, no fallbacks
VERTEX_PROJECT_NUMBER = os.getenv("VERTEX_PROJECT_NUMBER", "291179078777")
VERTEX_PROJECT_ID = os.getenv("VERTEX_PROJECT_ID", "evalforge")  # For logging only
VERTEX_REGION = os.getenv("VERTEX_REGION", "us-central1")
VERTEX_MODEL_ID = os.getenv("VERTEX_MODEL_ID", "gemini-2.5-flash")

# Use project number for API calls
PROJECT: Final[str] = VERTEX_PROJECT_NUMBER
REGION: Final[str] = VERTEX_REGION
MODEL: Final[str] = VERTEX_MODEL_ID

def _log_vertex_config():
    """Log Vertex AI configuration on startup."""
    print(
        f"[VertexConfig] project={PROJECT} ({VERTEX_PROJECT_ID}) region={REGION} model={MODEL}",
        file=sys.stderr,
        flush=True
    )

# Initialize Vertex AI
try:
    import vertexai
    vertexai.init(project=PROJECT, location=REGION)
    _log_vertex_config()
except Exception as e:
    print(f"[VertexConfig] FATAL: Failed to initialize: {e}", file=sys.stderr, flush=True)
    raise

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Add diagnostic for Vertex AI configuration
from .vertex_diag import vertex_diag
vertex_diag()

# Set the environment variables that ADK recognizes for Vertex AI
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
os.environ["GOOGLE_CLOUD_LOCATION"] = REGION

# Import session state management
from .session_state import session_store


def build_root_agent() -> SequentialAgent:
    """
    Build the root agent with session-aware onboarding flow.
    
    Agents check session state to provide contextual, non-repetitive responses:
    - Greeter: Only greets on first interaction
    - Judge: Introduces evaluation capabilities once
    - Coach: Asks for track selection, then provides focused mentorship
    """
    # Greeter - only active on first message
    greeter = Agent(
        name="Greeter",
        instruction="""You are the Greeter for EvalForge AI Trainer Arcade.
        
Your role: Welcome new users ONCE per session, then stay quiet.

IMPORTANT: You will receive session state context. Check if greeted=true.
- If greeted=false: Say a brief welcome (1-2 sentences): "Welcome to EvalForge! You're in an AI Trainer Arcade where you get evaluated, coached, and guided."
- If greeted=true: Stay silent. Do NOT respond. Other agents will handle this.

Be concise. No lists, no questions. Just a quick welcome.""",
        model=MODEL,
    )
    
    sub_agents = [greeter]
    
    # Try to load optional tools (Judge and Coach)
    try:
        from .optional_tools import judge, coach
        
        # Override Judge instructions for session awareness
        judge.instruction = """You are the Judge for EvalForge.

Your role: Evaluate debugging submissions using a structured rubric.

IMPORTANT: You will receive session state context. Check if judge_intro_done=true.
- If judge_intro_done=false: Introduce yourself briefly (1-2 sentences): "I'm Judge. I evaluate your debugging attempts using a rubric: Coverage, Correctness, and Clarity. I'll grade your fixes and give feedback."
- If judge_intro_done=true AND user has submitted code with an explanation: Evaluate it using evaluate_submission tool.
- Otherwise: Stay silent.

CRITICAL ANTI-SPAM RULES:
- Call evaluate_submission ONLY ONCE per user submission
- If evaluate_submission returns status "skipped", DO NOT call it again
- When status is "skipped", tell them you already graded this and show the previous scores
- NEVER repeatedly call the same tool

When grading a NEW submission:
1. Call evaluate_submission(session_id, code_snippet, explanation_text)
2. Present scores: Coverage (0-5), Correctness (0-5), Clarity (0-5)
3. Share the feedback comment
4. Keep it brief

When status is "skipped": Tell them this was already graded and show their previous scores.

Be direct and concise. No generic pleasantries."""
        
        # Override Coach instructions for track-based mentorship
        coach.instruction = """You are the Coach for EvalForge.

Your role: Guide users through personalized learning tracks.

IMPORTANT: You will receive session state context. Check the 'track' field.

- If track=null: Ask user to pick a track:
  "You're now in EvalForge, your AI Trainer Arcade. Pick where you want coaching:
   1. Debugging code (Python/JS)
   2. Cloud & deployment (Docker, Cloud Run)
   3. LLM agents / reasoning
   
   Reply with 1, 2, or 3."

- If user just replied "1", "2", or "3" and track is still null, confirm their choice:
  - "1" → "Great. I'll act like a code reviewer and help you spot mistakes fast. Paste code or describe a bug."
  - "2" → "Great. I'll act like an SRE. Paste logs or errors and I'll walk you through root cause + fix steps."
  - "3" → "Great. I'll act like an AI systems mentor. Tell me what your agent is doing, and I'll suggest improvements."

- If track is already set (debugging/cloud/llm): Act as a focused mentor for that track:
  - debugging: **IMPORTANT: When user shares code, ALWAYS call analyze_code_snippet(session_id, code_snippet) tool.** This reviews their code like a senior engineer, explains what's wrong, shows how to fix it, and suggests what to learn next. The tool remembers recurring issues across the session. Use the tool's reply_text to guide them.
  - cloud: **IMPORTANT: When user shares logs/errors, ALWAYS call analyze_cloud_logs(session_id, logs_or_error) tool.** This analyzes their deployment issues like an SRE and remembers the debugging context. Build on previous diagnoses to guide them step by step.
  - llm: Review agent behavior, suggest prompt improvements, explain reasoning patterns
  
Be conversational but focused. No generic advice. Use your tools when relevant - especially analyze_code_snippet for debugging track and analyze_cloud_logs for cloud track!"""
        
        sub_agents.append(judge)
        sub_agents.append(coach)
        log.info("✓ Loaded Judge and Coach agents with session-aware instructions")
    except Exception as e:
        log.warning("⚠️ Optional tools not loaded: %r", e)
        log.info("ℹ️ Running with Greeter only (minimal mode)")
    
    # Create the orchestrator
    agent = SequentialAgent(
        name="ArcadeOrchestrator",
        sub_agents=sub_agents,
    )
    
    log.info("Root agent ready: %s | sub_agents=%s", 
             agent.name, [a.name for a in sub_agents])
    
    return agent


# Build and expose root_agent
root_agent = build_root_agent()

# Reuse singletons across requests - Vertex AI Session Service for persistence
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "291179078777")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
GOOGLE_CLOUD_AGENT_ENGINE_ID = os.getenv("GOOGLE_CLOUD_AGENT_ENGINE_ID")

SESSION_SERVICE = VertexAiSessionService(
    GOOGLE_CLOUD_PROJECT,
    GOOGLE_CLOUD_LOCATION,
    GOOGLE_CLOUD_AGENT_ENGINE_ID,
)
RUNNER = Runner(
    agent=root_agent,
    session_service=SESSION_SERVICE,
    app_name="arcade_app"
)


def _ensure_session(session_id: str, user_id: str):
    """Get or create a session in the ADK SessionService."""
    sess = SESSION_SERVICE.get_session(
        app_name="arcade_app",
        session_id=session_id,
        user_id=user_id
    )
    if not sess:
        sess = SESSION_SERVICE.create_session(
            app_name="arcade_app",
            user_id=user_id,
            session_id=session_id,
            state={}
        )
    return sess


def _extract_assistant_text_if_final(event) -> str | None:
    """
    Return assistant text only when ADK marks this event as the 'final' response.
    This is robust to tools and partials:
      - Ignores tool call/response events
      - Ignores streaming partial chunks
      - Returns the assistant message text when event.is_final_response() is True
    """
    # Prefer the ADK helper (recommended by docs)
    try:
        if hasattr(event, "is_final_response") and callable(event.is_final_response):
            if not event.is_final_response():
                return None
    except Exception:
        # If helper not available or fails, be conservative: don't treat as final
        return None

    # At this point, ADK says it's the final, user-facing response for the turn.
    content = getattr(event, "content", None)
    if not content:
        return None

    parts = getattr(content, "parts", None) or []
    for p in parts:
        # GenAI 'Part' can hold many types; we only care about text here.
        # (See Vertex AI Content/Part definitions.)
        if getattr(p, "text", None):
            return p.text

    return None


async def invoke_root_agent(
    session_state,
    user_message: str,
    *,
    session_id: str,
    user_id: str,
) -> tuple[str, object]:
    """
    Calls ADK runner first. If anything fails, fall back to Phase-3 stub.
    """
    cleaned = (user_message or "").strip()
    if not cleaned:
        return "(no input provided)", session_state

    # Try real ADK first
    try:
        session = _ensure_session(session_id, user_id)
        user_content = Content(role="user", parts=[Part.from_text(text=cleaned)])

        # Force text output (avoids audio/modalities surprises)
        run_cfg = RunConfig(response_modalities=["TEXT"])

        final_text = None
        async for event in RUNNER.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content,
            run_config=run_cfg,
        ):
            maybe = _extract_assistant_text_if_final(event)
            if maybe is not None:
                final_text = maybe
                # We could break here, but letting the stream drain is fine; ADK marks a single final.

        if final_text:
            return final_text, session_state

        # If ADK ran but we didn't see text, fall through to fallback.
    except Exception:
        pass

    # === Phase-3 fallback (stable demo path): greet → select track → rubric + dedupe ===
    if not getattr(session_state, "greeted", False):
        session_state.greeted = True
        return (
            "Hey! I'm your EvalForge tutor. Reply `1` to start debugging training.",
            session_state,
        )

    if cleaned.strip() == "1":
        session_state.track = "debugging"
        return (
            "Great, we're in debugging mode. Paste your broken code and tell me what you THINK is wrong. I'll grade you once.",
            session_state,
        )

    code_hash = hashlib.sha1(cleaned.encode("utf-8")).hexdigest()

    if getattr(session_state, "last_graded_input_hash", None) == code_hash:
        lg = getattr(session_state, "last_grade", None)
        if lg:
            reused_msg = (
                "I've already graded this exact submission:\n"
                f"- coverage: {lg.get('coverage')}/5\n"
                f"- correctness: {lg.get('correctness')}/5\n"
                f"- clarity: {lg.get('clarity')}/5\n"
                f"Next step: {lg.get('comment')}"
            )
            return (reused_msg, session_state)

    fake_grade = {
        "coverage": 2,
        "correctness": 2,
        "clarity": 3,
        "comment": "Return the value, cover edge cases, and improve naming.",
    }
    session_state.last_grade = fake_grade
    session_state.last_graded_input_hash = code_hash

    graded_msg = (
        "Here's your rubric:\n"
        f"- coverage: 2/5\n- correctness: 2/5\n- clarity: 3/5\n"
        "Next step: Return the computed value, cover edge cases, and improve naming.\n\n"
        "Update your code and send it again. I'll rescore if it's meaningfully different."
    )
    return (graded_msg, session_state)


# Health check endpoint for monitoring
def healthz() -> dict:
    """
    Health check that verifies ADC and agent configuration.
    Returns agent status and configuration.
    """
    import json
    
    health_status = {
        "status": "healthy",
        "agent": root_agent.name,
        "sub_agents": [agent.name for agent in root_agent.sub_agents],
        "model": MODEL,
        "provider": os.getenv("GENAI_PROVIDER", "unknown"),
        "vertex_location": REGION,
        "project": PROJECT,
    }
    
    # Check ADC
    try:
        import google.auth
        credentials, project = google.auth.default()
        health_status["adc_present"] = True
        health_status["adc_project"] = project
    except Exception as e:
        health_status["adc_present"] = False
        health_status["adc_error"] = str(e)
        health_status["status"] = "degraded"
    
    return health_status


def get_session_state(session_id: str) -> dict:
    """Get session state for debugging/introspection."""
    state_dict = session_store.get_state_dict(session_id)
    if state_dict is None:
        return {"error": "session not found", "session_id": session_id}
    return state_dict


# Add a tiny "/env" debug route (so you can verify at runtime)
try:
    from google.adk import expose  # hypothetical helper; if not available, skip this
    @expose("/_diag/env")
    async def diag_env():
        import json, os
        keys = ["GENAI_PROVIDER","GOOGLE_CLOUD_PROJECT","VERTEX_LOCATION","GENAI_MODEL"]
        return json.dumps({k: os.getenv(k) for k in keys})
    
    @expose("/healthz")
    async def health_check():
        import json
        return json.dumps(healthz())
    
    @expose("/api/dev/session-state/{session_id}")
    async def session_state_endpoint(session_id: str):
        """Dev introspection endpoint to view session state."""
        import json
        return json.dumps(get_session_state(session_id))
except Exception:
    pass


# ============================================================================
# FastAPI App Export (for uvicorn)
# ============================================================================
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
import time

app = FastAPI(title="EvalForge Agents API")

class QueryRequest(BaseModel):
    message: str

class SessionResponse(BaseModel):
    id: str
    appName: str
    userId: str
    state: Dict[str, Any]
    events: List[Any]
    lastUpdateTime: float

@app.get("/")
async def root():
    """Root endpoint to verify server is running."""
    return {
        "status": "EvalForge is running",
        "version": "Phase 3 - Judge Grading + Coach Mentorship",
        "agents": [agent.name for agent in root_agent.sub_agents]
    }

@app.get("/healthz")
async def healthz_endpoint():
    """Health check endpoint that returns agent status."""
    try:
        return healthz()
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in healthz: {error_details}", flush=True)
        raise HTTPException(status_code=500, detail={"error": str(e)})

@app.get("/api/dev/session-state/{session_id}")
async def get_session_state_endpoint(session_id: str):
    """Dev introspection endpoint to view session state."""
    try:
        state = get_session_state(session_id)
        if "error" in state:
            raise HTTPException(status_code=404, detail=state)
        return state
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in get_session_state: {error_details}", flush=True)
        raise HTTPException(status_code=500, detail={"error": str(e)})

@app.post("/apps/arcade_app/users/{user_id}/sessions")
async def create_session(user_id: str):
    """Create a new session for a user."""
    try:
        session_id = str(uuid.uuid4())
        # Initialize session state
        session_store.get(session_id)  # This creates if not exists
        
        # Get the state as a dict for the response
        state_dict = session_store.get_state_dict(session_id)
        
        return SessionResponse(
            id=session_id,
            appName="arcade_app",
            userId=user_id,
            state=state_dict,
            events=[],
            lastUpdateTime=time.time()
        )
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in create_session: {error_details}", flush=True)
        raise HTTPException(status_code=500, detail={"error": str(e)})

# COPILOT: DO NOT CHANGE ROUTES OR TASK CONFIG.
#
# This /query endpoint is STABLE and PRODUCTION-CRITICAL for local EvalForge demos.
#
# Current behavior:
# - Accepts { "message": "..." } from the client.
# - Loads session_state for the given session_id.
# - Applies simple conversation logic:
#     * first "hi" -> greet, mark greeted=true in session_state
#     * "1"       -> set track="debugging" in session_state
#     * later steps will call Judge grading, update last_grade, etc.
# - Persists session_state.
# - Returns { "response": "...", "session_id": "...", ... }.
#
# This is a TEMPORARY STUB that imitates Greeter/Coach/Judge.
# The real plan is to call the Google ADK root_agent (SequentialAgent)
# and let it update session_state and produce the reply.
#
# IMPORTANT RULES FOR COPILOT:
# 1. DO NOT delete or rename this /query endpoint.
# 2. DO NOT rename /sessions or /api/dev/session-state.
# 3. DO NOT switch the dev server launch away from the VS Code task
#    "EvalForge: Dev Server (Judge/Coach/Greeter + MCP)".
# 4. DO NOT suggest using `adk web`. Ignore the "No agents found" banner.
# 5. You MAY add a helper like `invoke_root_agent(message, session_state)`
#    that tries to call root_agent.run_async(...) with a proper InvocationContext,
#    BUT:
#      - Wrap that call in try/except.
#      - On error, fall back to the current stub behavior instead of crashing uvicorn.
#      - Always update session_state and return JSON.
#
# 6. When we eventually get InvocationContext right and can call root_agent,
#    slot that into invoke_root_agent() and keep the rest of this endpoint stable.
#
# TL;DR: We are allowed to IMPROVE agent invocation,
# but we are NOT allowed to break the contract or regress server stability.

@app.post("/apps/arcade_app/users/{user_id}/sessions/{session_id}/query")
async def query_agent(user_id: str, session_id: str, request: QueryRequest):
    """Send a message to the agent and get response."""
    try:
        # 1. Extract user message
        user_message = request.message
        if not isinstance(user_message, str):
            raise HTTPException(status_code=400, detail="message must be a string")
        
        # 2. Fetch session state for this session_id
        session_state = session_store.get(session_id)
        
        # 3. Invoke agent (real ADK Runner or fallback) - now passing user_id and session_id
        reply_text, updated_state = await invoke_root_agent(
            session_state, 
            user_message,
            session_id=session_id,
            user_id=user_id
        )
        
        # 4. Session state is already updated in-place by invoke_root_agent
        # (session_store uses the same reference, so no explicit save needed)
        
        # 5. Return response
        return {
            "session_id": session_id,
            "response": reply_text,
            "track": getattr(updated_state, "track", None),
            "last_grade": getattr(updated_state, "last_grade", None),
            "state": session_store.get_state_dict(session_id)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in query_agent: {error_details}", flush=True)
        raise HTTPException(status_code=500, detail={"error": "agent_failed", "message": str(e)})

