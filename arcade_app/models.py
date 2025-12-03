from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime
import uuid
from pgvector.sqlalchemy import Vector
from enum import Enum

# --- ENUMS ---
class QuestSource(str, Enum):
    fundamentals = "fundamentals"
    project = "project"
    boss = "boss"

# --- USER & GAMIFICATION ---

# --- USER & GAMIFICATION ---

class AvatarDefinition(SQLModel, table=True):
    """
    Catalog of all available avatars.
    """
    id: str = Field(primary_key=True)  # e.g. "default_user", "neon_ghost"
    name: str
    description: str = Field(default="")

    # Unlock logic
    required_level: int = Field(default=1)
    rarity: str = Field(default="common")  # "common", "rare", "epic", "legendary"

    # Rendering config
    visual_type: str = Field(default="icon")   # "icon", "image", "css"
    visual_data: str                           # e.g. "user", "/assets/avatars/1.png", "neon-pulse"

    is_active: bool = Field(default=True)

    # Relationships
    users: List["User"] = Relationship(back_populates="avatar")


class User(SQLModel, table=True):
    id: str = Field(primary_key=True) # "leo"
    name: str
    avatar_url: Optional[str] = None
    
    current_avatar_id: str = Field(
        default="default_user",
        foreign_key="avatardefinition.id"
    )
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    avatar: Optional[AvatarDefinition] = Relationship(back_populates="users")
    profile: Optional["Profile"] = Relationship(back_populates="user")
    projects: List["Project"] = Relationship(back_populates="owner")

class ChatSession(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    mode: str = "judge"
    world_id: Optional[str] = None
    track_id: Optional[str] = None
    
    history: List[Dict] = Field(default=[], sa_type=JSON)
    state: Dict = Field(default={}, sa_type=JSON)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", unique=True)
    total_xp: int = 0
    global_level: int = 1
    skill_points: int = 0  # Points available for Tech Tree
    # Store world-specific progress as JSON for flexibility
    world_progress: Dict = Field(default={}, sa_type=JSON) 
    
    user: User = Relationship(back_populates="profile")

class SkillNode(SQLModel, table=True):
    """Static definition of a skill in the Tech Tree."""
    id: str = Field(primary_key=True)  # e.g. "syntax_highlighter"
    name: str
    description: str

    tier: int = 1              # Visual grouping (1–4)
    cost: int = 1              # Skill points required
    category: str = "core"     # e.g. ui, agent, analysis
    feature_key: str           # e.g. "syntax_highlighter", "agent_elara"

    parent_id: Optional[str] = Field(
        default=None,
        foreign_key="skillnode.id"
    )

class UserSkill(SQLModel, table=True):
    """Skills unlocked by a user."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    skill_id: str = Field(foreign_key="skillnode.id", index=True)
    unlocked_at: datetime = Field(default_factory=datetime.utcnow)

class UserMetric(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    metric_key: str  # e.g. "projects_synced", "bosses_defeated"
    value: int = 0
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class BadgeDefinition(SQLModel, table=True):
    id: str = Field(primary_key=True)  # e.g. "badge-first-sync"
    name: str
    description: str
    icon_url: Optional[str] = None
    xp_bonus: int = 0

class UserBadge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    badge_id: str = Field(foreign_key="badgedefinition.id")
    awarded_at: datetime = Field(default_factory=datetime.utcnow)

# --- PROJECTS & CONTENT ---

class Project(SQLModel, table=True):
    id: str = Field(default_factory=lambda: f"proj-{uuid.uuid4().hex[:8]}", primary_key=True)
    owner_user_id: str = Field(foreign_key="user.id")
    name: str
    repo_url: str
    provider: str = "github"
    source: str = "user" # "personal" | "user"
    
    default_world_id: str
    summary_data: Dict = Field(default={}, sa_type=JSON) # Stack, languages
    
    sync_status: str = "pending"
    last_sync_at: Optional[datetime] = None
    
    # Project Codex Status
    codex_status: str = Field(default="pending")  # pending, partial, complete, missing_docs
    codex_warnings: List[str] = Field(default_factory=list, sa_type=JSON)
    codex_last_sync: Optional[datetime] = None
    
    owner: User = Relationship(back_populates="projects")
    codex_docs: List["ProjectCodexDoc"] = Relationship(back_populates="project")

# --- KNOWLEDGE & RAG ---

class ProjectCodexDoc(SQLModel, table=True):
    """
    Structured documentation for a project, organized by doc_type.
    Auto-generated from repo files during sync.
    """
    __tablename__ = "projectcodexdoc"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: str = Field(foreign_key="project.id", index=True)
    doc_type: str = Field(index=True)  # overview, architecture, data_model, infra, observability, agents, quest_hooks
    
    # Content
    title: str
    summary: str  # 1-2 line TL;DR
    body_md: str  # Full markdown with YAML frontmatter
    
    # Metadata (parsed from frontmatter)
    world_ids: List[str] = Field(default_factory=list, sa_type=JSON)
    level: int = Field(default=2)  # Difficulty tier 1-5
    tags: List[str] = Field(default_factory=list, sa_type=JSON)
    metadata_json: Dict = Field(default_factory=dict, sa_type=JSON)
    
    # Tracking
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    auto_generated: bool = Field(default=True)  # False if manually edited
    
    # Relationships
    project: "Project" = Relationship(back_populates="codex_docs")

class KnowledgeChunk(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Metadata
    source_type: str  # "codex" | "repo"
    source_id: str    # filename or project_id
    chunk_index: int
    
    # The Content
    content: str
    
    # The Vector (768 dimensions is standard for Vertex/Gecko)
    embedding: List[float] = Field(sa_column=Column(Vector(768)))


# --- BOSS MODELS ---

class BossDefinition(SQLModel, table=True):
    """
    Static config for a Boss encounter.

    This is the 'what is this boss' record: name, world/track, timers, rewards.
    One row per boss type (e.g. boss-reactor-core).
    """
    id: str = Field(primary_key=True)  # e.g. "boss-reactor-core"
    name: str
    description: str = Field(default="")

    # Optional: link back into your worlds/tracks system
    world_id: Optional[str] = Field(default=None, index=True)   # e.g. "world-infra"
    track_id: Optional[str] = Field(default=None, index=True)   # e.g. "infra-fundamentals"

    # Gameplay / scoring knobs
    time_limit_seconds: int = Field(default=1800)  # 30 min default
    max_hp: int = Field(default=100)               # integrity pool
    base_xp_reward: int = Field(default=300)
    difficulty: str = Field(default="normal")      # "normal" | "hard"
    hint_codex_id: Optional[str] = Field(default=None) # Link to Strategy Guide

    enabled: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class BossRun(SQLModel, table=True):
    """
    One concrete attempt at a boss fight by a user.

    Used for history / analytics and to drive 'boss_result' events.
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: str = Field(index=True, foreign_key="user.id")
    boss_id: str = Field(index=True, foreign_key="bossdefinition.id")

    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    result: Optional[str] = Field(default=None)  # "win" | "loss" | "timeout"
    score: int = Field(default=0)                # judge score 0–100
    hp_remaining: int = Field(default=0)

    # Optional metadata for debugging / analytics
    judge_trace_id: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)


