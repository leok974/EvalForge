"""
Multi-agent system for AI Trainer Arcade.
Safe dynamic loading ensures discovery works even if optional tools fail.
"""
import os
import logging

from google.adk.agents import Agent, SequentialAgent

# hard source of truth for model/region
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
VERTEX_LOCATION = os.getenv("VERTEX_LOCATION", "us-central1")

# accept multiple env names, default to the versioned model
GENAI_MODEL = (
    os.getenv("GENAI_MODEL")
    or os.getenv("VERTEX_MODEL")
    or os.getenv("MODEL_ID")
    or "gemini-1.5-flash-002"
)

print(f"[startup] provider={os.getenv('GENAI_PROVIDER')} "
      f"project={GOOGLE_CLOUD_PROJECT} region={VERTEX_LOCATION} model={GENAI_MODEL}", flush=True)

# If you use the Vertex SDK directly, initialize it here to the right region/project
try:
    import vertexai  # type: ignore
    if GOOGLE_CLOUD_PROJECT and VERTEX_LOCATION:
        vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=VERTEX_LOCATION)
        print("[startup] vertexai.init() called", flush=True)
except Exception as _e:
    pass

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Add diagnostic for Vertex AI configuration
from arcade_app.vertex_diag import vertex_diag
vertex_diag()

# Set the environment variables that ADK recognizes for Vertex AI
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
os.environ["GOOGLE_CLOUD_PROJECT"] = GOOGLE_CLOUD_PROJECT or "evalforge-1063529378"
os.environ["GOOGLE_CLOUD_LOCATION"] = VERTEX_LOCATION


def build_root_agent() -> SequentialAgent:
    """
    Build the root agent with dynamic tool loading.
    
    This ensures the agent always loads successfully, even if optional
    tools fail to import or initialize.
    """
    # Always include the Greeter as a baseline
    greeter = Agent(
        name="Greeter",
        instruction="Say a short friendly greeting and confirm service health.",
        model=GENAI_MODEL,
    )
    
    sub_agents = [greeter]
    
    # Try to load optional tools (Judge and Coach)
    try:
        from arcade_app.optional_tools import judge, coach
        sub_agents.append(judge)
        sub_agents.append(coach)
        log.info("✓ Loaded Judge and Coach agents with full tools")
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
        "model": GENAI_MODEL,
        "provider": os.getenv("GENAI_PROVIDER", "unknown"),
        "vertex_location": VERTEX_LOCATION,
        "project": GOOGLE_CLOUD_PROJECT,
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
