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
        model=MODEL,
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
