from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field, JSON, Column
from sqlalchemy.dialects.postgresql import JSONB

class QuestAttempt(SQLModel, table=True):
    __tablename__ = "quest_attempts"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    quest_id: str = Field(index=True, nullable=False) # slug or int id cast to str

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_submit: bool = Field(default=False, nullable=False)

    passed: bool = Field(default=False, nullable=False)
    duration_ms: int = Field(default=0, nullable=False)

    code: str = Field(nullable=False) # Text equivalent
    code_hash: str = Field(nullable=False)

    stdout: Optional[str] = Field(default=None)
    stderr: Optional[str] = Field(default=None)

    # SQLModel doesn't always handle JSONB automatically with default={} so we be explicit if needed
    # But usually sa_type=JSON works fine in SQLModel
    objective_results: List[Dict[str, Any]] = Field(default=[], sa_type=JSON) 
    meta: Dict[str, Any] = Field(default={}, sa_type=JSON)


class QuestProgressV2(SQLModel, table=True):
    """
    V2 Progress model to differentiate from the one in models.py if any.
    User's snippet used 'QuestProgress'. 
    Exising 'models.py' has 'QuestProgress' linked to 'QuestDefinition'.
    The user's plan seems to want a generic string-based quest_id for simpler linking?
    However, existing 'QuestProgress' uses int ID foreign key.
    
    The User's plan says: 'quest_id = Column(String, nullable=False, index=True)'
    This suggests they want to link by Slug (String) which is often easier for loosely coupled quests.
    
    I will name this 'QuestProgress' but ensure I don't import the OTHER QuestProgress from models.py in the same file context.
    Actually, to avoid collision with 'models.py' QuestProgress, I will name the table 'quest_progress' (as requested) 
    and the class 'QuestProgress'.
    
    Wait, 'models.py' already defines a 'QuestProgress' class and table 'questprogress'.
    SQLAlchemy might complain if I define another 'QuestProgress' class even in a different file if they map to same table or I try to use both.
    
    User's snippet:
    class QuestProgress(Base):
        __tablename__ = "quest_progress" (explicit table name)
        
    models.py:
    class QuestProgress(SQLModel, table=True):
         ... (implicit table name 'questprogress')
         
    I should check if I can just EXTEND or USE the existing `QuestProgress` in `models.py`.
    Existing `QuestProgress`:
        id, user_id, quest_id (int FK), state, attempts, best_score, dates.
    
    User's New `QuestProgress`:
        status, attempts_count, runs_count, best_xp, last_xp, hint_tier_unlocked.
        quest_id is STRING.
    
    The user explicitly said "New tables... 2. quest_progress".
    If I use `__tablename__ = "quest_progress_v2"`, it's safer.
    Or I can modify `models.py` to match this new definition?
    Creating a separate file `progress_models.py` with `QuestProgress` might conflict if I import `models` * and `progress_models` *.
    
    Decision: I will use the user's definition but explicitly set `__tablename__ = "quest_tracker"` or similar to avoid collision with the partial implementation in `models.py`, OR I will assume this REPLACES the logic in `models.py`.
    
    Given the instruction "Backend plan (minimal + solid)", this looks like a fresh implementation.
    I will use `QuestTracker` as the class name to avoid name collision in imports, but map it to `quest_tracker` table to be safe, OR `quest_progress_refined`.
    
    Let's check the user request again. "quest_progress — per-user per-quest status + xp + counts".
    I'll name the class `QuestTracker` and table `quest_tracker` to avoid collision with the existing `QuestProgress` in `models.py` which is tied to `QuestDefinition` (int IDs).
    The user's new system uses string IDs (slugs) probably.
    "quest_id = Column(String...)"
    
    Actually, I'll stick to `QuestProgress` class name in THIS file, but I will be careful not to import the other one. 
    And I will use `__tablename__ = "quest_progress_nodes"` or something?
    No, I'll stick to `quest_progress` table name provided by user, assuming they want this specific table. 
    The existing `models.py` likely constructs table `questprogress` (no underscore).
    So `quest_progress` (with underscore) should be distinct in Postgres.
    """
    __tablename__ = "quest_progress"
    # User constraint: (user_id, quest_id) unique
    # In SQLModel, typically done via __table_args__
    
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    quest_id: str = Field(index=True, nullable=False) # Slug

    status: str = Field(default="in_progress") # in_progress|completed
    attempts_count: int = Field(default=0)
    runs_count: int = Field(default=0)

    first_started_at: datetime = Field(default_factory=datetime.utcnow)
    last_run_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)

    best_xp: int = Field(default=0)
    last_xp: int = Field(default=0)

    hint_tier_unlocked: int = Field(default=0)


class QuestHintUnlock(SQLModel, table=True):
    __tablename__ = "quest_hint_unlocks"
    
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    quest_id: str = Field(index=True, nullable=False)

    max_tier: int = Field(default=0)
    unlocked_at: datetime = Field(default_factory=datetime.utcnow)
