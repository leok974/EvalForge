from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
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
    print("🚧 Skipping Boss Seed (Temporary Fix)")
    return
