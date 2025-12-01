from sqlmodel import Session, select
from arcade_app.models import BossDefinition
from arcade_app.database import engine

REACTOR_STARTING_CODE = """# reactor.py
from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/reactor/status")
def reactor_status():
    # Simulate slow blocking I/O
    time.sleep(3)
    return {"status": "stable", "temperature": 900}
"""

REACTOR_RUBRIC = """
Scoring (0–100):

Async correctness (0–40 pts)
- async def on the route (10)
- At least one await in the function body (10)
- No time.sleep anywhere (10)
- Uses asyncio.sleep or equivalent (10)

Model & typing (0–30 pts)
- ReactorStatus model present, subclass of BaseModel (10)
- Has fields status: str and temperature: int (10)
- Route annotated to return ReactorStatus and/or uses response_model (10)

Structure & clarity (0–20 pts)
- Helper async def fetch_reactor_status() exists (10)
- Endpoint uses helper instead of inlining everything (5)
- No obvious junk / debug prints / unused imports (5)

Style & extras (0–10 pts)
- Good naming, docstring, or small extra (e.g. handling delay as a param).
"""

async def seed_bosses():
    async with Session(engine) as session:
        # Check if exists
        stmt = select(BossDefinition).where(BossDefinition.id == "boss_py_fastapi_refactor_01")
        existing = session.exec(stmt).first()
        
        if not existing:
            boss = BossDefinition(
                id="boss_py_fastapi_refactor_01",
                world_id="world-python",
                track_id="python-fundamentals",
                title="BOSS: The Reactor Core",
                slugline="Refactor a blocking FastAPI endpoint into a proper async, typed handler.",
                technical_objective=(
                    "You are given a blocking FastAPI endpoint using time.sleep() and no models. "
                    "Refactor it into an async, non-blocking, typed endpoint using asyncio.sleep, "
                    "a Pydantic model, and a separate async helper function."
                ),
                starting_code=REACTOR_STARTING_CODE,
                rubric=REACTOR_RUBRIC,
                time_limit_seconds=20 * 60,   # 20 minutes
                pass_threshold=75,            # Judge score needed
                xp_reward=800,
                integrity_damage=25,
                difficulty="hard",
            )
            session.add(boss)
            session.commit()
            print("✅ Seeded Boss: The Reactor Core")
        else:
            # Update existing if needed (optional, good for dev)
            existing.starting_code = REACTOR_STARTING_CODE
            existing.rubric = REACTOR_RUBRIC
            session.add(existing)
            session.commit()
            print("🔄 Updated Boss: The Reactor Core")
