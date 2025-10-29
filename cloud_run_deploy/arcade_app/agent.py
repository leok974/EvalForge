"""
Multi-agent system for AI Trainer Arcade.
Safe dynamic loading ensures discovery works even if optional tools fail.
"""
import os
import sys
import logging
from typing import Final

from google.adk.agents import Agent, SequentialAgent

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
from arcade_app.vertex_diag import vertex_diag
vertex_diag()

# Set the environment variables that ADK recognizes for Vertex AI
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
os.environ["GOOGLE_CLOUD_LOCATION"] = REGION

# Import session state management
from arcade_app.session_state import session_store


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
        from arcade_app.optional_tools import judge, coach
        
        # Override Judge instructions for session awareness
        judge.instruction = """You are the Judge for EvalForge.

Your role: Introduce evaluation capabilities ONCE, then evaluate submissions.

IMPORTANT: You will receive session state context. Check if judge_intro_done=true.
- If judge_intro_done=false: Introduce yourself briefly (1-2 sentences): "I'm Judge. I run tests, grade submissions, and give feedback on coverage and quality."
- If judge_intro_done=true AND user has a submission/code: Evaluate it using your tools.
- Otherwise: Stay silent.

Be direct. No generic pleasantries."""
        
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
  - debugging: Help spot code issues, explain bugs, suggest fixes
  - cloud: Analyze logs, diagnose deployment issues, explain infrastructure
  - llm: Review agent behavior, suggest prompt improvements, explain reasoning patterns
  
Be conversational but focused. No generic advice. Use your tools when relevant."""
        
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
        "provider": os.getenv("GENAI_PROVIDER", "vertex"),
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
    return session_store.get_state_dict(session_id)


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
except Exception:
    pass
