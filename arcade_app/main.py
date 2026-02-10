
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from arcade_app.database import init_db
from arcade_app.routers import routes_quests
from arcade_app.routers import routes_quests_runtime
from arcade_app.routers import routes_qa
from arcade_app.routers import routes_codex  # Phase 9.1: Tutorial System
from arcade_app.routers import routes_workshop
from arcade_app.routers import routes_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Startup: Initializing DB...")
    await init_db()
    
    # Log config
    project = os.getenv("GOOGLE_CLOUD_PROJECT", "unknown")
    logger.info(f"Config: Project={project}")
    
    yield
    # Shutdown
    logger.info("Shutdown")

app = FastAPI(
    title="EvalForge Arcade", 
    version="0.4.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for now, tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(routes_quests.router)
app.include_router(routes_quests_runtime.router)
app.include_router(routes_qa.router)
app.include_router(routes_codex.router)  # Phase 9.1: Codex API
app.include_router(routes_workshop.router) # Workshop Catalog API
app.include_router(routes_tools.router) # Phase 9.12: Explain/Debug Tools

# Health Routes
@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.4.0"}

@app.get("/healthz")
def healthz_check():
    return {"status": "ok", "version": "0.4.0"}

@app.get("/api/ready")
async def readiness_check():
    status = {"database": "unknown"}
    try:
        from arcade_app.database import get_session
        from sqlmodel import select
        async for session in get_session():
            await session.execute(select(1))
            status["database"] = "ok"
            break
    except Exception as e:
        status["database"] = f"error: {str(e)}"
        raise HTTPException(status_code=503, detail=status)
    return {"status": "ready", "components": status}

# Static Files (SPA)
web_dist = os.getenv("WEB_DIST", "static")
if os.path.exists(web_dist):
    app.mount("/assets", StaticFiles(directory=f"{web_dist}/assets"), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("ws/"):
            raise HTTPException(status_code=404, detail="Not Found")
        
        file_path = os.path.join(web_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        return FileResponse(os.path.join(web_dist, "index.html"))