class BossProgress(SQLModel, table=True):
    """
    Long-term per-user, per-boss progress.

    Drives the Strategy Guide system (fail streaks, hint levels, etc.).
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: str = Field(index=True, foreign_key="user.id")
    boss_id: str = Field(index=True, foreign_key="bossdefinition.id")

    fail_streak: int = Field(default=0)           # consecutive failures
    highest_hint_level: int = Field(default=0)    # 0 = none, 1..N = deeper hints

    last_attempt_at: datetime = Field(default_factory=datetime.utcnow)
    last_result: Optional[str] = Field(default=None)  # "win" | "loss" | "timeout"

# --- QUEST MODELS ---

class QuestDefinition(SQLModel, table=True):
    """
    Static content for a quest.
    """
    id: str = Field(primary_key=True) # e.g. "py_01"
    track_id: str = Field(index=True) # e.g. "python-fundamentals"
    
    sequence_order: int = Field(default=1)
    tier: int = Field(default=1)
    xp_reward: int = Field(default=100)
    
    title: str
    technical_objective: str
    rubric_hints: str = ""
    
    boss: bool = Field(default=False)

class UserQuest(SQLModel, table=True):
    """
    Tracks a user's progress on a specific quest instance.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    
    source: QuestSource = Field(default=QuestSource.fundamentals)
    quest_def_id: Optional[str] = Field(default=None, foreign_key="questdefinition.id")
    
    status: str = "active" # active, completed
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # For dynamic quests (not from curriculum)
    dynamic_objective: Optional[str] = None
